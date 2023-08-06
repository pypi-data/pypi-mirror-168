#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
    "randomname",
    "kubernetes",
    "escapism",
    "humanfriendly",
    "python-decouple",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Konstantin Taletskiy",
    author_email="konstantin.taletskiy@labshare.org",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="CLI translating common Docker commands to run containers in K8s",
    entry_points={
        "console_scripts": [
            "docker=dock8r.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="docker",
    name="dock8r",
    packages=find_packages(include=["dock8r", "dock8r.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/PolusAI/notebooks-hub",
    version="0.1.2",
    zip_safe=False,
)
