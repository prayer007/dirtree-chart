from setuptools import setup, find_packages
import pymaid

with open('README.md') as f:
    long_description = f.read()

setup(
    name='pyMaid',
    version=pymaid.__version__,
    author='Manuel Strohmaier',
    author_email='manuel.strohmaier@joanneum.at',
    description="Directory structure diagram generator",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/prayer007/pymaid",
    project_urls={
        'Documentation': 'https://github.com/prayer007/pymaid',
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
