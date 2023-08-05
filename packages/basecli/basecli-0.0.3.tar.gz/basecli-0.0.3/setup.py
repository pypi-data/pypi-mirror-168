from setuptools import setup, find_packages
from io import open
from os import path

import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# automatically captured required modules for install_requires in requirements.txt
with open(path.join(HERE, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [
    x.strip()
    for x in all_reqs
    if ("git+" not in x) and (not x.startswith("#")) and (not x.startswith("-"))
]
dependency_links = [x.strip().replace("git+", "") for x in all_reqs if "git+" not in x]
setup(
    name="basecli",
    description="A simple commandline app trying to make a cli version of deta base",
    version="0.0.3",
    packages=find_packages(),  # list of all packages
    install_requires=install_requires,
    python_requires=">=3.6",  # any python greater than 2.7
    entry_points="""
        [console_scripts]
        basecli=basecli.__main__:main
    """,
    author="Ayush Sehrawat",
    keyword="deta, python, deta base, cli, deta ui, basecli, deta base cli",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/AyushSehrawat/basecli",
    download_url="https://github.com/AyushSehrawat/basecli/archive/0.0.3.tar.gz",
    dependency_links=dependency_links,
    author_email="mini@minidev.me",
    classifiers=["Programming Language :: Python :: 3.8"],
)
