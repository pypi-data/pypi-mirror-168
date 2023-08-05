# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qlm', 'qlm.commands', 'qlm.github', 'qlm.tools', 'qlm.validators']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['qlm = qlm.main:app']}

setup_kwargs = {
    'name': 'qlm',
    'version': '0.0.3',
    'description': 'A command line app for taking beautiful notes.',
    'long_description': '<p align="center">\n  <a href="https://osintalex.github.io/qlm/">\n    <img src="https://osintalex.github.io/qlm/images/pen-orange.svg" alt="qlm" height="50px">\n  </a>\n</p>\n<p align="center">\n  <em>A command line app for taking beautiful notes.</em>\n</p>\n<p align="center">\n  <a href="https://github.com/osintalex/qlm/actions?query=event%3Apush+branch%3Amain+workflow%3ACI">\n    <img src="https://github.com/osintalex/qlm/workflows/ci-cd/badge.svg?event=push" alt="CI">\n  </a>\n<a href="https://codecov.io/gh/osintalex/qlm" >\n <img src="https://codecov.io/gh/osintalex/qlm/branch/main/graph/badge.svg?token=L82UIFTL0D"/>\n </a>\n  <a href="https://pypi.python.org/pypi/qlm">\n    <img src="https://img.shields.io/pypi/v/qlm.svg" alt="pypi">\n  </a>\n  <a href="https://github.com/osintalex/qlm">\n    <img src="https://img.shields.io/pypi/pyversions/qlm.svg" alt="versions">\n  </a>\n  <a href="https://github.com/osintalex/qlm/blob/main/LICENSE">\n    <img src="https://img.shields.io/github/license/osintalex/qlm.svg" alt="license">\n  </a>\n</p>\n\n---\n![](https://github.com/osintalex/qlm/raw/main/docs/images/intro.gif)\n\n___\n\n**qlm** gives you access to beautiful notes on any machine.\n\nThe name comes from the Arabic word for pen:\n\n## قلم\n\nwhich makes use of the three letter root _q-l-m_ to cut, snip, prune, clip or truncate. So\ntry to keep those notes concise ;-)\n\n## Basic Usage\n\n```commandline\npip install qlm\nqlm connect \'username/repo\'\necho \'# My notes\' > my_note.md\nqlm add my_note.md\nqlm show my_note.md\n```\n',
    'author': 'Alexander Darby',
    'author_email': '63904626+osintalex@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
