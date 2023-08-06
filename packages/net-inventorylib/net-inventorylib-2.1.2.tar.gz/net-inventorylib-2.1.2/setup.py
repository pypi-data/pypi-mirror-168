#!/usr/bin/env python3


import setuptools

import net_inventorylib


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="net-inventorylib",
    version=net_inventorylib.__version__,
    author="Robert Franklin",
    author_email="rcf34@cam.ac.uk",
    description="Network configuration library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.developers.cam.ac.uk/uis/netsys/udn/net-inventorylib",
    packages=setuptools.find_packages(),
    install_requires=[
        "deepops",
        "jinja2",
        "netaddr",
        "pyyaml",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
