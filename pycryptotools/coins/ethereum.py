from eth_hash.auto import keccak

from pycryptotools.coins.base_coin import BaseCoin
from pycryptotools.explorers.blockscout_explorer import BlockscoutExplorer


class Ethereum(BaseCoin):
    coin_symbol = "ETH"
    display_name = "Ethereum"
    use_compressed_addr = False
    magicbyte = 0
    script_magicbyte = 5
    nft_supported = True
    
    testnet_overrides = {
        'display_name': "Ethereum Testnet", # sepolia?
        'coin_symbol': "ETHTEST",
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

    def __init__(self, testnet=False, **kwargs):
        super().__init__(testnet, **kwargs)
        self.explorers = [BlockscoutExplorer(self, self.apikeys)]

    def pubtoaddr(self, pubkey: bytes) -> str:
        """
        Get address from a public key
        """
        size= len(pubkey)
        # ethereum use uncompressed address
        if size<64 or size>65:
            addr= f"Unexpected pubkey size {size}, should be 64 or 65 bytes"
            return addr
            #raise Exception(f"Unexpected pubkey size{size}, should be 64 or 65 bytes")
        if size== 65:
            pubkey= pubkey[1:]
        
        pubkey_hash= keccak(pubkey)
        pubkey_hash= pubkey_hash[-20:]
        addr= "0x" + pubkey_hash.hex()
        return addr
