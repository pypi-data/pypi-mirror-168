# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djfritz',
 'djfritz.admin',
 'djfritz.admin_views',
 'djfritz.management',
 'djfritz.management.commands',
 'djfritz.migrations',
 'djfritz.models',
 'djfritz.services',
 'djfritz.templatetags',
 'djfritz.tests',
 'djfritz.tests.fixtures',
 'djfritz_project',
 'djfritz_project.settings',
 'djfritz_project.tests',
 'djfritz_project.tests.admin']

package_data = \
{'': ['*'],
 'djfritz': ['locale/de/LC_MESSAGES/*',
             'locale/en/LC_MESSAGES/*',
             'templates/admin/djfritz/hostmodel/*',
             'templates/djfritz/*',
             'templates/djfritz/includes/*'],
 'djfritz_project': ['templates/admin/*']}

install_requires = \
['bx_django_utils',
 'bx_py_utils',
 'colorlog',
 'django',
 'django-admin-sortable2',
 'django-debug-toolbar',
 'django-reversion-compare',
 'django-tagulous',
 'django-tools',
 'fritzconnection']

entry_points = \
{'console_scripts': ['devshell = djfritz_project.dev_shell:devshell_cmdloop',
                     'run_testserver = '
                     'djfritz_project.manage:start_test_server']}

setup_kwargs = {
    'name': 'django-fritzconnection',
    'version': '0.3.0rc1',
    'description': 'Web based FritzBox management using Python/Django.',
    'long_description': '# django-fritzconnection\n\n![django-fritzconnection @ PyPi](https://img.shields.io/pypi/v/django-fritzconnection?label=django-fritzconnection%20%40%20PyPi)\n![Python Versions](https://img.shields.io/pypi/pyversions/django-fritzconnection)\n![License GPL V3+](https://img.shields.io/pypi/l/django-fritzconnection)\n\nWeb based FritzBox management using Python/Django and the great [fritzconnection](https://github.com/kbr/fritzconnection) library.\n\nThe basic idea is to block/unblock Internet access to a group of devices as easily as possible.\n\nCurrent state: **early development stage**\n\nExisting features:\n\n* actions:\n  * Change WAN access of a host or for all host of a group\n* models:\n  * HostModel - A host/device that is/was connected to your FritzBox\n    * "Static" storage for all `FritzHosts().get_hosts_info()` information\n    * Update in Admin via change list tools link and manage command\n  * HostGroupModel - Collect host/device into groups to manage "WAN access"\n    * Every group are listed on the front page\n    * Allow/Disallow "WAN access" for all hosts of a group with one click\n* a few "test" views:\n  * Host information\n    * Get information about registered hosts\n    * Get raw mesh topology\n  * Diagnose\n    * Test FritzBox connection\n    * List all FritzBox services\n\n\n[![Install django-fritzconnection with YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=django-fritzconnection)\n\n> [django-fritzconnection_ynh](https://github.com/YunoHost-Apps/django-fritzconnection_ynh) allows you to install django-fritzconnection quickly and simply on a YunoHost server. If you don\'t have YunoHost, please consult [the guide](https://yunohost.org/#/install) to learn how to install it.\n\nPull requests welcome ;)\n\n\n## Screenshots\n\n[more screenshots](https://github.com/jedie/jedie.github.io/tree/master/screenshots/django-fritzconnection)\n\n----\n\n![Group Management](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/django-fritzconnection/v0.1.0.rc1%20-%20Group%20Management.png)\n\n----\n\n![Host Change List](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/django-fritzconnection/v0.0.2%20-%20hosts%20change%20list.png)\n\n----\n\n[more screenshots](https://github.com/jedie/jedie.github.io/tree/master/screenshots/django-fritzconnection)\n\n\n## Quick start for developers\n\n```\n~$ git clone https://github.com/jedie/django-fritzconnection.git\n~$ cd django-fritzconnection\n~/django-fritzconnection$ ./devshell.py\n...\nDeveloper shell - djfritz - v0.1.0\n...\n\n(djfritz) run_testserver\n```\n\n## FritzBox Credentials\n\nSome of the FritzBox API requests needs a login. Currently the only way to store FritzBox Credentials is to add them into the environment.\n\nError message if login credentials are missing is: `Unable to perform operation. 401 Unauthorized`\n\nShell script work-a-round for developing, e.g.:\n\n```\n#!/bin/bash\n\n(\n    set -ex\n    export FRITZ_USERNAME="<username>"\n    export FRITZ_PASSWORD="<password>"\n\n    ./devshell.py run_testserver\n)\n```\nSee also: [Issues #5](https://github.com/jedie/django-fritzconnection/issues/5)\n\n## versions\n\n* [*dev*](https://github.com/jedie/django-fritzconnection/compare/v0.3.0rc1...main)\n  * Replace `DynamicViewMenu` with `bx_django_utils.admin_extra_views`\n  * Use RunServerCommand from django-tools\n  * Update test/CI setup\n  * TBC\n* [v0.2.0 - 15.05.2022](https://github.com/jedie/django-fritzconnection/compare/v0.1.0...v0.2.0)\n  * NEW: Hosts admin action to ping all IPs from selected hosts\n  * NEW: "unique host name" change list filter\n* [v0.1.0 - 08.04.2022](https://github.com/jedie/django-fritzconnection/compare/v0.0.2...v0.1.0)\n  * NEW: \'Manage host WAN access via host-groups\'\n  * NEW: Add "host group" model to collect hosts into groups\n  * NEW: \'List "last connect" information about hosts\' view\n  * Display `FRITZ_USERNAME` and `FRITZ_PASSWORD` (anonymized) on connection info page\n* [v0.0.2 - 04.04.2022](https://github.com/jedie/django-fritzconnection/compare/v0.0.1-alpha...v0.0.2)\n  * Store Host information\n  * Possible to set WAN access for one host\n* v0.0.1-alpha - 24.03.2022\n  * init the project\n',
    'author': 'JensDiemer',
    'author_email': 'git@jensdiemer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jedie/django-fritzconnection',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
