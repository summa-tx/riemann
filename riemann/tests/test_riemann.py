import unittest
import riemann
from riemann import networks


class test_riemann(unittest.TestCase):

    def setUp(self):
        pass

    def test_select_network(self):
        for n in networks.SUPPORTED:
            riemann.select_network(n)
            self.assertIs(riemann.network, networks.SUPPORTED[n])

    def test_get_current_network(self):
        for n in networks.SUPPORTED:
            riemann.select_network(n)
            self.assertIs(riemann.get_current_network(),
                          networks.SUPPORTED[n])

    def test_get_current_network_name(self):
        for n in networks.SUPPORTED:
            riemann.select_network(n)
            self.assertEqual(riemann.get_current_network_name(), n)

    def tearDown(self):
        riemann.select_network('bitcoin_main')
