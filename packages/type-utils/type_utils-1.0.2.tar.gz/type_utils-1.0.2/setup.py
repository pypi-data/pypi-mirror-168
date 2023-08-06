#!/usr/bin/env python

from setuptools import setup
import pathlib


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="type_utils",
    version="1.0.2",
    description="Type Utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tibotix",
    author_email="tizian@seehaus.net",
    url="https://github.com/tibotix/type_utils",
    package_dir={"type_utils": "src"},
    packages=["type_utils"],
    extras_require={"test": ["pytest"]},
    python_requires=">=3.7, <4",
)
