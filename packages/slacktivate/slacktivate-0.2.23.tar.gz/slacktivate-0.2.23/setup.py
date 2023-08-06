# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['slacktivate',
 'slacktivate.cli',
 'slacktivate.cli.commands',
 'slacktivate.helpers',
 'slacktivate.input',
 'slacktivate.macros',
 'slacktivate.slack']

package_data = \
{'': ['*']}

install_requires = \
['MarkupSafe==2.0.1',
 'Pillow==9.0.1',
 'aiohttp>=3.7.4,<4.0.0',
 'backoff>=1.10.0,<2.0.0',
 'click-option-group>=0.5.1,<0.6.0',
 'click>=7.1.2,<8.0.0',
 'click_help_colors>=0.8,<0.9',
 'click_spinner>=0.1.10,<0.2.0',
 'comma>=0.5.3,<0.6.0',
 'ipython[ipython]>=7.19.0,<8.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.24.0,<3.0.0',
 'slack-scim>=1.1.0,<2.0.0',
 'slackclient>=2.8.0,<3.0.0',
 'tqdm>=4.49.0,<5.0.0',
 'urllib3>=1.26.5,<2.0.0',
 'yaql>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['slacktivate = slacktivate.cli.__main__:main']}

setup_kwargs = {
    'name': 'slacktivate',
    'version': '0.2.23',
    'description': 'Slacktivate is a Python library and Command-Line Interface to assist in the provisioning and management of a Slack workspace.',
    'long_description': '# Slacktivate\n\n![pytest](https://github.com/jlumbroso/slacktivate/workflows/pytest/badge.svg)\n [![codecov](https://codecov.io/gh/jlumbroso/slacktivate/branch/master/graph/badge.svg?token=RCZNE245ZZ)](https://codecov.io/gh/jlumbroso/slacktivate)\n [![Documentation Status](https://readthedocs.org/projects/slacktivate/badge/?version=latest)](https://slacktivate.readthedocs.io/en/latest/?badge=latest)\n [![Downloads](https://pepy.tech/badge/slacktivate)](https://pepy.tech/project/slacktivate)\n [![Stargazers](https://img.shields.io/github/stars/jlumbroso/slacktivate?style=social)](https://github.com/jlumbroso/slacktivate)\n\n\nSlacktivate is a Python library and Command-Line Interface\nto assist in the provisioning and management of a Slack workspace, using\nboth the Slack API and the Slack SCIM API:\n\n- Write a YAML specifications to describe your users, channels and groups,\n  then have Slacktivate set up your workspace with no manual intervention.\n  \n- Use the self-documented Slacktivate REPL to immediately do batch operations\n  on your Slack workspace and build new powerful macros.\n\n- Robust, Pythonic wrapper to the Slack API and Slack SCIM API clients,\n  able to abstract some of the quirks of the API—as well as able to handle\n  typical error management (such as rate limiting) transparently.\n  \n- Find everything you need to be a Slack power user in one place, rather\n  than spread to a microcosm of evolving documentations.\n\n## Installation\n\nThe package is available on PyPI as `slacktivate` and so is available the\nusual way, i.e., `pip install slacktivate`; in addition to the Python package,\nthis should also install a CLI binary that is runnable, called `slacktivate`:\n\n```\n$ slacktivate --help\nUsage: slacktivate [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --token $SLACK_TOKEN  Slack API token (requires being an owner or admin).\n  --spec SPEC           Provide the specification for the Slack workspace.\n  -y, --dry-run         Do not actually perform the action.\n  --version             Show the version and exit.\n  --help                Show this message and exit.\n\nCommands:\n  list      Lists any type of object defined in the provided specification...\n  repl      A Python REPL with the Slacktivate package, and Slack clients...\n  users     Sub-command for operations on Slack users (e.g.: activate,...\n  validate  Validate the configuration file SPEC\n```\n\n## Specification Example\n\nThe following is an example of specification for a workspace, with the user\ninformation (name, emails, perhaps additional profile information) stored here\nin external CSV files:\n```yaml\nvars:\n  "TERM": "2020-Q4"\n\nusers:\n\n  - file: "input/{{ vars.TERM }}_managers*.csv"\n    sort: "newest"\n    type: "csv"\n    key: "{{ email }}"\n    fields:\n      "type": ["manager", "employee"]\n\n      # Slack normal fields\n      "givenName": "{{ first }}"\n      "familyName": "{{ last }}"\n      "userName": "{{ email.split(\'@\')[0] }}"\n\n  - file: "input/{{ vars.TERM }}_associates*.csv"\n    sort: "newest"\n    type: "csv"\n    key: "{{ email }}"\n    fields:\n      "type": ["employee"]\n\n      # Slack normal fields\n      "givenName": "{{ first }}"\n      "familyName": "{{ last }}"\n      "userName": "{{ email.split(\'@\')[0] }}"\n\nsettings:\n  slack_token: "<slack-token>"\n  workspace: "https://princetoncsgrad.slack.com/"\n  keep_customized_photos: true\n  keep_customized_name: true\n  extend_group_memberships: false\n  extend_channel_memberships: false\n  alternate_emails: "./output/alternate-emails.txt"\n\ngroups:\n  - name: "managers"\n    filter: "$.where(\'manager\' in $.type)"\n\n  - name: "employees"\n    filter: "$.where(\'employee\' in $.type)"\n\nchannels:\n  - name: "managers-only"\n    private: true\n    groups: ["manager"]\n\n  - name: "announcements"\n    permissions: "admin"\n\n  - name: "water-cooler"\n    groups: ["manager", "employee"]\n```\n\n## Introduction\n\nSlack is a wonderful platform for chat, with an extensive API that allows for\nmany powerful integrations. But the Slack client currently (in its most frequently\navailable interface) does not provide any support for batch operations.\n\nSlacktivate is a powerful tool that allows you to specify the users, group\nmemberships and channels in a YAML specification file, and to have the tool\nautomatically synchronize this specification with the Slack workspace.\n\nBelow is some context to explain why I created this tool.\n\n### Batch managing users in channels\n\nAs an example:\n- users [can only be added to a channel one-by-one](https://slack.com/help/articles/201980108-Add-people-to-a-channel),\n- users can only be removed from a channel one-by-one,\n\n![Slack modal to add users to a channel as of October 2020](docs/source/_static/slack-screenshots/add-user-to-channel-modal.png)\n\nand when you are managing a Slack workspace with hundreds of users, this can\nbecome a bottleneck of operations very quickly. Slack is actively trying to\naddress this point, but so far, is not really making a difference---[the\nchannel manager that was recently introduced](https://slack.com/help/articles/360047512554-Use-channel-management-tools)\nstill only provides the same modal to add users, and no additional options to remove users.\n\nThis problem exists throughout Slack. Beyond the membership of channels, this\nissue exists also with the membership of the workspace, of groups, and so on.\n\nPart of the issue is that Slack Enterprise Grid product relies on a\ncompany\'s existing directory solution to address these needs; but this is\nof no use to the many teams that are finding success with a lower tier of\nthe service. \n\n### The solution: Automating the process\n\n<to be written>\n\n## Prerequisites: Having Owner Access and Getting an API Token\n\nIn order to use the SCIM API, you need to be an owner of the workspace, and obtain an API token with `admin` scope.\n\nAs explained in [the official Slack SCIM API documentation](https://api.slack.com/scim#access), the easiest way to obtain a valid token for the purposes of SCIM provisioning is as follows:\n1. As *a Workspace/Organization Owner*, create [a new app for your workspace](https://api.slack.com/apps?new_app=1) (see [here](https://api.slack.com/start/overview#creating) for the documentation).\n2. Add the `admin` OAuth scope to [the "User Token Scopes" section](https://api.slack.com/authentication/quickstart#configuring).\n3. Install the app to your workspace (see [here](https://api.slack.com/start/overview#installing_distributing) for the documentation).\n4. Use the generated token available in the "OAuth & Permissions" tab (if you are provided with multiple tokens, use the "OAuth Access Token" not the "Bot User OAuth Access Token").\n\nNote that you can easily *reinstall your app* with different permissions if it turns out you did not select all the necessary permissions.\n\n\n## License\n\nThis project is licensed [under the LGPLv3 license](https://www.gnu.org/licenses/lgpl-3.0.en.html),\nwith the understanding that importing a Python modular is similar in spirit to dynamically linking\nagainst it.\n\n- You can use the library/CLI `slacktivate` in any project, for any purpose,\n  as long as you provide some acknowledgement to this original project for\n  use of the library (for open source software, just explicitly including\n  `slacktivate` in the dependency such as a `pyproject.toml` or `Pipfile`\n  is acknowledgement enough for me!).\n\n- If you make improvements to `slacktivate`, you are required to make those\n  changes publicly available.\n\nThis license is compatible with the license of all the dependencies as\ndocumented in [this project\'s own `pyproject.toml`](https://github.com/jlumbroso/slacktivate/blob/master/pyproject.toml#L29-L49).\n',
    'author': 'Jérémie Lumbroso',
    'author_email': 'lumbroso@cs.princeton.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jlumbroso/slacktivate',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
