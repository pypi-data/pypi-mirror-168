from setuptools import setup, find_packages
import codecs
import os

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

VERSION = "1.3"
DESCRIPTION = "PyOMA allows the experimental estimation of the modal parameters (natural frequencies, mode shapes, damping ratios) of a structure from measurements of the vibration response in operational condition."

# Setting up
setup(
    name="Py-OMA",
    version=VERSION,
    author="Dag Pasquale Pasca, Angelo Aloisio, Marco Martino Rosso, Stefanos Sotiropoulos",
    author_email="<supportPyOMA@polito.it>",
    license="GNU General Public License v3 (GPLv3)",
    description=DESCRIPTION,
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/dagghe/PyOMA",
    packages=find_packages(),
    install_requires=['numpy','scipy','pandas','matplotlib','seaborn','mplcursors'],
    keywords=['operational modal analysis', 'ambient vibration modal test', 'structural dynamics', 'frequency domain decomposition', 'stochastic subspace identification', 'structural health monitoring'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
