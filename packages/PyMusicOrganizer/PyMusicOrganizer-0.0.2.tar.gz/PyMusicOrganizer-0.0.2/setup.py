"""
    This is part of PyMusicOrganizer (C) 2022 Giacomo Battaglia
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name="PyMusicOrganizer",
    version="0.0.2",
    author="Giacomo Battaglia",
    author_email="battaglia.giacomo@yahoo.it",
    description="CLI tool to keep your music organized.",
    home_page="https://github.com/g-battaglia/pymusicorganizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/g-battaglia/pymusicorganizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Multimedia :: Sound/Audio",
        "Typing :: Typed",
    ],
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=["mutagen", "pathlib", "typer", "rich"],
)
