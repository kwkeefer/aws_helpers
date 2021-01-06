from setuptools import setup, find_packages
import os

with open(os.path.join("aws_helpers", 'version')) as version_file:
    version = version_file.read().replace(" ", "")

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.readlines()

setup(
    name='aws_helpers',
    packages=find_packages(),
    version=version,
    author="Kyle Keefer",
    install_requires=requirements
)
