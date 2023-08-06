# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ytm_ll_dl']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'sh>=1.14.3,<2.0.0',
 'yt-dlp>=2022.9.1,<2023.0.0',
 'ytmusicapi>=0.22.0,<0.23.0']

entry_points = \
{'console_scripts': ['ytm-ll-dl = ytm_ll_dl.main:main']}

setup_kwargs = {
    'name': 'ytm-ll-dl',
    'version': '0.1.0',
    'description': "Download 'Liked music' playlist from Youtube Music",
    'long_description': "# ytm-ll-dl\n\nPython app to download 'Liked music' playlist from Youtube Music.\n\n## Usage\n\nFor full help, run `ytm-ll-dl --help`.\n\nBasic usage:\n```sh\n$ ytm-ll-dl\n    --output ./data/ # Where to store downloaded music\n    --limit INT      # Limit how much tracks to fetch from the beginning of playlist\n    --skip INT       # Skip specified amount of tracks from the end of playlist\n```\n\nOn first run, this will ask you to provide auth data from YTM.\nSee [ytmusicapi documentation](https://ytmusicapi.readthedocs.io/en/latest/setup.html#copy-authentication-headers)\nfor details.\n\n`ytm-ll-dl` will download all liked tracks with thumbnails and some meta-info\n(author, album, name).\n\nYou can interrupt `ytm-ll-dl` --- download state will be saved and restored on the next run.",
    'author': 'kotborealis',
    'author_email': 'kotborealis@awooo.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
