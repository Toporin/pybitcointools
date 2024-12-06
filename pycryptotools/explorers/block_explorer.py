from abc import abstractmethod
from typing import Dict, List, Tuple, Any
import asyncio

from pycryptotools.explorers.base_explorer import BaseExplorer


class BlockExplorer(BaseExplorer):

    def __init__(self, coin_symbol: str, apikeys: Dict[str, str]):
        super().__init__(coin_symbol, apikeys)



    @abstractmethod
    def get_address_web_link(self, addr: str) -> str:
        """
        Get the web link for a given address.

        Args:
            addr (str): The blockchain address

        Returns:
            str: Web link to the address
        """
        pass

    @abstractmethod
    def get_token_web_link(self, contract: str) -> str:
        """
        Get the web link for a given token contract.

        Args:
            contract (str): The token contract address

        Returns:
            str: Web link to the token contract
        """
        pass

    @abstractmethod
    async def get_balance(self, addr: str) -> float:
        """
        Get the balance for a given address.

        Args:
            addr (str): The blockchain address

        Returns:
            float: Balance of the address
        """
        pass

    @abstractmethod
    async def get_asset_list(self, addr: str) -> Dict[str, List[Dict[str, str]]]:
        """
        Get detailed list of assets held in a given address.

        Args:
            addr (str): The blockchain address

        Returns:
            Dict[str, List[Dict[str, str]]]: Detailed asset list
        """
        pass

    @abstractmethod
    async def get_simple_asset_list(self, addr: str) -> List[Dict[str, str]]:
        """
        Get basic list of assets held in a given address.

        Args:
            addr (str): The blockchain address

        Returns:
            List[Dict[str, str]]: Basic asset list
        """
        pass

    @abstractmethod
    async def get_token_balance(self, addr: str, contract: str) -> float:
        """
        Get token balance for a specific token at a given address.

        Args:
            addr (str): The blockchain address
            contract (str): The token contract address

        Returns:
            float: Token balance
        """
        pass

    @abstractmethod
    async def get_token_info(self, contract: str) -> Dict[str, str]:
        """
        Get information about a token contract.

        Args:
            contract (str): The token contract address

        Returns:
            Dict[str, str]: Token information
        """
        pass

    @abstractmethod
    async def get_tx_info(self, tx_hash: str, index: int) -> Tuple[str, int]:
        """
        Get transaction information.

        Args:
            tx_hash (str): The transaction hash
            index (int): Transaction index

        Returns:
            Tuple[str, int]: Tuple of (script, value)
        """
        pass