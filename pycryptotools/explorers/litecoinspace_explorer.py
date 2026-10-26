import logging
from decimal import Decimal
from typing import Dict
import requests

from pycryptotools.coins.base_coin import BaseCoin
from pycryptotools.coins.asset_type import AssetType
from pycryptotools.explorers.block_explorer import BlockExplorer
from pycryptotools.explorers.explorer_exceptions import DataFetcherError

_logger = logging.getLogger(__name__)

class LitecoinspaceExplorer(BlockExplorer):

    def __init__(self, coin: BaseCoin, apikeys: Dict[str, str]):
        super().__init__(coin, apikeys)

    """Utilities"""

    def get_api_url(self) -> str:
        """Get base API URL based on coin symbol"""
        if self.coin_symbol == "LTC":
            return "https://litecoinspace.org/api/"
        return "https://litecoinspace.org/testnet/api/"

    def get_address_web_url(self, addr: str) -> str:
        """Get web link for an address"""
        if self.coin_symbol == "LTC":
            return "https://litecoinspace.org/address/" + addr
        return "https://litecoinspace.org/testnet/address/" + addr

    def get_token_web_url(self, contract: str) -> str:
        """Get web link for a token"""
        return "(not supported)"

    def get_nft_web_url(self, contract: str, tokenid: str) -> str:
        """Get web link for a token"""
        return "(not supported)"

    """API"""

    def get_coin_info(self, addr):
        """Get native coin info for an address"""
        _logger.debug("LitecoinspaceExplorer get_coin_info for: %s", addr)

        url = f"{self.get_api_url()}address/{addr}"
        _logger.debug("GET %s", url)

        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            _logger.warning("Failed to recover data from url %s, response status %s", url, response.status_code)
            raise DataFetcherError(DataFetcherError.INVALID_URL)

        data = response.json()
        coin_info = {}

        # compute balance
        funded_txo_sum= Decimal(data['chain_stats']['funded_txo_sum'])
        spent_txo_sum= Decimal(data['chain_stats']['spent_txo_sum'])
        balance= (funded_txo_sum - spent_txo_sum)/(10**8)
        coin_info['balance'] = balance

        # get exchange rate from third party
        try:
            rate = self.coin.get_exchange_rate_with("USD")
            coin_info['exchange_rate'] = rate
            coin_info['currency'] = "USD"
        except Exception as ex:
            coin_info['error'] = str(ex)

        # basic info
        coin_info['symbol'] = self.coin_symbol
        coin_info['name'] = self.coin.display_name
        coin_info['type'] = AssetType.COIN
        coin_info['address_explorer_url'] = self.get_address_web_url(addr)
        _logger.debug("coin_info: %s", coin_info)
        return coin_info

    def get_asset_list(self, addr):
        """Get asset info for an address"""
        _logger.debug("LitecoinspaceExplorer get_asset_list for: %s", addr)
        return []
