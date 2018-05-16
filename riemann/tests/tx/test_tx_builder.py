import unittest
from .. import helpers
from ...tx import tx_builder as tb


class TestTxBuilder(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_make_sh_output_script(self):
        pass

    def test_make_pkh_output_script(self):
        pass

    def test_make_p2sh_output_script(self):
        pass

    def test_make_p2pkh_output_script(self):
        pass

    def test_make_p2wsh_output_script(self):
        pass

    def test_make_p2wpkh_output_script(self):
        pass

    def test_make_putput(self):
        pass

    def test_make_sh_output(self):
        pass

    def test_make_p2sh_output(self):
        pass

    def test_make_p2wsh_output(self):
        pass

    def test_make_pkh_output(self):
        pass

    def test_make_p2pkh_output(self):
        pass

    def test_make_p2wpkh_output(self):
        pass

    def test_make_op_return_output(self):
        pass

    def test_make_empty_witness(self):
        pass

    def test_make_witness_stack_item(self):
        pass

    def test_make_witness(self):
        pass

    def test_make_decred_witness(self):
        pass

    def test_make_outpoint(self):
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.outpoint_tx_id,
            index=helpers.outpoint_index_int)

        self.assertEqual(
            outpoint,
            helpers.outpoint)

    def test_make_script_sig(self):
        pass

    def test_make_legacy_input(self):
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.outpoint_tx_id,
            index=helpers.outpoint_index_int)

        tx_in = tb.make_legacy_input(
            outpoint=outpoint,
            stack_script=helpers.stack_script,
            redeem_script=helpers.redeem_script,
            sequence=helpers.sequence_int)

        self.assertEqual(tx_in, helpers.tx_in)

    def test_make_legacy_input_and_empty_witness(self):
        pass

    def test_make_witness_input(self):
        pass

    def test_make_decred_input(self):
        pass

    def test_make_witness_input_and_witness(self):
        pass

    def test_make_tx(self):
        pass
