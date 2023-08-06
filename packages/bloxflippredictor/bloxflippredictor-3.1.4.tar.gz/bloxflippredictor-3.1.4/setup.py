from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '3.1.4'
DESCRIPTION = 'A package that predicts bloxflip games'

# Setting up
setup(
    name="bloxflippredictor",
    version=VERSION,
    author="xolo",
    author_email="robokidefe@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['cloudscraper'],
    keywords=['python', 'bloxflip', 'bloxflippredictor', 'predictor'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)