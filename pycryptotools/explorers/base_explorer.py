from typing import Dict

from pycryptotools.coins.base_coin import BaseCoin


class BaseExplorer(object):

    coin_symbol = ""
    apikeys = {}
    # (connect, read) timeouts in seconds for HTTP requests. The connect timeout applies to each
    # address the host resolves to: kept short so that an unreachable address (e.g. IPv6 advertised
    # by DNS but not routed by the local network) does not stall the request before IPv4 is tried.
    HTTP_TIMEOUT = (4, 20)

    def __init__(self, coin: BaseCoin, apikeys: Dict[str, str]):
        self.coin = coin
        self.coin_symbol = coin.coin_symbol
        self.apikeys = apikeys