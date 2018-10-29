import unittest
import riemann
from riemann import utils
from riemann.tx import sapling
from riemann.tests.tx.helpers import sapling_helpers


class TestSaplingTx(unittest.TestCase):

    def setUp(self):
        riemann.select_network('zcash_sapling_main')

    def attr_assert(self, attr_name, replacement, err_text):
        # Removes a named key from a dictionary and replaces it with b'\x00'
        temp_dict = dict((a, self.tx[a])
                         for a in self.tx
                         if a != attr_name)
        temp_dict[attr_name] = replacement
        with self.assertRaises(ValueError) as context:
            sapling.SaplingTx(**temp_dict)

        self.assertIn(err_text, str(context.exception))

    def test_from_hex(self):
        for txn in sapling_helpers.TXNS:
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

    def test_init_errors(self):
        # TODO
        pass

    def test_sighash(self):
        # TODO: Check blake2b implementation
        for txn in sapling_helpers.SIGHASH:
            test_tx = sapling.SaplingTx.from_hex(txn['hex'])
            self.assertEqual(
                test_tx._hash_prevouts(anyone_can_pay=False).hex(),
                txn['hashPrevouts'])
            self.assertEqual(
                test_tx._hash_sequence(
                    sighash_type=txn['sighash_type'],
                    anyone_can_pay=False).hex(),
                txn['hashSequence'])
            self.assertEqual(
                test_tx._hash_outputs(
                    sighash_type=txn['sighash_type'],
                    index=txn['index']).hex(),
                txn['hashOutputs'])
            self.assertEqual(
                test_tx._hash_joinsplits().hex(),
                txn['hashJoinSplits'])
            self.assertEqual(
                test_tx._hash_shielded_spends().hex(),
                txn['hashShieldedSpends'])
            self.assertEqual(
                test_tx._hash_shielded_outputs().hex(),
                txn['hashShieldedOutputs'])
            self.assertEqual(
                test_tx.sighash(
                    sighash_type=txn['sighash_type'],
                    index=txn['index'],
                    joinsplit=txn['joinsplit'],
                    script_code=bytes.fromhex(txn['script_code']),
                    anyone_can_pay=txn['anyone_can_pay'],
                    prevout_value=bytes.fromhex(txn['amount'])).hex(),
                txn['sighash'])
