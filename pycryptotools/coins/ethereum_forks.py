from ..explorers import bscscan
from ..explorers import blockscout
from .ethereum import Ethereum

class EthereumClassic(Ethereum):
    coin_symbol = "ETC"
    display_name = "Ethereum Classic"
    explorer = blockscout

    testnet_overrides = {
        'display_name': "ETC Mordor",
        'coin_symbol': "ETCTEST",
        'magicbyte': 111,
    }
    
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
    explorer = blockscout

    testnet_overrides = {
        'display_name': "(Unsupported)",
        'coin_symbol': "RBTCTEST",
        'magicbyte': 111,
    }
    
class xDai(Ethereum):
    coin_symbol = "XDAI"
    display_name = "xDai"
    explorer = blockscout

    testnet_overrides = {
        'display_name': "(Unsupported)",
        'coin_symbol': "XDAITEST",
        'magicbyte': 111,
    }
    
class POA(Ethereum):
    coin_symbol = "POA"
    display_name = "POA"
    explorer = blockscout

    testnet_overrides = {
        'display_name': "POA Sokol",
        'coin_symbol': "POATEST",
        'magicbyte': 111,
    }
    