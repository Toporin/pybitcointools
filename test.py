import random
import unittest

import pycryptotools.ripemd as ripemd
from pycryptotools import *
from pycryptotools.coins import *


class TestBases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Starting base change tests')

    def test_all(self):
        data = [
            [10, '65535', 16, 'ffff'],
            [16, 'deadbeef', 10, '3735928559'],
            [10, '0', 16, ''],
            [256, b'34567', 10, '219919234615'],
            [10, '444', 16, '1bc'],
            [256, b'\x03\x04\x05\x06\x07', 10, '12952339975'],
            [16, '3132333435', 256, b'12345']
        ]
        for prebase, preval, postbase, postval in data:
            self.assertEqual(changebase(preval, prebase, postbase), postval)

        for i in range(100):
            x = random.randrange(1, 9999999999999999)
            frm = random.choice([2, 10, 16, 58, 256])
            to = random.choice([2, 10, 16, 58, 256])
            self.assertEqual(decode(encode(x, to), to), x)
            self.assertEqual(changebase(encode(x, frm), frm, to), encode(x, to))
            self.assertEqual(decode(changebase(encode(x, frm), frm, to), to), x)


class TestRipeMD160PythonBackup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('Testing the pure python backup for ripemd160')

    def test_all(self):
        strvec = [
            '',
            'The quick brown fox jumps over the lazy dog',
            'The quick brown fox jumps over the lazy cog',
            'Nobody inspects the spammish repetition'
        ]

        target = [
            '9c1185a5c5e9fc54612808977ee8f548b2258d31',
            '37f332f68db77bd9d7edd4969571ad671cf9dd3b',
            '132072df690933835eb8b6ad0b77e7b6f14acad7',
            'cc4a5ce1b3df48aec5d22d1f16b894a0b894eccc'
        ]

        hash160target = [
            'b472a266d0bd89c13706a4132ccfb16f7c3b9fcb',
            '0e3397b4abc7a382b3ea2365883c3c7ca5f07600',
            '53e0dacac5249e46114f65cb1f30d156b14e0bdc',
            '1c9b7b48049a8f98699bca22a5856c5ef571cd68'
        ]

        for i, s in enumerate(strvec):
            digest = ripemd.RIPEMD160(s).digest()
            hash160digest = ripemd.RIPEMD160(bin_sha256(s)).digest()
            self.assertEqual(bytes_to_hex_string(digest), target[i])
            self.assertEqual(bytes_to_hex_string(hash160digest), hash160target[i])
            self.assertEqual(bytes_to_hex_string(bin_hash160(from_string_to_bytes(s))), hash160target[i])
            self.assertEqual(hash160(from_string_to_bytes(s)), hash160target[i])


class TestConversions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.privkey_hex = (
            "e9873d79c6d87dc0fb6a5778633389f4453213303da61f20bd67fc233aa33262"
        )
        cls.privkey_bin = (
            b"\xe9\x87=y\xc6\xd8}\xc0\xfbjWxc3\x89\xf4E2\x130=\xa6\x1f \xbdg\xfc#:\xa32b"
        )

        cls.pubkey_hex = (
            "04588d202afcc1ee4ab5254c7847ec25b9a135bbda0f2bc69ee1a714749fd77dc9f88ff2a00d7e752d44cbe16e1ebcf0890b76ec7c78886109dee76ccfc8445424"
        )
        cls.pubkey_bin = (
            b"\x04X\x8d *\xfc\xc1\xeeJ\xb5%LxG\xec%\xb9\xa15\xbb\xda\x0f+\xc6\x9e\xe1\xa7\x14t\x9f\xd7}\xc9\xf8\x8f\xf2\xa0\r~u-D\xcb\xe1n\x1e\xbc\xf0\x89\x0bv\xec|x\x88a\t\xde\xe7l\xcf\xc8DT$"
        )

    def test_privkey_to_pubkey(self):
        pubkey_hex = privkey_to_pubkey(self.privkey_hex)
        self.assertEqual(pubkey_hex, self.pubkey_hex)

    def test_changebase(self):
        self.assertEqual(
            self.pubkey_bin,
            changebase(
                self.pubkey_hex, 16, 256, minlen=len(self.pubkey_bin)
            )
        )

        self.assertEqual(
            self.pubkey_hex,
            changebase(
                self.pubkey_bin, 256, 16, minlen=len(self.pubkey_hex)
            )
        )

        self.assertEqual(
            self.privkey_bin,
            changebase(
                self.privkey_hex, 16, 256, minlen=len(self.privkey_bin)
            )
        )

        self.assertEqual(
            self.privkey_hex,
            changebase(
                self.privkey_bin, 256, 16, minlen=len(self.privkey_hex)
            )
        )


class TestRegressions(unittest.TestCase):
    """Offline regression tests for bugs fixed in 0.3.3"""

    def test_is_address(self):
        coin = Bitcoin()
        self.assertTrue(coin.is_address("1BoatSLRHtKNngkdXEeobR76b53LETtpyT"))
        self.assertTrue(coin.is_address("3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy"))
        self.assertFalse(coin.is_p2sh("1BoatSLRHtKNngkdXEeobR76b53LETtpyT"))
        self.assertTrue(coin.is_p2sh("3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy"))


    def test_blockscout_missing_exchange_rate(self):
        from pycryptotools.explorers.blockscout_explorer import BlockscoutExplorer
        data = {'coin_balance': '1500000000000000000', 'exchange_rate': None}
        coin_info = BlockscoutExplorer.parse_coin_info_json(data)
        self.assertEqual(coin_info['balance'], 1.5)
        self.assertIsNone(coin_info['exchange_rate'])


    def test_blockscout_asset_list_keeps_tokens_and_nfts(self):
        from unittest import mock
        from pycryptotools.coins.asset_type import AssetType
        from pycryptotools.explorers import blockscout_explorer

        def fake_get(url, timeout=None):
            response = mock.Mock(status_code=200)
            if '/nft' in url:
                response.json.return_value = {'items': [{'id': '1', 'token': {'type': 'ERC-721', 'name': 'NFT'}}]}
            else:
                response.json.return_value = {'items': [{'value': '1', 'token': {'type': 'ERC-20', 'name': 'TOKEN', 'decimals': '0'}}]}
            return response

        coin = Ethereum()
        with mock.patch.object(blockscout_explorer.requests, 'get', side_effect=fake_get):
            asset_list = coin.get_asset_list("0x0000000000000000000000000000000000000001")
        self.assertEqual(sorted(a['type'].name for a in asset_list), [AssetType.NFT.name, AssetType.TOKEN.name])

    def test_unsupported_chains_fail_instead_of_zero_balance(self):
        from unittest import mock
        addr_evm = "0x0000000000000000000000000000000000000001"
        with mock.patch('requests.get') as get:
            # Blockscout used to query a placeholder url whose 404 meant "balance 0"
            for coin in (BinanceSmartChain(), RSK(), xDai(), POA()):
                with self.assertRaises(ValueError):
                    coin.get_coin_info(addr_evm)
                with self.assertRaises(ValueError):
                    coin.get_address_web_url(addr_evm)
            # Blockstream used to query Bitcoin testnet for Dash/Doge
            for coin in (Dash(), Doge()):
                with self.assertRaises(ValueError):
                    coin.get_coin_info("XpESxaUmonkq8RaLLp46Brx2K39ggQe226")
            get.assert_not_called()

    def test_litecoin_testnet_unsupported(self):
        from unittest import mock
        coin = Litecoin(testnet=True)
        addr = "tltc1qw508d6qejxtdg4y5r3zarvary0c5xw7k7grplx"
        self.assertIsNone(coin.get_address_web_url(addr))
        with mock.patch('requests.get') as get:
            with self.assertRaises(ValueError):
                coin.get_coin_info(addr)
            get.assert_not_called()
        self.assertEqual(Litecoin().get_address_web_url("MQd1fJwqBJvwLuyhr17PhEFx1swiqDbPQS"),
                         "https://litecoinspace.org/address/MQd1fJwqBJvwLuyhr17PhEFx1swiqDbPQS")

    def test_polygon_falls_back_to_jsonrpc(self):
        from decimal import Decimal
        from unittest import mock
        addr = "0x0000000000000000000000000000000000000001"

        def fake_get(url, timeout=None):
            if 'blockscout' in url:
                return mock.Mock(status_code=403)  # Cloudflare challenge
            if 'coingate' in url:
                return mock.Mock(status_code=200, text="0.5")
            raise AssertionError(f"unexpected url {url}")

        def fake_post(url, json=None, timeout=None):
            self.assertEqual(json['method'], "eth_getBalance")
            response = mock.Mock(status_code=200)
            response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": hex(3 * 10**18)}
            return response

        coin = Polygon()
        with mock.patch('requests.get', side_effect=fake_get), mock.patch('requests.post', side_effect=fake_post):
            coin_info = coin.get_coin_info(addr)
            self.assertEqual(coin_info['balance'], 3)
            self.assertEqual(coin_info['exchange_rate'], Decimal("0.5"))
            self.assertEqual(coin_info['address_explorer_url'], "https://polygonscan.com/address/" + addr)
            # the fallback cannot list assets: report a failure, not an empty list
            with self.assertRaises(ValueError):
                coin.get_asset_list(addr)


if __name__ == '__main__':
    unittest.main()
