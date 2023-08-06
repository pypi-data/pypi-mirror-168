import os
import re
from codecs import open
from os import path

from setuptools import find_packages, setup

COMPANY_NAME = "chalk"
NAME = "chalk"
DESCRIPTION = f"Python SDK for Chalk"

REQUIRED = [
    "Click==8.*",
    "JSON-log-formatter",
    "aiosqlite",
    "dataclasses-json",
    "gitignore-parser>=0.0.8",
    "log-with-context",
    "mypy==0.931",
    "numpy",
    "pandas",
    "pandas-stubs",
    "pendulum",
    "psycopg2",
    "pydantic>=1.0.0",
    "pyyaml",
    "requests",
    "sqlalchemy>=1.4.26",
    "varname==0.9.0",
    "executing",
    "pure_eval",
    "cattrs==22.1.0",  # required to serialize dataclasses
]

repo_root = path.abspath(path.dirname(__file__))
LONG_DESCRIPTION = open(os.path.join(repo_root, "README.md"), "r").read()
VERSIONFILE = os.path.join(repo_root, "_version.py")
mo = re.search(
    r"^__version__ = ['\"]([^'\"]*)['\"]",
    open(VERSIONFILE, "rt").read(),
    re.M,
)

assert mo is not None, f"Unable to find version string in {str(VERSIONFILE)}"

version = mo.group(1)

setup(
    version=version,
    name="chalkpy",
    author="Chalk AI, Inc.",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    python_requires=">=3.8.0",
    url="https://chalk.ai",
    packages=find_packages(exclude=("tests",)),
    install_requires=REQUIRED,
    include_package_data=True,
    package_data={"chalk": ["py.typed"]},
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={"console_scripts": [f"chalkpy=chalk.cli:cli"]},
    setup_requires=[
        "setuptools_scm",
    ],
)
