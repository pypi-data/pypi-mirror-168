#!/usr/bin/env python

""" 

Author: Nikhil Mohite
Email: nikhilmohitelhs@gmail.com
GitHub: https://www.github.com/nkilm
Country: India

References:
https://blog.ionelmc.ro/presentations/packaging/#slide:11
https://stackoverflow.com/questions/49156529/adding-json-file-to-manifest-in-and-installing-package-results-in-an-error


"""

from setuptools import setup, find_packages
import os
import codecs

VERSION = "0.0.9"
DESCRIPTION = "Bird-eye view of a local git repository"

here = os.path.abspath(os.path.dirname(__file__))

def readme():
    with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
        long_description = "\n" + fh.read()
        return long_description


# Setting up
setup(
    name="git-logs",
    version=VERSION,
    author="Nikhil Mohite",
    author_email="nikhilmohitelhs@gmail.com",
    download_url="https://github.com/nkilm/git-logs",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=readme(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "git-logs = gitlogs.main:main",
            "gitlogs = gitlogs.main:main"
        ],
    },
    keywords=["python", "git", "statistics", "local repository", "git statistics"],
    classifiers=[
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Version Control :: Git",
        "Programming Language :: Python :: 3",
    ],
)
