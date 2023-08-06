from io import open
from setuptools import setup, find_packages


def read(f):
    return open(f, "r").read()


setup(
    name="motordantic",
    version='0.0.1a7',
    packages=find_packages(exclude=("tests", "docs", "examples")),
    install_requires=[
        "pydantic>=1.9,<2",
        "pymongo==4.1",
        "motor==3.0.0",
    ],
    description="Mongo ODM, based on motor+pydantic",
    author="bogdanjz",
    author_email="bzdv.dn@gmail.com",
    url="https://github.com/bogdanjz/motordantic",
    license="MIT",
    python_requires=">=3.8",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
)
