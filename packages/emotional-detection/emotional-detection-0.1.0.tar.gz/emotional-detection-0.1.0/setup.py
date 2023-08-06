# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['emotional_detection']

package_data = \
{'': ['*']}

install_requires = \
['deepface>=0.0.75,<0.0.76',
 'h5py>=3.7.0,<4.0.0',
 'imutils>=0.5.4,<0.6.0',
 'opencv-python>=4.6.0,<5.0.0',
 'scipy>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'emotional-detection',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'DevonPeroutky',
    'author_email': 'devonperoutky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
