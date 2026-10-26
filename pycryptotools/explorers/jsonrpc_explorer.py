import logging
from decimal import Decimal
from typing import Dict
import requests

from pycryptotools.coins.base_coin import BaseCoin
from pycryptotools.coins.asset_type import AssetType
from pycryptotools.explorers.block_explorer import BlockExplorer
from pycryptotools.explorers.explorer_exceptions import DataFetcherError

_logger = logging.getLogger(__name__)


class JsonRpcExplorer(BlockExplorer):
    """
    Explorer for EVM chains without a supported indexer API (e.g. not hosted by Blockscout).
    Native balance is read with eth_getBalance from public JSON-RPC nodes (no API key needed),
    and web links point to the chain's block explorer. Token/NFT listing is not supported.
    """

    # coin_symbol -> (JSON-RPC urls tried in order, web explorer base url)
    CHAINS = {
        "POLTEST": (  # Polygon Amoy testnet (chain id 80002)
            ["https://polygon-amoy-bor-rpc.publicnode.com", "https://rpc-amoy.polygon.technology"],
            "https://amoy.polygonscan.com/",
        ),
    }

    def __init__(self, coin: BaseCoin, apikeys: Dict[str, str]):
        super().__init__(coin, apikeys)
        self.rpc_urls, self.web_url = self.CHAINS.get(self.coin_symbol, ([], "https://notfound.org/"))

    """Utilities"""

    def get_address_web_url(self, addr: str) -> str:
        """Get web link for an address"""
        return f"{self.web_url}address/{addr}"

    def get_token_web_url(self, contract: str) -> str:
        """Get web link for a token"""
        return f"{self.web_url}token/{contract}"

    def get_nft_web_url(self, contract: str, tokenid: str) -> str:
        """Get web link for a token"""
        return f"{self.web_url}nft/{contract}/{tokenid}"

    def rpc_call(self, method: str, params: list):
        """Send a JSON-RPC request, trying each node in turn"""
        payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
        for url in self.rpc_urls:
            _logger.debug("POST %s method=%s", url, method)
            try:
                response = requests.post(url, json=payload, timeout=20)
                if response.status_code != 200:
                    _logger.warning("Failed to recover data from url %s, response status %s", url, response.status_code)
                    continue
                data = response.json()
                if 'result' in data:
                    return data['result']
                _logger.warning("JSON-RPC error from url %s: %s", url, data.get('error'))
            except (requests.exceptions.RequestException, ValueError) as ex:
                _logger.warning("Failed to recover data from url %s: %s", url, ex)
        raise DataFetcherError(DataFetcherError.INVALID_URL)

    """API"""

    def get_coin_info(self, addr):
        """Get native coin info for an address"""
        _logger.debug("JsonRpcExplorer get_coin_info for: %s", addr)

        balance_wei = self.rpc_call("eth_getBalance", [addr, "latest"])  # hex string
        coin_info = {}
        coin_info['balance'] = Decimal(int(balance_wei, 16)) / Decimal('1000000000000000000')
        if self.coin.is_testnet:
            # testnet coins are worthless
            coin_info['exchange_rate'] = Decimal(0)
            coin_info['currency'] = "USD"

        # basic info
        coin_info['symbol'] = self.coin_symbol
        coin_info['name'] = self.coin.display_name
        coin_info['type'] = AssetType.COIN
        coin_info['address_explorer_url'] = self.get_address_web_url(addr)
        _logger.debug("coin_info: %s", coin_info)
        return coin_info

    def get_asset_list(self, addr):
        """Get asset info for an address"""
        _logger.debug("JsonRpcExplorer get_asset_list for: %s", addr)
        return []
