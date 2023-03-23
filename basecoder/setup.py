from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="basecoder",
    description="basecoder",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="basecoder",
    url="https://github.com/basecoder/basecoder",
    project_urls={
        "Issues": "https://github.com/basecoder/basecoder/issues",
        "CI": "https://github.com/basecoder/basecoder/actions",
        "Changelog": "https://github.com/basecoder/basecoder/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["basecoder"],
    entry_points="""
        [console_scripts]
        basecoder=basecoder.cli:cli
    """,
    install_requires=["click"],
    extras_require={
        "test": ["pytest"]
    },
    python_requires=">=3.7",
)
