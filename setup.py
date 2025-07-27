#!/usr/bin/env python3
"""
Setup script for Python Code Executor
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='python-code-executor',
    version='1.0.0',
    description='A mobile application built with Kivy that allows users to write and execute Python code',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='Python Code Executor Team',
    author_email='',
    url='',
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
    ],
    entry_points={
        'console_scripts': [
            'python-code-executor=main:main',
        ],
    },
    keywords='kivy android mobile python code executor',
    project_urls={
        'Bug Reports': '',
        'Source': '',
        'Documentation': '',
    },
) 