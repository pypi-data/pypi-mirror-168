import setuptools
from pathlib import Path

setuptools.setup(
    name="abrsh_mac",
    version=1.0,
    long_description=Path("README.md").read_text(),
    author="Abrham Mesfin",
    author_email="abrshtgam@gmail.com",
    packages=setuptools.find_packages()
)
