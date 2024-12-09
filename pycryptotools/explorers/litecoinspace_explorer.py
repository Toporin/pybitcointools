import json
from decimal import Decimal
from typing import Dict, List, Optional, Tuple, Union, Any
import requests

from pycryptotools.coins.base_coin import BaseCoin
from pycryptotools.coins.asset_type import AssetType
from pycryptotools.explorers.block_explorer import BlockExplorer
from pycryptotools.explorers.explorer_exceptions import DataFetcherError

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
        if self.coin_symbol == "BTC":
            return "https://litecoinspace.org/address/" + addr
        return "https://litecoinspace.org/testnet/address/" + addr

    def get_token_web_url(self, contract: str) -> str:
        """Get web link for a token"""
        return f"(not supported)"

    def get_nft_web_url(self, contract: str, tokenid: str) -> str:
        """Get web link for a token"""
        return f"(not supported)"

    """API"""

    def get_coin_info(self, addr):
        """Get native coin info for an address"""
        print(f"In LitecoinspaceExplorer get_coin_info for: {addr}")

        url = f"{self.get_api_url()}address/{addr}"
        print(f"urlString: {url}")

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to recover data from url {url}, response status {response.status_code}")
            raise DataFetcherError(DataFetcherError.INVALID_URL)

        data = response.json()
        coin_info = {}

        # compute balance
        funded_txo_sum= Decimal(data['chain_stats']['funded_txo_sum'])
        print(f"DEBUG Litecoinspace funded_txo_sum {funded_txo_sum}")
        spent_txo_sum= Decimal(data['chain_stats']['spent_txo_sum'])
        print(f"DEBUG Litecoinspace spent_txo_sum {spent_txo_sum}")
        balance= (funded_txo_sum - spent_txo_sum)/(10**8)
        print(f"DEBUG Litecoinspace balance {balance}")
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
        print(f"coin_info: {coin_info}")
        return coin_info

    def get_asset_list(self, addr):
        """Get asset info for an address"""
        print(f"In LitecoinspaceExplorer get_asset_list for: {addr}")
        return []
