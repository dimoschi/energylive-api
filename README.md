# energylive
Python client for the [EnergyLive](https://www.energylive.cloud/) API

The API is currently undocumented.

## Installation
1. Clone this repository
2. `python3 -m pip install <path_to_cloned_repo>`

## Usage
The code currently creates a client based on requests session and uses the following two methods:
- get_day_ahead_prices(area, start_date, end_date)
- get_volume(area, start_date, end_date)

The user has also the option to get the data in both JSON (default) or XML by setting response_type once during EnergyLiveClient instantiation.

```python
from energylive import EnergyLiveClient
import pandas as pd

client = EnergyLiveClient(api_key=<YOUR API KEY>)

start_date = '2020-01-01' or pd.Timestamp('2020-01-01')
end_date = '2020-01-01' or pd.Timestamp('2020-01-01')
area = 'GR'  # Greece

# Methods
client.query_day_ahead_prices(country_code, start, end)
client.query_load(country_code, start, end)
```