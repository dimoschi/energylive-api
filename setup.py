# -*- coding: utf-8 -*-

"""
A setuptools based setup module for energylive-py.

Adapted from
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
from setuptools import find_packages, setup

__author__ = "Dimosthenis Schizas"
__maintainer__ = "Dimosthenis Schizas"
__email__ = "dimoschi@gmail.com"
__version__ = 0.1

VERSION = __version__

LONG_DESCRIPTION = (
    """An easy to use Python wrapper for EnergyLive API.
    Currently you can only pull data of say-ahead spot price and market volume.
    """
)

setup(
    name="energylive",
    version=VERSION,
    description="An easy to use Python wrapper for EnergyLive API.",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="energylive,API",
    author=__author__,
    author_email=__email__,
    license="MIT",
    packages=find_packages(),
    package_data={
        'energylive-py': ['LICENSE', 'README.md'],
    },
    install_requires=[
        "requests==2.23.0",
    ],
    include_package_data=True,
    zip_safe=False,
)
