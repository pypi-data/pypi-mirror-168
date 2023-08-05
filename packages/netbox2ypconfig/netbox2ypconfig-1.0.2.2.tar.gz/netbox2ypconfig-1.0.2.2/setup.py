"""A setuptools based setup module."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="netbox2ypconfig",
    version="1.0.2.2",
    description="Program to construct ypconfig YAML configuration file from NetBox.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    author="William Edwards",
    author_email="opensource@cyberfusion.nl",
    url="https://vcs.cyberfusion.nl/open-source/netbox2ypconfig",
    platforms=["linux"],
    packages=find_packages(
        include=[
            "netbox2ypconfig",
            "netbox2ypconfig.*",
        ]
    ),
    data_files=[],
    entry_points={"console_scripts": ["netbox2ypconfig=netbox2ypconfig:main"]},
    install_requires=[
        "PyYAML==5.4.1",
        "pynetbox==6.1.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["cyberfusion", "ypconfig"],
    license="MIT",
)
