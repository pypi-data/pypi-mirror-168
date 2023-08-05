# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['g']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['g = g:run']}

setup_kwargs = {
    'name': 'g',
    'version': '0.0.3a0',
    'description': 'cli command to easily sync current directory',
    'long_description': "# `$ g`\n\nPassthrough to your current directories vcs (or reach for it with --cwd)\n\n[![Python Package](https://img.shields.io/pypi/v/g.svg)](https://pypi.org/project/g/)\n[![Docs](https://github.com/vcs-python/g/workflows/docs/badge.svg)](https://g.git-pull.com)\n[![Build Status](https://github.com/vcs-python/g/workflows/tests/badge.svg)](https://github.com/vcs-python/g/actions?query=workflow%3A%22tests%22)\n[![Code Coverage](https://codecov.io/gh/vcs-python/g/branch/master/graph/badge.svg)](https://codecov.io/gh/vcs-python/g)\n[![License](https://img.shields.io/github/license/vcs-python/g.svg)](https://github.com/vcs-python/g/blob/master/LICENSE)\n\nShortcut / powertool for developers to access current repos' vcs, whether it's\nsvn, hg, mercurial.\n\n```console\n$ pip install --user g\n```\n\n```console\n$ g\n```\n\n### Developmental releases\n\nYou can test the unpublished version of g before its released.\n\n- [pip](https://pip.pypa.io/en/stable/):\n\n  ```console\n  $ pip install --user --upgrade --pre g\n  ```\n\n- [pipx](https://pypa.github.io/pipx/docs/):\n\n  ```console\n  $ pipx install --suffix=@next g --pip-args '\\--pre' --force\n  ```\n\n  Then use `g@next --help`.\n\n# Credits\n\n2021-12-05: Thanks to [John Shanahan](https://github.com/shanahanjrs) ([@\\_shanahanjrs](https://twitter.com/_shanahanjrs)) for giving g use [g](https://pypi.org/project/g/)\n\n# Donations\n\nYour donations fund development of new features, testing and support.\nYour money will go directly to maintenance and development of the\nproject. If you are an individual, feel free to give whatever feels\nright for the value you get out of the project.\n\nSee donation options at <https://git-pull.com/support.html>.\n\n# More information\n\n- Python support: >= 3.7, pypy\n- VCS supported: git(1), svn(1), hg(1)\n- Source: <https://github.com/vcs-python/g>\n- Docs: <https://g.git-pull.com>\n- Changelog: <https://g.git-pull.com/history.html>\n- API: <https://g.git-pull.com/api.html>\n- Issues: <https://github.com/vcs-python/g/issues>\n- Test Coverage: <https://codecov.io/gh/vcs-python/g>\n- pypi: <https://pypi.python.org/pypi/g>\n- Open Hub: <https://www.openhub.net/p/g>\n- License: [MIT](https://opensource.org/licenses/MIT).\n",
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://g.git-pull.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
