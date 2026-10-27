# Pycryptotools, Python library for crypto coin addresses and block explorers

[![Latest Version](https://img.shields.io/pypi/v/pycryptotools.svg?style=flat)](https://pypi.org/project/pycryptotools/)

This is a fork of Vitalik Buterin's original [pybitcointools](https://github.com/vbuterin/pybitcointools) library.

It has been heavily modified and simplified to provide basic service such as:
* recovering address from a public key for various blockchain
* recovering wif from private key
* get the balance for a given address on a blockchain, using block explorer web services API
* get assets (token & NFT) linked to a given address on a blockchain

Since v0.4.0, the library focuses on these coin and explorer features: the transaction, wallet, BIP32
and mnemonic code inherited from pybitcointools has been removed. Use `pycryptotools<0.4` if you need it.

Installation:

```bash
pip install pycryptotools
```

Library supports the following blockchains:

* Bitcoin mainnet & testnet
* Bitcoin Cash mainnet & testnet
* Litecoin mainnet & testnet
* Dogecoin mainnet & testnet
* Counterparty mainnet & testnet
* Ethereum mainnet & testnet
* Ethereum Classic mainnet & testnet
* Polygon mainnet & testnet

Requires Python 3.8 or later.

## API keys

Coins take an optional `apikeys` dict, passed to their block explorers. Litecoin and Dogecoin
balances come from [SoChain](https://sochain.com/), whose API expects a key:

```python
from pycryptotools.coins import Litecoin

coin = Litecoin(apikeys={'API_KEY_SOCHAIN': '...'})
coin.get_coin_info(address)
```

SoChain may reject or rate-limit requests sent without a key; `get_coin_info()` then raises
`ValueError`. The other supported coins need no API key.

## Logging

The library logs through the standard `logging` module, under the `pycryptotools` logger, and is
silent by default. To see its output, configure logging in your application, or set the level of
all pycryptotools loggers at once:

```python
import logging
import pycryptotools

logging.basicConfig()
pycryptotools.set_log_level(logging.DEBUG)
```


## Note

This software is provided 'as-is', without any express or implied warranty. 
In no event will the authors be held liable for any damages arising from the use of this software.