import binascii
import re

from .. import compress, pubtolegacy, electrum_pubkey, output_script_to_address, bin_to_b58check, \
    hex_to_b58check, hash160, segwit_addr, mk_p2w_scripthash_script, mk_scripthash_script, mk_pubkey_script, \
    mk_p2wpkh_script, privtopub, pubkey_to_hash, bin_sha256, safe_from_hex, mk_multisig_script, SIGHASH_ALL, \
    magicbyte_to_prefix
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
    hashcode = SIGHASH_ALL
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

    def electrum_address(self, masterkey, n, for_change=0):
        """
        For old electrum seeds
        """
        pubkey = electrum_pubkey(masterkey, n, for_change=for_change)
        return self.pubtoaddr(pubkey)

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

    def output_script_to_address(self, script):
        """
        Convert an output script to an address
        """
        return output_script_to_address(script, self.magicbyte)

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

    def addrtoscript(self, addr):
        """
        Convert an output address to a script
        """
        if self.segwit_hrp:
            witver, witprog = segwit_addr.decode(self.segwit_hrp, addr)
            if witprog is not None:
                return mk_p2w_scripthash_script(witver, witprog)
        if self.is_p2sh(addr):
            return mk_scripthash_script(addr)
        else:
            return mk_pubkey_script(addr)

    def pubtop2w(self, pub):
        """
        Convert a public key to a pay to witness public key hash address (P2WPKH, required for segwit)
        """
        if not self.segwit_supported:
            raise Exception("Segwit not supported for this coin")
        compressed_pub = compress(pub)
        return self.scripttoaddr(mk_p2wpkh_script(compressed_pub))

    def privtop2w(self, priv):
        """
        Convert a private key to a pay to witness public key hash address
        """
        return self.pubtop2w(privtopub(priv))

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

    def mk_multsig_address(self, *args):
        """
        :param args: List of public keys to used to create multisig and M, the number of signatures required to spend
        :return: multisig script
        """
        script = mk_multisig_script(*args)
        address = self.p2sh_scriptaddr(script)
        return script, address

    def is_segwit(self, priv, addr):
        """
        Check if addr was generated from priv using segwit script
        """
        if not self.segwit_supported:
            return False
        if self.segwit_hrp and addr.startswith(self.segwit_hrp):
            return True
        segwit_addr = self.privtop2w(priv)
        return segwit_addr == addr
