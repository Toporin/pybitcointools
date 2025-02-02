from .base_coin import BaseCoin
from .bitcoin import Bitcoin
from ..explorers.coingate_price_explorer import Coingate
from ..explorers.fullstack_explorer import FullstackExplorer
from ..transaction import SIGHASH_ALL, SIGHASH_FORKID

from cashaddress import convert # cashAddr conversion for bcash

class BitcoinCash(Bitcoin):
    coin_symbol = "BCH"
    display_name = "Bitcoin Cash"
    segwit_supported = False
    magicbyte = 0
    script_magicbyte = 5
    wif_prefix = 0x80
    hd_path = 145
    hashcode = SIGHASH_ALL | SIGHASH_FORKID
    testnet_overrides = {
        'display_name': "Bitcoin Cash Testnet",
        'coin_symbol': "BCHTEST",
        'magicbyte': 111,
        'script_magicbyte': 196,
        'wif_prefix': 0xef,
        'xprv_headers': {
            'p2pkh': 0x04358394,
        },
        'xpub_headers': {
            'p2pkh': 0x043587cf,
        },
        'hd_path': 1,
    }

    def __init__(self, testnet=False, legacy=False, **kwargs):
        super(BitcoinCash, self).__init__(testnet=testnet, **kwargs)
        self.hd_path = 0 if legacy and testnet else self.hd_path
        self.explorers = [FullstackExplorer(self, self.apikeys)]
        self.price_explorers = [Coingate(self, self.apikeys)]
        
    def pubtoaddr(self, pubkey):
        """
        Get address from a public key
        """
        #addr_legacy= super(BitcoinCash, self).pubtoaddr(pubkey, magicbyte=self.magicbyte)
        addr_legacy= super().pubtolegacy(pubkey)
        print("ADDR_LEGACY: "+addr_legacy)
        addr= convert.to_cash_address(addr_legacy) #cashAddr conversion
        
        return addr
        
        
        