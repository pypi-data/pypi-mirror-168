"""Initial setup for the package."""
from setuptools import find_packages, setup

import surrealdb


with open("README.md", "r") as file:
    long_description = file.read()


setup(
    name=surrealdb.__title__,
    version=surrealdb.__version__,
    description=surrealdb.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sam Kenney",
    author_email="sam.kenney@me.com",
    url="https://github.com/mr-strawberry66/surrealdb-python",
    packages=["surrealdb"]
    + [f"surrealdb.{package}" for package in find_packages("surrealdb")],
    install_requires=["httpx>=0.23.0"],
)
