# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['berhoel', 'berhoel.helper', 'berhoel.helper.tests']

package_data = \
{'': ['*']}

install_requires = \
['setuptools>=65.3.0,<66.0.0', 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['set_lib_version = berhoel.helper.set_version:build']}

setup_kwargs = {
    'name': 'bhoelhelper',
    'version': '1.3.2',
    'description': 'Misc helper functionalities.',
    'long_description': '====================\n bhoelHelper module\n====================\n\nSome helper modules used in my other modules.\n\nInstallation\n============\n\npip install bhoelHelper\n\nAvailability\n============\n\nThe latest version should be available at my `GitLab\n<https://gitlab.com/berhoel/python/bhoelHelper.git>`_ repository, the\npackage is avaliable at `pypi\n<https://pypi.org/project/bhoelHelper/>`_ via ``pip install\nbhoelHelper``.\n\nDocumentation\n=============\n\nDocumentation for the project is avaliable `here <https://python.höllmanns.de/bhoelHelper/>`_.\n',
    'author': 'Berthold Höllmann',
    'author_email': 'berhoel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://python.xn--hllmanns-n4a.de/bhoelHelper/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0',
}


setup(**setup_kwargs)
