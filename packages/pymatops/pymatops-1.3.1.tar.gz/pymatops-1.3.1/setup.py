from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.3.1'
DESCRIPTION = 'A Python package for Matrix Operations'
with open("README.md", "r") as fh:
    long_description = fh.read()

# Setting up
setup(
    name="pymatops",
    version=VERSION,
    author="Yash Seth",
    author_email="<yashseth2002@gmail.com>",
    description=DESCRIPTION,
    long_description = long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    url="https://github.com/yash-seth/pymatops",
    keywords=['python', 'matrix', 'operations', 'maths', 'matrices', 'mathematics'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)