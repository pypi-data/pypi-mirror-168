# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wemulate',
 'wemulate.controllers',
 'wemulate.core',
 'wemulate.core.database',
 'wemulate.ext',
 'wemulate.ext.settings',
 'wemulate.ext.utils',
 'wemulate.plugins',
 'wemulate.templates',
 'wemulate.utils']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy==1.4.3',
 'colorlog==6.6.0',
 'jinja2==3.1.2',
 'netifaces==0.11.0',
 'pyroute2==0.7.1',
 'pyyaml==6.0',
 'rich>=12.5.1,<13.0.0',
 'tcconfig==0.27.1',
 'typer==0.6.1']

entry_points = \
{'console_scripts': ['wemulate = wemulate.main:app']}

setup_kwargs = {
    'name': 'wemulate',
    'version': '2.0.3',
    'description': 'A modern WAN Emulator',
    'long_description': '**A modern WAN Emulator developed by the Institute for Networked Solutions**\n# WEmulate\n\nHave a look at the [documentation](https://wemulate.github.io/wemulate) for detailed information.\n\n## Installation\n\n### Prerequisites\n* Virtual machine or physical device with at least two interfaces\n* Root permissions \n\n### Getting Started\nInstall wemulate cli application  \n```\nbash -c "$(curl -fsSL https://raw.githubusercontent.com/wemulate/wemulate/main/install/install.sh)"\n```\nYou have different options available over the install script:\n```\nSyntax: install.sh [-h|f|i|v|a]\noptions:\n-h               Print this Help.\n-f               Force install.\n-i <int1,int2>   Management interfaces to configure.\n-v               Install frontend module.\n-a               Install api module.\n```\nYou can for example install the cli, api and frontend module together with two management interfaces with the following command:\n```\ncurl -fsSL https://raw.githubusercontent.com/wemulate/wemulate/main/install/install.sh | bash -s -- -a -v -i ens2,ens3 -f\n```\n\n## Usage \n![WEmulate CLI Commands](/docs/img/animation-wemulate-cli.gif)\n\n```bash\n# Add a new connection\n$ wemulate add connection -n connectionname -i LAN-A LAN-B\n\n# Delete a connection\n$ wemulate delete connection -n connectionname\n\n# Add parameters bidirectional\n$ wemulate add parameter -n connectionname -j 20 -d 40\n\n# Add parameters in specific direction\n$ wemulate add parameter -n connectionname -j 20 -d 40 -src LAN-A -dst LAN-B\n\n```\n\n## Development\nConfigure poetry to create the environment inside the project path, in order that VSCode can recognize the virtual environment.\n```\n$ poetry config virtualenvs.in-project true\n```\nInstall the virtualenv.\n```\n$ poetry install\n```\n',
    'author': 'Julian Klaiber',
    'author_email': 'julian.klaiber@ost.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://wemulate.github.io/wemulate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
