# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cryptodatapy',
 'cryptodatapy.conf',
 'cryptodatapy.datasets',
 'cryptodatapy.extract',
 'cryptodatapy.extract.data_vendors',
 'cryptodatapy.extract.libraries',
 'cryptodatapy.transform',
 'cryptodatapy.util']

package_data = \
{'': ['*'],
 'cryptodatapy.conf': ['.pytest_cache/*', '.pytest_cache/v/cache/*'],
 'cryptodatapy.extract.data_vendors': ['.ipynb_checkpoints/*',
                                       '.pytest_cache/*',
                                       '.pytest_cache/v/cache/*']}

install_requires = \
['DBnomics>=1.2.3',
 'ccxt>=1.91.52',
 'investpy>=1.0.8',
 'matplotlib>=3.5.2',
 'numpy>=1.23.2,<2.0.0',
 'pandas-datareader>=0.10.0,<0.11.0',
 'pandas>=1.4.4,<2.0.0',
 'responses>=0.21.0,<0.22.0',
 'selenium>=4.4.3,<5.0.0',
 'statsmodels>=0.13.2',
 'webdriver-manager>=3.8.3']

extras_require = \
{':python_version >= "3.7" and python_version < "4.0"': ['requests>=2.28.0',
                                                         'coinmetrics-api-client>=2022.6.17',
                                                         'prophet>=1.1,<2.0']}

setup_kwargs = {
    'name': 'cryptodatapy',
    'version': '0.1.0',
    'description': 'Cryptoasset data library',
    'long_description': "![](cryptodatapy_logo.jpeg)\n\n# CryptoDataPy\n### _Better data beats fancier algorithms_\n<br/>\n\n**CryptoDataPy** is a python library which makes it easy to build high quality data pipelines \nfor the analysis of digital assets. By providing easy access to over 100,000 time series for thousands of  assets, \nit facilitates the pre-processing of a wide range of data from different sources.\n\nCryptoassets generate a huge amount of market, on-chain and off-chain data. \nBut unlike legacy financial markets, this data is often fragmented, \nunstructured and dirty. By extracting data from various sources, \npre-processing it into a user-friendly (tidy) format, detecting and repairing 'bad' data,\nand allowing for easy storage and retrieval, CryptoDataPy allows you to spend less time gathering \nand cleaning data, and more time analyzing it.\n\nOur data includes:\n\n- **Market:** market prices of varying granularity (e.g. tick, trade and bar data, aka OHLC),\nfor spot, futures and options markets, as well as funding rates for the analysis of \ncryptoasset returns.\n- **On-chain:** network health and usage data, circulating supply, asset holder positions and \ncost-basis, for the analysis of underlying crypto network fundamentals.\n- **Off-chain:** news, social media, developer activity, web traffic and search for project interest and \nsentiment, as well as traditional financial market and macroeconomic data for broader financial and \neconomic conditions.\n\nThe library's intuitive interface facilitates each step of the ETL/ETL (extract-transform-load) process:\n\n- **Extract**: Extracting data from a wide range of data sources and file formats.\n- **Transform**: \n  - Wrangling data into a pandas DataFrame in a structured and user-friendly format, \n  a.k.a [tidy data](https://www.jstatsoft.org/article/view/v059i10). \n  - Detecting, scrubbing and repairing 'bad' data (e.g. outliers, missing values, 0s, etc.) to improve the accuracy and reliability\nof machine learning/predictive models.\n- **Load**: Storing clean and ready-for-analysis data and metadata for easy access.\n\n## Installation\n\n```bash\n$ pip install cryptodatapy\n```\n\n## Usage\n\n**CryptoDataPy** allows you to pull ready-to-analyze data from a variety of sources \nwith only a few lines of code.\n\nFirst specify which data you want with a `DataRequest`:\n\n```python\n# import DataRequest\nfrom cryptodatapy.extract.datarequest import DataRequest\n# specify parameters for data request: tickers, fields, start date, end_date, etc.\ndata_req = DataRequest(\n    data_source='glassnode',  # name of data source\n    tickers=['btc', 'eth'], # list of asset tickers, in CryptoDataPy format, defaults to 'btc'\n    fields=['close', 'add_act', 'hashrate'],  # list of fields, in CryptoDataPy, defaults to 'close'\n    freq=None,  # data frequency, defaults to daily  \n    quote_ccy=None,  # defaults to USD/USDT\n    exch=None,  # defaults to exchange weighted average or Binance\n    mkt_type= 'spot',  # defaults to spot\n    start_date=None,  # defaults to start date for longest series\n    end_date=None,  # defaults to most recent \n    tz=None,  # defaults to UTC time\n    cat=None,  # optional, should be specified when asset class is not crypto, eg. 'fx', 'rates', 'macro', etc.\n)\n```\nThen get the data :\n\n```python\n# import GetData\nfrom cryptodatapy.extract.getdata import GetData\n# get data\nGetData(data_req).get_series()\n```\n\nWith same data request parameters, can you retrieve the same data from another source:\n\n```python\n# modify data source parameter\ndata_req = DataRequest(data_source='coinmetrics', \n                       tickers=['btc', 'eth'], \n                       fields=['close', 'add_act', 'hashrate'], \n                       freq='d',\n                      start_date='2016-01-01')\n# get data\nGetData(data_req).get_series()\n```\n\nFor more detailed code examples and interactive tutorials see our [documention]().\n\n## Supported Data Sources\n\n- [CryptoCompare](https://min-api.cryptocompare.com/documentation)\n- [CCXT](https://docs.ccxt.com/en/latest/)\n- [Glassnode](https://docs.glassnode.com/)\n- [Coin Metrics](https://docs.coinmetrics.io/api/v4/)\n- [Tiingo](https://api.tiingo.com/documentation/general/overview)\n- [DBnomics](https://db.nomics.world/docs/)\n- [investpy](https://investpy.readthedocs.io/)\n- [FRED](https://pandas-datareader.readthedocs.io/en/latest/)\n- [Yahoo Finance](https://pandas-datareader.readthedocs.io/en/latest/readers/index.html)\n\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines and \ncontact us at info@systamental.com. Please note that this project is \nreleased with a Code of Conduct. By contributing to this project, you agree \nto abide by its terms.\n\n## License\n\n`cryptodatapy` was created by Systamental. \nIt is licensed under the terms of the Apache License 2.0 license.\n\n",
    'author': 'Systamental',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
