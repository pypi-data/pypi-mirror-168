# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alnoda_wrk', 'alnoda_wrk.tui', 'alnoda_wrk.wrk.ui.macros']

package_data = \
{'': ['*'],
 'alnoda_wrk': ['wrk/*',
                'wrk/requires/*',
                'wrk/ui/*',
                'wrk/ui/conf/*',
                'wrk/ui/docs/*',
                'wrk/ui/docs/assets/*',
                'wrk/ui/docs/assets/home/*',
                'wrk/ui/docs/javascript/*',
                'wrk/ui/docs/pages/*',
                'wrk/ui/docs/pages/my_apps/*',
                'wrk/ui/docs/stylesheets/*',
                'wrk/ui/overrides/partials/*']}

install_requires = \
['Cerberus>=1.3,<2.0',
 'PyYAML>=6.0,<7.0',
 'jinja2>=3.0,<4.0',
 'pyTermTk>=0.10.22a0,<0.11.0',
 'pyfiglet>=0.8.post1,<0.9',
 'typer[all]>=0.6,<0.7']

entry_points = \
{'console_scripts': ['alnoda-wrk = alnoda_wrk.main:app']}

setup_kwargs = {
    'name': 'alnoda-wrk',
    'version': '0.2.18',
    'description': 'A tool to build Alnoda workspaces',
    'long_description': '# alnoda-wrk\n\nA tool to build alnoda workspaces\n\n\n',
    'author': 'bluxmit',
    'author_email': 'bluxmit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
