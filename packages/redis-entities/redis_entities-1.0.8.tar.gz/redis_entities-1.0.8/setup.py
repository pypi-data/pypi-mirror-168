#!/usr/bin/env python

from setuptools import setup
import pathlib


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")
install_requires = (here / "requirements.txt").read_text(encoding="utf-8").splitlines()

setup(
    name="redis_entities",
    version="1.0.8",
    description="Redis Entities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tibotix",
    author_email="tizian@seehaus.net",
    url="https://github.com/tibotix/redis_entities",
    package_dir={"redis_entities": "src"},
    packages=["redis_entities", "redis_entities.mixins"],
    install_requires=install_requires,
    extras_require={"test": ["pytest", "fakeredis"]},
    python_requires=">=3.8, <4",
)
