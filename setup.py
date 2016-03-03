from setuptools import setup
import rpI2C

rpI2C_classifiers = []

with open("README.md", "r") as f:
    rpI2C_long_description = f.read()

setup(name="rpI2C",
      version=rpI2C.__version__,
      author="Fernando Chorney",
      author_email="fchorney@djsbx.com",
      url="http://pypi.python.org/pypi/rpI2C/",
      py_modules=["rpI2C"],
      description="Raspberry Pi I2C library",
      long_description=rpI2C_long_description,
      license="MIT",
      classifiers=rpI2C_classifiers
      )