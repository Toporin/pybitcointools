from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Optional

from pycryptotools.coins.base_coin import BaseCoin
from pycryptotools.explorers.base_explorer import BaseExplorer


class PriceExplorer(BaseExplorer):
    def __init__(self, coin: BaseCoin, apikeys: Dict[str, str]):
        """
        Initialize the PriceExplorer.

        Args:
            coin (str): BaseCoin for the currency
            apikeys (Dict[str, str]): Dictionary of API keys
        """
        super().__init__(coin, apikeys)

    @abstractmethod
    def get_exchange_rate_between(self, coin: Optional[str] = None, other_coin: Optional[str] = None) -> Decimal:
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
    def get_price_web_url(self) -> str:
        """
        Get the web URL for price information.

        Returns:
            str: Web URL for price information
        """
        pass