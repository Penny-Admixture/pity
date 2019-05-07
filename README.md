# Pity: Peercoin made easy

[![PyPI](https://img.shields.io/pypi/v/pity.svg?style=flat-square)](https://pypi.python.org/pypi/pity/)
[![](https://img.shields.io/badge/python-3.5+-blue.svg)](https://www.python.org/download/releases/3.5.0/)
[![Build Status](https://travis-ci.org/peercoin/pity.svg?branch=master)](https://travis-ci.org/peercoin/pity)

Forked from Ofek's awesome [Bit library](https://github.com/ofek/bit).

Pity is based on Bit, the [Python's fastest](https://ofek.github.io/bit/guide/intro.html#why-bit)
Bitcoin library and was designed from the beginning to feel intuitive, be
effortless to use, and have readable source code.

**Pity is so easy to use, in fact, you can do this:**

```
    >>> from bit import Key
    >>>
    >>> my_key = Key(wif="...")
    >>> my_key.get_balance('eur')
    '12.51'
    >>> # Let's pity the fool! Umm,... Let's donate!
    >>> outputs = [
    >>>     # the Peercoin Foundation
    >>>     ('p92W3t7YkKfQEPDb7cG9jQ6iMh7cpKLvwK', 10, 'usd'),
    >>>     # Beer for willy, PeerExplorer <https://peercoinexplorer.net/charts/>
    >>>     ('PA3VZmupxdsX5TuS1PyXZPsbbhZGT2htPz', 3, 'eur')
    >>> ]
    >>>
    >>> my_key.send(outputs)
    '1da615c003bb1bd98354378fa5e95287993dab152d876fa0cc3980566ce6d7ee'
```

## Features

- Python's fastest available implementation (100x faster than closest library)
- Seamless integration with existing server setups
- Supports keys in cold storage
- Fully supports 25 different currencies
- First class support for storing data in the blockchain
- Deterministic signatures via RFC 6979
- Access to the blockchain (and testnet chain) through multiple APIs for redundancy
- Exchange rate API, with optional caching
- Optimal transaction fee API, with optional caching
- Compressed public keys by default
- Multiple representations of private keys; WIF, PEM, DER, etc.
- Legacy P2PKH and Segwit nested-P2WPKH transactions
- Legacy P2SH and Segwit nested-P2WSH transactions

If you are intrigued, continue reading. If not, continue all the same!

## Installation

Bit is distributed on `PyPI` as a universal wheel and is available on Linux/macOS
and Windows and supports Python 3.5+ and PyPy3.5-v5.7.1+.

``pip`` >= 8.1.2 is required.

> $ pip install pity

Documentation
-------------

Docs are [hosted by Github Pages](https://ofek.github.io/bit/) and are automatically built and published
by Travis after every successful commit to Bit's ``master`` branch.

## Credits

- [ofek](https://github.com/ofek/bit) for the original bit codebase.
- [backpacker](https://github.com/backpacker69/) for help with the porting.
- [Additional](AUTHORS.rst)
