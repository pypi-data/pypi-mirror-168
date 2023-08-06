# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dnac_sidekick',
 'dnac_sidekick.device_commands',
 'dnac_sidekick.health',
 'dnac_sidekick.inventory',
 'dnac_sidekick.licenses']

package_data = \
{'': ['*']}

install_requires = \
['Pygments==2.13.0',
 'attrs==22.1.0',
 'black==22.8.0',
 'certifi==2022.6.15.1',
 'charset-normalizer==2.1.1',
 'click==8.1.3',
 'commonmark==0.9.1',
 'coverage==6.4.4',
 'idna==3.3',
 'iniconfig==1.1.1',
 'mypy-extensions==0.4.3',
 'packaging==21.3',
 'pathspec==0.10.1',
 'platformdirs==2.5.2',
 'pluggy==1.0.0',
 'py==1.11.0',
 'pyparsing==3.0.9',
 'pytest-cov==3.0.0',
 'pytest==7.1.3',
 'python-dotenv==0.21.0',
 'requests==2.28.1',
 'rich==12.5.1',
 'tomli==2.0.1',
 'typing-extensions==4.3.0',
 'urllib3==1.26.12']

entry_points = \
{'console_scripts': ['dnac-sidekick = dnac_sidekick.cli:dnac_cli']}

setup_kwargs = {
    'name': 'dnac-sidekick',
    'version': '0.1.1',
    'description': 'A CLI app used to interact with Cisco DNA Center',
    'long_description': '[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![codecov](https://codecov.io/gh/dannywade/dnac-sidekick/branch/main/graph/badge.svg?token=IWBEDN1YXH)](https://codecov.io/gh/dannywade/dnac-sidekick)\n\n# dnac-sidekick\nDNAC Sidekick is a CLI app used to interact with Cisco DNA Center (DNAC). It\'s built using the [Click](https://github.com/pallets/click) and [Rich](https://github.com/Textualize/rich) libraries. The Rich library is what helps make the output look cleaner to the end-user. \n\nThe goal of the tool is to provide a clean and user-friendly CLI interface to quickly pull information from DNA Center. All interactions with DNAC uses DNA Center\'s REST API, so please make sure that the REST API is enabled and the user account(s) used with this tool have proper API permissions.\n\n## Installation\nInstall using `pip` or any other PyPi package manager:\n```\npip install dnac-sidekick\n```\n\n## Getting Started\n\n### Authenticating to DNAC\nDNAC-Sidekick pulls all user-specific information from environmnet variables. Ideally, this would be a more automated process with less manual work for the user, but for now, the following environment variables must be set manually before using the tool:\n```\nUnix/MacOS\nexport DNAC_URL=<https://dnac_url>\nexport DNAC_USER=<username>\nexport DNAC_PASS=<password>\n\nWindows\nset DNAC_URL=<https://dnac_url>\nset DNAC_USER=<username>\nset DNAC_PASS=<password>\n```\n\nOnce set, we will need to generate a bearer token, which is used to authenticate to the DNAC REST API. You can manually generate this token using curl or Postman, but there\'s also a built-in command that will generate one for you. This will only work if the URL, username, and password environment variables are set.\n\n```\ndnac-sidekick login \n\nToken generated successfully!\nCopy token below and set as environment variable for future requests:\neyJhbGciOiJS.....\n```\n\n*IMPORTANT:* Please make sure to generate the bearer token using the `dnac-sidekick login` command *AFTER* setting the necessary environment variables. Once the token is generated, don\'t forget to set it as an evironment variable as well.\n\n```\nUnix/MacOS\nexport DNAC_TOKEN=<token>\n\nWindows\nset DNAC_TOKEN=<token>\n```\n\n## Usage\nTo see what commands are available, use the `--help` option. Here\'s a brief look at the current root commands available:\n```\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  command-runner  Run \'show\' commands on network devices in DNAC.\n  get             Action for read-only tasks and gathering information.\n  login           Use username and password to authenticate to DNAC.\n```\n\n## Feature Highlights\nThe goal is to provide features that help extract the most useful information from DNAC for the user. The tool is not built to have a command for every available DNAC API call - it\'s simply meant to be an engineer\'s *sidekick* :grin: when interacting with Cisco DNA Center. This feature list will grow, but here are the current tasks that can be performed using DNAC Sidekick:\n\n**Inventory**\n- Device information (all devices or a specific device via hostname)\n  - Hostname\n  - Device type\n  - Serial number\n  - Software version\n- Device license information\n  - Network license level\n  - DNA license level\n  - License validity (valid or expired)\n  - Virtual account\n  - Device UDI\n\n**Assurance**\n- Device health\n- Client health\n  - All\n  - Wired\n  - Wireless\n\n**Command Runner**\n- Run *valid* `show` commands on any device in DNAC inventory\n  - Valid `show` commands are dictated by DNAC\n\n## Examples:\n**Inventory** \n```\n# All devices\ndnac-sidekick get inventory devices\n\n# Specific device\ndnac-sidekick get inventory devices --hostname leaf1.abc.inc\n\n# License info\ndnac-sidekick get licenses\n```\n\n**Assurance** \n```\n# Device health\ndnac-sidekick get health devices\n\n# Client health\ndnac-sidekick get health clients\n```\n\n**Command Runner** \n```\ndnac-sidekick command-runner --device leaf1.abc.inc --command "show run"\n```\n\n<details>\n<summary>Sample Outputs</summary>\n\n***All sample outputs use the Cisco DevNet Always-on DNAC sandbox.***\n\n### Network Inventory\n![Network Inventory](./imgs/get_network_inventory.png)\n\n### Network Inventory - Specific Device\n![Inventory - Specific Device](./imgs/get_specific_device.png)\n\n### Device Licensing\n![Device Licensing](./imgs/get_device_licensing.png)\n\n### Device Health\n![Device Health](./imgs/get_device_health.png)\n\n### Client Health\n![Client Health](./imgs/get_client_health.png)\n\n</details>\n<br>\n\n## Compatibility\nTested with:\n- DNA Center 2.2.3.4\n\n*If you are able to test with other versions, please open a PR and add it to the list!*\n',
    'author': 'Dan Wade',
    'author_email': 'danny.wade35@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dannywade/dnac-sidekick',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
