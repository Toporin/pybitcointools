# Pycryptotools, Python library for Crypto coins signatures and transactions

[![Latest Version](https://img.shields.io/pypi/v/pycryptotools.svg?style=flat)](https://pypi.org/project/pycryptotools/)

This is a fork of Vitalik Buterin's original [pybitcointools](https://github.com/vbuterin/pybitcointools) library.

It has been heavily modified and simplified to provide basic service such as:
* recovering address from a public key for various blockchain
* recovering wif from private key
* get the balance for a given address on a blockchain, using block explorer web services API
* get assets (token & NFT) linked to a given address on a blockchain

Installation:

```bash
pip install pycryptotools
```

Library supports the following blockchains:

* Bitcoin mainnet & testnet 
* Bitcoin Cash mainnet & testnet
* Litecoin mainnet & testnet
* Counterparty mainnet & testnet
* Ethereum mainnet & testnet
* Polygon mainnet & testnet


## Note

This software is provided 'as-is', without any express or implied warranty. 
In no event will the authors be held liable for any damages arising from the use of this software.