import unittest
import riemann
from riemann import utils
from riemann.tx import sapling
from riemann.tests.tx.helpers import sapling_helpers


class TestSaplingTx(unittest.TestCase):

    def setUp(self):
        riemann.select_network('zcash_sapling_main')
        self.helpers = sapling_helpers.TXNS

    def test_from_hex(self):
        for txn in self.helpers:
            test_tx = sapling.SaplingTx.from_hex(txn['hex'])
            self.assertEqual(
                test_tx.binding_sig.hex(),
                txn['bindingSig'])
            self.assertEqual(
                utils.le2i(test_tx.expiry_height),
                txn['expiryHeight'])
            for pair in zip(test_tx.tx_shielded_spends, txn['vShieldedSpend']):
                self.assertEqual(
                    pair[0].cv.hex(),
                    pair[1]['cv'])
                self.assertEqual(
                    pair[0].anchor.hex(),
                    pair[1]['anchor'])
                self.assertEqual(
                    pair[0].nullifier.hex(),
                    pair[1]['nullifier'])
                self.assertEqual(
                    pair[0].zkproof.hex(),
                    pair[1]['zkproof'])
                self.assertEqual(
                    pair[0].spend_auth_sig.hex(),
                    pair[1]['spendAuthSig'])
