import requests
from .utils import parse_addr_args

def get_url(coin_symbol):
    if coin_symbol == "ETH":
        return "https://api.etherscan.io/api"
    return "https://api-ropsten.etherscan.io/api"
  
utxo_url = "%s/address/%s/utxo"
address_url = "%s/address/%s"

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

def address_weburl(addr, coin_symbol="ETH", apikeys={}):
    if coin_symbol == "ETH":
        return "https://etherscan.io/address/"+addr 
    return "https://ropsten.etherscan.io/address/"+addr

def balance(addr, coin_symbol="ETH", apikeys={}):
    '''
    https://api.etherscan.io/api
        ?module=account
        &action=balance
        &address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
        &tag=latest
        &apikey=YourApiKeyToken
   '''
    
    apikey= apikeys.get('API_KEY_ETHERSCAN','0')    
    base_url = get_url(coin_symbol)
    url= base_url + "?module=account&action=balance&address=" + addr + "&tag=latest&apikey=" + apikey
    print(f"DEBUG ETHERSCAN {url}")
    response = requests.get(url, headers=headers)
    print(f"DEBUG ETHERSCAN {response}")
    
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
    https://api.etherscan.io/api
       ?module=account
       &action=tokenbalance
       &contractaddress=0x57d90b64a1a57749b0f932f1a3395792e12e7055
       &address=0xe04f27eb70e025b78871a2ad7eabe85e61212761
       &tag=latest&apikey=YourApiKeyToken
   '''
    # addrs = parse_addr_args(*args)
    # if len(addrs) == 0:
        # return []
    # if len(addrs)>1: #only one address per request...
        # addrs= [addrs[0]]
    
    apikey= apikeys.get('API_KEY_ETHERSCAN','0')    
    base_url = get_url(coin_symbol)
    print(f"DEBUG ETHERSCAN B {base_url}")
    #url = utxo_url % (base_url, '|'.join(addrs))
    url= base_url + "?module=account&action=tokenbalance&contractaddress="+contract+"&address=" + addr + "&tag=latest&apikey=" + apikey
    print(f"DEBUG ETHERSCAN {url}")
    response = requests.get(url, headers=headers)
    print(f"DEBUG ETHERSCAN {response}")
    
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
    
    apikey= apikeys.get('API_KEY_ETHPLORER','0')    
    base_url = "https://api.ethplorer.io"
    url=  base_url + "/getTokenInfo/" + contract + "?apiKey=" + apikey
    
    response = requests.get(url, headers=headers)
    if response.text == "[]":
        return []
    try:
        token_info = response.json()
        print("debug outputs type:"+str(type(token_info)))
        print("debug outputs :"+str(token_info))
        return token_info
    except (ValueError, KeyError):
        raise Exception("get_token_info: unable to decode JSON from result: %s" % response.text)
        
        
        
        

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
