from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='1inch.py',
    version='1.6.5',
    url='https://github.com/RichardAtCT/1inch_wrapper',
    long_description_content_type="text/markdown",
    long_description=long_description,
    keywords="1inch, wrapper, aggregator, DEX",
    packages=find_packages(include=['oneinch_py', 'oneinch_py.*']),
    install_requires=[
            'requests>=2.28.1',
            'web3>=5.30.0',
            'setuptools>=57.0.0'],
    # data_files=[('abis', ['oneinch_py/oracle.json', 'oneinch_py/multicall.json', 'oneinch_py/erc20.json'])],
    python_requires=">=3.7, <4",
    include_package_data=True,
    license='MIT',
    author='RichardAt',
    author_email='richardatk01@gmail.com',
    description='a Python wrapper for the 1inch API'
)
