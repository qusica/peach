import unittest
from types import SimpleNamespace

from peach.routes_api import _local_player_request, _loopback_url


class LocalPlayerSecurityTests(unittest.TestCase):
    def test_loopback_only(self):
        for url in ("http://127.0.0.1:8900/", "http://localhost:8900/", "http://[::1]:8900/"):
            self.assertTrue(_loopback_url(url))
        for url in ("https://peach.example/", "http://192.168.1.8:8900/", "http://127.0.0.1.attacker.test/"):
            self.assertFalse(_loopback_url(url))

    def test_remote_origin_denied_even_if_proxy_is_loopback(self):
        def request(client, base, origin):
            return SimpleNamespace(
                client=SimpleNamespace(host=client),
                base_url=base,
                headers={"origin": origin},
            )
        self.assertFalse(_local_player_request(request("127.0.0.1", "http://127.0.0.1:8900", "https://remote.example")))
        self.assertFalse(_local_player_request(request("192.168.1.50", "http://127.0.0.1:8900", "http://127.0.0.1:8900")))
        self.assertTrue(_local_player_request(request("127.0.0.1", "http://127.0.0.1:8900", "http://127.0.0.1:8900")))
