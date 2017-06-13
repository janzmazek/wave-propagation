from setuptools import setup, find_packages

setup(
    name = "WavePropagation",
    version = "0.1.0",
    packages = find_packages(exclude=['*test']),
    #scripts = ['scripts/greengraph'],
    install_requires = ['tkinter', 'argparse', 'numpy','scipy', 'matplotlib',
        'networkx, yaml', 'threading']
)
