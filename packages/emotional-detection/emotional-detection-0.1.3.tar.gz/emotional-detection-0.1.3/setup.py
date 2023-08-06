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
    'version': '0.1.3',
    'description': 'Standalone package for capturing video from the webcam, detecting all faces in the video and then runing the DeepFace emotional classifier on each face. The output of the emotional classfications will be written as JSON to a Unix pipe to be consumed by any other process',
    'long_description': '# Overview\nThis packages is a very basic script that captures video from the webcam, detects all faces in the video and then runs the DeepFace emotional classifier on each face. The output of the emotional classfications will be written to a Unix pipe to be consumed by any other process.\n\n# Instructions\nEverything is contained in `emotional_detection/main.py`. You simply install the dependencies and run. This project works out of the box with [poetry](https://python-poetry.org/), but you could install the dependencies using any dependency manager + virtual environment combination you choose.\n',
    'author': 'DevonPeroutky',
    'author_email': 'devonperoutky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DevonPeroutky/emotional-detection',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
