#!/usr/bin/env python
import setuptools

setuptools.setup(name='ReadOIFITS',
      version='0.1.0',
      description='Python package to read OIFITS files',
      author='Jacques Kluska',
      author_email='jacques.kluska@kuleuven.be',
      url='https://github.com/kluskaj/ReadOIFITS',
      packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ),
    install_requires=['astropy', 'matplotlib', 'numpy', 'scikit-learn', 'scipy']
)
