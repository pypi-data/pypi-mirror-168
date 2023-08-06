from setuptools import setup, find_packages
import codecs
import os
VERSION = '0.1.3'
DESCRIPTION = 'Module to create Matrix and use Matrix Functions.'

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Setting up
setup(
    name="scitrix",
    version=VERSION,
    author="Prakhar Srivastava",
    author_email="<prakhartech983@gmail.com>",
    url='https://github.com/PrakEntech/scitrix',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['tabulate'],
    keywords=['python', 'matrix', 'determinant', 'adjoint', 'functions'],
    classifiers=[
        "Topic :: Scientific/Engineering :: Mathematics",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
