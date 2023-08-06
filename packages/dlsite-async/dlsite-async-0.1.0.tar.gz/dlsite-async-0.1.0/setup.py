# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dlsite_async', 'dlsite_async.play']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'lxml>=4.9.1,<5.0.0']

setup_kwargs = {
    'name': 'dlsite-async',
    'version': '0.1.0',
    'description': 'DLsite Async',
    'long_description': '# DLsite Async\n\n[![PyPI](https://img.shields.io/pypi/v/dlsite-async.svg)][pypi status]\n[![Status](https://img.shields.io/pypi/status/dlsite-async.svg)][pypi status]\n[![Python Version](https://img.shields.io/pypi/pyversions/dlsite-async)][pypi status]\n[![License](https://img.shields.io/pypi/l/dlsite-async)][license]\n\n[![Read the documentation at https://dlsite-async.readthedocs.io/](https://img.shields.io/readthedocs/dlsite-async/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/bhrevol/dlsite-async/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/bhrevol/dlsite-async/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi status]: https://pypi.org/project/dlsite-async/\n[read the docs]: https://dlsite-async.readthedocs.io/\n[tests]: https://github.com/bhrevol/dlsite-async/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/bhrevol/dlsite-async\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- Async DLsite API for fetching work metadata\n- Supports most DLsite sites:\n  - Comipo (`comic`)\n  - Doujin (All-ages/`home`, Adult/`maniax`)\n  - Adult comics (`books`)\n  - All-ages games (`soft`)\n  - Galge (`pro`)\n  - Apps (`appx`)\n- Supports common metadata for most DLsite work types\n- Japanese and English locale support\n  (English metadata may not be available for all works)\n\n## Requirements\n\n- Python 3.9+\n\n## Installation\n\nYou can install _DLsite Async_ via [pip] from [PyPI]:\n\n```console\n$ pip install dlsite-async\n```\n\n## Usage examples\n\nFetch manga information:\n\n```py\n>>> import asyncio\n>>> from dlsite_async import DlsiteAPI\n>>> async def f():\n...     async with DlsiteAPI() as api:\n...         return await api.get_work("BJ370220")\n...\n>>> asyncio.run(f())\nWork(\n    product_id=\'BJ370220\',\n    site_id=\'comic\',\n    maker_id=\'BG01675\',\n    work_name=\'衛宮さんちの今 日のごはん (6)\\u3000レシピ本付特装版\',\n    age_category=<AgeCategory.ALL_AGES: 1>,\n    circle=None,\n    brand=None,\n    publisher=\'KADOKAWA\',\n    work_image=\'//img.dlsite.jp/.../BJ370220_img_main.jpg\',\n    regist_date=datetime.datetime(2021, 10, 28, 0, 0),\n    work_type=<WorkType.MANGA: \'MNG\'>,\n    book_type=<BookType.BOOK: \'comic\'>,\n    ...\n    author=[\'TAa\', \'只野まこと\', \'ＴＹＰＥ−ＭＯＯＮ\'],\n    ...\n    genre=[\'少年コミック\', \'ギャグ\', \'コメディ\', \'ほのぼの\'],\n    label=\'KADOKAWA\',\n    ...\n    page_count=307\n)\n```\n\nFetch English voice/ASMR information:\n\n```py\n>>> async def f():\n...     async with DlsiteAPI(locale="en_US") as api:\n...         return await api.get_work("RJ294126")\n...\n>>> asyncio.run(f())\nWork(\n    product_id=\'RJ294126\',\n    site_id=\'maniax\',\n    maker_id=\'RG51931\',\n    work_name=\'Pure Pussy on Duty\',\n    age_category=<AgeCategory.R18: 3>,\n    circle=\'aoharu fetishism\',\n    brand=None,\n    publisher=None,\n    work_image=\'//img.dlsite.jp/.../RJ294126_img_main.jpg\',\n    regist_date=datetime.datetime(2020, 8, 30, 0, 0),\n    work_type=<WorkType.VOICE_ASMR: \'SOU\'>,\n    ...\n    illustration=[\'ぬこぷし\'],\n    voice_actor=[\'逢坂成美\'],\n    ...\n    genre=[\'Healing\', \'Dirty Talk\', \'Binaural\', \'ASMR\', ...],\n    ...\n    file_format=[\'WAV\'],\n    file_size=\'Total 010.63GB\',\n    ...\n)\n```\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_DLsite Async_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/bhrevol/dlsite-async/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/bhrevol/dlsite-async/blob/main/LICENSE\n[contributor guide]: https://github.com/bhrevol/dlsite-async/blob/main/CONTRIBUTING.md\n[command-line reference]: https://dlsite-async.readthedocs.io/en/latest/usage.html\n',
    'author': 'byeonhyeok',
    'author_email': 'bhrevol@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bhrevol/dlsite-async',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
