#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


# Add your dependencies in requirements.txt
# Note: you can add test-specific requirements in tox.ini
requirements = []
with open('requirements.txt') as f:
    for line in f:
        stripped = line.split("#")[0].strip()
        if len(stripped) > 0:
            requirements.append(stripped)


# https://github.com/pypa/setuptools_scm
use_scm = {"write_to": "misic_ui/_version.py"}

setup(
    name='misic-napari',
    author='S. Panigrahi & L. Espinosa, IAM, LCB',
    version="0.2.2",
    author_email='spanigrahi@imm.cnrs.fr',
    license='MIT',
    url='https://github.com/pswap/misic',
    description='Segmentation of bacteria agnostic to imaging modality',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={'': ['MiSiCv2.h5']},
    python_requires='>=3.6',
    install_requires=requirements,
    #use_scm_version=use_scm,
    #use_scm_version={'root'       : '..','relative_to': os.path.dirname(__file__)},
    setup_requires=['setuptools_scm'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Framework :: napari',        
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'napari.plugin': [
            'misic-napari = misic_ui'
        ],
    },
)
