import setuptools
from setuptools import setup, find_packages

setuptools.setup(
    name="dir2docker",
    version="0.0.3",
    description="Convert any working python environment to a docker image/file ",
    install_requires=["single_source"],
    long_description=open("README.md").read().strip(),
    author="Sachin Chandra",
    author_email="sachin@netbook.ai",
    py_modules=["directory2docker"],
    license="MIT License",
    zip_safe=False,
    keywords="Package python environment as docker",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
