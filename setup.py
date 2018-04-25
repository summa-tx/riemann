from setuptools import setup

setup(
    name='riemann-tx',
    version='0.6.0',
    description=('Transaction creation library for Bitcoin-like coins'),
    author='James Prestwich',
    license='AGPLv3.0',
    install_requires=[],
    packages=['riemann'],
    package_dir={'riemann': 'riemann'},
)
