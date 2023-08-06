# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="honeydew",
    version="0.1.8",
    description="Collection of connectors for ETL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://honeydew-lib.github.io/",
    project_urls = {
        'Repository': 'https://github.com/honeydew-lib/honeydew',
        'Documentation': 'https://honeydew-lib.github.io/'
    },
    author="Poltak Jefferson",
    author_email="poltak.jefferson@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["honeydew"],
    include_package_data=True,
    install_requires=["pandas","numpy","mysql-connector-python","google-cloud","google-auth","google-cloud-bigquery","google-cloud-bigquery-storage","google-cloud-storage", "pandas_gbq", "paramiko", "scp", 'pytz']
)