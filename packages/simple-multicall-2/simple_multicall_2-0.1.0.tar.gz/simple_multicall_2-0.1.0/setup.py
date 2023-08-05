from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.1.0' 
DESCRIPTION = 'Simple Web3 multicall 2'

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='simple_multicall_2',
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='',
    author_email= '',
    packages=find_packages(),
    license='MIT',
    keywords=['multicall', 'web3', 'multicall2'],
    requires=['Web3'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3"
    ]
)
