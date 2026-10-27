import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional
import requests
from decimal import Decimal, InvalidOperation

from pycryptotools.coins.base_coin import BaseCoin
from pycryptotools.explorers.price_explorer import PriceExplorer
from pycryptotools.explorers.explorer_exceptions import DataFetcherError

_logger = logging.getLogger(__name__)


@dataclass
class CachedExchangeRate:
    """Class to store cached exchange rate data"""
    exchange_rate: Decimal
    last_check: datetime


class Coingate(PriceExplorer):
    def __init__(self, coin: BaseCoin, api_keys: Dict[str, str]):
        """Initialize Coingate price explorer"""
        super().__init__(coin, api_keys)
        self.cached_exchange_rate_dict: Dict[str, CachedExchangeRate] = {}

    def get_api_url(self) -> str:
        """Get base API URL for Coingate"""
        return "https://api.coingate.com/v2/rates/merchant/"

    def get_exchange_rate_between(self,  coin: Optional[str] = None, other_coin: Optional[str] = None) -> Decimal:
        """
        Get exchange rate between two cryptocurrencies.

        Args:
            other_coin: The cryptocurrency to get exchange rate against
            coin: The base cryptocurrency (optional, uses instance coin_symbol if not provided)

        Returns:
            Decimal: Exchange rate between the cryptocurrencies

        Raises:
            DataFetcherError: If there's an error fetching or parsing the data
        """

        # Handle deprecated method signature
        if coin and not other_coin:
            # testnet coins are worthless
            if self.coin.is_testnet:
                return Decimal(0)
            # use self.coin versus provided coin
            return self._get_exchange_rate(self.coin.coin_symbol, coin)
        elif coin and other_coin:
            return self._get_exchange_rate(coin, other_coin)
        else:
            raise ValueError("Invalid parameters for get_exchange_rate_between")

    def _get_exchange_rate(self, coin: str, other_coin: str) -> Decimal:
        """Internal method to fetch exchange rate with caching"""
        _logger.debug("Coingate get exchange rate between %s and %s", coin, other_coin)

        # Return 1 if same coin
        if coin == other_coin:
            return Decimal(1.0)

        # Check cache
        cache_key = f"{coin}:{other_coin}"
        if cache_key in self.cached_exchange_rate_dict:
            cached_data = self.cached_exchange_rate_dict[cache_key]
            time_diff = datetime.now() - cached_data.last_check

            # Cache data is valid for 300 seconds
            if time_diff.total_seconds() < 300:
                _logger.debug("Using cached rate for %s (age %.0fs)", cache_key, time_diff.total_seconds())
                return Decimal(cached_data.exchange_rate)

        # Fetch new data
        url = f"{self.get_api_url()}{coin}/{other_coin}"
        _logger.debug("GET %s", url)

        try:
            response = requests.get(url, timeout=self.HTTP_TIMEOUT)
            if response.status_code != 200:
                raise DataFetcherError(DataFetcherError.INVALID_URL)

            # Get response text and convert to Decimal
            rate_str = response.text

            try:
                rate = Decimal(rate_str)
                _logger.debug("Coingate rate for %s: %s", cache_key, rate)

                # Cache the result
                self.cached_exchange_rate_dict[cache_key] = CachedExchangeRate(
                    exchange_rate=rate,
                    last_check=datetime.now()
                )

                return rate
            except (ValueError, InvalidOperation):
                raise DataFetcherError(DataFetcherError.MISSING_DATA)

        except requests.exceptions.RequestException:
            raise DataFetcherError(DataFetcherError.INVALID_URL)

    def get_price_web_url(self, coin: Optional[str] = None) -> str:
        """
        Get web URL for price information.

        Args:
            coin: Optional specific cryptocurrency to get price URL for

        Returns:
            str: Web URL for price information
        """
        return "https://coingate.com/exchange-rates"