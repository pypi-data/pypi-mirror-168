#! python3  # noqa: E265

from setuptools import find_packages, setup

# package (to get version)
from bubbleio import __about__
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="bubbleio",
    version=__about__.__version__,
    author=__about__.__author__,
    author_email=__about__.__email__,
    url="https://github.com/vlebert/bubbleio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["bubbleio"],
    # packaging
    packages=find_packages(
        exclude=["contrib", "docs", "*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    include_package_data=True,
    install_requires=[
        "requests",
    ],
)
