from importlib.metadata import entry_points
from pathlib import Path
from setuptools import setup, find_packages
from version import __version__, __rootdir__


setup(
    author="Fábio Lucas Pereira Carneiro",
    author_email="fabiolucas.carneiro@gmail.com",
    license="GNU General Public License v3.0",
    url="https://github.com/fabiocfabini/pymink",
    name=__rootdir__,
    version=__version__,
    description='A Python library to perform N Gram based text analysis.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'nltk',
        'pandas',
        'matplotlib',
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            f'{__rootdir__}.gn = {__rootdir__}.cli:guess_number',
            f'{__rootdir__}.sn = {__rootdir__}.cli:square_number',
        ],
    },
)
