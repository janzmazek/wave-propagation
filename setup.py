from setuptools import setup, find_packages

setup(
    name = "WavePropagation",
    version = "1.0.0",
    packages = find_packages(exclude=['*test']),
    install_requires = ['numpy','scipy']
)
