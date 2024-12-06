from abc import abstractmethod
from typing import Dict


class BaseExplorer(object):

    coin_symbol = ""
    apikeys = {}

    def __init__(self, coin_symbol: str, apikeys: Dict[str, str]):
        self.coin_symbol = coin_symbol
        self.apikeys = apikeys

    @abstractmethod
    def get_coin_info(self, addr):
        """
        returns a dict with the following fields:
        * name: str
        * symbol: str
        * type: AssetType.COIN
        * balance: decimal
        * exchange_rate: double
        * currency: str (usually "USD")
        * address_explorer_url: str (url)
        """
        pass

    @abstractmethod
    def get_asset_list(self, addr):
        pass
