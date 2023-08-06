# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['package_root']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'package-root',
    'version': '1.0.0',
    'description': 'import package_root # into your PYTHON_PATH',
    'long_description': "# Package √Root\n\n[![PyPI version](https://badge.fury.io/py/package_root.svg)](https://badge.fury.io/py/package_root)\n[![Test](https://github.com/fny/python-package_root/actions/workflows/test.yml/badge.svg)](https://github.com/fny/python-package_root/actions/workflows/test.yml)\n\n***import package_root # into your PYTHONPATH***\n\nStop appending your package root path to your Python path by hand like this:\n\n```python\nfrom os.path import abspath, dirname, join\nsys.path.insert(1, abspath(join(dirname(__file__), '..')))\n```\n\nIt's annoying and error prone. Let us do it for you. <3\n\n```python\nimport package_root\n```\n\nHow does this witchcraft work you ask?\n\nWe detect the file that called `import package_root`. We search until we find a parent directory without an `__init__.py` file. That's your `package_root`. We make it `sys.path[1]` because friends don't let friends mess with [`sys.path[0]`](https://docs.python.org/3/library/sys.html#sys.path).\n\nStill confused? Let's say you have the following setup:\n\n```\nyour_awesome_pacakge/\n    foo/\n        __init__.py\n        your_dope_module.py\n        bar/\n            __init__.py\n            baz.ipynb\n            baz.py\n    .no_init_at_this_level\n```\n\nIf you're in `baz.ipynb` or `baz.py`, we'll append `your_awesome_package` to your path so you can import whatever you want from `your_awesome_package`.\n\n```python\n# baz.ipynb or baz.py\nimport package_root\nimport foo.your_dope_module # works!\n```\nDon't believe us? We have tests to prove it.\n\n## Important Notes\n\n - You shouldn't have an `__init__.py` in your package root.\n - This is intended for Jupyter notebooks where [relative imports don't work](https://stackoverflow.com/questions/34478398/import-local-function-from-a-module-housed-in-another-directory-with-relative-im).\n\n## Installation\n\n    pip install package_root\n\n## Usage\n\n```python\nimport package_root # And nothing else\n```\n\n## Contributing\n\nFeel free to report bugs, but we won't accept feature requests since this package is intended to [do one thing and do it well](https://en.wikipedia.org/wiki/Unix_philosophy).\n",
    'author': 'Faraz Yashar',
    'author_email': 'faraz.yashar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fny/python-package_root',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
