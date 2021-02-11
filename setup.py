#!/usr/bin/env python

from setuptools import setup

import persiantools


def readme():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name="persiantools",
    version=persiantools.__version__,
    description="Jalali date and datetime with other tools",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Persian",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Localization",
        "Topic :: Utilities",
    ],
    keywords="jalali shamsi persian digits characters converter jalalidate "
    "jalalidatetime date datetime jdate jdatetime farsi",
    url="https://github.com/majiidd/persiantools",
    author="Majid Hajiloo",
    author_email="majid.hajiloo@gmail.com",
    license="MIT",
    packages=["persiantools"],
    python_requires=">=3.6",
    tests_require=["pytest", "pytest-cov"],
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
)
