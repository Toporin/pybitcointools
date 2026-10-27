# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.4.0 - Unreleased]

The library now focuses on coins and block explorers: address derivation, WIF encoding,
balances, asset listings and exchange rates. Code that served other purposes has been removed.
**This is a breaking change**: applications that need the removed APIs should pin
`pycryptotools<0.4`.

### Removed
* modules `transaction`, `deterministic` (BIP32/Electrum keys), `mnemonic` (with the `english.txt`
  wordlist), `keystore`, `wallet_utils`, `wallet`, `blocks`, `composite`, `stealth`, `constants`
  and `py2specials`
* `Bitcoin` methods `addrtoscript`, `output_script_to_address`, `pubtop2w`, `privtop2w`,
  `mk_multsig_address`, `is_segwit` and `electrum_address`, and the `hashcode` attribute
* `main`: ECDSA signing/verification/recovery and message signing, `random_key`,
  `random_electrum_seed`, key arithmetic (`add_pubkeys`, `multiply`, `divide`, …), the CLI helpers
  (`access`, `multiaccess`, `slice`, `count`, `sum`), `change_curve`, `getG` and the `pubtoaddr`
  alias (use `pubtolegacy`); names from `ripemd` are no longer re-exported by the package
* `keccak`: everything except `Keccak256` (Keccak-224/384/512, SHA3, SHAKE)
* the `cryptotool` command-line script
* the `pbkdf2` dependency

### Fixed
Explorer correctness:
* BSC, RSK, xDai and POA silently reported a zero balance: Blockscout queried a placeholder url
  whose 404 was read as "address not found". Unsupported chains now raise an error
* Dash and Doge queried Bitcoin testnet through `BlockstreamExplorer`; they now raise an error
  (no supported explorer yet)
* Litecoin testnet: litecoinspace.org has no working testnet API, so `get_coin_info()` raises
  and the address link is `None`
* Polygon mainnet: polygon.blockscout.com blocks API clients with a Cloudflare challenge. The
  balance now falls back to a public JSON-RPC node (`JsonRpcExplorer`, link to polygonscan.com)
  with the exchange rate from Coingate. Tokens and NFTs are unavailable while Blockscout is
  blocked, and `get_asset_list()` then raises instead of returning an empty list

Bug fixes and code quality:
* `Bitcoin.is_address()`/`is_p2sh()` crashed (missing `address_prefixes`)
* Blockscout: tokens were overwritten by NFTs in `get_asset_list()`, and a missing exchange rate
  (e.g. on testnets) made `get_coin_info()` fail; it is now returned as None
* Coingate/Tokenscan: invalid price data is handled, NFT descriptions are stored
* explorer HTTP requests use a 20s timeout instead of potentially hanging forever
* Dogecoin testnet `coin_symbol` is now `DOGETEST` (was `Dogecoin`)
* `python_requires` raised to 3.7 (the package already required `dataclasses`)
* remove unused imports and dead code, avoid bare `except:`

Fix Bitcoin Cash balance and explorer link (https://github.com/Toporin/Satochip-Utils/issues/41):
the Fullstack.cash API no longer serves data, so `get_coin_info()` failed for BCH and BCH testnet.
The new `FulcrumExplorer` fetches balances from public Electrum protocol (Fulcrum) servers over TLS
with `blockchain.address.get_balance`. Mainnet addresses link to blockchair.com; testnet (chipnet)
has no supported explorer link.

Fix Polygon testnet having no explorer link (https://github.com/Toporin/Satochip-Utils/issues/42):
Blockscout does not host Polygon Amoy, so `get_coin_info()` always failed for POLTEST. The new
`JsonRpcExplorer` reads the balance from public Amoy JSON-RPC nodes (no API key needed) and links
to amoy.polygonscan.com. Token/NFT listing is not available on Polygon testnet.

Replace `print()` with the standard `logging` module:
* each module logs to `pycryptotools.<module>`; the package logger has a `NullHandler`, so
  nothing is output unless the application configures logging
* new `pycryptotools.set_log_level(level)` sets the level of all pycryptotools loggers at once
* security: the Etherscan/BscScan modules no longer print request URLs containing the API key.
  In 0.3.2, BIP39 checksum validation (`mnemonic.words_verify`) printed the mnemonic entropy to
  stdout; that module is removed in this release
* remove leftover debug traces; explorer failures are logged as warnings, request traces as debug

Note: output that used to be printed to stdout is now silent by default. Use
`logging.basicConfig(level=logging.DEBUG)` (or `set_log_level()` with a configured handler) to
see it.

## [0.3.2]: 

Improve Blockscout explorer:
*  Patch som parsing issues sur as links, symbol, contract data
* Improve parsing of NFTs, add more NFT info such as attributes


## [0.3.1]: 

* remove eth_hash (and cryptodome dependency) 
* use keccak.py instead

## [0.3.0]: 

* remove old unmaintained code
* Add support for asset listing with simplified API
* Add polygon support

## [0.2.1]: 

Add Counterparty (XCP) and UnsupportedCoin (???) support.
UnsupportedCoin is the default coin when support does not exist yet. 

### Added

Add basic Counterparty support:
    - Add Xchain.io explorer
    
## [0.2.0]: 

Use segwit by default for pubtoaddr.    
If segwit is not supported, use legacy address.
Legacy address is also supported through pubtolegacy.

### Added

Add basic NFT support:
    - Add Rarible explorer
    - Add Opensea explorer (WIP - still issues with API requests rejected by server)
    
Via Rarible, it is possible to fetch some NFT asset info based on contract & tokenid:
    - NFT name
    - description
    - image preview url
    - web link to rarible (& opensea)

## [0.1.2]: 

### Fixed

- Add pycryptodome in requirements (used by eth-hash)


## [0.1.1]: 

### Fixed

- Fix requirements in setup.py and MANIFEST.in

## [0.1.0]: 

Initial version of the package forked from https://github.com/Alcofribas4/pybitcointools.

### Changed 

- Changed module & package name to pycryptotools

### Added 

- Add API support for getting balance from explorers.
- Add support for API keys (required for etherscan/bscscan)
  
- Add coins:
-- Ethereum
-- BCS, ETC & other ethereum forks
    
- Add Explorers: etherscan, bcsscan, blockscout, fullstack.cash (BCH)

- Add address_weburl() function in explorers: this function returns a url link to the explorer that the user can browse to have detailed info for a given address

- Add test suite for functionalities used by Satodime
  Methods included in tests:
    - coin.display_name
    - coin.coin_symbol
    - coin.segwit_supported
    - coin.use_compressed_addr
    - coin.pubtoaddr
    - coin.pubtosegwit
    - coin.encode_privkey
    - (coin.address_weburl)
    
### Fixed

- Correct wif_prefix for Dogecoin & Litecoin

### Removed

- Blockdozer explorer appears to be discontinued