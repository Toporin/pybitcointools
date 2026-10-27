import logging
from decimal import Decimal
from typing import Dict
import requests

from pycryptotools.coins.base_coin import BaseCoin
from pycryptotools.coins.asset_type import AssetType
from pycryptotools.explorers.block_explorer import BlockExplorer
from pycryptotools.explorers.explorer_exceptions import DataFetcherError

_logger = logging.getLogger(__name__)


class SochainExplorer(BlockExplorer):
    """
    SoChain explorer (https://sochain.com/docs/balance) for Litecoin and Dogecoin, mainnet and testnet.
    Only native coin balances are supported (no tokens or NFTs).
    The API key is read from apikeys['API_KEY_SOCHAIN'] and sent in the API-KEY header only,
    never in the url, so it cannot leak through logs or request exceptions.
    """

    API_URL = "https://sochain.com/api/v3/"
    WEB_URL = "https://sochain.com/"
    # coin_symbol -> SoChain network identifier
    NETWORKS = {
        "LTC": "LTC",
        "LTCTEST": "LTCTEST",
        "DOGE": "DOGE",
        "DOGETEST": "DOGETEST",
    }
    APIKEY_NAME = "API_KEY_SOCHAIN"

    def __init__(self, coin: BaseCoin, apikeys: Dict[str, str]):
        super().__init__(coin, apikeys)

    """Utilities"""

    def get_network(self) -> str:
        """Get the SoChain network identifier for the coin"""
        if self.coin_symbol not in self.NETWORKS:
            raise DataFetcherError(f"SoChain does not support {self.coin_symbol}")
        return self.NETWORKS[self.coin_symbol]

    def get_apikey(self):
        """Get the API key, if any (configparser sections lowercase their keys)"""
        apikeys = self.apikeys or {}
        return apikeys.get(self.APIKEY_NAME) or apikeys.get(self.APIKEY_NAME.lower())

    def get_address_web_url(self, addr: str) -> str:
        """Get web link for an address"""
        return f"{self.WEB_URL}{self.get_network().lower()}/address/{addr}"

    def get_token_web_url(self, contract: str) -> str:
        """Get web link for a token"""
        return "(not supported)"

    def get_nft_web_url(self, contract: str, tokenid: str) -> str:
        """Get web link for a token"""
        return "(not supported)"

    """API"""

    def get_coin_info(self, addr):
        """Get native coin info for an address"""
        _logger.debug("SochainExplorer get_coin_info for: %s", addr)

        url = f"{self.API_URL}balance/{self.get_network()}/{addr}"
        _logger.debug("GET %s", url)
        apikey = self.get_apikey()
        headers = {"API-KEY": apikey} if apikey else {}
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code != 200:
            # 401: invalid API key, 404: invalid address, 429: too many requests
            _logger.warning("Failed to recover data from url %s, response status %s", url, response.status_code)
            raise DataFetcherError(DataFetcherError.INVALID_URL)

        data = response.json()
        if data.get('status') != "success":
            raise DataFetcherError(DataFetcherError.MISSING_DATA)

        coin_info = {}
        coin_info['balance'] = Decimal(data['data']['confirmed'])  # exact decimal string, in coins

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
        _logger.debug("SochainExplorer get_asset_list for: %s", addr)
        return []
