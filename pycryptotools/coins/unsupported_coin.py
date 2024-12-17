#from ..explorers import blockchain
from typing import List, Dict, Any

from pycryptotools.coins.asset_type import AssetType
from pycryptotools.coins.base_coin import BaseCoin


class UnsupportedCoin(BaseCoin):
    coin_symbol = "UNKNOWN"
    display_name = "Unsupported Coin"
    key_slip44_hex = "0x"
    testnet_overrides = {
        'display_name': "Unsupported Testnet",
        'coin_symbol': "UNKNOWNTEST",
        'magicbyte': 111,
        'script_magicbyte': 196,
        'hd_path': 1,
        'wif_prefix': 0xef,
        'xprv_headers': {
            'p2pkh': 0x04358394,
            'p2wpkh-p2sh': 0x044a4e28,
            'p2wsh-p2sh': 0x295b005,
            'p2wpkh': 0x04358394,
            'p2wsh': 0x2aa7a99
        },
        'xpub_headers': {
            'p2pkh': 0x043587cf,
            'p2wpkh-p2sh': 0x044a5262,
            'p2wsh-p2sh': 0x295b43f,
            'p2wpkh': 0x043587cf,
            'p2wsh': 0x2aa7ed3
        },
    }

    def get_address_web_url(self, addr: str) -> str:
        # raise ValueError(f"Unsupported coin!")
        return "https://example.com"

    def get_coin_info(self, addr) -> Dict[str, Any]:
        # raise ValueError(f"Unsupported coin!")
        coin_info= {}
        coin_info['symbol'] = self.coin_symbol
        coin_info['name'] = self.display_name
        coin_info['type'] = AssetType.COIN
        coin_info['address_explorer_url'] = self.get_address_web_url(addr)
        return coin_info

    def get_asset_list(self, addr: str) -> List[Dict[str, Any]]:
        return []

        ######################################
        #            PRICE EXPLORER          #
        ######################################

    def get_exchange_rate_with(self, other_coin: str):
        raise ValueError(f"Unsupported coin!")


    def pubtoaddr(self, pubkey):
        return f"(unsupported coin 0x{self.key_slip44_hex})"

