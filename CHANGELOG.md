# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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