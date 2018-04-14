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


tb


class TestTxBuilder(unittest.TestCase):

    def setUp(self):
        pass
