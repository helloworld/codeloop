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
    name="codeloop",
    description="An AI tool to generate CLIs",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Sashank Thupukari",
    url="https://github.com/helloworld/codeloop",
    project_urls={
        "Issues": "https://github.com/helloworld/codeloop/issues",
        "CI": "https://github.com/helloworld/codeloop/actions",
        "Changelog": "https://github.com/helloworld/codeloop/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["codeloop"],
    entry_points="""
        [console_scripts]
        codeloop=codeloop.cli:cli
    """,
    install_requires=["click"],
    extras_require={
        "test": ["pytest"]
    },
    python_requires=">=3.7",
)
