from setuptools import setup
import rpI2C

rpI2C_classifiers = []

setup(
    name="rpI2C",
    version=rpI2C.__version__,
    author="Fernando Chorney",
    author_email="fchorney@djsbx.com",
    url="https://github.com/DJSymBiotiX/rpI2C",
    py_modules=["rpI2C"],
    description=(
        "Raspberry Pi I2C library. "
        "See https://github/com/DJSymBiotiX/rpI2C for more."
    ),
    license="MIT",
    keywords=['raspberry', 'pi', 'i2c'],
    classifiers=rpI2C_classifiers
)
