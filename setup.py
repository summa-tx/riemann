# flake8: noqa

from setuptools import setup

setup(
    name='riemann-tx',
    version='0.8.0',
    description=('Transaction creation library for Bitcoin-like coins'),
    url='https://github.com/integral-tx/riemann',
    author='James Prestwich',
    author_email='james''@prestwi.ch',
    license='LGPLv3.0',
    install_requires=[],
    packages=['riemann'],
    package_dir={'riemann': 'riemann'},
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security :: Cryptography',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
)
