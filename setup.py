from setuptools import setup, find_packages

setup(
    name='riemann_tx',
    version='0.9.0',
    description=('Transaction creation library for Bitcoin-like coins'),
    url='https://github.com/summa-tx/riemann',
    author='James Prestwich',
    author_email='james@summa.one',
    license='LGPLv3.0',
    install_requires=[],
    packages=find_packages(),
    install_package_data=True
)
