from .bitcoin import Bitcoin
from ..explorers.coingate_price_explorer import Coingate
from ..explorers.litecoinspace_explorer import LitecoinspaceExplorer


class Litecoin(Bitcoin):
    coin_symbol = "LTC"
    display_name = "Litecoin"
    segwit_supported = True
    magicbyte = 48
    script_magicbyte = 50 #Supposed to be new magicbyte
    #script_magicbyte = 5 #Old magicbyte still recognised by explorers
    wif_prefix = 0xb0
    segwit_hrp = "ltc"
    hd_path = 2
    testnet_overrides = {
        'display_name': "Litecoin Testnet",
        'coin_symbol': "LTCTEST",
        'magicbyte': 111,
        'script_magicbyte': 58,   #Supposed to be new magicbyte
        #'script_magicbyte': 196, #Old magicbyte still recognised by explorers,
        'wif_prefix': 0xef,
        'segwit_hrp': "tltc",
        'hd_path': 1,
        'xpriv_prefix': 0x04358394,
        'xpub_prefix': 0x043587cf
    }

    def __init__(self, testnet=False, **kwargs):
        super().__init__(testnet, **kwargs)
        self.explorers = [LitecoinspaceExplorer(self, self.apikeys)]
        self.price_explorers = [Coingate(self, self.apikeys)]
