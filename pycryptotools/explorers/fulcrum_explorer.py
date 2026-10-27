import json
import logging
import random
import socket
import ssl
from decimal import Decimal
from typing import Dict, List, Optional, Tuple

from pycryptotools.coins.base_coin import BaseCoin
from pycryptotools.coins.asset_type import AssetType
from pycryptotools.explorers.block_explorer import BlockExplorer
from pycryptotools.explorers.explorer_exceptions import DataFetcherError

_logger = logging.getLogger(__name__)


class FulcrumExplorer(BlockExplorer):
    """
    Bitcoin Cash explorer using public Electrum protocol servers (Fulcrum) over TLS.
    Balance is fetched with the blockchain.address.get_balance RPC.
    Servers are tried in random order until one answers.
    TLS certificates are verified, so servers with self-signed certificates are not listed.
    """

    SERVERS = {
        "BCH": [
            ("bch.imaginary.cash", 50002),
            ("electrum.imaginary.cash", 50002),
            ("cashnode.bch.ninja", 50002),
            ("bch.loping.net", 50002),
            ("blackie.c3-soft.com", 50002),
            ("bch.crypto.mldlabs.com", 50002),
            ("node.minisatoshi.cash", 50002),
        ],
        "BCHTEST": [  # chipnet
            ("chipnet.bch.ninja", 50002),
            ("chipnet.imaginary.cash", 50002),
            ("chipnet.c3-soft.com", 64002),
            ("cbch.loping.net", 62102),
        ],
    }
    CONNECT_TIMEOUT = 4  # seconds, per resolved address (see BaseExplorer.HTTP_TIMEOUT)
    TIMEOUT = 10  # seconds, per server, for the TLS handshake and RPC exchange

    def __init__(self, coin: BaseCoin, apikeys: Dict[str, str]):
        super().__init__(coin, apikeys)
        self.servers: List[Tuple[str, int]] = list(self.SERVERS.get(self.coin_symbol, []))

    """Utilities"""

    def get_address_web_url(self, addr: str) -> Optional[str]:
        """Get web link for an address"""
        if self.coin_symbol == "BCH":
            return f"https://blockchair.com/bitcoin-cash/address/{addr}"
        return None # unsupported

    def get_token_web_url(self, contract: str) -> str:
        """Get web link for a token"""
        return "(not supported)"

    def get_nft_web_url(self, contract: str, tokenid: str) -> str:
        """Get web link for a token"""
        return "(not supported)"

    @staticmethod
    def _ssl_context() -> ssl.SSLContext:
        # certifi (a requests dependency) provides CA certificates in frozen apps,
        # where the system store may not be available
        try:
            import certifi
            return ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            return ssl.create_default_context()

    def _rpc_call_server(self, host: str, port: int, method: str, params: list):
        """Open a TLS session with one server and send a single RPC after the version handshake"""
        context = self._ssl_context()
        with socket.create_connection((host, port), timeout=self.CONNECT_TIMEOUT) as raw_sock:
            raw_sock.settimeout(self.TIMEOUT)
            with context.wrap_socket(raw_sock, server_hostname=host) as sock:
                stream = sock.makefile('rwb')
                requests = [("server.version", ["pycryptotools", "1.4"]), (method, params)]
                result = None
                for request_id, (request_method, request_params) in enumerate(requests):
                    payload = {"jsonrpc": "2.0", "id": request_id, "method": request_method, "params": request_params}
                    stream.write((json.dumps(payload) + "\n").encode())
                    stream.flush()
                    while True:  # skip notifications, if any
                        line = stream.readline()
                        if not line:
                            raise ConnectionError("connection closed by server")
                        response = json.loads(line)
                        if response.get("id") == request_id:
                            break
                    if "error" in response:
                        raise ValueError(f"RPC error: {response['error']}")
                    result = response.get("result")
                return result

    def rpc_call(self, method: str, params: list):
        """Send an RPC to the first server that answers"""
        servers = list(self.servers)
        random.shuffle(servers)
        for host, port in servers:
            _logger.debug("Electrum RPC %s to %s:%s", method, host, port)
            try:
                return self._rpc_call_server(host, port, method, params)
            except (OSError, ValueError) as ex:  # includes socket, TLS and JSON errors
                _logger.warning("Failed to recover data from %s:%s: %s", host, port, ex)
        raise DataFetcherError(DataFetcherError.INVALID_URL)

    """API"""

    def get_coin_info(self, addr):
        """Get native coin info for an address"""
        _logger.debug("FulcrumExplorer get_coin_info for: %s", addr)

        result = self.rpc_call("blockchain.address.get_balance", [addr])
        coin_info = {}
        balance = Decimal(result['confirmed'])  # in satoshi
        coin_info['balance'] = balance / (10 ** 8)  # in BCH

        # get exchange rate from third party
        try:
            rate = self.coin.get_exchange_rate_with("USD")
            coin_info['exchange_rate'] = rate
            coin_info['currency'] = "USD"
        except Exception as ex:
            coin_info['error'] = str(ex)

        # basic info
        coin_info['symbol'] = self.coin_symbol
        coin_info['name'] = self.coin.display_name
        coin_info['type'] = AssetType.COIN
        coin_info['address_explorer_url'] = self.get_address_web_url(addr)
        _logger.debug("coin_info: %s", coin_info)
        return coin_info

    def get_asset_list(self, addr):
        """Get asset info for an address"""
        _logger.debug("FulcrumExplorer get_asset_list for: %s", addr)
        return []
