# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pythoncommons',
 'pythoncommons.file_parser',
 'pythoncommons.test-scripts',
 'pythoncommons.test-scripts.commands.testcommand',
 'pythoncommons.tests']

package_data = \
{'': ['*']}

install_requires = \
['Colr>=0.9.1,<0.10.0',
 'GitPython>=3.1.27,<4.0.0',
 'bs4>=0.0.1,<0.0.2',
 'dataclasses-json>=0.5.7,<0.6.0',
 'docker>=6.0.0,<7.0.0',
 'google-api-python-client==1.7.9',
 'google-auth-httplib2==0.0.3',
 'google-auth-oauthlib==0.4.1',
 'gspread>=5.5.0,<6.0.0',
 'humanize>=4.4.0,<5.0.0',
 'jira>=3.4.1,<4.0.0',
 'oauth2client>=4.1.3,<5.0.0',
 'pytest>=6.2.3,<6.3.0',
 'requests>=2.28.1,<3.0.0',
 'sh>=1.14.1,<1.15.0',
 'tabulate>=0.8.10,<0.9.0']

setup_kwargs = {
    'name': 'python-common-lib',
    'version': '1.0.1',
    'description': '',
    'long_description': '# python-commons\n\nRun ./setup.sh to set up git pre/post push hook scripts.\nThen, a similar script loaded to the environment will execute the pre/post push hook scripts: \nhttps://stackoverflow.com/a/3812238/1106893\n\nFor example loading this script and defining an alias like this will do the trick:\n`alias gpwh="git-push-with-hooks.sh"`\n\n\n## Setup of precommit\n\nConfigure precommit as described in this blogpost: https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/\nCommands:\n1. Install precommit: `pip install pre-commit`\n2. Make sure to add pre-commit to your path. For example, on a Mac system, pre-commit is installed here: \n   `$HOME/Library/Python/3.8/bin/pre-commit`.\n2. Execute `pre-commit install` to install git hooks in your `.git/` directory.\n\n## Troubleshooting\n\n### Installation issues\nIn case you\'re facing a similar issue:\n```\nAn error has occurred: InvalidManifestError: \n=====> /<userhome>/.cache/pre-commit/repoBP08UH/.pre-commit-hooks.yaml does not exist\nCheck the log at /<userhome>/.cache/pre-commit/pre-commit.log\n```\n, please run: `pre-commit autoupdate`\nMore info here: https://github.com/pre-commit/pre-commit/issues/577',
    'author': 'Szilard Nemeth',
    'author_email': 'szilard.nemeth88@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
