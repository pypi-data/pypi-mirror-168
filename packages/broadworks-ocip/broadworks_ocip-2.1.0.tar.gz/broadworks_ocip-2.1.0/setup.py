# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['broadworks_ocip']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.4.0,<22.0.0', 'lxml>=4.7.1,<5.0.0', 'null-object>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'broadworks-ocip',
    'version': '2.1.0',
    'description': 'API interface to the OCI-P provisioning interface of a Broadworks softswitch',
    'long_description': '# Broadworks OCI-P Interface\n\n[![Tests](https://github.com/nigelm/broadworks_ocip/workflows/Tests/badge.svg)](https://github.com/nigelm/broadworks_ocip/actions?workflow=Tests)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://nigelm.github.io/broadworks_ocip/)\n[![pypi version](https://img.shields.io/pypi/v/broadworks_ocip.svg)](https://pypi.python.org/pypi/broadworks_ocip)\n\n`broadworks_ocip` interfaces to the OCI-P provisioning interface of a Broadworks softswitch\n\n\n- Free software: BSD license\n- Documentation: https://nigelm.github.io/broadworks_ocip/\n\n----\n\n## Features\n\n- python objects to match all Broadworks schema objects\n- API framework to talk to a Broadworks server\n- additional magic to handle authentication and sessions\n- Based on Broadworks schema R24\n\n## Current Version\n\nVersion: `2.1.0`\n\n----\n\n## Installation\n\nWith `pip`:\n```bash\npython3 -m pip install broadworks-ocip\n```\n\n----\n\n## Usage\n\nMore details is given within the usage section of the documentation, but the\nminimal summary is:-\n\n```python\nfrom broadworks_ocip import BroadworksAPI\n\n# configure the API, connect and authenticate to the server\napi = BroadworksAPI(\n    host=args.host, port=args.port, username=args.username, password=args.password,\n)\n\n# get the platform software level\nresponse = api.command("SystemSoftwareVersionGetRequest")\nprint(response.version)\n```\n\n## Version 2\n\nDespite the bump in version number there are no known major incompatibilities\nfrom previous versions.  However the underlying class base has been changed\nto a vanilla python slots based system - the thinking behind this is in the\nAPI internals documentation.  This will change the underlying requirements.\n\nAdditionally at the same time I have converted to Broadworks R24 API schema\nfiles as the basis for generating these classes.  This will change the set of\navailable commands and classes.\n\n\n## Credits\n\nThe class used to be built using Michael DeHaan\'s [`ClassForge`]\n(https://classforge.io/) object system, however from version 2.0.0 it has\nbeen based on vanilla python slotted objects.\n\nDevelopment on the python version was done by\n[Nigel Metheringham `<nigelm@cpan.org>`](https://github.com/nigelm/)\n\nKarol Skibiński has been using the package, and has a talent for both finding\nbugs within it and providing a good bug report that allows a test case and fix\nto be made.  The package has been immensely improved by this work.\n\n----\n',
    'author': 'Nigel Metheringham',
    'author_email': 'nigelm@cpan.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/broadworks-ocip/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
