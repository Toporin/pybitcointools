import requests
from .utils import parse_addr_args

def get_url(coin_symbol):
    if coin_symbol == "BTC":
        return "https://blockstream.info/api"
    return "https://blockstream.info/testnet/api"
  
utxo_url = "%s/address/%s/utxo"
address_url = "%s/address/%s"

def address_weburl(addr, coin_symbol="BTC", apikeys={}):
    if coin_symbol == "BTC":
        return "https://blockstream.info/address/"+addr
    return "https://blockstream.info/testnet/address/"+addr

def balance(addr, coin_symbol="BTC", apikeys={}):
    
    base_url = get_url(coin_symbol)
    url = address_url % (base_url, addr)
    print(f"DEBUG blockstream {url}")
    response = requests.get(url)
    
    if response.text == "[]":
        return []
    try:
        res = response.json()
        funded_txo_sum= res['chain_stats']['funded_txo_sum']
        print(f"DEBUG blockstream funded_txo_sum {funded_txo_sum}")
        spent_txo_sum= res['chain_stats']['spent_txo_sum']
        print(f"DEBUG blockstream spent_txo_sum {spent_txo_sum}")
        balance= (funded_txo_sum - spent_txo_sum)/(10**8)
        print(f"DEBUG blockstream balance {balance}")
        return balance
        
    except (ValueError, KeyError):
        raise Exception("Unable to decode JSON from result: %s" % response.text)
  
def unspent(*args, coin_symbol="BTC"):

    addrs = parse_addr_args(*args)
    if len(addrs) == 0:
        return []
    if len(addrs)>1:
        addrs= [addrs[0]]
    
    base_url = get_url(coin_symbol)
    url = utxo_url % (base_url, '|'.join(addrs))
    print(f"DEBUG blockstream {url}")
    response = requests.get(url)
    
    if response.text == "[]":
        return []
    try:
        outputs = response.json()
        #print("debug outputs type:"+str(type(outputs)))
        for i, o in enumerate(outputs):
            outputs[i] = {
                        "output": o['txid']+':'+str(o['vout']),
                        "value": o['value']
                    }
            #print(f"debug outputs[{i}] = {outputs[i]}")
        return outputs
    except (ValueError, KeyError):
        raise Exception("Unable to decode JSON from result: %s" % response.text)

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
