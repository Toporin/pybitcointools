# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`pycryptotools` (published on PyPI) is a heavily simplified fork of Vitalik Buterin's `pybitcointools`, maintained by Satochip. Its main consumer is SatodimeTool: it derives addresses/WIF from keys for several blockchains and queries block-explorer web APIs for balances, token/NFT asset lists and exchange rates. The repo directory is named `pybitcointools`, but the package is `pycryptotools/`.

## Commands

```bash
pip install -r requirements.txt        # deps: requests, pbkdf2, base58, cashaddress
python3 -m unittest test               # core crypto tests (ECC, bases, electrum, tx serialize/sign)
python3 -m unittest test_satodime      # per-coin address/WIF tests + live explorer tests
python3 -m unittest test_stealth
python3 -m unittest test_logging        # logging conventions + no-secret-leak checks
python3 -m unittest test_satodime.BitcoinCase.test_address   # single test
python3 setup.py sdist bdist_wheel     # build (output in dist/)
```

The `test_explorer` tests in `test_satodime.py` make real HTTP calls to third-party explorers, so they need network access and can fail because of the remote service rather than the code. No lint configuration exists.

Releases bump `version` in `setup.py` and add a `CHANGELOG.md` entry (Keep a Changelog format).

## Architecture

**Low-level crypto (flat modules re-exported by `pycryptotools/__init__.py`):** `main.py` (secp256k1 math, key encoding, hashing), `transaction.py`, `deterministic.py` (BIP32), `mnemonic.py`, `keystore.py`, `stealth.py`, `segwit_addr.py`, plus pure-Python `keccak.py` and `ripemd.py`. Keccak lives in-tree on purpose: the `eth_hash`/cryptodome dependency was removed in 0.3.1. `py2specials.py`/`py3specials.py` hold the base-conversion helpers. Most code uses `from pycryptotools import *`.

**Coins (`pycryptotools/coins/`):** each coin subclasses `BaseCoin` (`base_coin.py`) and is configured mostly through class attributes (`coin_symbol`, `magicbyte`, `script_magicbyte`, `segwit_hrp`, `wif_prefix`, xprv/xpub headers, …). Testnet works through `testnet_overrides`: `BaseCoin.__init__(testnet=True)` copies that dict onto the instance with `setattr`, and extra kwargs override attributes the same way. `Bitcoin` is the base for the UTXO coins (Litecoin, BCH, Dash, Doge, Counterparty). `Ethereum` is the base for EVM chains in `ethereum_forks.py` (Polygon, ETC, BSC, …). `UnsupportedCoin` is the fallback when a chain isn't supported yet. `pubtoaddr` defaults to segwit when `segwit_supported`, otherwise legacy.

**Explorers (`pycryptotools/explorers/`):** each coin's `__init__` populates `self.explorers` (list of `BlockExplorer` subclasses) and `self.price_explorers` (list of `PriceExplorer`). `BaseCoin.get_coin_info` / `get_asset_list` / `get_address_web_url` / `get_exchange_rate_with` try each explorer in order, print failures and move on, and raise `ValueError` only if all fail. To add a data source, subclass `BlockExplorer`, implement `get_coin_info(addr)` (returns a dict: name, symbol, type=`AssetType.COIN`, balance, exchange_rate, currency, address_explorer_url) and `get_asset_list(addr)`, then register it in the coin's `__init__`. Explorers are constructed with `(coin, apikeys)`; API keys come from the coin's `apikeys` dict (e.g. `API_KEY_ETHERSCAN`).

Current wiring: BTC → Blockstream, LTC → litecoinspace, BCH → Fullstack, XCP → Tokenscan (xchain), ETH/EVM forks → Blockscout (POL testnet → `JsonRpcExplorer`, since Blockscout does not host Amoy), prices → Coingate. Older module-level explorers (`etherscan.py`, `bscscan.py`, `sochain.py`, `opensea.py`, `rarible.py`) follow a previous function-based API and are mostly legacy.

## Logging

Library code never calls `print()`. Each module defines `_logger = logging.getLogger(__name__)` after its imports. The leading underscore matters: the package relies heavily on `from x import *`, and a public `logger` name would leak into callers' namespaces. Module loggers must stay at NOTSET, so never call `setLevel()`, add handlers or call `basicConfig()` in the library. `pycryptotools/__init__.py` installs a `NullHandler` and exposes `set_log_level()`. Never log key material, mnemonics or entropy, or URLs that embed API keys (etherscan, bscscan and ethplorer put the key in the query string). `test_logging.py` enforces the no-`print()` rule.

Levels: DEBUG for request traces and parsed results, WARNING for a failed or partially parsed explorer response that the code recovers from (fallback, skipped asset), INFO for device paired/unpaired events.

## Gotchas

- `cryptotool` (installed as a script by `setup.py`) still imports the old `cryptos` package and is stale.
- `build/`, `dist/` and `pycryptotools.egg-info/` are build artifacts. Don't edit them.
