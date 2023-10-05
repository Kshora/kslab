# Author: Kenta Nakamura <c60evaporator@gmail.com>
# Copyright (c) 2020-2021 Kenta Nakamura
# License: BSD 3 clause

from setuptools import setup
import kslab

DESCRIPTION = "kslab : useful modueles for data analysis"
NAME = 'kslab'
AUTHOR = 'Shora Kurokawa'
AUTHOR_EMAIL = 'kurokawa.shora.42w@st.kyoto-u.ac.jp'
URL = 'https://github.com/Kshora/kslab'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/Kshora/kslab'
VERSION = kslab.__version__
PYTHON_REQUIRES = ">=3.7"

INSTALL_REQUIRES = [
    'numpy >=1.20.3',
    'xarray',
    'pandas>=1.2.4',
    'matplotlib>=3.3.4',
    'scipy>=1.6.3',
    'datetime',
    'plotly>=4.14.3',
    'lmfit>=1.0.2',
    'xarray',
]


PACKAGES = [
    'kslab'
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Multimedia :: Graphics',
    'Framework :: Matplotlib',
]


setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
    #   long_description=long_description,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      packages=PACKAGES,
      classifiers=CLASSIFIERS
    )
