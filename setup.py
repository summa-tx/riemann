# flake8: noqa

from setuptools import setup

setup(
    name='riemann-tx',
    version='0.6.0',
    description=('Transaction creation library for Bitcoin-like coins'),
    url='https://github.com/integral-tx/riemann-tx',
    author='James Prestwich',
    author_email='james''@prestwi.ch',
    license='LGPLv3.0',
    install_requires=[],
    packages=['riemann'],
    package_dir={'riemann': 'riemann'},
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
)
