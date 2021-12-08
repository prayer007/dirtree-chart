from setuptools import setup, find_packages
import dirtree_chart

with open('README.md') as f:
    long_description = f.read()

setup(
    name='dirtree-chart',
    version=dirtree_chart.__version__,
    author='Manuel Strohmaier',
    author_email='manuel.strohmaier@joanneum.at',
    description="Directory structure diagram generator",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/prayer007/dirtree-chart",
    project_urls={
        'Documentation': 'https://github.com/prayer007/dirtree-chart',
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
