from abc import abstractmethod
from typing import Dict, List, Tuple

from pycryptotools.coins.base_coin import BaseCoin
from pycryptotools.explorers.base_explorer import BaseExplorer


class BlockExplorer(BaseExplorer):

    def __init__(self, coin: BaseCoin, apikeys: Dict[str, str]):
        super().__init__(coin, apikeys)


    def get_address_web_url(self, addr):
        """
        returns a url to a blockchain explorer on the web:
        """
        pass

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

    # @abstractmethod
    # def get_address_web_url(self, addr: str) -> str:
    #     """
    #     Get the web link for a given address.
    #
    #     Args:
    #         addr (str): The blockchain address
    #
    #     Returns:
    #         str: Web link to the address
    #     """
    #     pass
    #
    # @abstractmethod
    # def get_token_web_url(self, contract: str) -> str:
    #     """
    #     Get the web link for a given token contract.
    #
    #     Args:
    #         contract (str): The token contract address
    #
    #     Returns:
    #         str: Web link to the token contract
    #     """
    #     pass
    #
    # @abstractmethod
    # async def get_balance(self, addr: str) -> float:
    #     """
    #     Get the balance for a given address.
    #
    #     Args:
    #         addr (str): The blockchain address
    #
    #     Returns:
    #         float: Balance of the address
    #     """
    #     pass
    #
    # @abstractmethod
    # async def get_asset_list(self, addr: str) -> Dict[str, List[Dict[str, str]]]:
    #     """
    #     Get detailed list of assets held in a given address.
    #
    #     Args:
    #         addr (str): The blockchain address
    #
    #     Returns:
    #         Dict[str, List[Dict[str, str]]]: Detailed asset list
    #     """
    #     pass
    #
    # @abstractmethod
    # async def get_simple_asset_list(self, addr: str) -> List[Dict[str, str]]:
    #     """
    #     Get basic list of assets held in a given address.
    #
    #     Args:
    #         addr (str): The blockchain address
    #
    #     Returns:
    #         List[Dict[str, str]]: Basic asset list
    #     """
    #     pass
    #
    # @abstractmethod
    # async def get_token_balance(self, addr: str, contract: str) -> float:
    #     """
    #     Get token balance for a specific token at a given address.
    #
    #     Args:
    #         addr (str): The blockchain address
    #         contract (str): The token contract address
    #
    #     Returns:
    #         float: Token balance
    #     """
    #     pass
    #
    # @abstractmethod
    # async def get_token_info(self, contract: str) -> Dict[str, str]:
    #     """
    #     Get information about a token contract.
    #
    #     Args:
    #         contract (str): The token contract address
    #
    #     Returns:
    #         Dict[str, str]: Token information
    #     """
    #     pass
    #
    # @abstractmethod
    # async def get_tx_info(self, tx_hash: str, index: int) -> Tuple[str, int]:
    #     """
    #     Get transaction information.
    #
    #     Args:
    #         tx_hash (str): The transaction hash
    #         index (int): Transaction index
    #
    #     Returns:
    #         Tuple[str, int]: Tuple of (script, value)
    #     """
    #     pass