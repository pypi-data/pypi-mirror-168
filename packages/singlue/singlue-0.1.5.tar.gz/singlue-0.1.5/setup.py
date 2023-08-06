# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['singlue']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['singlue = singlue.main:main']}

setup_kwargs = {
    'name': 'singlue',
    'version': '0.1.5',
    'description': '',
    'long_description': '# singlue\n[![PyPI version](https://badge.fury.io/py/singlue.svg)](https://pypi.org/project/singlue/)\n![Python Versions](https://img.shields.io/pypi/pyversions/singlue.svg)\n\n\nA CLI tool to resolve function,class codes and integrate them to single file.\n\nThis program depends on `ast.unparse()`(added in `python3.9`).\n\n## installation\n```sh\npip install singlue\n```\n\n## example usage\n\n```sh\nsinglue main.py > output.py\n```\n\n![image](./resource/image.png)\n\n`singlue` generates `output.py` from `main.py`,`library.py`.\n\n\n\n### `main.py`\n```python\nfrom library import one, two, Three\n\n\nassert one() + two() == Three().three()\n```\n\n### `library.py`\n```python\ndef one() -> int:\n    return 1\n\n\ndef two() -> int:\n    return 2\n\n\nclass Three:\n    def __init__(self):\n        self.value = 3\n\n    def three(self):\n        return self.value\n```\n\n### `output.py`\n```python\ndef one() -> int:\n    return 1\ndef two() -> int:\n    return 2\nclass Three:\n\n    def __init__(self):\n        self.value = 3\n\n    def three(self):\n        return self.value\nassert one() + two() == Three().three()\n```\n',
    'author': 'kawagh',
    'author_email': 'kawagh@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
