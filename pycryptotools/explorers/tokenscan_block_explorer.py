from typing import Dict, List, Optional, Tuple, Union, Any
from decimal import Decimal
import requests

from pycryptotools.coins.base_coin import BaseCoin
from pycryptotools.coins.asset_type import AssetType
from pycryptotools.explorers.block_explorer import BlockExplorer
from pycryptotools.explorers.explorer_exceptions import DataFetcherError


class TokenscanExplorer(BlockExplorer):

        def __init__(self, coin: BaseCoin, apikeys: Dict[str, str]):
            super().__init__(coin, apikeys)

        def get_url(self) -> str:
            """Get base URL based on coin symbol"""
            urls = {
                "XCP": "https://tokenscan.io/",
                "XCPTEST": "https://testnet.tokenscan.io/",
                "XDP": "https://dogeparty.tokenscan.io/",
                "XDPTEST": "https://dogeparty-testnet.tokenscan.io/"
            }
            return urls.get(self.coin_symbol, "https://notfound.org/")

        def get_address_web_url(self, addr: str) -> str:
            """Get web link for an address"""
            return f"{self.get_url()}address/{addr}"

        def get_token_web_url(self, contract: str) -> str:
            """Get web link for a token"""
            return f"{self.get_url()}asset/{contract}"

        def get_coin_info(self, addr):
            """Get native coin info for an address"""
            print(f"In TokenscanExplorer get_coin_info for: {addr}")

            url = f"{self.get_url()}api/address/{addr}"
            print(f"urlString: {url}")

            response = requests.get(url)
            if response.status_code != 200:
                raise DataFetcherError(DataFetcherError.INVALID_URL)

            data = response.json()

            coin_info = {}
            coin_info['balance'] = Decimal(data.get('xcp_balance'))
            rates = data.get('estimated_value', {})  # this is the estimated value of all assets held!
            try:
                coin_info['exchange_rate'] = Decimal(rates.get('usd'))/Decimal(rates.get('xcp'))
                coin_info['currency'] = "USD"
            except Exception as ex:
                print(f"Exception in tokenscanExplorer get exchange rate: {ex}")
            print(f"DEBUG TokenscanExplorer type(rates): {type(rates)}")
            print(f"DEBUG TokenscanExplorer rates: {rates}")
            print(f"DEBUG TokenscanExplorer type(coin_info['exchange_rate)']: {type(coin_info.get('exchange_rate'))}")
            print(f"DEBUG TokenscanExplorer coin_info['exchange_rate']: {coin_info.get('exchange_rate')}")
            print(f"DEBUG TokenscanExplorer type(coin_info['currency']): {type(coin_info.get('currency'))}")
            print(f"DEBUG TokenscanExplorer coin_info['currency']: {coin_info.get('currency')}")
            print(f"DEBUG TokenscanExplorer coin_info: {coin_info}")

            # add more info
            coin_info['symbol'] = self.coin_symbol
            coin_info['name'] = self.coin.display_name
            coin_info['type'] = AssetType.COIN
            coin_info['address_explorer_url'] = self.get_address_web_url(addr)
            print(f"coin_info: {coin_info}")
            return coin_info

        def get_asset_list(self, addr):
            """Get simple asset list for an address"""
            print(f"in TokenscanExplorer get_asset_list - addr: {addr}")

            url = f"{self.get_url()}api/balances/{addr}"
            print(f"urlString: {url}")

            response = requests.get(url)
            if response.status_code != 200:
                raise DataFetcherError(DataFetcherError.INVALID_URL)

            asset_list = []
            data = response.json()
            items = data.get('data', [])
            print(f"asset_list size: {len(items)}")
            for item in items:
                try:
                    print(f"DEBUG asset: {item}")
                    asset = {}
                    asset['name'] = item.get('asset', "")
                    asset['symbol'] = item.get('symbol', "")
                    asset['description'] = item.get('description', "")
                    asset['balance'] = Decimal(item.get('quantity', ""))
                    # exchange rate
                    try:
                        rates = item.get('estimated_value', {})
                        asset['exchange_rate'] = Decimal(rates.get('usd'))
                        asset['currency'] = "USD"
                    except Exception as ex:
                        print(f"Exception in tokenscanExplorer get exchange rate: {ex}")

                    # get nft info if any from description
                    description = item.get("description", "")
                    if description:
                        # description can be a link or a shortcut
                        # imgur/6rF0Dar.jpg; FAKEAPEPOKER => https://i.imgur.com/6rF0Dar.jpg
                        # https://i.imgur.com/aPzAR0i.jpg;KARNADI
                        # https://easyasset.art/j/omhf84/MARSJUWANNA.json
                        try:
                            if description.startswith("*"):  # some starts with *
                                description = description[len("*"):]  # .removeprefix("*") requires python 3.9

                            if description.startswith("imgur/"):
                                blob = description[len("imgur/"):]  # .removeprefix("*") requires python 3.9
                                blobsplit = blob.split(";")
                                part = blobsplit[0]
                                imlink = "https://i.imgur.com/" + part
                                asset["nft_image_url"] = imlink

                            elif description.startswith("https://") or description.startswith("http://"):
                                if (description.endswith(".png")
                                        or description.endswith(".jpg")
                                        or description.endswith(".jpeg")
                                        or description.endswith(".gif")):
                                    asset["nft_image_url"] = description

                                elif description.endswith(".json"):
                                    json_link = description
                                    print(f"DEBUG tokenscan.io json_link: {json_link}")
                                    response2 = requests.get(json_link)
                                    print(f"DEBUG tokenscan.io json_link response: {response2}")
                                    res2 = response2.json()
                                    asset["nft_image_url"] = res2.get("image_large", res2.get("image", ""))
                                    #asset["nft_image_large_url"] = res2.get("image_large", res2.get("image", ""))

                                else:
                                    asset["nft_description"] += description

                        except Exception as ex:
                            print(f"EXCEPTION tokenscan.io get_nft_info json_link exception: {ex}")

                    if asset.get('nft_image_url',""):
                        asset["type"] = AssetType.NFT
                        asset["nft_explorer_url"] = self.get_token_web_url(asset['name'])
                    else:
                        asset["type"] = AssetType.TOKEN
                        asset["token_explorer_url"] = self.get_token_web_url(asset['name'])

                    asset["address_explorer_url"] = self.get_address_web_url(addr)

                    # add to list
                    asset_list += [asset]
                except Exception as ex:
                    print(f"Exception in TokenscanExplorer get_asset_list - failed to parse 1 asset: {str(ex)}")

            return asset_list

        # async def get_balance(self, addr: str) -> float:
        #     """Get balance for an address"""
        #     print(f"In TokenscanExplorer getBalance for: {addr}")
        #
        #     url = f"{self.get_url()}api/address/{addr}"
        #     print(f"urlString: {url}")
        #
        #     async with aiohttp.ClientSession() as session:
        #         async with session.get(url) as response:
        #             if response.status != 200:
        #                 raise DataFetcherError(DataFetcherError.INVALID_URL)
        #
        #             data = await response.json()
        #             result = JsonResponseBalance(**data)
        #             print(f"result: {result}")
        #
        #             return float(result.xcp_balance)
        #
        #
        #
        # async def get_simple_asset_list(self, addr: str) -> List[Dict[str, str]]:
        #     """Get simple asset list for an address"""
        #     print(f"in TokenscanExplorer getSimpleAssetList - addr: {addr}")
        #
        #     url = f"{self.get_url()}api/balances/{addr}"
        #
        #     async with aiohttp.ClientSession() as session:
        #         async with session.get(url) as response:
        #             if response.status != 200:
        #                 raise DataFetcherError(DataFetcherError.INVALID_URL)
        #
        #             data = await response.json()
        #             result = JsonResponseTokenBalance(**data)
        #             print(f"result: {result}")
        #
        #             asset_list: List[Dict[str, str]] = []
        #
        #             for item in result.data:
        #                 if item.asset == "XCP":
        #                     continue
        #
        #                 asset_data: Dict[str, str] = {
        #                     "balance": item.quantity,
        #                     "decimals": "0",
        #                     "contract": item.asset,
        #                     "name": item.asset,
        #                     "type": "token",
        #                     "tokenExplorerLink": self.get_token_web_url(item.asset)
        #                 }
        #
        #                 # Exchange rate calculation
        #                 usd_value = item.estimated_value.usd
        #                 try:
        #                     usd_value_float = float(usd_value)
        #                     quantity_float = float(item.quantity)
        #
        #                     if quantity_float != 0:
        #                         exchange_rate = usd_value_float / quantity_float
        #                         asset_data["tokenExchangeRate"] = str(exchange_rate)
        #                         asset_data["currencyForExchangeRate"] = "USD"
        #                 except (ValueError, ZeroDivisionError):
        #                     pass
        #
        #                 asset_list.append(asset_data)
        #
        #             print(f"assetList: {asset_list}")
        #             return asset_list
        #
        # async def get_token_balance(self, addr: str, contract: str) -> float:
        #     """Get balance for a specific token at an address"""
        #     print(f"in TokenscanExplorer getTokenBalance - addr: {addr}")
        #
        #     url = f"{self.get_url()}api/balances/{addr}"
        #
        #     async with aiohttp.ClientSession() as session:
        #         async with session.get(url) as response:
        #             if response.status != 200:
        #                 raise DataFetcherError(DataFetcherError.INVALID_URL)
        #
        #             data = await response.json()
        #             result = JsonResponseTokenBalance(**data)
        #             print(f"result: {result}")
        #
        #             balance_string = next(
        #                 (item.quantity for item in result.data if item.asset == contract),
        #                 "0"
        #             )
        #
        #             try:
        #                 balance_float = float(balance_string)
        #                 print(f"balanceDouble: {balance_float}")
        #                 return balance_float
        #             except ValueError:
        #                 raise DataFetcherError(DataFetcherError.MISSING_DATA)
        #
        # async def get_token_info(self, contract: str) -> Dict[str, str]:
        #     """Get token information"""
        #     print(f"in TokenscanExplorer getTokenInfo - contract: {contract}")
        #
        #     return {
        #         "name": contract,
        #         "symbol": "",
        #         "decimals": "0"
        #     }