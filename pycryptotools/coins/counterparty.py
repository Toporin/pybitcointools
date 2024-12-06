#from ..explorers import blockchain
from .bitcoin import Bitcoin
# from ..explorers import xchain
# from .base_coin import BaseCoin
from ..explorers.xchain_block_explorer import XchainBlockExplorer


class Counterparty(Bitcoin):
    coin_symbol = "XCP"
    display_name = "Counterparty"
    segwit_supported = False # currently, use legacy
    magicbyte = 0
    script_magicbyte = 5
    segwit_hrp = "bc"
    use_compressed_addr = True
    supports_nft= True
    supports_token= True
    explorer = XchainBlockExplorer(coin_symbol, apikeys={})  # xchain
    #nft_explorer= xchain
    
    client_kwargs = {
        'server_file': 'bitcoin.json',
    }

    testnet_overrides = {
        'display_name': "Counterparty Testnet",
        'coin_symbol': "XCPTEST",
        'magicbyte': 111,
        'script_magicbyte': 196,
        'segwit_hrp': 'tb',
        'hd_path': 1,
        'wif_prefix': 0xef,
        'client_kwargs': {
            'server_file': 'bitcoin_testnet.json',
        },
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