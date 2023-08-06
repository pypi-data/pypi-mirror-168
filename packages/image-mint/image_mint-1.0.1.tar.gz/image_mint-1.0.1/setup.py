"""
image_mint
-----------
image_mint is a python package for downloading images from search engines
`````
* Source
  https://github.com/kouroshparsa/image_mint
"""
from setuptools import setup, find_packages
version = '1.0.1'
long_description = ''
with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="image_mint",
    version=version,
    author="Kourosh Parsa",
    author_email="kouroshtheking@gmail.com",
    description='image_mint is a python package for searching for and downloading images',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kouroshparsa/image_mint",
    keywords=['google', 'bing', 'yahoo', 'images', 'scraping', 'search'],
    packages=find_packages(),
    install_requires=[
        'selenium',
        'requests',
        'argparse',
        'Pillow'
    ],
    classifiers=(
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': ['image_mint=image_mint.console:main'],
    }
)