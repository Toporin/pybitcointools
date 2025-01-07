from abc import abstractmethod
from typing import List

import pycryptotools
from ..main import *

class BaseCoin(object):
    """
    Base implementation of crypto coin class
    All child coins must follow same pattern.
    """

    coin_symbol = None
    display_name = None
    apikeys = {}
    is_testnet = False
    testnet_overrides = {}
    hd_path = 0
    # used for privkey WIF encoding
    use_compressed_addr = True
    wif_prefix = 0x80
    wif_script_types = {
        'p2pkh': 0,
        'p2wpkh': 1,
        'p2wpkh-p2sh': 2,
        'p2sh': 5,
        'p2wsh': 6,
        'p2wsh-p2sh': 7
    }
    # used in keystore.py
    xprv_headers = {
        'p2pkh': 0x0488ade4,
        'p2wpkh-p2sh': 0x049d7878,
        'p2wsh-p2sh': 0x295b005,
        'p2wpkh': 0x4b2430c,
        'p2wsh': 0x2aa7a99
    }
    xpub_headers = {
        'p2pkh': 0x0488b21e,
        'p2wpkh-p2sh': 0x049d7cb2,
        'p2wsh-p2sh': 0x295b43f,
        'p2wpkh': 0x4b24746,
        'p2wsh': 0x2aa7ed3
    }
    electrum_xprv_headers = xprv_headers
    electrum_xpub_headers = xpub_headers

    def __init__(self, testnet=False, **kwargs):
        if testnet:
            self.is_testnet = True
            for k, v in self.testnet_overrides.items():
                setattr(self, k, v)
        # override default attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
        # block explorers
        self.explorers: List[pycryptotools.explorers.block_explorer.BlockExplorer] = []
        self.price_explorers: List[pycryptotools.explorers.price_explorer.PriceExplorer] = []

    ######################################
    #            BLOCK EXPLORER          #
    ######################################

    def get_address_web_url(self, addr:str):
        for explorer in self.explorers:
            try:
                return explorer.get_address_web_url(addr)
            except Exception as ex:
                print(f"Failed to get address web url from {explorer}: {str(ex)}")

        # if not explorers returned to info, raise
        raise ValueError(f"Failed to recover url from explorers!")

    def get_coin_info(self, addr):
        for explorer in self.explorers:
            try:
                coin_info = explorer.get_coin_info(addr)
                return coin_info
            except Exception as ex:
                print(f"Failed to get coin_info from {explorer}: {str(ex)}")

        # if not explorers returned to info, raise
        raise ValueError(f"Failed to recover coin info from explorers!")

    def get_asset_list(self, addr):
        for explorer in self.explorers:
            try:
                asset_list = explorer.get_asset_list(addr)
                return asset_list
            except Exception as ex:
                print(f"Failed to get asset list from {explorer}: {str(ex)}")

        # if not explorers returned to info, raise
        raise ValueError(f"Failed to recover asset list from explorers!")

    ######################################
    #            PRICE EXPLORER          #
    ######################################

    def get_exchange_rate_with(self, other_coin: str):
        for explorer in self.price_explorers:
            try:
                rate = explorer.get_exchange_rate_between(other_coin)
                return rate
            except Exception as ex:
                print(f"Failed to get exchange rate from {explorer}: {str(ex)}")

        # if not explorers returned to info, raise
        raise ValueError(f"Failed to get exchange rate from explorers!")

    ######################################
    #           KEY  &  ADDRESS          #
    ######################################
    def privtopub(self, privkey: bytes):
        """
        Get public key from private key
        """
        return privtopub(privkey)  # see main.py

    @abstractmethod
    def pubtoaddr(self, pubkey: bytes):
        """
        Get address from a public key
        """
        pass

    def privtoaddr(self, privkey: bytes):
        """
        Get address from a private key
        """
        pub = self.privtopub(privkey)
        addr = self.pubtoaddr(pub)
        return addr

    def encode_privkey(self, privkey: bytes, formt=None, script_type="p2pkh"):

        if formt == None:
            formt = 'wif_compressed' if self.use_compressed_addr else 'wif'

        return encode_privkey(privkey, formt=formt, vbyte=self.wif_prefix + self.wif_script_types[script_type])
