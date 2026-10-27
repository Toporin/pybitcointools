import json
import logging
from decimal import Decimal, InvalidOperation
from typing import Dict, Union, Any
import requests

from pycryptotools.coins.base_coin import BaseCoin
from pycryptotools.coins.asset_type import AssetType
from pycryptotools.explorers.block_explorer import BlockExplorer
from pycryptotools.explorers.explorer_exceptions import DataFetcherError

_logger = logging.getLogger(__name__)


class BlockscoutExplorer(BlockExplorer):

    def __init__(self, coin: BaseCoin, apikeys: Dict[str, str]):
        super().__init__(coin, apikeys)

    """Utilities"""

    def get_web_url(self) -> str:
        """Get base URL based on coin symbol"""
        urls = {
            "ETH": "https://eth.blockscout.com/",
            "ETHTEST": "https://eth-sepolia.blockscout.com/",
            "ETC": "https://etc.blockscout.com/",
            "ETCTEST": "https://etc-mordor.blockscout.com/",
            "BASE": "https://base.blockscout.com/",
            "BASETEST": "https://base-sepolia.blockscout.com/",
            "POL": "https://polygon.blockscout.com/",
        }
        if self.coin_symbol not in urls:
            # a placeholder url would answer 404, i.e. "address not found" with a zero balance
            raise DataFetcherError(f"Blockscout does not support {self.coin_symbol}")
        return urls[self.coin_symbol]

    def get_api_url(self) -> str:
        """Get base API URL based on coin symbol"""
        url = self.get_web_url() + "api/v2/"
        return url

    def get_address_web_url(self, addr: str) -> str:
        """Get web link for an address"""
        return f"{self.get_web_url()}address/{addr}"

    def get_token_web_url(self, contract: str) -> str:
        """Get web link for a token"""
        return f"{self.get_web_url()}token/{contract}"

    def get_nft_web_url(self, contract: str, tokenid: str) -> str:
        """Get web link for a token"""
        return f"{self.get_web_url()}token/{contract}/instance/{tokenid}"

    """API"""

    def get_coin_info(self, addr):
        """Get native coin info for an address"""
        _logger.debug("BlockscoutExplorer get_coin_info for: %s", addr)

        url = f"{self.get_api_url()}addresses/{addr}"
        _logger.debug("GET %s", url)

        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            if response.status_code == 404:
                # Not found in blockchain
                coin_info = {}
                coin_info['balance'] = Decimal(0)
                coin_info['symbol'] = self.coin_symbol
                coin_info['name'] = self.coin.display_name
                coin_info['type'] = AssetType.COIN
                coin_info['address_explorer_url'] = self.get_address_web_url(addr)
                _logger.debug("Address not found on chain, coin_info: %s", coin_info)
                return coin_info
            else:
                _logger.warning("Failed to recover data from url %s, response status %s", url, response.status_code)
                raise DataFetcherError(DataFetcherError.INVALID_URL)

        data = response.json()
        coin_info = self.parse_coin_info_json(data)
        coin_info['symbol'] = self.coin_symbol
        coin_info['name'] = self.coin.display_name
        coin_info['type'] = AssetType.COIN
        coin_info['address_explorer_url'] = self.get_address_web_url(addr)
        _logger.debug("coin_info: %s", coin_info)
        return coin_info

    def get_asset_list(self, addr):
        """Get asset info for an address"""
        _logger.debug("BlockscoutExplorer get_asset_list for: %s", addr)

        # url = f"{self.get_api_url()}addresses/{addr}/tokens?type=ERC-20%2CERC-721%2CERC-1155"
        # url = f"{self.get_api_url()}addresses/{addr}/tokens"
        url = f"{self.get_api_url()}addresses/{addr}/tokens?type=ERC-20" # only erc20
        _logger.debug("GET %s", url)

        # todo: pagination https://docs.blockscout.com/devs/apis/rest
        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            if response.status_code == 404:
                # Not found in blockchain
                _logger.debug("Address not found on chain: %s", url)
                return []
            else:
                _logger.warning("Failed to recover data from url %s, response status %s", url, response.status_code)
                raise DataFetcherError(DataFetcherError.INVALID_URL)

        data = response.json()

        # get nfts
        url = f"{self.get_api_url()}addresses/{addr}/nft"  # no erc20, but erc721, erc404 & erc1155
        _logger.debug("GET %s", url)

        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            if response.status_code == 404:
                # no NFT found: keep the tokens already recovered
                _logger.debug("Address not found on chain: %s", url)
                data_nft = {}
            else:
                _logger.warning("Failed to recover data from url %s, response status %s", url, response.status_code)
                raise DataFetcherError(DataFetcherError.INVALID_URL)
        else:
            data_nft = response.json()

        # merge token & nft data (both responses list assets under 'items')
        data['items'] = data.get('items', []) + data_nft.get('items', [])

        asset_list = self.parse_asset_list_json(addr, data)
        _logger.debug("asset_list: %s", asset_list)
        return asset_list

    """Parsers"""

    @staticmethod
    def parse_coin_info_json(json_data: Union[str, Dict]) -> Dict[str, Any]:
        """
        Parse Ethereum address JSON data into a cleaned dictionary format.

        Args:
            json_data: Either a JSON string or dictionary containing address information

        Returns:
            Dictionary containing parsed and formatted address information
        """
        try:
            # Parse JSON if string, otherwise use the dict directly
            data = json.loads(json_data) if isinstance(json_data, str) else json_data

            # Convert balance from wei to ether if present
            coin_balance_wei = data.get('coin_balance', '0')
            coin_balance_eth = (
                Decimal(coin_balance_wei) / Decimal('1000000000000000000')
                if coin_balance_wei is not None
                else Decimal(0)
            )

            parsed_data = {}
            parsed_data['balance'] = coin_balance_eth
            try:
                parsed_data['exchange_rate'] = Decimal(data.get('exchange_rate'))
            except (TypeError, InvalidOperation):
                # no price available, e.g. on testnets
                parsed_data['exchange_rate'] = None
            parsed_data['currency'] = "USD"
            parsed_data['ens_domain'] = data.get('ens_domain_name')

            return parsed_data

        except (json.JSONDecodeError, ValueError, InvalidOperation) as e:
            #raise ValueError(f"Error parsing JSON data: {e}")
            parsed_data = {
                'error': str(e)
            }
            return parsed_data

    def parse_asset_list_json(self, addr, json_data: Union[str, Dict]) -> [Dict[str, Any]]:

        asset_list = []

        # Parse JSON if string, otherwise use the dict directly
        data = json.loads(json_data) if isinstance(json_data, str) else json_data

        items = data.get('items', [])  # list of assets
        for item in items:
            try:
                asset = {}
                token = item.get('token', {})
                asset['name'] = token.get('name')
                asset['contract'] = token.get('address_hash', None)
                asset['symbol'] = token.get('symbol', None)
                asset['icon_url'] = token.get('icon_url', None)

                # exchange rate
                try:
                    asset['exchange_rate'] = Decimal(token.get('exchange_rate'))
                    asset['currency'] = "USD"
                except Exception as ex:
                    asset['exchange_rate'] = None
                    asset['currency'] = None

                # balance
                try:
                    decimals = token.get('decimals', 0) or 0
                    asset['balance'] = Decimal(item.get('value')) / (10**Decimal(decimals))
                except Exception as ex:
                    asset['balance'] = None

                asset_type = token.get('type')
                if asset_type == "ERC-20":
                    asset['type'] = AssetType.TOKEN
                else:
                    asset['type'] = AssetType.NFT

                asset['external_app_url'] = item.get('external_app_url', None)

                # NFTs
                asset['tokenid'] = item.get('id', None)
                asset['nft_image_url'] = item.get('image_url', None)
                asset['nft_explorer_url'] = self.get_nft_web_url(asset.get("contract"), asset.get("tokenid"))

                # NFT details
                metadata = item.get('metadata', {})
                asset['nft_attributes'] = metadata.get('attributes', None)
                asset['nft_description'] = metadata.get('description', None)
                asset['nft_name'] = metadata.get('name', None)

                # nft = item.get('token', None)
                # if isinstance(nft, Dict):
                #     asset['tokenid'] = nft.get('id', "")
                #     asset['nft_image_url'] = nft.get('image_url', "")
                #     asset['nft_explorer_url'] = self.get_nft_web_url(asset.get("contract"), asset.get("tokenid"))

                asset_list += [asset]

                # explorer links
                asset['token_explorer_url'] = self.get_token_web_url(asset.get("contract"))
                asset['address_explorer_url'] = self.get_address_web_url(addr)

            except Exception as ex:
                _logger.warning("Failed to parse asset in BlockscoutExplorer: %s", ex)
                _logger.debug("Unparsed asset: %s", item)

        return asset_list
