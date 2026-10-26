import logging
import requests

# TODO refactor into a BlockExplorer class (or remove)

_logger = logging.getLogger(__name__)

utxo_url = "%s/address/%s/utxo"
address_url = "%s/address/%s"

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

def get_api_url(coin_symbol:str="ETH"):
    if coin_symbol == "ETH":
        return "https://ethereum-api.rarible.org/v0.1/" # main
    return "https://ethereum-api-dev.rarible.org/v0.1/" # Ropsten
    
def get_nft_owner_weburl(addr:str, coin_symbol:str="ETH", apikeys={}):
    web_url="https://example.com"
    return web_url

def get_nft_weburl(contract:str, tokenID:str, apikeys={}):
    web_url="https://rarible.com/token/" + contract  + ":" + tokenID
    return web_url

def get_nft_info(contract:str, tokenID:str, apikeys={}):
    
    nftInfoMap={}
    nftInfoMap["nft_name"]=""
    nftInfoMap["nft_description"]=""
    nftInfoMap["nft_image_url"]=""
    nftInfoMap["nft_explorer_link"]=""
    
    try:
        
        base_url = get_api_url()
        url= base_url + "nft/items/"+contract+":" + tokenID + "/meta"
        _logger.debug("GET %s", url)
        response = requests.get(url) # requests.get(url, headers=headers)
        
        # parse json
        data = response.json()
        
        name = data.get("name", "")
        nftInfoMap["nft_name"]= name
        
        description = data.get("description", "")
        nftInfoMap["nft_description"]= description
        
        image_dic= data.get("image", {})
        image_url= image_dic.get("url", {}).get("PREVIEW", "")
        nftInfoMap["nft_image_url"]=image_url
        
        nftInfoMap["nft_explorer_link"]=get_nft_weburl(contract, tokenID)
            
    except Exception as ex:
        _logger.warning("Failed to get NFT info from Rarible: %s", ex)
        
    return nftInfoMap
    
    


