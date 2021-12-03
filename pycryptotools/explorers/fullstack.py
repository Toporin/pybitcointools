import re
import requests

#Docs: https://api.fullstack.cash/docs/
# see also https://api.fullstack.cash/ & https://tapi.fullstack.cash/

def get_url(coin_symbol):
    if coin_symbol == "BCH":
        return "https://api.fullstack.cash/v5"
    return "https://tapi.fullstack.cash/v5"

balance_url= "%s/electrumx/balance/%s"
utxo_url= "%s/electrumx/utxos/%s"

def address_weburl(addr, coin_symbol="BCH", apikeys={}):
    # address in cashaddress format such as bchtest:qps822p04zpg676v6krnwhjhtqx44klcvqjrg353rc
    if coin_symbol=="BCH":
        web_url= "https://www.blockchain.com/bch/address/%s" % (addr)
    else:
        web_url= "https://www.blockchain.com/bch-testnet/address/%s" % (addr)
    return web_url

def balance(addr, coin_symbol="BCH", apikeys={}):
    #https://api.fullstack.cash/v5/electrumx/balance/{addr}
    
    base_url= get_url(coin_symbol)
    url = balance_url % (base_url, addr)
    response = requests.get(url)
    try:
        result = response.json()
        print(f"DEBUG FULLSTACK {result}")
        is_success= result['success']
        if is_success:
            balance= result['balance']['confirmed']# in satoshi
            balance= balance/(10**8) # in BCH
            return balance
        else:
            raise 
    except ValueError:
        raise Exception("Unable to decode JSON from result: %s" % response.text)

def unspent(addr, coin_symbol="BCH", apikeys={}):
    # https://api.fullstack.cash/v5/electrumx/utxos/bitcoincash:qr69kyzha07dcecrsvjwsj4s6slnlq4r8c30lxnur3
    
    base_url= get_url(coin_symbol)
    url = utxo_url % (base_url, addr)
    response = requests.get(url)
    try:
        result = response.json()
        print(f"DEBUG FULLSTACK {result}")
        is_success= result['success']
        if is_success:
            outputs= result['utxos']
            for i, o in enumerate(outputs):
                outputs[i] = {
                        "output": o['tx_hash']+':'+str(o['tx_pos']),
                        "value": o['value']
                    }
            return outputs
        else:
            raise 
    except ValueError:
        raise Exception("Unable to decode JSON from result: %s" % response.text)
