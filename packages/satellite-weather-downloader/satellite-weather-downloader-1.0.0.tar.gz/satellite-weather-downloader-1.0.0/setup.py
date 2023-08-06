# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['satellite_weather_downloader']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'satellite-weather-downloader',
    'version': '1.0.0',
    'description': 'The routines available in this package are designed to capture and process satellite images',
    'long_description': '<!-- satellite_weather_downloader -->\n',
    'author': 'Flavio Codeco Coelho',
    'author_email': 'fccoelho@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/osl-incubator/satellite-weather-downloader',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
