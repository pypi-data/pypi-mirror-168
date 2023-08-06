#!/usr/bin/env python3

import sys
from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    install_requires=requirements,
    entry_points={
        "console_scripts": ["flasket = flasket.middleware.gunicorn:main", "flasket-dev = flasket.middleware.flask:main"]
    },
)
