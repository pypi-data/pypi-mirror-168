import setuptools
from setuptools import setup, find_packages

setuptools.setup(
    name="dir2docker",
    version="0.0.1",
    description="Python Package Boilerplate",
    long_description=open("README.md").read().strip(),
    author="Sachin Chandra",
    author_email="sachin@netbook.ai",
    py_modules=["directory2docker"],
    install_requires=[],
    license="MIT License",
    zip_safe=False,
    keywords="Package python enviroment as docker",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
