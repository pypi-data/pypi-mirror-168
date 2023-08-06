from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Using NuOCR service via APIs'
LONG_DESCRIPTION = 'A package that allows to utilize NuOCR sevices through API implementation.'

# Setting up
setup(
    name="NuOCR",
    version=VERSION,
    author="Nuvento (Jigar Makwana)",
    author_email="<makwana.jigar@nuvento.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['grpcio'],
    keywords=['python', 'NuOCR', 'OCR'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)