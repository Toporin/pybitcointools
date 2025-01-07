from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional
import requests
from decimal import Decimal

from pycryptotools.coins.base_coin import BaseCoin
from pycryptotools.explorers.price_explorer import PriceExplorer
from pycryptotools.explorers.explorer_exceptions import DataFetcherError


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
        print(f"Coingate getExchangeRateBetween: {coin} and {other_coin}")

        # Return 1 if same coin
        if coin == other_coin:
            return Decimal(1.0)

        # Check cache
        cache_key = f"{coin}:{other_coin}"
        if cache_key in self.cached_exchange_rate_dict:
            cached_data = self.cached_exchange_rate_dict[cache_key]
            time_diff = datetime.now() - cached_data.last_check
            print(f"timeInterval {time_diff.total_seconds()}")

            # Cache data is valid for 300 seconds
            if time_diff.total_seconds() < 300:
                print(f"fetch cached data for {cache_key}")
                return Decimal(cached_data.exchange_rate)

        # Fetch new data
        url = f"{self.get_api_url()}{coin}/{other_coin}"
        print(f"urlString: {url}")

        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise DataFetcherError(DataFetcherError.INVALID_URL)

            # Get response text and convert to Decimal
            rate_str = response.text
            print(f"Coingate getExchangeRateBetween data: {rate_str}")

            try:
                rate = Decimal(rate_str)
                print(f"Coingate getExchangeRateBetween rate: {rate}")

                # Cache the result
                print(f"save cached data for {cache_key}")
                self.cached_exchange_rate_dict[cache_key] = CachedExchangeRate(
                    exchange_rate=rate,
                    last_check=datetime.now()
                )

                return rate
            except ValueError:
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