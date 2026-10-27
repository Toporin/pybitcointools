from pycryptotools.explorers import bscscan
from pycryptotools.explorers.blockscout_explorer import BlockscoutExplorer
from pycryptotools.explorers.coingate_price_explorer import Coingate
from pycryptotools.explorers.jsonrpc_explorer import JsonRpcExplorer
from pycryptotools.coins.ethereum import Ethereum


class EthereumClassic(Ethereum):
    coin_symbol = "ETC"
    display_name = "Ethereum Classic"

    testnet_overrides = {
        'display_name': "ETC Mordor",
        'coin_symbol': "ETCTEST",
        'magicbyte': 111,
    }


class Polygon(Ethereum):
    coin_symbol = "POL"
    display_name = "Polygon"

    testnet_overrides = {
        'display_name': "Polygon testnet",
        'coin_symbol': "POLTEST",
        'magicbyte': 111,
    }

    def __init__(self, testnet=False, **kwargs):
        super().__init__(testnet, **kwargs)
        if self.is_testnet:
            # Blockscout does not host Polygon Amoy
            self.explorers = [JsonRpcExplorer(self, self.apikeys)]
        else:
            # polygon.blockscout.com may block API clients (Cloudflare challenge):
            # fall back to a public JSON-RPC node for the balance
            self.explorers = [BlockscoutExplorer(self, self.apikeys), JsonRpcExplorer(self, self.apikeys)]
            self.price_explorers = [Coingate(self, self.apikeys)]


class BinanceSmartChain(Ethereum):
    coin_symbol = "BSC"
    display_name = "Binance Smart Chain"
    explorer = bscscan

    testnet_overrides = {
        'display_name': "BSC Testnet",
        'coin_symbol': "BSCTEST",
        'magicbyte': 111,
    }
    
class RSK(Ethereum):
    coin_symbol = "RBTC"
    display_name = "RSK"

    testnet_overrides = {
        'display_name': "(Unsupported)",
        'coin_symbol': "RBTCTEST",
        'magicbyte': 111,
    }
    
class xDai(Ethereum):
    coin_symbol = "XDAI"
    display_name = "xDai"

    testnet_overrides = {
        'display_name': "(Unsupported)",
        'coin_symbol': "XDAITEST",
        'magicbyte': 111,
    }
    
class POA(Ethereum):
    coin_symbol = "POA"
    display_name = "POA"

    testnet_overrides = {
        'display_name': "POA Sokol",
        'coin_symbol': "POATEST",
        'magicbyte': 111,
    }
    