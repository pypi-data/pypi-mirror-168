# 30/04/2021

import pathlib
from setuptools import setup, find_packages

setup(
    name="inoryp",
    version="2.0.23",
    author="R0htg0r",
    author_email="osvaldo.pedreiro.ecaminhoneiro@gmail.com",
    url="https://github.com/R0htg0r",
    description="Essa biblioteca foi desenvolvida com o intuito de fornecer o acesso rápido ao seu Endereço IP(LAN).",
    long_description=open("README.md", 'r').read(),
    long_description_content_type="text/markdown",

    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True,
    install_requires=['requests', 'pysocks', 'pypi-json', 'Raney'],
    keywords=['Python', 'Python3', 'IP', 'API', 'Informations', 'InformaIP' 'Security', 'Requests'],
    packages=find_packages(),
)

