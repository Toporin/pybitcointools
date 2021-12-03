import requests
from .utils import parse_addr_args

def get_url(coin_symbol):
    if coin_symbol == "BSC":
        return "https://api.bscscan.com/api"
    return "https://api-testnet.bscscan.com/api"
  
def address_weburl(addr, coin_symbol="BSC", apikeys={}):
    if coin_symbol == "BSC":
        return "https://bscscan.com/address/"+addr 
    return "https://testnet.bscscan.com/address/"+addr

def balance(addr, coin_symbol="BSC", apikeys={}):
    '''
    https://api.bscscan.com/api
        ?module=account
        &action=balance
        &address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
        &tag=latest
        &apikey=YourApiKeyToken
   '''
    
    apikey= apikeys.get('API_KEY_BSCSCAN','0')    
    base_url = get_url(coin_symbol)
    url= base_url + "?module=account&action=balance&address=" + addr + "&tag=latest&apikey=" + apikey
    print(f"DEBUG BSCSCAN {url}")
    response = requests.get(url)
    print(f"DEBUG BSCSCAN {response}")
    
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
    '''
    https://api.bscscan.com/api
       ?module=account
       &action=tokenbalance
       &contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055
       &address=0xe04f27eb70e025b78871a2ad7eabe85e61212761
       &tag=latest&apikey=YourApiKeyToken
   '''
    
    apikey= apikeys.get('API_KEY_BSCSCAN','0')    
    base_url = get_url(coin_symbol)
    print(f"DEBUG BSCSCAN B {base_url}")
    url= base_url + "?module=account&action=tokenbalance&contractaddress="+contract+"&address=" + addr + "&tag=latest&apikey=" + apikey
    print(f"DEBUG BSCSCAN {url}")
    response = requests.get(url)
    print(f"DEBUG BSCSCAN {response}")
    
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

def get_token_info(addr:str, contract:str, coin_symbol="ETH", apikeys={}):
    #TODO: find api!
    return {'decimals':"18", "name":"Unsupported", "symbol":"???"}
    # apikey= apikeys.get('API_KEY_ETHPLORER','0')    
    # base_url = "https://api.ethplorer.io"
    # url=  base_url + "/getTokenInfo/" + contract + "?apiKey=" + apikey
    
    # response = requests.get(url)
    # if response.text == "[]":
        # return []
    # try:
        # token_info = response.json()
        # print("debug outputs type:"+str(type(token_info)))
        # print("debug outputs :"+str(token_info))
        # return token_info
    # except (ValueError, KeyError):
        # raise Exception("get_token_info: unable to decode JSON from result: %s" % response.text)
        
        
        
        

####
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
