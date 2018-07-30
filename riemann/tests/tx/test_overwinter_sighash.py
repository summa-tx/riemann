import unittest
import riemann
from riemann.tx import tx
from riemann.tests.tx import overwinter_helpers as helpers


class OverwinterSighash(unittest.TestCase):

    def setUp(self):
        riemann.select_network('zcash_overwinter_main')
        self.tx = tx.OverwinterTx.from_bytes(helpers.RAW_TX)

    def test_hash_prevouts(self):
        self.assertEqual(
            self.tx._hash_prevouts(anyone_can_pay=False),
            helpers.HASH_PREVOUTS)

    def test_hash_outputs(self):
        self.assertEqual(
            self.tx._hash_outputs(tx.SIGHASH_SINGLE, index=1),
            helpers.HASH_OUTPUTS)

    def test_hash_joinsplits(self):
        self.assertEqual(
            self.tx._hash_joinsplits(),
            helpers.HASH_JOINSPLITS)

    def test_sighash(self):
        self.assertEqual(
            self.tx.sighash_single(
                tx.SIGHASH_SINGLE,
                index=1,
                script_code=helpers.SCRIPT_CODE,
                prevout_value=helpers.PREVOUT_VALUE),
            helpers.SIGHASH)
