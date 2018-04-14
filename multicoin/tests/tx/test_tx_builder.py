import unittest
from ...tx import tx_builder as tb

# NB:
# How to make more of these.
# 1. Install python-bitcoinlib
# 2. Compile a script to an array of ints (same as input to bytes clase)
# 2. Follow procedure below
#
# from bitcoin.core.script import CScript
# from bitcoin.wallet import CBitcoinAddress
# a = CScript(SCRIPT_INTS_GO_HERE)
# print(CBitcoinAddress.from_scriptPubKey(a.to_scriptPubKey))


OP_IF_P2SH = '3MpTk145zbm5odhRALfT9BnUs8DB5w4ydw'


class TestTxBuilder(unittest.TestCase):

    def setUp(self):
        pass

    def test_make_p2sh_address(self):

        res = tb.make_p2sh_address('OP_IF')
        self.assertEqual(res, OP_IF_P2SH)
