# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['authmethod', 'descope', 'descope.authmethod']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.4.0,<3.0.0',
 'cryptography>=38.0.1,<39.0.0',
 'email-validator>=1.2.1,<2.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'descope',
    'version': '0.1.0',
    'description': 'Descope Python SDK',
    'long_description': "# Descope SDK for Python\n\nUse the Descope SDK for Python to quickly and easily add user authentication to your application or website.\n\nThe SDK supports Python 3.6 and above.\n\n## Installing the SDK\n\nReplace any instance of `<ProjectID>` in the code below with your company's Project ID, which can be found in the [Descope console](https://app.descope.com).\n\nRun the following code in your project. These commands will add the Descope ExpresSDK for Python as a project dependency, and set the `DESCOPE_PROJECT_ID` variable to a valid \\<ProjectID\\>.\n\n```code\npip install descope\nexport DESCOPE_PROJECT_ID=<ProjectID>\n```\n\n## What do you want to implement?\n\nClick one of the following links to open the documentation for that specific functionality.\n\n- [x] [One time passwords (OTP)](./docs/otp.md)\n- [x] [Magic Links](./docs/magiclink.md)\n\n## License\n\nThe Descope ExpresSDK for Python is licensed for use under the terms and conditions of the [MIT license Agreement](https://github.com/descope/python-sdk/blob/main/LICENSE).\n",
    'author': 'Descope',
    'author_email': 'info@descope.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://descope.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
