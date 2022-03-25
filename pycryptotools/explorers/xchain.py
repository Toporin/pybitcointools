import requests
from .utils import parse_addr_args

# api: https://xchain.io/api#intro

def get_url(coin_symbol="XCP"):
    if coin_symbol == "XCP":
        return "https://xchain.io/"
    elif coin_symbol== "XCPTEST":
        return "https://testnet.xchain.io/"
    elif coin_symbol== "XDP":
        return "https://dogeparty.xchain.io/"
    elif coin_symbol== "XDPTEST":
        return "https://dogeparty-testnet.xchain.io/"
    else:  
        return "https://notfound.org/"

def address_weburl(addr, coin_symbol="XCP", apikeys={}):
    base_url = get_url(coin_symbol)
    return base_url + "address/" + addr

def get_nft_owner_weburl(addr:str, coin_symbol:str="XCP", apikeys={}):
    base_url = get_url(coin_symbol)
    return base_url + "address/" + addr
    
def get_nft_weburl(contract:str, tokenid:str, coin_symbol:str="XCP", apikeys={}):
    base_url = get_url(coin_symbol)
    return base_url + "asset/" + contract

def balance(addr, coin_symbol="XCP", apikeys={}):
    
    base_url = get_url(coin_symbol)
    url = base_url + "api/address/"+  addr #address_url % (base_url, addr)
    print(f"DEBUG xchain.io {url}")
    response = requests.get(url)
    
    if response.text == "[]":
        return -1
    try:
        res = response.json()
        balance= res['xcp_balance']
        return float(balance)
        
    except Exception as ex:
        print(f"EXCEPTION xchain.io balance exception: {ex}")
        return -1
  

def balance_token(addr:str, contract:str, coin_symbol="XCP", apikeys={}):
    
    base_url = get_url(coin_symbol)
    url= base_url + "api/balances/"+  addr
    print(f"DEBUG xchain.io url: {url}")
    response = requests.get(url)
    print(f"DEBUG xchain.io response: {response.text}")
    
    balance=0;
    try:
        res = response.json()
        data_array= res["data"]
        for item in data_array: 
            print("DEBUG xchain.io item: "+str(item))
            asset= item["asset"]
            if asset==contract:
                balance= item["quantity"]
                return float(balance)
        return balance

    except Exception as ex:
        print(f"EXCEPTION xchain.io balance_token exception: {ex}")
        return -1

def get_token_info(addr:str, contract:str, coin_symbol="XCP", apikeys={}):
    
    print(f"DEBUG xchain.io get_token_info() addr: {addr}")
    print(f"DEBUG xchain.io get_token_info() contract: {contract}")
    base_url = get_url(coin_symbol)
    print(f"DEBUG xchain.io get_token_info() base_url: {base_url}")
    url= base_url + "api/balances/"+  addr
    print(f"DEBUG xchain.io url: {url}")
    response = requests.get(url)
    print(f"DEBUG xchain.io response: {response.text}")
    
    token_info={}
    token_info["decimals"]=0
    token_info["symbol"]="not found"
    token_info["name"]=contract
    try:
        res = response.json()
        data_array= res["data"]
        for item in data_array: 
            print("DEBUG xchain.io item: "+str(item))
            asset= item["asset"]
            if asset==contract:
                token_info["symbol"]=item.get("long_name", item.get("name", contract)) 
                token_info["name"]=contract
                return token_info
        return token_info

    except Exception as ex:
        print(f"EXCEPTION xchain.io get_token_info exception: {ex}")
        return token_info
    
def get_nft_info(contract:str, tokenid:str, coin_symbol:str="XCP", apikeys={}):
    
    # token_id is not used 
    
    base_url = get_url(coin_symbol)
    url= base_url + "api/asset/"+  contract
    print(f"DEBUG xchain.io url: {url}")
    response = requests.get(url)
    print(f"DEBUG xchain.io response: {response.text}")
    
    nft_info={}
    nft_info["nft_name"]=""
    nft_info["nft_description"]=""
    nft_info["nft_image_url"]=""
    nft_info["nft_image_large_url"]=""
    nft_info["nft_explorer_link"]=""
    
    try:
        res = response.json()
        nft_info["nft_name"]= contract
        nft_info["asset_id"]= res.get("asset_id", 0)
        nft_info["asset_longname"]= res.get("asset_longname", "")
        nft_info["divisible"]= str(res.get("divisible", "(unknonw)"))
        nft_info["locked"]= str(res.get("locked",  "(unknonw)"))
        nft_info["supply"]= str(res.get("supply",  "(unknonw)"))
        nft_info["description"]= res.get("description", "")
        
        details= ("Divisible: " + nft_info["divisible"] + "\n" 
                            "Locked: " + nft_info["locked"] + "\n"
                                "Supply: " + nft_info["supply"] + "\n")
        nft_info["nft_description"]=details
        
        description= nft_info["description"]
        if description!="":
            # description can be a link or a shortcut
            # imgur/6rF0Dar.jpg; FAKEAPEPOKER => https://i.imgur.com/6rF0Dar.jpg
            # https://i.imgur.com/aPzAR0i.jpg;KARNADI
            # https://easyasset.art/j/omhf84/MARSJUWANNA.json
            try:          
                if description.startswith("*"): # some starts with *
                    description= description[len("*"):] #.removeprefix("*") requires python 3.9
                    
                if description.startswith("imgur/"):
                    blob= description[len("imgur/"):] #.removeprefix("*") requires python 3.9
                    blobsplit= blob.split(";")
                    part= blobsplit[0]
                    imlink= "https://i.imgur.com/" + part
                    nft_info["nft_image_url"]=imlink
                    nft_info["nft_image_large_url"]= imlink
                    nft_info["nft_description"]+=description
                
                elif description.startswith("https://") or description.startswith("http://"):
                    if (description.endswith(".png")
                           or description.endswith(".jpg") 
                           or description.endswith(".jpeg")
                           or description.endswith(".gif") ):
                        # blobsplit= description.split(";")
                        # imlink= blobsplit[0]
                        nft_info["nft_image_url"]=description
                        nft_info["nft_image_large_url"]= description
                        nft_info["nft_description"]+=description
                        
                    elif description.endswith(".json"):
                        json_link= description
                        print(f"DEBUG xchain.io json_link: {json_link}")
                        response2 = requests.get(json_link)
                        print(f"DEBUG xchain.io json_link response: {response2}")
                        res2 = response2.json()
                        nft_info["nft_description"]+=description
                        nft_info["nft_image_url"]=res2.get("image","")
                        nft_info["nft_image_large_url"]=res2.get("image_large","")
                        
                    else:
                        nft_info["nft_description"]+= description
                    
            except Exception as ex:
                print(f"EXCEPTION xchain.io get_nft_info json_link exception: {ex}")
        
        return nft_info
        
    except Exception as ex:
        print(f"EXCEPTION xchain.io get_nft_info exception: {ex}")
        return nft_info
    
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
