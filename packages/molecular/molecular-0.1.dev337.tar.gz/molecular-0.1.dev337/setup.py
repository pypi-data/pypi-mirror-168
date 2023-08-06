"""
setup.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

# import setuptools  # noqa
import numpy as np
import os.path
from setuptools import Extension, setup

from Cython.Build import cythonize

# Read version
with open('version.yml', 'r') as f:
    data = f.read().splitlines()
version_dict = dict([element.split(': ') for element in data])

# Convert the version_data to a string
version = '.'.join([str(version_dict[key]) for key in ['major', 'minor']])
if version_dict['micro'] != 0:
    version += '.' + version_dict['micro']
print(version)

# Read in requirements.txt
with open('requirements.txt', 'r') as buffer:
    requirements = buffer.read().splitlines()

# Long description
with open('README.rst', 'r') as buffer:
    long_description = buffer.read()


# First make sure numpy is installed
# _setup(install_requires=['numpy'])


# Cython code
ext_modules = [
    Extension('molecular.io._read_dcd', [os.path.join('molecular', 'io', '_read_dcd.pyx')], include_dirs=[
        np.get_include()]),
    Extension('molecular.analysis._analysis_utils', [os.path.join('molecular', 'analysis', '_analysis_utils.pyx')],
              include_dirs=[np.get_include()]),
]


# Then, install molecular
# FIXME make sure _include is included
setup(
    name='molecular',
    version=version,
    author='C. Lockhart',
    author_email='chris@lockhartlab.org',
    description='A toolkit for molecular dynamics simulations',
    long_description=long_description,
    url="https://www.lockhartlab.org",
    packages=[
        'molecular',
        'molecular.analysis',
        'molecular.analysis.protein',
        'molecular.bioinformatics',
        'molecular.core',
        'molecular.energy',
        'molecular.external',
        'molecular.fep',
        'molecular.geometry',
        'molecular.io',
        # 'molecular.io.fortran',
        'molecular.misc',
        'molecular.simulations',
        'molecular.statistics',
        'molecular.transform',
        'molecular.viz'
    ],
    install_requires=requirements,
    include_package_data=True,
    zip_safe=True,
    ext_modules=cythonize(ext_modules)
)
