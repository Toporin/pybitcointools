from abc import ABC, abstractmethod
from typing import Dict, Optional

from pycryptotools.explorers.base_explorer import BaseExplorer


class PriceExplorer(BaseExplorer):
    def __init__(self, coin_symbol: str, is_testnet: bool, apikeys: Dict[str, str]):
        """
        Initialize the PriceExplorer.

        Args:
            coin_symbol (str): Symbol of the cryptocurrency
            is_testnet (bool): Flag to indicate if it's a testnet environment
            api_keys (Dict[str, str]): Dictionary of API keys
        """
        super().__init__(coin_symbol, apikeys)
        self.is_testnet = is_testnet

    @abstractmethod
    async def get_exchange_rate_between(self, coin: Optional[str] = None, other_coin: Optional[str] = None) -> float:
        """
        Get exchange rate between two cryptocurrencies.

        This method supports two signatures:
        1. get_exchange_rate_between(other_coin='BTC')
        2. get_exchange_rate_between(coin='XCP', other_coin='BTC')

        Args:
            other_coin (str): The cryptocurrency to get exchange rate against
            coin (str, optional): The base cryptocurrency (if not using the instance's coin_symbol)

        Returns:
            float: Exchange rate between the cryptocurrencies
        """
        pass

    @abstractmethod
    def get_price_weburl(self) -> str:
        """
        Get the web URL for price information.

        Returns:
            str: Web URL for price information
        """
        pass