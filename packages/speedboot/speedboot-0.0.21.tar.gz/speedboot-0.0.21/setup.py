from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.21'
DESCRIPTION = 'Speed Bootstrap'
LONG_DESCRIPTION = 'This library lets you boostrap vector-valued statistics fast as it uses parallel processing. Ploting estimates distribution and computation of bias-corrected and accelerated confidence intervals are available. To see a quick demo click <a href="https://github.com/fcgrolleau/speedboot/blob/main/speedboot/demo.ipynb">here</a>. Source code is available <a href="https://github.com/fcgrolleau/speedboot/blob/main/speedboot/speedboot.py">there</a>.'

# Setting up
setup(
    name="speedboot",
    version=VERSION,
    author="François Grolleau",
    author_email="<francois.grolleau@aphp.fr>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['joblib', 'tqdm'],
    keywords=['bootstrap', 'confidence intervals', 'statistics', 'inference', 'parallel'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)