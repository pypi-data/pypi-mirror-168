#!/usr/bin/env python
"""
Mapilio Map
"""
from __future__ import (absolute_import, division, print_function)

import sys

from setuptools import find_packages, setup

if sys.version_info < (3, 5):
    raise RuntimeError(
        "Mapilio Map tools supports Python 3.6 and above. "
    )

# This import must be below the above `sys.version_info` check,
# because the code being imported here is not compatible with the older
# versions of Python.

from increment_version import __version__
from map.util import __name__
# from map.util import __version__ as version # use first pypi package

INSTALL_REQUIRES = [
    "folium"

]

setup(
    name=__name__,
    version=__version__,
    description='Mapilio Map Library',
    url='https://github.com/mapilio/helper.git',
    author='Mapilio - Ozcan Durak & M.Can VARER',
    author_email='ozcan@visiosoft.com.tr',
    license='licensed',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    python_requires=">=3.6, <4",
    project_urls={  # Optional
            'Bug Reports': 'https://github.com/mapilio/map/issues',
            'Say Thanks!': 'https://mapilio.com/#contact',
            'Source': 'https://github.com/mapilio/map/',
        },
)
