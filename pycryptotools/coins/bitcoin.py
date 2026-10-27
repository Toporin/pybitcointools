import binascii
import re

from .. import compress, pubtolegacy, bin_to_b58check, hex_to_b58check, hash160, segwit_addr, privtopub, \
    pubkey_to_hash, bin_sha256, safe_from_hex, magicbyte_to_prefix
from .base_coin import BaseCoin
from ..explorers.blockstream_explorer import BlockstreamExplorer
from ..explorers.coingate_price_explorer import Coingate


class Bitcoin(BaseCoin):
    coin_symbol = "BTC"
    display_name = "Bitcoin"
    segwit_supported = True
    magicbyte = 0
    script_magicbyte = 5
    segwit_hrp = "bc"
    use_compressed_addr = True
    client_kwargs = {
        'server_file': 'bitcoin.json',
    }

    testnet_overrides = {
        'display_name': "Bitcoin Testnet",
        'coin_symbol': "BTCTEST",
        'magicbyte': 111,
        'script_magicbyte': 196,
        'segwit_hrp': 'tb',
        'hd_path': 1,
        'wif_prefix': 0xef,
        'client_kwargs': {
            'server_file': 'bitcoin_testnet.json',
        },
        'xprv_headers': {
            'p2pkh': 0x04358394,
            'p2wpkh-p2sh': 0x044a4e28,
            'p2wsh-p2sh': 0x295b005,
            'p2wpkh': 0x04358394,
            'p2wsh': 0x2aa7a99
        },
        'xpub_headers': {
            'p2pkh': 0x043587cf,
            'p2wpkh-p2sh': 0x044a5262,
            'p2wsh-p2sh': 0x295b43f,
            'p2wpkh': 0x043587cf,
            'p2wsh': 0x2aa7ed3
        },
    }

    def __init__(self, testnet=False, **kwargs):
        super().__init__(testnet, **kwargs)
        self.address_prefixes = magicbyte_to_prefix(magicbyte=self.magicbyte)
        if self.script_magicbyte:
            self.script_prefixes = magicbyte_to_prefix(magicbyte=self.script_magicbyte)
        else:
            self.script_prefixes = ()
        self.explorers = [BlockstreamExplorer(self, self.apikeys)]
        self.price_explorers = [Coingate(self, self.apikeys)]

    ######################################
    #           KEY  &  ADDRESS          #
    ######################################

    # TODO: refactor & clean!

    def pubtoaddr(self, pubkey):
        """
        Get address from a public key
        """
        if self.segwit_supported:
            return self.pubtosegwit(pubkey)
        else:
            return self.pubtolegacy(pubkey)

    def privtoaddr(self, privkey):
        """
        Get address from a private key
        """
        pub = self.privtopub(privkey)
        addr = self.pubtoaddr(pub)
        return addr

    def pubtolegacy(self, pubkey, use_compressed_addr=None):
        """
        Get address from a public key
        """
        if use_compressed_addr == None:
            use_compressed_addr = self.use_compressed_addr
        if use_compressed_addr and len(pubkey) == 65:
            pubkey = compress(pubkey)  # see main.py
        return pubtolegacy(pubkey, magicbyte=self.magicbyte)

    def is_address(self, addr):
        """
        Check if addr is a valid address for this chain
        """
        all_prefixes = ''.join(list(self.address_prefixes) + list(self.script_prefixes))
        return any(str(i) == addr[0] for i in all_prefixes)

    def is_p2sh(self, addr):
        """
        Check if addr is a a pay to script address
        """
        return not any(str(i) == addr[0] for i in self.address_prefixes)

    def scripttoaddr(self, script):
        """
        Convert an input public key hash to an address
        """
        if re.match('^[0-9a-fA-F]*$', script):
            script = binascii.unhexlify(script)
        if script[:3] == b'\x76\xa9\x14' and script[-2:] == b'\x88\xac' and len(script) == 25:
            return bin_to_b58check(script[3:-2], self.magicbyte)  # pubkey hash addresses
        else:
            # BIP0016 scripthash addresses
            return bin_to_b58check(script[2:-1], self.script_magicbyte)

    def p2sh_scriptaddr(self, script):
        """
        Convert an output p2sh script to an address
        """
        if re.match('^[0-9a-fA-F]*$', script):
            script = binascii.unhexlify(script)
        return hex_to_b58check(hash160(script), self.script_magicbyte)

    def hash_to_segwit_addr(self, hash):
        """
        Convert a hash to the new segwit address format outlined in BIP-0173
        """
        return segwit_addr.encode(self.segwit_hrp, 0, hash)

    def privtosegwit(self, privkey):
        """
        Convert a private key to the new segwit address format outlined in BIP01743
        """
        return self.pubtosegwit(self.privtopub(privkey))

    def pubtosegwit(self, pubkey, use_compressed_addr=None):
        """
        Convert a public key to the new segwit address format outlined in BIP01743
        """
        if use_compressed_addr == None:
            use_compressed_addr = self.use_compressed_addr
        if use_compressed_addr and len(pubkey) == 65:
            pubkey = compress(pubkey)
        return self.hash_to_segwit_addr(pubkey_to_hash(pubkey))

    def script_to_p2wsh(self, script):
        """
        Convert a script to the new segwit address format outlined in BIP01743
        """
        return self.hash_to_segwit_addr(bin_sha256(safe_from_hex(script)))  # debugSatochip
        # return self.hash_to_segwit_addr(sha256(safe_from_hex(script))) #orig
