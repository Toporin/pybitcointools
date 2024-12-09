import unittest
from typing import List
import base58

from pycryptotools.coins.base_coin import BaseCoin
from pycryptotools.coins.counterparty import Counterparty
from pycryptotools.coins.ethereum_forks import EthereumClassic, Polygon
from pycryptotools.coins.bitcoin import Bitcoin
from pycryptotools.coins.bitcoin_cash import BitcoinCash
from pycryptotools.coins.dash import Dash
from pycryptotools.coins.dogecoin import Doge
from pycryptotools.coins.ethereum import Ethereum
from pycryptotools.coins.litecoin import Litecoin

# test functions specifically used by SatodimeTool
# test vectors made with https://iancoleman.io/bip39/
# seed: tonight stem cause eyebrow estate smart duck wrong toe under job danger
# path: m/84'/0'/0'/0/* (using BIP84 path to get bech32 and base58 address)
# to run test: python3 -m unittest test_satodime


def wif2priv(private_key_WIF):
    first_encode = base58.b58decode(private_key_WIF)
    private_key_full = first_encode.hex() #binascii.hexlify(first_encode)
    private_key = private_key_full[2:-8]
    if len(private_key)==66:
        private_key= private_key[0:-2] # remove compression byte
    #print(private_key)
    return private_key # return a hex

def test_explorer(coin: BaseCoin, addrs: List[str]):
    try:
        print(f"TEST explorer for: {coin.coin_symbol}")
        for addr in addrs:
            print(f"TEST explorer addr: {addr}")
            coin_info = coin.get_coin_info(addr)
            print(f"TEST coin_info: {coin_info}")
            asset_list = coin.get_asset_list(addr)
            print(f"TEST asset_list size: {len(asset_list)}")
            print(f"TEST asset_list: {asset_list}")
    except Exception as ex:
        print(f"test_explorer() raised exception: {str(ex)}")
        raise

### BITCOIN ###

PUBKEY_BTC= [
    "03b7b3957daedecee4488dcb0b8cf3f3372d64d5c559953d2a2539f55e6474c8ce",
    "03e5c1e865d21a239c6639e75586df1f0a5e59853694601e78dccb22481fad08c0",
    "03f21a3b7ff93a4396d886b04b045b8a4dfaa3e13ae169adf36a7390f65af964c0",
    "035f6cb6545543c6b69ba402e19362a71c9ff58a93f8c2d812e0a6c27c6304e5d2",
    "03e1d8b41fa14419293b29ad6f98d5bd1827ae21b5f1083a7cc001955db2ee628c",
]
ADDRESS_BTC= [
    "1Q6QXhpreAW8wDRwaL6jvdEcbbceFMw2mv",
    "1976pT5yu88hDa7HsQK76tpbyYtPTyN3cF",
    "1QC6JNGbXdmQFkBp69yFFXdYZKvXtfCeEx",
    "14Kz6dHFJjJNqj2hvQ84vSzYq78T9pmoWi",
    "1Lr8JCa936osnV288Jm3LYBKKvvvQJkdfy",
]
ADDRESS_SEGWIT_BTC= [
    "bc1ql4gf6wjve0enmmsvr0vrv4f0v9cnxzcnhpjnx2",
    "bc1qtr59h4kqargu5les2as8w2tumqreh58ew2ks5d",
    "bc1qle37gu93ja9csxndeu7q57g49jf5j4qsckw9g0",
    "bc1qy3lcdhn4crpev6ppejlt20kzhdg528f3t4wp27",
    "bc1qmx6deexe6r8vvn775e5hjur78g2q4n5fe0fzyn",
]
PRIVKEY_WIF_BTC= [
    "KzsYHPmjK3VbtFvRL4PbaEAnUePcgQjJZC1B4RjcR1AXbZbC5Yfu",
    "L4cWMhJWvJwBFv1WrwfoTZYW4EDrT33KSoYtQEfnruzgNiupUNnq",
    "L4wZXSWJNr2fWbmf2Pfh1XyFew9tSog65nxUiA6767fhot4kGBeX",
    "L1Xb8kjGUgT322K2pGpUV3EYzzUucT9hsR34mAphtY1C8RwVqLWP",
    "KxF9SWjzRygz8DP32RdPhak19aMruJiFBYyavcMXRqQT3rr2n41w",
]

ADDRESS_BTC_EXPLORER = [  # testing block explorer
"bc1ql49ydapnjafl5t2cp9zqpjwe6pdgmxy98859v2" # some whale
]


class BitcoinCase(unittest.TestCase):
    
    coin = Bitcoin(testnet=False)
    
    @classmethod
    def setUpClass(cls):
        print(f'Starting {cls.coin.display_name} test') 

    def test_address(self):
        
        self.assertEqual(self.coin.display_name, "Bitcoin")
        self.assertEqual(self.coin.coin_symbol, "BTC")
        self.assertEqual(self.coin.segwit_supported, True)
        self.assertEqual(self.coin.use_compressed_addr, True)
        PUBKEY= PUBKEY_BTC
        ADDRESS= ADDRESS_BTC
        PRIVKEY_WIF= PRIVKEY_WIF_BTC
        ADDRESS_SEGWIT= ADDRESS_SEGWIT_BTC
        
        for i, pubkey_hex in enumerate(PUBKEY):
            
            #pub_bytes= bytes.fromhex(pubkey_hex)
            pubkey_list= list(bytes.fromhex(pubkey_hex))
            addr= self.coin.pubtoaddr(bytes(pubkey_list))
            #self.assertEqual(addr, ADDRESS[i])
            self.assertEqual(addr, ADDRESS_SEGWIT[i])
            
            privkey_hex= wif2priv(PRIVKEY_WIF[i])
            privkey_list= list(bytes.fromhex(privkey_hex))
            if self.coin.use_compressed_addr:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif_compressed')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
            else:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
            
            # segwit
            if self.coin.segwit_supported:
                # addr_segwit= self.coin.pubtosegwit(bytes(pubkey_list))
                # self.assertEqual(addr_segwit, ADDRESS_SEGWIT[i])
                addr_legacy= self.coin.pubtolegacy(bytes(pubkey_list))
                self.assertEqual(addr_legacy, ADDRESS[i])
            
            #url
            url= self.coin.get_address_web_url(addr)
            print(f"URL= {url}")

    def test_explorer(self):
        test_explorer(self.coin, ADDRESS_BTC_EXPLORER)

class CounterpartyCase(unittest.TestCase):
    """  COUNTERPARTY  """

    ADDRESS_XCP_EXPLORER = [
        "1Do5kUZrTyZyoPJKtk4wCuXBkt5BDRhQJ4",
    ]
    coin = Counterparty(testnet=False)

    @classmethod
    def setUpClass(cls):
        print(f'Starting {cls.coin.display_name} test')

    def test_address(self):

        self.assertEqual(self.coin.display_name, "Counterparty")
        self.assertEqual(self.coin.coin_symbol, "XCP")
        self.assertEqual(self.coin.segwit_supported, False)
        self.assertEqual(self.coin.use_compressed_addr, True)
        PUBKEY = PUBKEY_BTC
        PRIVKEY_WIF = PRIVKEY_WIF_BTC

        for i, pubkey_hex in enumerate(PUBKEY):

            # pub_bytes= bytes.fromhex(pubkey_hex)
            pubkey_bytes = bytes.fromhex(pubkey_hex)
            addr = self.coin.pubtoaddr(pubkey_bytes)
            self.assertEqual(addr, ADDRESS_BTC[i])

            privkey_hex = wif2priv(PRIVKEY_WIF[i])
            privkey_list = list(bytes.fromhex(privkey_hex))
            if self.coin.use_compressed_addr:
                privkey_wif = self.coin.encode_privkey(privkey_list, 'wif_compressed')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
            else:
                privkey_wif = self.coin.encode_privkey(privkey_list, 'wif')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])

    def test_explorer(self):
        test_explorer(self.coin, self.ADDRESS_XCP_EXPLORER)



### TESTNET BTC ####

PUBKEY_BTCTEST=[
    "02860988886ecd730c1bd2f4d5d8a015492aa656f92d7dff09ef0f951677211a9a",
    "021a3d3978e501156197af1dc22ba09fd1597251de126c27448cf67a91064f3ede",
    "021f3d54734d7ac715fba56650d4a8fa12ab64939c8256729eba78ef2188fb4a5c",
    "0381872214b49468e718ba324bfb91c9a4a9b777339b1abdc8167030a1f33f916a",
    "02393edebdbe0c8886e1954c8791094393b4b160a96e32e7d799dfb7ea65dbc0d9",
]

ADDRESS_BTCTEST= [
    "mpinvcSCUmojQm64yDJzqfXg5NSuDCNX5k",
    "mgAYcUwkxyXq1N5crAXEcikty78ey2vBvt",
    "mghgGiTJkeJmpUyGX42QtVRFN95wnoWHxV",
    "mzRVdJPhiVVFFcr7vZv5spjgTKdk1HUh5E",
    "mnn9xeNVv9Dix2v2QMnZwY2Qhpwb6HCr4R",
]

ADDRESS_SEGWIT_BTCTEST=[
    "tb1qvnmy6khtlw06w49y2wzlmxn2xu09lyr7mfd794",
    "tb1qquwqn8mq444yzraecu9rwszws4zhguggjp3ldk",
    "tb1qpnl4xuh8v4s5wftjnmm9srvchya64kje0nepyr",
    "tb1qea3qcu5vmf6js2axyyzyzx9ef3x0k84g2vh43v",
    "tb1qf75dhyp0txvey0ll9gmc6kzxtmaqpzgwqzg7uz",
]

PRIVKEY_WIF_BTCTEST=[
    "cRWGHNwyxeZaw4B2XxogNsmyiahQdUdjoRFtMWew7CQbebPqHuyd",
    "cPQjd8KzYQ8T9N6XTFrQgjp9gkHCVcwukgiw8xfNf4P1zsR74Qus",
    "cSdfwpP9djT15W6XdxdvWyjqGPk3C1a38hZucUTx1pjNMKjeaJFp",
    "cQLHgHLBxdtePeXeBUhYj5rPs3CVP7GKMdQ4JmMHvz6DfjkhtWUo",
    "cUpjKR37hJX3tnkKN8Ui1stxFKp1LK8BUf1bEevFy5fwhervSfBi",
]

ADDRESS_BTCTEST_EXPLORER =[
    "mxufU2tFwZgUCF2LhUP8BRN8brtCKNoqx3", # legacy
    "tb1qm6juaswhsmdl4w4ezj7lqx5c6xdz7ct99weumg" # segwit
]

class BitcoinTestCase(unittest.TestCase):
    
    coin= Bitcoin(testnet= True)
    
    @classmethod
    def setUpClass(cls):
        print(f'Starting {cls.coin.display_name} test') 
        
        
    def test_address(self):
        
        self.assertEqual( self.coin.display_name, "Bitcoin Testnet")
        self.assertEqual( self.coin.coin_symbol, "BTCTEST")
        self.assertEqual( self.coin.segwit_supported, True)
        self.assertEqual( self.coin.use_compressed_addr, True)
        PUBKEY= PUBKEY_BTCTEST
        ADDRESS= ADDRESS_BTCTEST
        PRIVKEY_WIF= PRIVKEY_WIF_BTCTEST
        ADDRESS_SEGWIT= ADDRESS_SEGWIT_BTCTEST
        
        for i, pubkey_hex in enumerate(PUBKEY):
            
            #pub_bytes= bytes.fromhex(pubkey_hex)
            pubkey_list= list(bytes.fromhex(pubkey_hex))
            addr= self.coin.pubtoaddr(bytes(pubkey_list))
            #self.assertEqual(addr, ADDRESS[i])
            self.assertEqual(addr, ADDRESS_SEGWIT[i])
            
            #PRIVKEY_WIF= PRIVKEY_WIF[i]
            privkey_hex= wif2priv(PRIVKEY_WIF[i])
            privkey_list= list(bytes.fromhex(privkey_hex))
            if self.coin.use_compressed_addr:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif_compressed')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
            else:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
            
            # segwit
            if self.coin.segwit_supported:
                # addr_segwit= self.coin.pubtosegwit(bytes(pubkey_list))
                # self.assertEqual(addr_segwit, ADDRESS_SEGWIT[i])
                addr_legacy= self.coin.pubtolegacy(bytes(pubkey_list))
                self.assertEqual(addr_legacy, ADDRESS[i])
            
            #url
            url= self.coin.get_address_web_url(addr)
            print(f"URL= {url}")

    def test_explorer(self):
        test_explorer(self.coin, ADDRESS_BTCTEST_EXPLORER)

### LITECOIN ###

PUBKEY_LTC=[
    "031f0ed4b5cbd756626ec5f108f19b29fff7e93670e083a21cc32265ab4f4adece",
    "036f4cc9dbdc277c673870ad95d9e250119fe264f1905deab8de1ebdefc8ea45a4",
    "0294372dfc1cf72677bb3d86d93152261483d77870de046f3b859a97cfd9aca2c4",
    "02468a479f0e51a943e13173f827f7af43c51f864c8690a988f5b21975cd2d5bbe",
    "035f96c6cb9e2f0b372976c65766882a4d2d57954aa713ec9c35109fe58d23fdbc",
]
ADDRESS_LTC=[
    "Lc7WkFsqnS6bYrCYqdWzt5CatK2EkmLB6K",
    "LavvkpWGy9RteJXrhLYpK7d13oV8bqsaey",
    "LM7ScWi4LPQ3au34wSMUJ5C1HfNd5A6NN3",
    "LM9xJXSELgWhqYuTTsmVMw4s4pMiuZKvvH",
    "LbASsVLAwx7eZZBU7XG46XdgwJ8Uty15fa",
]
ADDRESS_SEGWIT_LTC=[
    "ltc1qh9p90tp8ffkyqsh6ptpa9hrnkgzsn0ul232qjm",
    "ltc1q43y6auh4q9wzq6n047tyucejt3sdruurtlqz7z",
    "ltc1qzj6sz4j35tjup6h6ytnx66utp54qzu0yyfeher",
    "ltc1qz5hfa7s5svk7zquc3zhcjkprkk6mtvyk5k74jl",
    "ltc1q4mvr4j9apt43gpytgwk92djw76c689z6qmn50e",
]
PRIVKEY_WIF_LTC=[
    "T87X7mAR3JkHb9nBSiyZnNTcnTZ31XTLbbYuP2gMF1uCpyxa6kgN",
    "T4A27wtfX4W7cFVDiLhNAYyqco3SdqEDSYFvrET8PGxwP8qMdGmn",
    "T9ywaRQ5iWuTH366NNzS6nKNUDX3XQda3KBH9iBmLgDqCiLMH1NT",
    "T4EoWASE91AoELW3wCs4Z7wxFuaieHd99eHeSswBVyg21fRPrLpF",
    "T3svmt7X7wWsWTWQ6e7vSj7S14KVLQSkbsEZ7rrYNJdjLZSYpAAo",
]
ADDRESS_LTC_EXPLORER=[
    "MQd1fJwqBJvwLuyhr17PhEFx1swiqDbPQS", # top account
    "ltc1qr07zu594qf63xm7l7x6pu3a2v39m2z6hh5pp4t",
    "LZEjckteAtWrugbsy9zU8VHEZ4iUiXo9Nm",
]


class LitecoinCase(unittest.TestCase):
    
    coin = Litecoin(testnet=False)
    
    @classmethod
    def setUpClass(cls):
        print(f'Starting {cls.coin.display_name} test') 
        
        
    def test_address(self):
        
        self.assertEqual( self.coin.display_name, "Litecoin")
        self.assertEqual( self.coin.coin_symbol, "LTC")
        self.assertEqual( self.coin.segwit_supported, True)
        self.assertEqual( self.coin.use_compressed_addr, True)
        PUBKEY= PUBKEY_LTC
        ADDRESS= ADDRESS_LTC
        PRIVKEY_WIF= PRIVKEY_WIF_LTC
        ADDRESS_SEGWIT= ADDRESS_SEGWIT_LTC
        
        for i, pubkey_hex in enumerate(PUBKEY):
            
            #pub_bytes= bytes.fromhex(pubkey_hex)
            pubkey_list= list(bytes.fromhex(pubkey_hex))
            addr= self.coin.pubtoaddr(bytes(pubkey_list))
            #self.assertEqual(addr, ADDRESS[i])
            self.assertEqual(addr, ADDRESS_SEGWIT[i])
            
            #PRIVKEY_WIF= PRIVKEY_WIF[i]
            privkey_hex= wif2priv(PRIVKEY_WIF[i])
            privkey_list= list(bytes.fromhex(privkey_hex))
            if self.coin.use_compressed_addr:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif_compressed')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
            else:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
            
            # segwit
            if self.coin.segwit_supported:
                # addr_segwit= self.coin.pubtosegwit(bytes(pubkey_list))
                # self.assertEqual(addr_segwit, ADDRESS_SEGWIT[i])
                addr_legacy= self.coin.pubtolegacy(bytes(pubkey_list))
                self.assertEqual(addr_legacy, ADDRESS[i])
            
            #url
            url= self.coin.get_address_web_url(addr)
            print(f"URL= {url}")

    def test_explorer(self):
        test_explorer(self.coin, ADDRESS_LTC_EXPLORER)

### LTCTEST ###

PUBKEY_LTCTEST=[
"02860988886ecd730c1bd2f4d5d8a015492aa656f92d7dff09ef0f951677211a9a",
"021a3d3978e501156197af1dc22ba09fd1597251de126c27448cf67a91064f3ede",
"021f3d54734d7ac715fba56650d4a8fa12ab64939c8256729eba78ef2188fb4a5c",
"0381872214b49468e718ba324bfb91c9a4a9b777339b1abdc8167030a1f33f916a",
"02393edebdbe0c8886e1954c8791094393b4b160a96e32e7d799dfb7ea65dbc0d9",
]
ADDRESS_LTCTEST=[
"mpinvcSCUmojQm64yDJzqfXg5NSuDCNX5k",
"mgAYcUwkxyXq1N5crAXEcikty78ey2vBvt",
"mghgGiTJkeJmpUyGX42QtVRFN95wnoWHxV",
"mzRVdJPhiVVFFcr7vZv5spjgTKdk1HUh5E",
"mnn9xeNVv9Dix2v2QMnZwY2Qhpwb6HCr4R",
]
ADDRESS_SEGWIT_LTCTEST=[
"tltc1qvnmy6khtlw06w49y2wzlmxn2xu09lyr7zp0q4u",
"tltc1qquwqn8mq444yzraecu9rwszws4zhguggtfnpal",
"tltc1qpnl4xuh8v4s5wftjnmm9srvchya64kjekmml52",
"tltc1qea3qcu5vmf6js2axyyzyzx9ef3x0k84gny4tp9",
"tltc1qf75dhyp0txvey0ll9gmc6kzxtmaqpzgwe22qvt",
]
# # iancoleman.io uses non-standard cst values?
# ADDRESS_SEGWIT_LTCTEST=[
# "litecointestnet1qvnmy6khtlw06w49y2wzlmxn2xu09lyr7rfn4a4",
# "litecointestnet1qquwqn8mq444yzraecu9rwszws4zhgugg2p054k",
# "litecointestnet1qpnl4xuh8v4s5wftjnmm9srvchya64kjehn82ur",
# "litecointestnet1qea3qcu5vmf6js2axyyzyzx9ef3x0k84gjvf7fv",
# "litecointestnet1qf75dhyp0txvey0ll9gmc6kzxtmaqpzgwczk4yz",
# ]
# # using wif_prefix= 0xb0 (same as main)
# PRIVKEY_WIF_LTCTEST=[
# "T6yYGDFJvxqvYTLdhBwRDupJ3D3K37YwYb1g6tpyB3vkujs5A9Te",
# "T4t1bxdKWiQnkmG8cUz9XmrU1Nd6uFs7VrUitLqQiuuBG1rf1nPb",
# "T86wvegUc3jLguG8oBmfN1n9b25wbeVEssKhMrdz5gFXcUEadGH9",
# "T5oZf7dWvxAz13hFLhqHa7tiBfYPnkBX6o9r49XKzqcNvt957Pwc",
# "TAJ1JFLSfcoPWBuvXMcSruwGZx9ujx3PDpmNz36J2wC6xoJXSy8P",
# ]
# iancoleman.io uses wif_prefix =0xef (same as btc testnet) instead of 0xb0 (this is the official implementation)
# see https://github.com/litecoin-project/litecoin/blob/master/src/chainparams.cpp => base58Prefixes[SECRET_KEY]
PRIVKEY_WIF_LTCTEST=[
"cRWGHNwyxeZaw4B2XxogNsmyiahQdUdjoRFtMWew7CQbebPqHuyd",
"cPQjd8KzYQ8T9N6XTFrQgjp9gkHCVcwukgiw8xfNf4P1zsR74Qus",
"cSdfwpP9djT15W6XdxdvWyjqGPk3C1a38hZucUTx1pjNMKjeaJFp",
"cQLHgHLBxdtePeXeBUhYj5rPs3CVP7GKMdQ4JmMHvz6DfjkhtWUo",
"cUpjKR37hJX3tnkKN8Ui1stxFKp1LK8BUf1bEevFy5fwhervSfBi",
]
class LitecoinTestCase(unittest.TestCase):
    
    coin = Litecoin(testnet=True)
    
    @classmethod
    def setUpClass(cls):
        print(f'Starting {cls.coin.display_name} test') 
        
        
    def test_address(self):
        
        self.assertEqual( self.coin.display_name, "Litecoin Testnet")
        self.assertEqual( self.coin.coin_symbol, "LTCTEST")
        self.assertEqual( self.coin.segwit_supported, True)
        self.assertEqual( self.coin.use_compressed_addr, True)
        PUBKEY= PUBKEY_LTCTEST
        ADDRESS= ADDRESS_LTCTEST
        PRIVKEY_WIF= PRIVKEY_WIF_LTCTEST
        ADDRESS_SEGWIT= ADDRESS_SEGWIT_LTCTEST
        
        for i, pubkey_hex in enumerate(PUBKEY):
            
            #pub_bytes= bytes.fromhex(pubkey_hex)
            pubkey_list= list(bytes.fromhex(pubkey_hex))
            addr= self.coin.pubtoaddr(bytes(pubkey_list))
            #self.assertEqual(addr, ADDRESS[i])
            self.assertEqual(addr, ADDRESS_SEGWIT[i])
            
            #PRIVKEY_WIF= PRIVKEY_WIF[i]
            privkey_hex= wif2priv(PRIVKEY_WIF[i])
            privkey_list= list(bytes.fromhex(privkey_hex))
            if self.coin.use_compressed_addr:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif_compressed')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
                #print(privkey_wif)
            else:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
            
            # segwit
            if self.coin.segwit_supported:
                # addr_segwit= self.coin.pubtosegwit(bytes(pubkey_list))
                # self.assertEqual(addr_segwit, ADDRESS_SEGWIT[i])
                addr_legacy= self.coin.pubtolegacy(bytes(pubkey_list))
                self.assertEqual(addr_legacy, ADDRESS[i])
                #print(addr_segwit)
            
            #url
            url= self.coin.get_address_web_url(addr)
            print(f"URL= {url}")

    def test_explorer(self):
        test_explorer(self.coin, ADDRESS_SEGWIT_LTCTEST)

### DOGE ###
# using path: m/0/*
PUBKEY_DOGE=[
"037f38c987d3e7ca6534b87588bc26c8c77739316c6af2b01ca5879c8d292472c2",
"020649a9b59a1f986efed9320fe61f9b1ae217e35b37a71bfe166d695742987b6d",
"0384c82879d42884922dfd3a9a1875730a6f642360fee8d28adb9f60c340713b85",
"03c056e24e61951169616e6a8e019ff54849822d65b9d947361b6bf05203ad8d15",
"02a931823029e1e305880d8bdc17f2a413c7c7cdc9eefffc4ace0777ef9d944977",
]
ADDRESS_DOGE=[
"DGz8cKG9BAQzMG4qTGcZSUgBj431QiQpPy",
"DD7DMsG5MQEWiyUV25wQPQyg2sAmuFoxrL",
"DPduibc3npShXmCidounsmCtXMMSk62saa",
"DGs7Nanzhd5d7BSUDRZTWEV2XGPv5AucTa",
"DFKY5RhMBn6r3rd2v9ZyYi3F7j1Sr8ptDR",
]
ADDRESS_SEGWIT_DOGE=[
]
# https://github.com/dogecoin/dogecoin/blob/master/src/chainparams.cpp#L157 => base58Prefixes[SECRET_KEY]
PRIVKEY_WIF_DOGE=[
"QTQ7ubYKBP6e5c9CNWksdm9pY7RzJLbr6HX2EmoQ98SwTbvbfNNG",
"QRU74ccQhCJ47C5RxGt3kUefCzmT5Yu8mmMiJSRVcbknFxWHZw7r",
"QTyrmUUnqD7BGyPEuETHf1HV7ywA2uPdYePF96FUuBxGFpa9vCiV",
"QU2WVDe5ixgLALbmNCsarRUn1J9rziRaqRANE36pz1NZTuvXBj1y",
"QTpaLMGssmkuhVjDQqAJXyXX81XGAT5iBPus2g2bEuJ5aSvp7Nk7",
]
class DogeCase(unittest.TestCase):
    
    coin = Doge(testnet=False)
    
    @classmethod
    def setUpClass(cls):
        print(f'Starting {cls.coin.display_name} test') 
        
        
    def test_address(self):
        
        self.assertEqual( self.coin.display_name, "Dogecoin")
        self.assertEqual( self.coin.coin_symbol, "DOGE")
        self.assertEqual( self.coin.segwit_supported, False)
        self.assertEqual( self.coin.use_compressed_addr, True)
        PUBKEY= PUBKEY_DOGE
        ADDRESS= ADDRESS_DOGE
        PRIVKEY_WIF= PRIVKEY_WIF_DOGE
        ADDRESS_SEGWIT= ADDRESS_SEGWIT_DOGE
        
        for i, pubkey_hex in enumerate(PUBKEY):
            
            #pub_bytes= bytes.fromhex(pubkey_hex)
            pubkey_list= list(bytes.fromhex(pubkey_hex))
            addr= self.coin.pubtoaddr(bytes(pubkey_list))
            self.assertEqual(addr, ADDRESS[i])
            
            #PRIVKEY_WIF= PRIVKEY_WIF[i]
            privkey_hex= wif2priv(PRIVKEY_WIF[i])
            privkey_list= list(bytes.fromhex(privkey_hex))
            if self.coin.use_compressed_addr:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif_compressed')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
                #print(privkey_wif)
            else:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
            
            # segwit
            if self.coin.segwit_supported:
                addr_segwit= self.coin.pubtosegwit(bytes(pubkey_list))
                self.assertEqual(addr_segwit, ADDRESS_SEGWIT[i])
                #print(addr_segwit)
            
            #url
            url= self.coin.get_address_web_url(addr)
            print(f"URL= {url}")


### DASH ###

# using path m/0/*
PUBKEY_DASH=[
"037f38c987d3e7ca6534b87588bc26c8c77739316c6af2b01ca5879c8d292472c2",
"020649a9b59a1f986efed9320fe61f9b1ae217e35b37a71bfe166d695742987b6d",
"0384c82879d42884922dfd3a9a1875730a6f642360fee8d28adb9f60c340713b85",
"03c056e24e61951169616e6a8e019ff54849822d65b9d947361b6bf05203ad8d15",
"02a931823029e1e305880d8bdc17f2a413c7c7cdc9eefffc4ace0777ef9d944977",
]
ADDRESS_DASH=[
"XnXsuJyPqTjHyCUpaZwDkFCNgFtQ7FSbz8",
"XiexeryL1hYpLutU9PG4hBVrz52Ac1o8ja",
"XuBf1bKJT7m19hchm7ETBXj5UZCqQcPtTA",
"XnQrfaWFMvPvj7rTLit7p11DUUFJmCM7HX",
"XksHNRQbr5R9fo323StdrUZS4vrqXHKVGJ",
]
ADDRESS_SEGWIT_DASH=[]
PRIVKEY_WIF_DASH=[
"XG58D27hETExuQkXozuxFmWDz6fzhb5HacB1yfjkj97gQq48V75R",
"XE97N3BnkGSNvzgmPm38NV14ez1TUoNaG61i3LMrCcRXDBgmm73W",
"XGes4u4AtHFW6mzaLicNH1dtZyBAS9s52y3EszBqVCd1D3gB4E1W",
"XGhWneDTn2pez9D6oh2fURqBTHPsPxu2KjpMxw3Ba23JR94S3YWh",
"XGVadmrFvquEXJLYrKKP9ysvZzmGZhZ9fiZrmZxwpuxpXg83gVJu",
]

class DashCase(unittest.TestCase):
    
    coin = Dash(testnet=False)
    
    @classmethod
    def setUpClass(cls):
        print(f'Starting {cls.coin.display_name} test') 
        
        
    def test_address(self):
        
        self.assertEqual( self.coin.display_name, "Dash")
        self.assertEqual( self.coin.coin_symbol, "DASH")
        self.assertEqual( self.coin.segwit_supported, False)
        self.assertEqual( self.coin.use_compressed_addr, True)
        PUBKEY= PUBKEY_DASH
        ADDRESS= ADDRESS_DASH
        PRIVKEY_WIF= PRIVKEY_WIF_DASH
        ADDRESS_SEGWIT= ADDRESS_SEGWIT_DASH
        
        for i, pubkey_hex in enumerate(PUBKEY):
            
            #pub_bytes= bytes.fromhex(pubkey_hex)
            pubkey_list= list(bytes.fromhex(pubkey_hex))
            addr= self.coin.pubtoaddr(bytes(pubkey_list))
            self.assertEqual(addr, ADDRESS[i])
            
            #PRIVKEY_WIF= PRIVKEY_WIF[i]
            privkey_hex= wif2priv(PRIVKEY_WIF[i])
            privkey_list= list(bytes.fromhex(privkey_hex))
            if self.coin.use_compressed_addr:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif_compressed')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
                #print(privkey_wif)
            else:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
            
            # segwit
            if self.coin.segwit_supported:
                addr_segwit= self.coin.pubtosegwit(bytes(pubkey_list))
                self.assertEqual(addr_segwit, ADDRESS_SEGWIT[i])
                #print(addr_segwit)
            
            #url
            url= self.coin.get_address_web_url(addr)
            print(f"URL= {url}")

### Bitcoin Cash ###

# path: m/0/*
PUBKEY_BCH = [
"037f38c987d3e7ca6534b87588bc26c8c77739316c6af2b01ca5879c8d292472c2",
"020649a9b59a1f986efed9320fe61f9b1ae217e35b37a71bfe166d695742987b6d",
"0384c82879d42884922dfd3a9a1875730a6f642360fee8d28adb9f60c340713b85",
"03c056e24e61951169616e6a8e019ff54849822d65b9d947361b6bf05203ad8d15",
"02a931823029e1e305880d8bdc17f2a413c7c7cdc9eefffc4ace0777ef9d944977",
]
ADDRESS_BCH = [
"1Cr354KVskWhpFtEigcztiWaqvJi35Hrfn",
"18y7pcKS3zLEByHtHVwqqep59jSUduumMR",
"1KVpBLfQVQYQzm27uDvEL13HeDd9PWqzJ9",
"1Cj1qKrMQDBLaBFsUqZtxUKRe8fckR9hBk",
"1BBSYAkhtNCZWrSSBZaQzwseEbH9YYXjeL",
]
# TODO: move to cashaddress
ADDRESS_BCH_CASHADDR = [
"bitcoincash:qzq77lnqvtk8afrsjr2qqcha39lhm4wcmq5e75xsrg",
"bitcoincash:qptkth3meaxcwla5rgy4yxdqtck47ptt75k74y0y92",
"bitcoincash:qr9w2jeq3qnn8k2ty7h8vvaa54lfelcjys05gczr8n",
"bitcoincash:qzqfhr9dapn4qvgcufnulgu8lstk5zey2cdpepg8mg",
"bitcoincash:qph640pg8rtdcf4wfys3ngfacpd9r7kt6vgrkfj820",
]
ADDRESS_SEGWIT_BCH = []
PRIVKEY_WIF_BCH = [
"L21CkkjKvmcWr5k9nEv5kYKD55QRFnU3D2q7T9QZQmqb1fz9N3e4",
"Kz5BumoRSaovsfgPN13FsFp3jxjt2zmKtWfoWp2etF9Rp2adWVAP",
"L2awcdfoabd43SzCJxcVmnSsewuazMFpfPhLMTreAqLuotcNBfYG",
"L2dbLNq6UMCCvpCimw2nyCeAYG8HxAHmxAUTSQhzFemD1yzoaNiS",
"L2RfBWTtdAGnTyLApZKWekgueyVh7twuJ9DxF3dkWYgj8WxC4JsW",
]
ADDRESS_BCH_EXPLORER = [
    "1PUwPCNqKiC6La8wtbJEAhnBvtc8gdw19h", # top accounts
    "1P86nZCNWUiynP52AK2eTuTGZXYUTwX6qQ",
    "qrmfkegyf83zh5kauzwgygf82sdahd5a55x9wse7ve",
    "qre24q38ghy6k3pegpyvtxahu8q8hqmxmqqn28z85p",
]


class BitcoinCashCase(unittest.TestCase):
    
    coin = BitcoinCash(testnet=False)
    
    @classmethod
    def setUpClass(cls):
        print(f'Starting {cls.coin.display_name} test') 
        
    def test_address(self):
        
        self.assertEqual( self.coin.display_name, "Bitcoin Cash")
        self.assertEqual( self.coin.coin_symbol, "BCH")
        self.assertEqual( self.coin.segwit_supported, False)
        self.assertEqual( self.coin.use_compressed_addr, True)
        PUBKEY= PUBKEY_BCH
        ADDRESS= ADDRESS_BCH_CASHADDR #ADDRESS_BCH
        PRIVKEY_WIF= PRIVKEY_WIF_BCH
        ADDRESS_SEGWIT= ADDRESS_SEGWIT_BCH
        
        for i, pubkey_hex in enumerate(PUBKEY):
            
            #pub_bytes= bytes.fromhex(pubkey_hex)
            pubkey_list= list(bytes.fromhex(pubkey_hex))
            addr= self.coin.pubtoaddr(bytes(pubkey_list))
            self.assertEqual(addr, ADDRESS[i])
            
            #PRIVKEY_WIF= PRIVKEY_WIF[i]
            privkey_hex= wif2priv(PRIVKEY_WIF[i])
            privkey_list= list(bytes.fromhex(privkey_hex))
            if self.coin.use_compressed_addr:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif_compressed')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
                #print(privkey_wif)
            else:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
            
            # segwit
            if self.coin.segwit_supported:
                addr_segwit= self.coin.pubtosegwit(bytes(pubkey_list))
                self.assertEqual(addr_segwit, ADDRESS_SEGWIT[i])
                #print(addr_segwit)
            
            #url
            url= self.coin.get_address_web_url(addr)
            print(f"URL= {url}")

    def test_explorer(self):
        test_explorer(self.coin, ADDRESS_BCH_EXPLORER)


class EthereumCase(unittest.TestCase):
    """ Ethereum """

    PUBKEY_ETH = [
        "0x037f38c987d3e7ca6534b87588bc26c8c77739316c6af2b01ca5879c8d292472c2",
        "0x020649a9b59a1f986efed9320fe61f9b1ae217e35b37a71bfe166d695742987b6d",
        "0x0384c82879d42884922dfd3a9a1875730a6f642360fee8d28adb9f60c340713b85",
        "0x03c056e24e61951169616e6a8e019ff54849822d65b9d947361b6bf05203ad8d15",
        "0x02a931823029e1e305880d8bdc17f2a413c7c7cdc9eefffc4ace0777ef9d944977",
    ]
    ADDRESS_ETH = [
        "0x83da5A7e7E02E88237a6AF11598e8322a12CCda1",
        "0x3273BcF2b748Ea196663Ae900B7Cf5C3a5b9B912",
        "0xb62990a87649B658D0f49158ed68Ab8921442354",
        "0xe2A7152113cC018EC24F88C67fC8CE1C47B989a5",
        "0xc29bB40B3265Fa3c0925B38916D1C0C92e54E5A4",
    ]
    ADDRESS_SEGWIT_ETH = []
    PRIVKEY_ETH = [
        "0x8ec0b10753bb2c7c8462f3328afb86bb45f2c766f8c2e2bc4fd93b13ae4732ea",
        "0x5520cfb01a87374da0989fcbe4d7b5fe99f262bb93ce8adfff4273a6e62ff127",
        "0xa01bfb418815a1c8063caa9503b4b6e60897b4c5d1deefc2fd61fc6ac0d61c6a",
        "0xa179055a8bba685407579bf8a1465bb52323095a5dde5ce6a6ff00720afeea27",
        "0x9b55672fd34e5d0b597fe801910c23186e6f8b03443ddeb5b6a4652a089637ff",
    ]
    PRIVKEY_WIF_ETH = []  # not used in ETH?
    ADDRESS_ETH_EXPLORER = [  # testing block explorer
        "0xd5b06c8c83e78e92747d12a11fcd0b03002d48cf",
        "0x86b4d38e451c707e4914ffceab9479e3a8685f98",
        "0xE71a126D41d167Ce3CA048cCce3F61Fa83274535",  # cryptopunk
        "0xed1bf53Ea7fD8a290A3172B6c00F1Fb3657D538F",  # usdt
        "0x2c4ebd4b21736e992f3efeb55de37ae66457199d",  # grolex nft
    ]

    # Also work for ETC, BSC and other Ethereum forks
    coin = Ethereum(testnet= False)

    @classmethod
    def setUpClass(cls):
        print(f'Starting {cls.coin.display_name} test') 
        
    def test_address(self):
        
        self.assertEqual( self.coin.display_name, "Ethereum")
        self.assertEqual( self.coin.coin_symbol, "ETH")
        self.assertEqual( self.coin.use_compressed_addr, False)
        PUBKEY= self.PUBKEY_ETH
        ADDRESS= self.ADDRESS_ETH
        PRIVKEY_WIF= self.PRIVKEY_WIF_ETH
        PRIVKEY= self.PRIVKEY_ETH
        ADDRESS_SEGWIT= self.ADDRESS_SEGWIT_ETH
        from pycryptotools.main import decompress
        
        for i, pubkey_hex in enumerate(PUBKEY):
            
            # remove 0x
            pubkey_hex=pubkey_hex[2:]
            pubkey_hex= decompress(pubkey_hex)
            print(f"pubkey_decomp_hex: {pubkey_hex}")
            
            #pub_bytes= bytes.fromhex(pubkey_hex)
            pubkey_list= list(bytes.fromhex(pubkey_hex)) # should be uncompressed...
            addr= self.coin.pubtoaddr(bytes(pubkey_list))
            self.assertEqual(addr, ADDRESS[i].lower()) # todo: implement checksummed address: https://kb.myetherwallet.com/en/transactions/not-checksummed/
            print(addr)
            print(ADDRESS[i])
            
            # Ethereum does not seem to use WIF format
            privkey_hex= PRIVKEY[i]
            privkey_hex= privkey_hex[2:] # remove '0x'
            privkey_list= list(bytes.fromhex(privkey_hex))
            if self.coin.use_compressed_addr:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif_compressed')
                self.assertEqual(privkey_wif, PRIVKEY_WIF[i])
                #print(privkey_wif)
            else:
                privkey_wif= self.coin.encode_privkey(privkey_list, 'wif')
                privkey_dec= wif2priv(privkey_wif)
                self.assertEqual(privkey_hex, privkey_dec)
                #print(privkey_hex)
                #print(privkey_dec)
            
            # debug
            pubkey_hex2= self.coin.privtopub(privkey_hex)
            self.assertEqual(pubkey_hex, pubkey_hex2)
            
            #url
            url= self.coin.get_address_web_url(addr)
            print(f"URL= {url}")

    def test_explorer(self):
        test_explorer(self.coin, self.ADDRESS_ETH_EXPLORER)


class EthereumClassicCase(unittest.TestCase):
    """  Ethereum Classic  """

    ADDRESS_ETC_EXPLORER = [  # testing block explorer
        "0x13CDee29cAd8e11523095900e2195088Ed6d02Ad",  # top account (https://etc.blockscout.com/accounts)
        "0x00cd5Bf5bFB8fd1d139eF486ce35B8dfc00aDE91",  # top account
    ]
    # ALso work for ETC, BSC and other Ethereum forks
    coin = EthereumClassic(testnet=False)

    @classmethod
    def setUpClass(cls):
        print(f'Starting {cls.coin.display_name} test')

    def test_explorer(self):
        test_explorer(self.coin, self.ADDRESS_ETC_EXPLORER)


class PolygonCase(unittest.TestCase):
    """  Polygon  """

    ADDRESS_POL_EXPLORER = [  # testing block explorer
        "0x8db853Aa2f01AF401e10dd77657434536735aC62",
        "0x86d22A8219De3683CF188778CDAdEE62D1442033",
        "0xE976c3052Df18cc2Dc878b9bc3191Bba68Ef3d80",  # DolZ nft
        "0x440D4955a914D5e29F861aC024A608aE41c56cB6",  # PookyBall nft contract
        "0xd7f1cbca340c831d77c0d8d3dc843a07873ade44",  # PookyBall nft vault
        "0xF977814e90dA44bFA03b6295A0616a897441aceC",  # Binance hot wallet with USDT
    ]
    coin = Polygon(testnet=False)

    @classmethod
    def setUpClass(cls):
        print(f'Starting {cls.coin.display_name} test')

    def test_explorer(self):
        test_explorer(self.coin, self.ADDRESS_POL_EXPLORER)


if __name__ == '__main__':
    unittest.main()
