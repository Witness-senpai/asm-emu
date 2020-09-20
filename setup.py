import os
from setuptools import setup, find_packages

setup_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name="pyasm",
    version="1.0",
    author="Darkovsky Ilya",
    description="A Assembler compiler",
    packages=find_packages(),
)
