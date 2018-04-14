import unittest
from ...encoding import addresses as addr

OP_IF_P2SH = '3MpTk145zbm5odhRALfT9BnUs8DB5w4ydw'


class TestAddresse(unittest.TestCase):

    def test_make_p2sh_address(self):
        res = addr.make_p2sh_address('OP_IF')
        self.assertEqual(res, OP_IF_P2SH)
