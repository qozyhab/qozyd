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
    "aiohttp",
]

setup(
    name="qozyd",
    version=VERSION,
    description="qozyd",
    long_description=README,
    author="qozy.io",
    author_email="contact@qozy.io",
    url="https://www.qozy.io",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={
        "full": ["qozy-ui", "qozy-client", "qozy-ssh", "qozy-wifiled"]
    },
    entry_points={
        "console_scripts": [
            "qozyd = qozyd.main:main",
        ]
    },
)
