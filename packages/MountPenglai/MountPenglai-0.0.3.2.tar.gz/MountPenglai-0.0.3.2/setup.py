from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='MountPenglai',  # package name
    version='0.0.3.2',  # package version
    author='RMSHE',
    author_email='asdfghjkl851@outlook.com',
    url='https://github.com/RMSHE-MSH/Python-Homework-Open-Source-Project',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
)
