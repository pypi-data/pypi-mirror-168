# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yarndevtools',
 'yarndevtools.cdsw',
 'yarndevtools.cdsw.job_configs',
 'yarndevtools.cdsw.libreloader',
 'yarndevtools.cdsw.scripts.experiments',
 'yarndevtools.commands',
 'yarndevtools.commands.branchcomparator',
 'yarndevtools.commands.reviewsheetbackportupdater',
 'yarndevtools.commands.reviewsync',
 'yarndevtools.commands.unittestresultaggregator',
 'yarndevtools.commands.unittestresultfetcher',
 'yarndevtools.commands.upstreamumbrellafetcher',
 'yarndevtools.common']

package_data = \
{'': ['*'],
 'yarndevtools.cdsw': ['resources/*',
                       'scripts/*',
                       'unit-test-result-aggregator/*']}

install_requires = \
['bs4',
 'dacite',
 'dataclasses-json',
 'gitpython',
 'google-api-wrapper2==1.0.2',
 'humanize',
 'jira',
 'python-common-lib==1.0.2']

entry_points = \
{'console_scripts': ['exec-yarndevtools = yarndevtools.yarn_dev_tools:run']}

setup_kwargs = {
    'name': 'yarn-dev-tools',
    'version': '1.1.1',
    'description': '',
    'long_description': '[![CI for YARN dev tools (pip)](https://github.com/szilard-nemeth/yarn-dev-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/szilard-nemeth/yarn-dev-tools/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/szilard-nemeth/yarn-dev-tools/branch/master/graph/badge.svg?token=OQD6FIFF7I)](https://codecov.io/gh/szilard-nemeth/yarn-dev-tools)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![GitHub language count](https://img.shields.io/github/languages/count/szilard-nemeth/yarn-dev-tools)\n\n\n# YARN-dev tools\n\nThis project contains various developer helper scripts in order to simplify everyday tasks related to Git and Apache Hadoop YARN development.\n\n### Getting started / Setup\n\nYou need to have Python 3.8 and [poetry](https://python-poetry.org/docs/#installation) installed.\n\nRun `make` from this directory and all python dependencies will be installed required by the project.\n\n\n## Running the tests\n\nTODO\n\n## Main dependencies\n\n* [gitpython](https://gitpython.readthedocs.io/en/stable/) - GitPython is a python library used to interact with git repositories, high-level like git-porcelain, or low-level like git-plumbing.\n* [tabulate](https://pypi.org/project/tabulate/) - python-tabulate: Pretty-print tabular data in Python, a library and a command-line utility.\n* [bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Beautiful Soup is a Python library for pulling data out of HTML and XML files.\n## Contributing\n\nTODO \n\n## Authors\n\n* **Szilard Nemeth** - *Initial work* - [Szilard Nemeth](https://github.com/szilard-nemeth)\n\n## License\n\nTODO \n\n## Acknowledgments\n\nTODO\n\n\n## Example commands\n\n\n## Setup of precommit\n\nConfigure precommit as described in this blogpost: https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/\nCommands:\n1. Install precommit: `pip install pre-commit`\n2. Make sure to add pre-commit to your path. For example, on a Mac system, pre-commit is installed here: \n   `$HOME/Library/Python/3.8/bin/pre-commit`.\n2. Execute `pre-commit install` to install git hooks in your `.git/` directory.\n\n## Troubleshooting\n\n### Installation issues\nIn case you\'re facing a similar issue:\n```\nAn error has occurred: InvalidManifestError: \n=====> /<userhome>/.cache/pre-commit/repoBP08UH/.pre-commit-hooks.yaml does not exist\nCheck the log at /<userhome>/.cache/pre-commit/pre-commit.log\n```\n, please run: `pre-commit autoupdate`\nMore info here: https://github.com/pre-commit/pre-commit/issues/577\n\n## Setting up handy aliases to use YARN-dev tools\n\nThere\'s only 1 prerequisite step to install all dependencies of yarn-dev-tools.\nThe project root contains a pyproject.toml file that has all the dependencies listed that will understood by Poetry.\nSimply go to the root of this project and execute: \n```\npoetry install\n```\n\nAfter this, you are ready to set up some aliases. In my system, I have [these aliases](\nhttps://github.com/szilard-nemeth/linux-env/blob/badf82f11f08d77cafbdbb19a1e2da83f392b1e4/workplace-specific/cloudera/scripts/yarn/yarn-dev-tools.sh#L73-L101).\n\nwhere: \n- SYSTEM_PYTHON_EXECUTABLE should be set to "/usr/local/bin/python3": \n```\n➜ ls -la /usr/local/bin/python3\nlrwxr-xr-x  1 snemeth  admin  38 Jun 14 23:43 /usr/local/bin/python3 -> ../Cellar/python@3.9/3.9.5/bin/python3\n```\n- VENV should be set to a virtualenv where yarndevtools is installed to. On my system it is set to "/Users/snemeth/development/my-repos/linux-env/venv"\n- HADOOP_DEV_DIR should be set to the upstream Hadoop repo root, e.g.: "/Users/snemeth/development/apache/hadoop/"\n- CLOUDERA_HADOOP_ROOT should be set to the downstream Hadoop repo root, e.g.: "/Users/snemeth/development/cloudera/hadoop/"\nThe latter 2 environment variables is better to be added to your bashrc file to keep them between the shells.\n\n\n### Examples for YARN backporter\nTo backport YARN-6221 to 2 branches, run these commands:\n```\nyarn-backport YARN-6221 COMPX-6664 cdpd-master\nyarn-backport YARN-6221 COMPX-6664 CDH-7.1-maint --no-fetch\n```\nThe first argument is the upstream Jira ID<br>\nThe second argument is the downstream Jira ID.<br>\nThe third argument is the downstream branch.<br>\nThe `--no-fetch` option is a means to skip git fetch on both repos.\n\n### How to backport to an already existing relation chain?\n1. Go to Gerrit UI and download the patch.\nFor example: \n```\ngit fetch "https://gerrit.sjc.cloudera.com/cdh/hadoop" refs/changes/29/156429/5 && git checkout FETCH_HEAD\n```\n2. Checkout a new branch\n```\ngit checkout -b my-relation-chain \n```\n\n3. Run backporter with: \n```\nyarn-backport-c6 YARN-10314 COMPX-7855 CDH-7.1.7.1000 --no-fetch --downstream_base_ref my-relation-chain\n```\nwhere:<br>\nThe first argument is the upstream Jira ID<br>\nThe second argument is the downstream Jira ID.<br>\nThe third argument is the downstream branch.<br>\nThe `--no-fetch` option is a means to skip git fetch on both repos.<br>\nThe `--downstream_base_ref <local-branch` is a way to use a local branch to base the backport on so the Git remote name won\'t be prepended.\n\n\nFinally, I set up two aliases for pushing the changes to the downstream repo:\n```\nalias git-push-to-cdpdmaster="git push <REMOTE> HEAD:refs/for/cdpd-master%<REVIEWER_LIST>"\nalias git-push-to-cdh71maint="git push <REMOTE> HEAD:refs/for/CDH-7.1-maint%<REVIEWER_LIST>"\n```\nwhere REVIEWER_LIST is in this format: "r=user1,r=user2,r=user3,..."\n\n## CDSW Initial setup\n1. Upload the initial setup scripts to the CDSW files, to the root directory (/home/cdsw)\n- [initial-cdsw-setup.sh](yarndevtools/cdsw/scripts/initial-cdsw-setup.sh)\n- [install-requirements.sh](yarndevtools/cdsw/scripts/install-requirements.sh)\n\n2. Create a new CDSW session.\nWait for the session to be launched and open up a terminal by Clicking "Terminal access" on the top menu bar.\n\n\n3. Execute this command:\n```\n~/initial-cdsw-setup.sh user cloudera\n```\n\n\nThe script performs the following actions: \n1. Downloads the scripts that are cloning the upstream and downstream Hadoop repositories + installing yarndevtools itself as a python module.\nThe download location is: `/home/cdsw/scripts`<br>\nPlease note that the files will be downloaded from the GitHub master branch of this repository!\n- [clone_downstream_repos.sh](yarndevtools/cdsw/scripts/clone_downstream_repos.sh)\n- [clone_upstream_repos.sh](yarndevtools/cdsw/scripts/clone_upstream_repos.sh)\n\n2. Executes the script described in step 2. \nThis can take some time, especially cloning Hadoop.\nNote: The individual CDSW jobs should make sure for themselves to clone the repositories.\n\n3. Copies the [python-based job configs](yarndevtools/cdsw/job_configs) for all jobs to `/home/cdsw/jobs`\n\n4. All you have to do in CDSW is to set up the projects and their starter scripts like this:\n\n| Project                                                                | Starter script location         | Arguments for script          |\n|------------------------------------------------------------------------|---------------------------------|-------------------------------|\n| Jira umbrella data fetcher (Formerly: Jira umbrella checker reporting) | scripts/start_job.py            | jira-umbrella-data-fetcher    |\n| Unit test result aggregator                                            | scripts/start_job.py            | unit-test-result-aggregator   |\n| Unit test result fetcher (Formerly: Unit test result reporting)        | scripts/start_job.py            | unit-test-result-fetcher      |\n| Branch comparator (Formerly: Downstream branchdiff reporting)          | scripts/start_job.py            | branch-comparator             |\n| Review sheet backport updater                                          | scripts/start_job.py | review-sheet-backport-updater |\n| Reviewsync                                                             | scripts/start_job.py | reviewsync                    |',
    'author': 'Szilard Nemeth',
    'author_email': 'szilard.nemeth88@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/szilard-nemeth/yarn-dev-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
