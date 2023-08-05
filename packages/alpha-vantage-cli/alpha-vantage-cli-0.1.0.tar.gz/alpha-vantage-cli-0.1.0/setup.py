# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['alpha_vantage_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['av = alpha_vantage_cli.cli:cli']}

setup_kwargs = {
    'name': 'alpha-vantage-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': "# WIP: Command line interface for Alpha Vantage APIs\n\nWork in progress.\n\n\n###  Getting started\n\nGet an alpha vantage free api key. Visit http://www.alphavantage.co/support/#api-key\n\nInstall ``alpha-vantage-cli``:\n```bash\npip install alpha-vantage-cli\n```\n\nSet your api key:\n```\nav set-key\n```\n\nTry it out:\n```bash\nav stock quote ibm\n```\n\n\n## Usage examples\n\n```bash\nav --help\n```\n\nOutput:\n\n```\nUsage: av [OPTIONS] COMMAND [ARGS]...\n\n  Unofficial Alpha Vantage command line interaface.\n\n  Get stocks data from the command line.\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  crypto  Manages the Cryptocurrences APIs (Not yet implemented)\n  data    Manages the Fundamental Data APIs (Not yet implemented)\n  econ    Manages the Economic Indicators APIs (Not yet implemented)\n  forex   Manages the Forex APIs (Not yet implemented)\n  intel   Manages the Alpha Intelligence APIs (Not yet implemented)\n  stock   Manages the Core Stocks APIs\n  tech    Manages the Technical Indicators APIs (Not yet implemented)\n```\n\n\n### Get quote for stock\n\n```bash\nav stock quote aapl\n```\n\nSample output:\n\n```\n{'Global Quote': {'01. symbol': 'AAPL', '02. open': '151.2100', '03. high': '151.3500', '04. low': '148.3700', '05. price': '150.7000', '06. volume': '162278841', '07. latest trading day': '2022-09-16', '08. previous close': '152.3700', '09. change': '-1.6700', '10. change percent': '-1.0960%'}}\n```\n\n### Download monthly data as CSV\n\n```bash\nav stock monthly ibm --datatype=csv > ibm.csv\n```",
    'author': 'Omar Sosa Rodriguez',
    'author_email': 'omarfsosa@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
