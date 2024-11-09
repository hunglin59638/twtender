# -*- coding: utf-8 -*-
import toml
from pathlib import Path
from setuptools import setup


def read_pyproject_toml():
    pyproject_toml = Path(__file__).parent / "pyproject.toml"
    pyproject = toml.loads(pyproject_toml.read_text())
    return pyproject


def readme():
    readme = Path(__file__).parent / "README.md"
    return readme.read_text()


pyproject = read_pyproject_toml()

author, author_email = [
    row.strip(" <>") for row in pyproject["tool"]["poetry"]["authors"][0].split("<")
]

packages = ["twtender"]

package_data = {"": ["*"]}

install_requires = [
    "bs4>=0.0.2,<0.0.3",
    "click>=8.1.7,<9.0.0",
    "fastapi-class>=3.6.0,<4.0.0",
    "fastapi>=0.115.4,<0.116.0",
    "pandas>=2.2.3,<3.0.0",
    "requests>=2.32.3,<3.0.0",
    "toml>=0.10.2,<0.11.0",
    "uvicorn>=0.32.0,<0.33.0",
]

setup_kwargs = {
    "name": pyproject["tool"]["poetry"]["name"],
    "version": pyproject["tool"]["poetry"]["version"],
    "description": "API to get tenders from Taiwan",
    "long_description": readme(),
    "author": author,
    "author_email": author_email,
    "maintainer": author,
    "maintainer_email": author_email,
    "url": pyproject["tool"]["poetry"]["repository"],
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.10,<4.0",
    "entry_points": {"console_scripts": ["twtender = twtender.main:main"]},
}


setup(**setup_kwargs)
