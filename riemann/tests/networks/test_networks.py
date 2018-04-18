import unittest
import riemann.networks as networks


class TestNetworks(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_network(self):
        for name in networks.SUPPORTED:
            n = networks.get_network(name)
            self.assertEqual(n, networks.SUPPORTED[name])

        # Test Error case
        with self.assertRaises(ValueError) as context:
            networks.get_network('toast')

        self.assertIn('Unknown chain specifed: {}'.format('toast'),
                      str(context.exception))
