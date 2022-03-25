import requests
from .utils import parse_addr_args
  
utxo_url = "%s/address/%s/utxo"
address_url = "%s/address/%s"

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

def get_api_url(coin_symbol:str="ETH"):
    if coin_symbol == "ETH":
        return "https://api.opensea.io/api/v1/" # main
    return "https://rinkeby-api.opensea.io/api/v1/" # Rinkeby
    
def address_weburl(addr:str, coin_symbol:str="ETH", apikeys={}):
    web_url="https://opensea.io/" + addr
    return web_url;
    
def get_nft_owner_weburl(addr:str, coin_symbol:str="ETH", apikeys={}):
    return address_weburl(addr, coin_symbol, apikeys)

def get_nft_weburl(contract:str, tokenID:str, apikeys={}):
    web_url="https://opensea.io/assets/" + contract  + "/" + tokenID
    return web_url;

def get_nft_info(contract:str, tokenID:str, apikeys={}):
    
    nftInfoMap={}
    nftInfoMap["nft_name"]=""
    nftInfoMap["nft_description"]=""
    nftInfoMap["nft_image_url"]=""
    nftInfoMap["nft_explorer_link"]=""
    
    try:
        apikey= apikeys.get('API_KEY_OPENSEA','0')   
        headers['X-API-KEY']= apikey 
        
        base_url = get_api_url()
        url= base_url + "asset/"+contract+"/" + tokenID
        
        print(f"DEBUG OPENSEA URL: {url}")
        response = requests.get(url, headers=headers) # requests.get(url, headers=headers)
        print(f"DEBUG OPENSEA RESPONSE: {response}")
        
        # parse json
        data = response.json()
        
        name = data.get("name", "")
        nftInfoMap["nft_name"]= name
        
        description = data.get("description", "")
        nftInfoMap["nft_description"]= description
        
        image_url= data.get("image_preview_url", "")
        nftInfoMap["nft_image_url"]=image_url
        
        nftInfoMap["nft_explorer_link"]=get_nft_weburl(contract, tokenID)
        
    except Exception as ex:
        print(f"DEBUG OPENSEA Exception in get_nft_info: {ex}")
        
    return nftInfoMap
    
    


