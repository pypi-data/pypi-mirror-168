# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyasstosrt']

package_data = \
{'': ['*']}

extras_require = \
{'cli': ['fire>=0.3.1', 'pyfiglet']}

setup_kwargs = {
    'name': 'pyasstosrt',
    'version': '1.2.1',
    'description': 'Convert ASS subtitle to SRT format',
    'long_description': 'pyasstosrt\n=================================================================================================================================================================================\n\n[![Build Status](https://travis-ci.com/GitBib/pyasstosrt.svg?branch=master)](https://travis-ci.com/GitBib/pyasstosrt) [![alt text](https://img.shields.io/pypi/v/pyasstosrt.svg?style=flat)](https://pypi.org/project/pyasstosrt/) [![Downloads](https://pepy.tech/badge/pyasstosrt)](https://pepy.tech/project/pyasstosrt) [![codecov](https://codecov.io/gh/GitBib/pyasstosrt/branch/master/graph/badge.svg?token=VGTJ3NYHOV)](https://codecov.io/gh/GitBib/pyasstosrt)\n\n**pyasstosrt** – this tool will help you convert Advanced SubStation Alpha (ASS/SSA) subtitle files to SubRip (SRT) files.\n\nSupport for str path:\n```python\nfrom pyasstosrt import Subtitle\n\nsub = Subtitle(\'sub.ass\')\nsub.export()\n```\n\nSupport for all Path-like objects, instead of only pathlib\'s Path:\n\n```python\nfrom pathlib import Path\n\nfrom pyasstosrt import Subtitle\n\npath = Path(\'sub.ass\')\nsub = Subtitle(path)\nsub.export()\n```\n\nYou can get a sheet with dialogue by specifying output_dialogues.\n\n```python\nfrom pathlib import Path\n\nfrom pyasstosrt import Subtitle\n\npath = Path(\'sub.ass\')\nsub = Subtitle(path)\nsub.export(output_dialogues=True)\n```\nCLI\n------------\n```bash\npyasstosrt --filepath=/Users/user/sub/sub.ass export\n```\n\n**Optional** You can specify an export folder.\n```bash\npyasstosrt --filepath=/Users/user/sub/sub.ass export /Users/user/sub/srt\n```\n\nInstallation\n------------\nMost users will want to simply install the latest version, hosted on PyPI:\n\n    $ pip install "pyasstosrt[cli]"\n\nIf you just want to use it as a library and don\'t need the CLI, you can omit the `[cli]` extra.\n',
    'author': 'GitBib',
    'author_email': 'me@bnff.website',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/GitBib/pyasstosrt',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
