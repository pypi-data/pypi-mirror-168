# Python Competitive Programming Tools

This is an example project demonstrating how to publish a python module to PyPI.

## Installation

Run the following to install:

```bash
$ pip install pycpt
```

## Usage

```python
from cpin import si,mi

# Get single int input value
t = si()

for _ in range(t):
    # Get multiple int input values
    a, b, c = mi()
    print("yay!")
```

## Development

To install pycpt, along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
$ pip install -e .[dev]
```