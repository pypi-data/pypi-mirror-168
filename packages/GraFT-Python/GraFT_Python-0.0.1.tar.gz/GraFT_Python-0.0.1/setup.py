# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 17:36:41 2022

@author: noga mudrik
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    packages=setuptools.find_packages(),
    author="Noga Mudrik",

    name="GraFT_Python",
    version="0.0.01",
    
    author_email="<nmudrik1@jhmi.edu>",
    description="Python implementation for the GraFT model presented in https://pubmed.ncbi.nlm.nih.gov/35533160/",
    long_description=long_description,
    long_description_content_type="text/markdown",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    python_requires=">=3.8",
    install_requires = ['numpy', 'matplotlib','scipy','scipy','pandas','webcolors','qpsolvers',
                        'seaborn','colormap','sklearn', 'pylops','dill','mat73', 'easydev']
)

