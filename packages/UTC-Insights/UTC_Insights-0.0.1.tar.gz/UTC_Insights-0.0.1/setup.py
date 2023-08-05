#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Insights based on truck data'
LONG_DESCRIPTION = 'A package that gives Insights of UltraTech truck data as pdf file. Types: 1) All India based Report 2) Plant-wise Report 3) Zone-wise Report'

# Setting up
setup(
    name="UTC_Insights",
    version=VERSION,
    author="Somaay Maheshwari, Vidhi Khatwani, Nikhil Tattikota",
    author_email="<somaay.maheshwari70@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'fpdf'],
    keywords=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

