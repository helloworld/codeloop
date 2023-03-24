# codeloop

[![PyPI](https://img.shields.io/pypi/v/codeloop.svg)](https://pypi.org/project/codeloop/)
[![Changelog](https://img.shields.io/github/v/release/helloworld/codeloop?include_prereleases&label=changelog)](https://github.com/helloworld/codeloop/releases)
[![Tests](https://github.com/helloworld/codeloop/workflows/Test/badge.svg)](https://github.com/helloworld/codeloop/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/helloworld/codeloop/blob/master/LICENSE)

An AI tool to generate CLIs

## Installation

Install this tool using `pip`:

    pip install codeloop

## Usage

Run `codeloop generate`
And fill in your requirements
Or just run `codeloop generate --demo` to use a pre written requirements doc

While it runs, you should see new files get created inside your specified project folder like in `basecoder/`. The code files will get continually updated as needed to pass the tests.

For help, run:

    codeloop --help

You can also use:

    python -m codeloop --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd codeloop
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
