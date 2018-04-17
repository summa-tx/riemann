import unittest
import multicoin
from multicoin import networks


class test_multicoin(unittest.TestCase):

    def setUp(self):
        pass

    def test_select_network(self):
        for n in networks.SUPPORTED:
            multicoin.select_network(n)
            self.assertIs(multicoin.network, networks.SUPPORTED[n])

    def test_get_current_network(self):
        for n in networks.SUPPORTED:
            multicoin.select_network(n)
            self.assertIs(multicoin.get_current_network(),
                          networks.SUPPORTED[n])

    def test_get_current_network_name(self):
        for n in networks.SUPPORTED:
            multicoin.select_network(n)
            self.assertEqual(multicoin.get_current_network_name(), n)

    def tearDown(self):
        multicoin.select_network('bitcoin_main')
