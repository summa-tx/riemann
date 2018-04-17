import unittest
from .. import helpers
from ...encoding import addresses as addr

# NB:
# How to make more of these.
# 1. Install python-bitcoinlib
# 2. Compile a script to an array of ints (same as input to bytes class)
# 3. Follow procedure below
#
# from bitcoin.core.script import CScript
# from bitcoin.wallet import CBitcoinAddress
# a = CScript(bytes.fromhex('HEX SCRIPT'))
# CBitcoinAddress.from_scriptPubKey(a.to_p2sh_scriptPubKey()
#
# For more P2PKH addresses:
# P2PKHBitcoinAddress.from_pubkey(PUBKEY_BYTES, accept_invalid=True)


class TestAddresse(unittest.TestCase):

    def test_make_p2sh_address(self):
        a = addr.make_p2sh_address('OP_IF')
        self.assertEqual(a, helpers.OP_IF_P2SH)

    def test_make_p2sh_address_msig(self):
        a = addr.make_p2sh_address(helpers.MSIG_TWO_TWO_SCRIPT)
        self.assertEqual(a, helpers.MSIG_TWO_TWO_P2SH)

    def test_make_p2wsh_address(self):
        pass

    def test_make_p2pkh_address(self):
        a = addr.make_p2pkh_address(b'\x00' * 65)
        self.assertEqual(a, helpers.P2PKH_0)
        b = addr.make_p2pkh_address(b'\x11' * 65)
        self.assertEqual(b, helpers.P2PKH_1)
