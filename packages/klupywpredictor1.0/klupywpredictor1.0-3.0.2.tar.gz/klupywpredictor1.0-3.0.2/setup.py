from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '3.0.2'
DESCRIPTION = 'A package that predicts bloxflip games by Maska'

# Setting up
setup(
    name="klupywpredictor1.0",
    version=VERSION,
    author="maska",
    author_email="mask121575@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['cloudscraper'],
    keywords=['python', 'bloxflip', 'klupywpredictor', 'predictor'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)