#from ..explorers import blockchain
from ..explorers import etherscan
from ..explorers import rarible
from ..explorers import opensea
from .base import BaseCoin

#from eth_utils import keccak
from eth_hash.auto import keccak

class Ethereum(BaseCoin):
    coin_symbol = "ETH"
    display_name = "Ethereum"
    segwit_supported = False
    use_compressed_addr= False
    magicbyte = 0
    script_magicbyte = 5
    explorer = etherscan
    nft_explorer= rarible #opensea # rarible # 
    nft_supported= True
    
    testnet_overrides = {
        'display_name': "Ropsten Testnet",
        'coin_symbol': "ROP",
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
    
    def pubtoaddr(self, pubkey:bytes)-> str:
        """
        Get address from a public key
        """
        size= len(pubkey)
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
        
    def get_nft_owner_weburl(self, address:str) -> str:
        return opensea.get_nft_owner_weburl(address)
        
    def get_nft_weburl(self, contract:str, token_id:str)->str:
        return opensea.get_nft_weburl(contract, token_id)