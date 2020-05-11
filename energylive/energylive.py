import datetime
import logging
from functools import wraps
from socket import gaierror
from time import sleep

import requests

from .exceptions import UnknownDatetime, UnknownResponseType

__title__ = "energylive-py"
__version__ = "0.1"
__author__ = "Dimosthenis Schizas"
__license__ = "MIT"

URL = 'https://www.energylive.cloud/api/v1'


def retry(func):
    """Catches connection errors, waits and retries"""
    @wraps(func)
    def retry_wrapper(*args, **kwargs):
        self = args[0]
        error = None
        for _ in range(self.retry_count):
            try:
                result = func(*args, **kwargs)
            except (requests.ConnectionError, gaierror) as e:
                error = e
                logging.error(
                    "Connection Error, retrying in {} seconds".format(
                        self.retry_delay
                    )
                )
                # Incremental delay
                sleep(self.retry_delay * self.retry_count)
                continue
            else:
                return result
        else:
            raise error
    return retry_wrapper


class EnergyLiveClient:
    """
    Client to perform API calls and return the responses
    """

    def __init__(
        self, api_key, session=None, retry_count=4, retry_delay=0.5,
        proxies=None, response_type='json'
    ):
        """
        Arguments:
            api_key {str} -- [API Key as provided by EnergyLive]

        Keyword Arguments:
            session {requests.Session} -- Basic requests session
                                          default: {None})
            retry_count {int} -- Number of retries (default: {4})
            retry_delay {float} -- Base retry delay (default: {0.5})
            proxies {dict} -- proxies to use (default: {None})

        Raises:
            TypeError: Error raised when API is None
            UnknownResponseType: Exception raised when response_type
                                 is not valid
        """

        if api_key is None:
            raise TypeError("API key cannot be None")
        self.api_key = api_key
        # Session prepare
        self.response_type = response_type
        if session is None:
            session = requests.Session()
            if self.response_type == 'json':
                session.headers.update({'Accept': 'application/json'})
            elif self.response_type == 'xml':
                session.headers.update({'Accept': 'application/xml'})
            else:
                raise UnknownResponseType
        if proxies:
            session.proxies = proxies
        self.session = session

        self.retry_count = retry_count
        self.retry_delay = retry_delay

    @retry
    def _base_request(self, params, start, end):
        """Base request method to be used for every request

        Arguments:
            params {dict} -- Requests parameters
            start {pd.Timestamp/str} -- Request parameters start date
            end {pd.Timestamp/str} -- Request parameters end date

        Raises:
            UnknownDatetime: Exception raised when Datetime is not datetime/str

        Returns:
            [requests.Response] -- Requests response
        """

        if isinstance(start, datetime.datetime):
            start_str = self._datetime_to_str(start)
        elif isinstance(start, str):
            start_str = start
        else:
            raise UnknownDatetime

        if isinstance(end, datetime.datetime):
            end_str = self._datetime_to_str(end)
        elif isinstance(start, str):
            end_str = end
        else:
            raise UnknownDatetime

        base_params = {
            'access-token': self.api_key,
            'from': start_str,
            'to': end_str
        }
        params.update(base_params)

        logging.debug(f'Performing request to {URL} with params {params}')
        response = self.session.get(url=URL, params=params)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise e
        else:
            return response

    @staticmethod
    def _datetime_to_str(dtm):
        """Convert a datetime object to a string in CET/CEST

        Arguments:
            dtm {pd.Timestamp} -- Date as datetime.datetime

        Returns:
            [str] -- Date as string
        """

        if dtm.tzinfo is not None:
            dtm = dtm.tz_convert("Europe/Berlin")
        fmt = '%Y-%m-%d'
        ret_str = dtm.strftime(fmt)
        return ret_str

    def get_day_ahead_prices(self, area, start_date, end_date):
        """Method to get day ahead prices for one or more areas.

        Arguments:
            area {str/list} -- Area(s) to get day ahead prices
            start_date {str/pd.Timestamp} -- Start date
            end {str/pd.Timestamp} -- End date

        Returns:
            [str] -- Requests response as string
        """

        params = {
            'param': 'price',
            'area': ','.join(area) if isinstance(area, list) else area
        }
        response = self._base_request(
            params=params, start=start_date, end=end_date
        )
        return response.text

    def get_volume(self, area, start_date, end_date):
        """Method to get market volume for one or more areas.

        Arguments:
            area {str/list} -- Area(s) to get day ahead prices
            start_date {str/pd.Timestamp} -- Start date
            end {str/pd.Timestamp} -- End date

        Returns:
            [str] -- Requests response as string
        """

        params = {
            'param': 'volume',
            'area': ','.join(area) if isinstance(area, list) else area
        }
        response = self._base_request(
            params=params, start=start_date, end=end_date
        )
        return response.text
