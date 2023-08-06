# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecoindex_scraper']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'ecoindex>=5.0.0,<6.0.0',
 'undetected-chromedriver>=3.1.5,<4.0.0']

setup_kwargs = {
    'name': 'ecoindex-scraper',
    'version': '2.4.0',
    'description': 'Ecoindex_scraper module provides a way to scrape data from given website while simulating a real web browser',
    'long_description': '# ECOINDEX SCRAPER PYTHON\n\n![Quality check](https://github.com/cnumr/ecoindex_scrap_python/workflows/Quality%20checks/badge.svg)\n[![PyPI version](https://badge.fury.io/py/ecoindex-scraper.svg)](https://badge.fury.io/py/ecoindex-scraper)\n\nThis module provides a simple interface to get the [Ecoindex](http://www.ecoindex.fr) of a given webpage using module [ecoindex-python](https://pypi.org/project/ecoindex/)\n\n## Requirements\n\n- Python ^3.8 with [pip](https://pip.pypa.io/en/stable/installation/)\n- Google Chrome installed on your computer\n\n## Install\n\n```shell\npip install ecoindex-scraper\n```\n\n## Use\n\n### Get a page analysis\n\nYou can run a page analysis by calling the function `get_page_analysis()`:\n\n```python\n(function) get_page_analysis: (url: HttpUrl, window_size: WindowSize | None = WindowSize(width=1920, height=1080), wait_before_scroll: int | None = 1, wait_after_scroll: int | None = 1) -> Coroutine[Any, Any, Result]\n```\n\nExample:\n\n```python\nimport asyncio\nfrom pprint import pprint\n\nfrom ecoindex_scraper.scrap import EcoindexScraper\n\npprint(\n    asyncio.run(\n        EcoindexScraper(url="http://ecoindex.fr")\n        .init_chromedriver()\n        .get_page_analysis()\n    )\n)\n```\n\nResult example:\n\n```python\nResult(width=1920, height=1080, url=HttpUrl(\'http://ecoindex.fr\', ), size=549.253, nodes=52, requests=12, grade=\'A\', score=90.0, ges=1.2, water=1.8, ecoindex_version=\'5.0.0\', date=datetime.datetime(2022, 9, 12, 10, 54, 46, 773443), page_type=None)\n```\n\n> **Default behaviour:** By default, the page analysis simulates:\n>\n> - Window size of **1920x1080** pixels (can be set with parameter `window_size`)\n> - Wait for **1 second when page is loaded** (can be set with parameter `wait_before_scroll`)\n> - Scroll to the bottom of the page (if it is possible)\n> - Wait for **1 second after** having scrolled to the bottom of the page (can be set with parameter `wait_after_scroll`)\n\n### Get a page analysis and generate a screenshot\n\nIt is possible to generate a screenshot of the analyzed page by adding a `ScreenShot` property to the `EcoindexScraper` object.\nYou have to define an id (can be a string, but it is recommended to use a unique id) and a path to the screenshot file (if the folder does not exist, it will be created).\n\n```python\nimport asyncio\nfrom pprint import pprint\nfrom uuid import uuid1\n\nfrom ecoindex_scraper.models import ScreenShot\nfrom ecoindex_scraper.scrap import EcoindexScraper\n\npprint(\n    asyncio.run(\n        EcoindexScraper(\n            url="http://www.ecoindex.fr/",\n            screenshot=ScreenShot(id=str(uuid1()), folder="./screenshots"),\n        )\n        .init_chromedriver()\n        .get_page_analysis()\n    )\n)\n```\n\n## Contribute\n\nYou need [poetry](https://python-poetry.org/) to install and manage dependencies. Once poetry installed, run :\n\n```bash\npoetry install\n```\n\n## Tests\n\n```shell\npoetry run pytest\n```\n\n## [Contributing](CONTRIBUTING.md)\n\n## [Code of conduct](CODE_OF_CONDUCT.md)\n',
    'author': 'Vincent Vatelot',
    'author_email': 'vincent.vatelot@ik.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://www.ecoindex.fr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
