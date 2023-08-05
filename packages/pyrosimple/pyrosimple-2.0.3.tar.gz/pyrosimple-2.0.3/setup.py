# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyrosimple',
 'pyrosimple.data.config',
 'pyrosimple.io',
 'pyrosimple.job',
 'pyrosimple.scripts',
 'pyrosimple.torrent',
 'pyrosimple.ui',
 'pyrosimple.util']

package_data = \
{'': ['*'],
 'pyrosimple': ['data/htdocs/*',
                'data/htdocs/css/*',
                'data/htdocs/img/*',
                'data/htdocs/js/*',
                'data/img/*',
                'data/screenlet/*',
                'data/screenlet/themes/blueish/*',
                'data/screenlet/themes/default/*'],
 'pyrosimple.data.config': ['color-schemes/*',
                            'rtorrent.d/*',
                            'templates/*',
                            'templates/conky/*']}

install_requires = \
['Jinja2>=3.1.0,<4.0.0',
 'bencode.py>=4.0.0,<5.0.0',
 'dynaconf[toml]>=3.1.0,<4.0.0',
 'parsimonious>=0.9.0,<0.10.0',
 'prometheus-client>=0.14.1,<0.15.0',
 'prompt-toolkit>=3.0.30,<4.0.0',
 'python-daemon>=2.3.0,<3.0.0',
 'requests>=2.28.1,<3.0.0']

extras_require = \
{':python_version < "3.9"': ['importlib-resources>=5.4.0,<6.0.0'],
 'torque': ['APScheduler>=3.9.0,<4.0.0', 'pyinotify>=0.9.6,<0.10.0']}

entry_points = \
{'console_scripts': ['chtor = pyrosimple.scripts.chtor:run',
                     'lstor = pyrosimple.scripts.lstor:run',
                     'mktor = pyrosimple.scripts.mktor:run',
                     'pyroadmin = pyrosimple.scripts.pyroadmin:run',
                     'pyrotorque = pyrosimple.scripts.pyrotorque:run',
                     'rtcontrol = pyrosimple.scripts.rtcontrol:run',
                     'rtxmlrpc = pyrosimple.scripts.rtxmlrpc:run']}

setup_kwargs = {
    'name': 'pyrosimple',
    'version': '2.0.3',
    'description': 'A stripped-down version of the pyrocore tools for working with rTorrent',
    'long_description': "# pyrosimple\n\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/kannibalox/pyrosimple/Pylint)](https://github.com/kannibalox/pyrosimple/actions/workflows/pylint.yml)\n[![PyPI](https://img.shields.io/pypi/v/pyrosimple)](https://pypi.org/project/pyrosimple/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyrosimple)\n\nA overhauled Python 3 fork of the [pyrocore tools](https://github.com/pyroscope/pyrocore),\nfor working with the\n[rTorrent client](https://github.com/rakshasa/rtorrent).\n\n## Installation\n\n```bash\npip install pyrosimple\n```\n\nSee the [documentation for usage](https://kannibalox.github.io/pyrosimple/).\nIf you've used rtcontrol/rtxmlrpc before, you should feel right at home.\n\n## What's the point of this?\n\nThe pyrocore tools are great, but being stuck on python 2, along with\nthe complicated install procedure made integrating both the tools and\nthe code into other processes very painful.\n\n## Differences from pyrocore\n\nThe following lists are not exhaustive, and don't cover many of the\ninternal improvements and refactoring.\n\n- Only supports python 3 and rTorrent 0.9.8+ (0.9.6/0.9.7 should still\n  work just fine, but aren't officially supported)\n- Simpler poetry-based build/install system with a single package\n- Performance improvements\n\n### New features\n\n- Multi-instance support for rtcontrol/rtxmlrpc\n- Replaced Tempita with Jinja2\n- Support for JSON-RPC (only implemented by\n  https://github.com/jesec/rtorrent)\n- Actions to move torrent between paths, or torrents between hosts\n\n## Legacy branch\n\nIf you just want to use the pyrocore tools on python 3 without all the\nnew features, you can use the `release-1.X` branch (1.3 is the latest\nrelease at time of writing).  These releases will only receive bug\nfixes or changes to maintain compatibility with the original pyrocore\ntools.\n",
    'author': 'kannibalox',
    'author_email': 'kannibalox@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kannibalox/pyrosimple',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
