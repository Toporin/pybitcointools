import requests
from .utils import parse_addr_args

# for supported projects, see https://docs.blockscout.com/for-projects/supported-projects
# https://blockscout.com/etc/mainnet/api-docs
# https://blockscout.com/etc/mordor/api-docs
# https://blockscout.com/xdai/mainnet/api-docs
# 

def get_url(coin_symbol):
    base_url= "https://blockscout.com/xdai/mainnet/api"
    
    if coin_symbol == "ETC":
        return "https://blockscout.com/etc/mainnet/api"
    elif coin_symbol == "ETCTEST":
        return "https://blockscout.com/etc/mordor/api"
    elif coin_symbol in ["xDAI", "xDAITESt"]:
        return "https://blockscout.com/xdai/mainnet/api"
    elif coin_symbol in ["RBTC", "RBTCTEST"]: # RSK
        return "https://blockscout.com/rsk/mainnet/api"
    elif coin_symbol =="POA":
        return "https://blockscout.com/poa/core/api"
    elif coin_symbol == "POATEST": 
        return "https://blockscout.com/poa/sokol/api"
    else:
        return "https://blockscout.com/etc/mainnet/api" #?
  
    # returns web link for browsing
    def address_weburl(addr, coin_symbol="ETC", apikeys={}):
        base_url= "https://blockscout.com/%s/%s/address/%s"
        if coin_symbol == "ETC":
            return base_url % (etc, mainnet, addr)
        elif coin_symbol == "ETCTEST":
            return base_url % (etc, mordor, addr)
        elif coin_symbol in ["xDAI", "xDAITESt"]:
            return base_url % (xdai, mainnet, addr)
        elif coin_symbol in ["RBTC", "RBTCTEST"]: # RSK
            return base_url % (rsk, mainnet, addr)
        elif coin_symbol =="POA":
            return base_url % (poa, core, addr)
        elif coin_symbol == "POATEST": 
            return base_url % (poa, sokol, addr)
        else:
            return base_url % (etc, mainnet, addr) # default?
      
def balance(addr, coin_symbol="ETC", apikeys={}):
    
    #apikey= apikeys.get('API_KEY_ETHERSCAN','0')    
    base_url = get_url(coin_symbol)
    url= base_url + "?module=account&action=balance&address=" + addr
    print(f"DEBUG BLOCKSCOUT {url}")
    response = requests.get(url)
    print(f"DEBUG BLOCKSCOUT {response}")
    
    if response.text == "[]":
        return []
    try:
        outputs = response.json()
        print("debug outputs type:"+str(type(outputs)))
        print("debug outputs :"+str(outputs))
        balance= outputs['result'] # in str format
        balance= int(balance) 
        balance= balance/(10**18) # wei to ether
        return balance
    except (ValueError, KeyError):
        raise Exception("Unable to decode JSON from result: %s" % response.text)

def balance_token(addr:str, contract:str, coin_symbol="ETH", apikeys={}):
    
    #apikey= apikeys.get('API_KEY_ETHERSCAN','0')    
    base_url = get_url(coin_symbol)
    url= base_url + "?module=account&action=tokenbalance&contractaddress=" + contract + "&address=" + addr
    print(f"DEBUG BLOCKSCOUT {url}")
    response = requests.get(url)
    print(f"DEBUG BLOCKSCOUT {response}")
    
    if response.text == "[]":
        return []
    try:
        outputs = response.json()
        print("debug outputs type:"+str(type(outputs)))
        print("debug outputs :"+str(outputs))
        balance= outputs['result'] # in str format
        balance= int(balance) 
        #balance= balance/(10**18) # most ERC20 use 18 decimals but etherscan does not offer reliable way to find out...
        return balance #{'value':balance}
    except (ValueError, KeyError):
        raise Exception("Unable to decode JSON from result: %s" % response.text)

def get_token_info(addr:str, contract:str, coin_symbol="ETC", apikeys={}):
    
    #apikey= apikeys.get('API_KEY_ETHPLORER','0')    
    base_url = "https://api.ethplorer.io"
    url=  base_url + "?module=token&action=getToken&contractaddress=" + contract
    
    response = requests.get(url)
    if response.text == "[]":
        return []
    try:
        token_info = response.json()
        print("debug outputs type:"+str(type(token_info)))
        print("debug outputs :"+str(token_info))
        return token_info
    except (ValueError, KeyError):
        raise Exception("get_token_info: unable to decode JSON from result: %s" % response.text)
        
## TODO ##
def fetchtx(txhash, coin_symbol="BTC"):    
        raise NotImplementedError

def tx_hash_from_index(index, coin_symbol="BTC"):
    raise NotImplementedError

def txinputs(txhash, coin_symbol="BTC"):
    raise NotImplementedError

def pushtx(tx, coin_symbol="BTC"):
    raise NotImplementedError

# Gets the transaction output history of a given set of addresses,
# including whether or not they have been spent
def history(*args, coin_symbol="BTC"):
    raise NotImplementedError

def block_height(txhash, coin_symbol="BTC"):
    raise NotImplementedError

def block_info(height, coin_symbol="BTC"):
    raise NotImplementedError

def current_block_height(coin_symbol="BTC"):
    raise NotImplementedError
