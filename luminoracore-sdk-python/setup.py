#!/usr/bin/env python3
"""
LuminoraCore SDK Python - Advanced Python client for personality management.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Advanced Python SDK for LuminoraCore personality management"

# Read version from __init__.py
def get_version():
    init_path = os.path.join(os.path.dirname(__file__), 'luminoracore', '__init__.py')
    if os.path.exists(init_path):
        with open(init_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('=')[1].strip().strip('"\'')
    return '1.0.0'

setup(
    name="luminoracore-sdk",
    version=get_version(),
    description="Advanced Python SDK for LuminoraCore personality management",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="LuminoraCore Team",
    author_email="sdk@luminoracore.com",
    url="https://github.com/luminoracore/sdk-python",
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'luminoracore>=1.0.0,<2.0.0',
        'pydantic>=2.0.0,<3.0.0',
        'httpx>=0.24.0,<1.0.0',
        'aiofiles>=23.0.0,<24.0.0',
        'typing-extensions>=4.5.0; python_version<"3.11"',
        'tenacity>=8.2.0,<9.0.0',
        'structlog>=23.1.0,<24.0.0',
        'opentelemetry-api>=1.18.0,<2.0.0',
        'opentelemetry-sdk>=1.18.0,<2.0.0',
    ],
    extras_require={
        'openai': ['openai>=1.0.0,<2.0.0'],
        'anthropic': ['anthropic>=0.7.0,<1.0.0'],
        'cohere': ['cohere>=4.21.0,<5.0.0'],
        'google': ['google-generativeai>=0.3.0,<1.0.0'],
        'redis': ['redis>=4.5.0,<5.0.0'],
        'postgres': ['asyncpg>=0.28.0,<1.0.0'],
        'mongodb': ['motor>=3.2.0,<4.0.0'],
        'all': [
            'openai>=1.0.0,<2.0.0',
            'anthropic>=0.7.0,<1.0.0',
            'cohere>=4.21.0,<5.0.0',
            'google-generativeai>=0.3.0,<1.0.0',
            'redis>=4.5.0,<5.0.0',
            'asyncpg>=0.28.0,<1.0.0',
            'motor>=3.2.0,<4.0.0',
        ],
        'dev': [
            'pytest>=7.3.0',
            'pytest-cov>=4.0.0',
            'pytest-asyncio>=0.21.0',
            'pytest-benchmark>=4.0.0',
            'pytest-mock>=3.10.0',
            'black>=23.0.0',
            'isort>=5.12.0',
            'flake8>=6.0.0',
            'mypy>=1.3.0',
            'pre-commit>=3.3.0',
            'sphinx>=6.0.0',
            'sphinx-rtd-theme>=1.2.0',
            'sphinx-autodoc-typehints>=1.23.0',
            'responses>=0.23.0',
            'aioresponses>=0.7.4',
            'factory-boy>=3.2.1',
            'freezegun>=1.2.2',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: AsyncIO',
        'Typing :: Typed',
    ],
    keywords='ai personality session llm openai claude async',
)
