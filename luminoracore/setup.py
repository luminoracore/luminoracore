#!/usr/bin/env python3
"""
LuminoraCore - Universal AI Personality Management Standard
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Universal standard for AI personality management"

# Read version from __init__.py
def get_version():
    init_path = os.path.join(os.path.dirname(__file__), 'luminoracore', '__init__.py')
    if os.path.exists(init_path):
        with open(init_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('=')[1].strip().strip('"\'')
    return '0.1.0'

setup(
    name="luminoracore",
    version=get_version(),
    description="Universal standard for AI personality management",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="LuminoraCore Team",
    author_email="team@luminoracore.dev",
    url="https://github.com/luminoracore/luminoracore",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'luminoracore': ['schema/*.json', 'personalities/*.json'],
    },
    entry_points={
        'console_scripts': [
            'luminora=luminoracore.tools.cli:main',
        ],
    },
    install_requires=[
        'jsonschema>=4.17.2',
        'pydantic>=2.0.0',
        'click>=8.1.0',
        'colorama>=0.4.6',
        'pyyaml>=6.0',
        'requests>=2.31.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.5.0',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='ai personality llm prompt management standard',
)
