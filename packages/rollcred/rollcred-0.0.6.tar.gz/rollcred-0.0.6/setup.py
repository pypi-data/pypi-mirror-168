# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rollcred']

package_data = \
{'': ['*']}

install_requires = \
['click==7.1.2', 'pyperclip==1.8.2']

setup_kwargs = {
    'name': 'rollcred',
    'version': '0.0.6',
    'description': '',
    'long_description': '# Summary\n\nA package to help replace AWS credentials from the sso window. When you click\non an AWS credential, the text is copied to the clipboard. This package reads\nthe clipboard buffer and replaces the correct profile credentials in your\n`~/.aws/credentials` file.\n\n## Installation\n\n`pip install rollcred`\n\n## Usage\n\nGoto to your AWS SSO login screen. Select the account and profile you would like to roll\ncredentials for, click on the link that says `command line or programmatic access`.\nUnder the section labeled **Option 2** click the box with the credentials. Clicking\nthe box will copy the contents to the clipboard.\n\nOpen a terminal window and type `rollcred`. The credential will be replaced in your\ncreds file. If the credential does not exist it will be appended to the end of the\nfile. If the file does not exist, it will be created at `~/.aws/credentials`\n',
    'author': 'trejas',
    'author_email': '4763901+trejas@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
