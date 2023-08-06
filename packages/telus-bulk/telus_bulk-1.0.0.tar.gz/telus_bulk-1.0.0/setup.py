import os
import re
from setuptools import find_packages, setup

VERSION = "1.0.0"
DESCRIPTION = "A BASIC PACKAGES THAT CONTAINS TMF 645 MODELS"

setup(
    name="telus_bulk",
    version=VERSION,
    description=DESCRIPTION,
    url="https://github.com/jose-olmedo-telus/telus-bulk-python-types",
    author="José Alejandro Olmedo",
    packages=find_packages(),
    install_requires=["fastapi-camelcase==1.0.5"],
    include_package_data=True,
)
