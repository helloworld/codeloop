# basecoder

[![PyPI](https://img.shields.io/pypi/v/basecoder.svg)](https://pypi.org/project/basecoder/)
[![Changelog](https://img.shields.io/github/v/release/basecoder/basecoder?include_prereleases&label=changelog)](https://github.com/basecoder/basecoder/releases)
[![Tests](https://github.com/basecoder/basecoder/workflows/Test/badge.svg)](https://github.com/basecoder/basecoder/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/basecoder/basecoder/blob/master/LICENSE)

basecoder

## Installation

Install this tool using `pip`:

    pip install basecoder

## Usage

For help, run:

    basecoder --help

You can also use:

    python -m basecoder --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd basecoder
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
