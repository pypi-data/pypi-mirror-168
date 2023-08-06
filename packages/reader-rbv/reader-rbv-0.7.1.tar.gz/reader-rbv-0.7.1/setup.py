# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reader_rbv']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.0.0,<23.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'cachetools>=5.2.0,<6.0.0',
 'requests>=2.28.0,<3.0.0',
 'ujson>=5.4.0,<6.0.0']

setup_kwargs = {
    'name': 'reader-rbv',
    'version': '0.7.1',
    'description': 'SDK / Client python untuk Ruang Baca Virtual Universitas Terbuka.',
    'long_description': '# Reader RBV\n\n[![reader-rbv - PyPi](https://img.shields.io/pypi/v/reader-rbv)](https://pypi.org/project/reader-rbv/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/reader-rbv)](https://pypi.org/project/reader-rbv/)\n[![LICENSE](https://img.shields.io/github/license/UnivTerbuka/reader-rbv)](https://github.com/UnivTerbuka/reader-rbv/blob/main/LICENSE)\n[![Code Style - Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nSDK / Client python untuk Ruang Baca Virtual.\n\n## Install\n\nInstall dengan [python](https://www.python.org/)\n\n```bash\npip install --upgrade reader-rbv\n```\n\n## Penggunaan\n\n```python\nfrom reader_rbv import Reader\n\nreader = Reader("username", "Passw0rd")\n\nbook1 = reader["BOOK1"]\n\nchapter1_book1 = book1["chapter1"]\n\npage1_chapter1_book1 = chapter1_book1[1]\n\nprint(page1_chapter1_book1)\n```\n\nRubah folder cache dengan menyetel env `READER_RBV_HOME` dengan folder yang dituju.\n\n## Legal / Hukum\n\nKode ini sama sekali tidak berafiliasi dengan, diizinkan, dipelihara, disponsori atau didukung oleh [Universitas Terbuka](https://ut.ac.id/) atau afiliasi atau anak organisasinya. Ini adalah perangkat lunak yang independen dan tidak resmi. Gunakan dengan risiko Anda sendiri.\n',
    'author': 'hexatester',
    'author_email': 'habibrohman@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
