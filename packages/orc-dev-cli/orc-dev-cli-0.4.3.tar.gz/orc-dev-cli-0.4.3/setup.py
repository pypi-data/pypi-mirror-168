# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orc_dev_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0', 'requests>=2.28.1,<3.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['orc = orc_dev_cli.cli:cli']}

setup_kwargs = {
    'name': 'orc-dev-cli',
    'version': '0.4.3',
    'description': 'CLI dev tool for interacting with openshift clusters and RHOAM addons.',
    'long_description': '# Welcome to orc-dev-cli\n\nOrc-dev-cli gives developers a CLI tool called orc.\nOrc is used to interact with openshift osd clusters and the openshift addon RHOAM.\n\nAs this is a dev tool kude-admin access to the clusters is expected.\n\n## Installation\nEasiest way to install orc is by using pip\n```shell\npip install orc-dev-cli\n```\n\n## Basic Commands\n\n* `orc addon`   Get the current state of an installed addon instances\n* `orc config`  Open configuration file\n* `orc delete`  Delete cluster.\n* `orc login`   Get cluster kubeadmin login details.\n* `orc osd`     Get basic state information on osd cluster\n\n## Shell Completion\n\n### Bash\n\n1. Create temporary bash script.\n2. Add `_ORC_COMPLETE=bash_source orc > ~/.orc-complete.bash`.\n3. Run script.\n4. Source the newly created `~/.orc-complete.bash` in `~/.bashrc` as follows `. ~/.orc-complete.bash`.\n5. Restart the shell to complete.\n',
    'author': 'Jim Fitzpatrick',
    'author_email': 'jimfity@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
