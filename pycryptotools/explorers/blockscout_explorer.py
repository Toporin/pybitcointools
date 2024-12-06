import json
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List, Optional, Tuple, Union, Any
import aiohttp
import requests

from pycryptotools.coins.asset_type import AssetType
from pycryptotools.explorers.base_explorer import BaseExplorer
from pycryptotools.explorers.block_explorer import BlockExplorer
from pycryptotools.explorers.explorer_exceptions import DataFetcherError


class BlockscoutExplorer(BaseExplorer):

    def __init__(self, coin_symbol: str, apikeys: Dict[str, str]):
        super().__init__(coin_symbol, apikeys)

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
        return urls.get(self.coin_symbol, "https://notfound.org/")

    def get_api_url(self) -> str:
        """Get base API URL based on coin symbol"""
        url = self.get_web_url() + "/api/v2/"
        return url

    def get_address_web_link(self, addr: str) -> str:
        """Get web link for an address"""
        return f"{self.get_web_url()}address/{addr}"

    def get_token_web_link(self, contract: str) -> str:
        """Get web link for a token"""
        return f"{self.get_web_url()}token/{contract}"

    def get_nft_web_link(self, contract: str, tokenid: str) -> str:
        """Get web link for a token"""
        return f"{self.get_web_url()}token/{contract}/instance/{tokenid}"

    """API"""

    def get_coin_info(self, addr):
        """Get native coin info for an address"""
        print(f"In BlockscoutExplorer get_coin_info for: {addr}")

        url = f"{self.get_api_url()}addresses/{addr}"
        print(f"urlString: {url}")

        response = requests.get(url)
        if response.status_code != 200:
            raise DataFetcherError(DataFetcherError.INVALID_URL)

        data = response.json()
        coin_info = self.parse_coin_info_json(data)
        coin_info['symbol'] = self.coin_symbol
        coin_info['name'] = self.coin_symbol  # todo name
        coin_info['type'] = AssetType.COIN
        coin_info['address_explorer_url'] = self.get_address_web_link(addr)
        print(f"coin_info: {coin_info}")
        return coin_info

        # async with aiohttp.ClientSession() as session:
        #     async with session.get(url) as response:
        #         if response.status != 200:
        #             raise DataFetcherError(DataFetcherError.INVALID_URL)
        #
        #         data = await response.json()
        #         coin_info = self.parse_coin_info_json(data)
        #         coin_info['symbol'] = self.coin_symbol
        #         coin_info['name'] = self.coin_symbol # todo name
        #         coin_info['type'] = AssetType.COIN
        #         print(f"coin_info: {coin_info}")
        #         return coin_info


    def get_asset_list(self, addr):
        """Get asset info for an address"""
        print(f"In BlockscoutExplorer get_asset_list for: {addr}")

        # url = f"{self.get_api_url()}addresses/{addr}/tokens?type=ERC-20%2CERC-721%2CERC-1155"
        url = f"{self.get_api_url()}addresses/{addr}/tokens"
        print(f"urlString: {url}")

        # todo: pagination https://docs.blockscout.com/devs/apis/rest
        response = requests.get(url)
        if response.status_code != 200:
            raise DataFetcherError(DataFetcherError.INVALID_URL)

        data = response.json()
        asset_list = self.parse_asset_list_json(addr, data)
        print(f"asset_list: {asset_list}")
        return asset_list

        # async with aiohttp.ClientSession() as session:
        #     async with session.get(url) as response:
        #         if response.status != 200:
        #             raise DataFetcherError(DataFetcherError.INVALID_URL)
        #
        #         data = await response.json()
        #         asset_list = self.parse_asset_list_json(addr, data)
        #         print(f"asset_list: {asset_list}")
        #         return asset_list


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
            coin_balance_wei = data.get('coin_balance')
            coin_balance_eth = (
                Decimal(coin_balance_wei) / Decimal('1000000000000000000')
                if coin_balance_wei is not None
                else None
            )

            parsed_data = {}
            parsed_data['balance'] = coin_balance_eth
            parsed_data['exchange_rate'] = data.get('exchange_rate'),
            parsed_data['currency'] = data.get('USD'),
            parsed_data['ens_domain'] = data.get('ens_domain_name')


            # Build parsed dictionary with formatted data
            # full_parsed_data = {
            #     # Basic information
            #     'address': {
            #         'hash': data.get('hash'),
            #         'ens_domain': data.get('ens_domain_name'),
            #     },
            #
            #     # Balance information
            #     'balance': {
            #         'wei': coin_balance_wei,
            #         'ether': coin_balance_eth,
            #         'last_updated_block': data.get('block_number_balance_updated_at'),
            #         'exchange_rate_usd': data.get('exchange_rate'),
            #     },
            #
            #     # Address properties
            #     'properties': {
            #         'is_contract': data.get('is_contract', False),
            #         'is_verified': data.get('is_verified', False),
            #         'is_scam': data.get('is_scam', False),
            #     },
            #
            #     # Blockchain activity
            #     'activity': {
            #         'has_tokens': data.get('has_tokens', False),
            #         'has_token_transfers': data.get('has_token_transfers', False),
            #         'has_validated_blocks': data.get('has_validated_blocks', False),
            #         'has_beacon_chain_withdrawals': data.get('has_beacon_chain_withdrawals', False),
            #         'has_logs': data.get('has_logs', False),
            #     },
            #
            #     # Creation details
            #     'creation': {
            #         'transaction_hash': data.get('creation_transaction_hash') or data.get('creation_tx_hash'),
            #         'creator_address': data.get('creator_address_hash'),
            #     },
            #
            #     # Tags and metadata
            #     'tags': {
            #         'public': data.get('public_tags', []),
            #         'private': data.get('private_tags', []),
            #         'watchlist': data.get('watchlist_names', []),
            #     }
            # }

            return parsed_data

        except (json.JSONDecodeError, ValueError) as e:
            #raise ValueError(f"Error parsing JSON data: {e}")
            parsed_data = {
                'error': str(e)
            }
            return parsed_data

    def parse_asset_list_json(self, addr, json_data: Union[str, Dict]) -> [Dict[str, Any]]:

        asset_list = []

        # Parse JSON if string, otherwise use the dict directly
        data = json.loads(json_data) if isinstance(json_data, str) else json_data

        items = data.get('items', []) # list of assets
        for item in items:
            asset = {}
            token = item.get('token', {})
            asset['name'] = token.get('name')
            asset['exchange_rate'] = token.get('exchange_rate')
            asset['currency'] = "USD"
            asset['contract'] = token.get('address', '')

            try:
                asset['balance'] = Decimal(item.get('value')) / (10**Decimal(token.get('decimals')))
            except Exception as ex:
                asset['balance'] = None

            type = token.get('type')
            if type == "ERC-20":
                asset['type'] = AssetType.TOKEN
            elif type == "ERC-1155":
                asset['type'] = AssetType.NFT
            elif type == "ERC-721":
                asset['type'] = AssetType.NFT

            nft = item.get('token_instance', None)
            if isinstance(nft, Dict):
                asset['tokenid'] = nft.get('id', "")
                asset['nft_image_url'] = nft.get('image_url', "")
                asset['nft_explorer_url'] = self.get_nft_web_link(asset.get("contract"), asset.get("tokenid"))

            asset_list += [asset]

            # explorer links
            asset['token_explorer_url'] = self.get_token_web_link(asset.get("contract"))
            asset['address_explorer_url'] = self.get_address_web_link(addr)

        return asset_list
