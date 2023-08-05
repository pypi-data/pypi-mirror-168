# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pykeyatome']

package_data = \
{'': ['*']}

install_requires = \
['fake-useragent>=0.1.11,<0.2.0',
 'requests>=2.22.0,<3.0.0',
 'simplejson>=3.16.0,<4.0.0']

setup_kwargs = {
    'name': 'pykeyatome',
    'version': '2.0.0',
    'description': 'A simple API for key atome electricity consumption',
    'long_description': '# KeyAtome PyPi\n![GitHub release](https://img.shields.io/github/release/jugla/pyKeyAtome)\n\nGet your energy consumption data from Atome, a Linky-compatible device made by Total/Direct-Energie.\nA account can have several linky. With this library, you can address them one by one\n\n### Installing\n```\npip install pykeyatome\n```\n\n## Use\nThe `__main__.py` is provided to show an example of use.\n\n4 types of function provided by client.py in `AtomeClient` class:\n- login : to be logged to the server\n- get_user_reference : to know which linky you have addressed \n- get_live : to retrieve live statistics (instant power)\n- get_consumption(period) : to retrieve the consumption since a period (day/week/month/year)\n\n## Acknowledgments\n* Thanks to k20human for the original inspiration with https://github.com/k20human/domoticz-atome\n* Thanks to reverse engineering of Atome IOS APP performed by BaQs.\n* This project is a fork of https://github.com/BaQs/pyAtome (seems to be unmaintained)\n\n### Breaking change\n**V1.2.0** Since this version PyAtomeError exception is no more used. Instead login return *False* if error , and live/consumption return *None*\n\n**V1.3.0** Login return *None* if error\n',
    'author': 'jugla',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jugla/pyKeyAtome',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<3.11',
}


setup(**setup_kwargs)
