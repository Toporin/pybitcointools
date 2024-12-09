from abc import abstractmethod
from typing import Dict

from pycryptotools.coins.base_coin import BaseCoin


class BaseExplorer(object):

    coin_symbol = ""
    apikeys = {}

    def __init__(self, coin: BaseCoin, apikeys: Dict[str, str]):
        self.coin = coin
        self.coin_symbol = coin.coin_symbol
        self.apikeys = apikeys