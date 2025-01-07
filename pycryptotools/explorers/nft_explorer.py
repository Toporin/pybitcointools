from abc import ABC, abstractmethod
from typing import Dict, List, Any

from pycryptotools.explorers.base_explorer import BaseExplorer


class NftExplorer(BaseExplorer):
    def __init__(self, coin_symbol: str, apikeys: Dict[str, str]):
        """
        Initialize the NftExplorer.

        Args:
            coin_symbol (str): Symbol of the cryptocurrency
            api_keys (Dict[str, str]): Dictionary of API keys
        """
        super().__init__(coin_symbol, apikeys)

    @abstractmethod
    def get_nft_owner_web_url(self, addr: str) -> str:
        """
        Get the web link for an NFT owner.

        Args:
            addr (str): The address of the NFT owner

        Returns:
            str: Web link to the NFT owner's page
        """
        pass

    @abstractmethod
    def get_nft_web_url(self, contract: str, tokenid: str) -> str:
        """
        Get the web link for a specific NFT.

        Args:
            contract (str): The NFT contract address
            tokenid (str): The specific token ID

        Returns:
            str: Web link to the specific NFT
        """
        pass

    @abstractmethod
    async def get_nft_list(self, addr: str, contract: str) -> List[Dict[str, str]]:
        """
        Get a list of NFTs for a given address and contract.

        Args:
            addr (str): The address to query
            contract (str): The NFT contract address

        Returns:
            List[Dict[str, str]]: List of NFTs with their details
        """
        pass

    @abstractmethod
    async def get_nft_info(self, contract: str, tokenid: str) -> Dict[str, str]:
        """
        Get information about a specific NFT.

        Args:
            contract (str): The NFT contract address
            tokenid (str): The specific token ID

        Returns:
            Dict[str, str]: Information about the NFT
        """
        pass