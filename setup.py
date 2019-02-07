import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md")) as f:
    README = f.read()

with open(os.path.join(here, "VERSION")) as f:
    VERSION = f.read()

requires = [
    "ZODB",
    "jsonschema",
    "logdecorator",
]

setup(
    name="qozyd",
    version=VERSION,
    description="qozyd",
    long_description=README,
    author="",
    author_email="",
    url="",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points={
        "console_scripts": [
            "qozyd = qozyd.main:main",
        ]
    },
    test_suite="qozyd.tests",
)
