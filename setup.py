#!/usr/bin/env python
import os
from setuptools import setup, find_packages
from distutils.core import setup, Extension
from Cython.Build import cythonize


base = os.path.dirname(os.path.abspath(__file__))

README_PATH = os.path.join(base, "README.rst")

install_requires = ["lru-dict"]

tests_require = []

ext_modules = [
    Extension(
        name="fnmatch_vendor",
        sources=[
            os.path.join('carbon_index', 'fnmatch_vendor.pyx'),
        ],
        language="c++",
    ),
    Extension(
        name="expand_utils",
        sources=[
            os.path.join('carbon_index', 'expand_utils.pyx'),
        ],
        language="c++",
    )
]

setup(name='carbon-index',
      version='0.1.11',
      description='',
      long_description=open(README_PATH).read(),
      author='Yun Xu',
      author_email='yunxu1992@gmail.com',
      url='',
      packages=find_packages(),
      install_requires=install_requires,
      ext_modules=cythonize(ext_modules),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Operating System :: MacOS',
          'Operating System :: POSIX :: Linux',
          'Topic :: System :: Software Distribution',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
      ]
)
