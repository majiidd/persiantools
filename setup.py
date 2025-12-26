import re

from setuptools import setup


def readme():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


def read_version():
    with open("persiantools/__init__.py", encoding="utf-8") as f:
        m = re.search(r"^__version__\s*=\s*['\"]([^'\"]+)['\"]", f.read(), re.M)
        if not m:
            raise RuntimeError("Cannot find __version__ in persiantools/__init__.py")
        return m.group(1)


setup(
    name="persiantools",
    version=read_version(),
    description="Jalali date and datetime with other tools",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: Persian",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
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
    project_urls={
        "Source": "https://github.com/majiidd/persiantools",
        "Issues": "https://github.com/majiidd/persiantools/issues",
    },
    author="Majid Hajiloo",
    author_email="majid.hajiloo@gmail.com",
    license="MIT",
    license_files=("LICENSE",),
    packages=["persiantools"],
    python_requires=">=3.10",
    install_requires=["tzdata; platform_system == 'Windows'"],
    include_package_data=True,
    zip_safe=False,
)
