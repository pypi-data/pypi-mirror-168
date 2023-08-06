# pyformatters_textranksummarizer

[![license](https://img.shields.io/github/license/oterrier/pyformatters_textranksummarizer)](https://github.com/oterrier/pyformatters_textranksummarizer/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyformatters_textranksummarizer/workflows/tests/badge.svg)](https://github.com/oterrier/pyformatters_textranksummarizer/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyformatters_textranksummarizer)](https://codecov.io/gh/oterrier/pyformatters_textranksummarizer)
[![docs](https://img.shields.io/readthedocs/pyformatters_textranksummarizer)](https://pyformatters_textranksummarizer.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyformatters_textranksummarizer)](https://pypi.org/project/pyformatters_textranksummarizer/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyformatters_textranksummarizer)](https://pypi.org/project/pyformatters_textranksummarizer/)

Formatter/processor based on TextRank

## Installation

You can simply `pip install pyformatters_textranksummarizer`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyformatters_textranksummarizer
```

### Running the test suite

You can run the full test suite against all supported versions of Python (3.8) with:

```
tox
```

### Building the documentation

You can build the HTML documentation with:

```
tox -e docs
```

The built documentation is available at `docs/_build/index.html.
