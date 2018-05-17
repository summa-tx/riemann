import unittest
import riemann
from .. import helpers
from ...tx import tx_builder as tb


class TestTxBuilder(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        riemann.select_network('bitcoin_main')

    def test_make_sh_output_script(self):
        self.assertEqual(
            tb.make_sh_output_script('OP_IF'),
            helpers.OP_IF_OUTPUT_SCRIPT)
        self.assertEqual(
            tb.make_sh_output_script(helpers.P2WSH_SCRIPT, witness=True),
            helpers.P2WSH_OUTPUT_SCRIPT)

        riemann.select_network('bitcoin_cash_main')
        with self.assertRaises(ValueError) as context:
            tb.make_sh_output_script(helpers.P2WSH_SCRIPT, witness=True)

        self.assertIn(
            'Network bitcoin_cash_main does not support witness scripts.',
            str(context.exception))

    def test_make_pkh_output_script(self):
        self.assertEqual(
            tb.make_pkh_output_script(helpers.PK_0_BYTES),
            helpers.PKH_0_OUTPUT_SCRIPT)
        self.assertEqual(
            tb.make_pkh_output_script(helpers.PK_0_BYTES, witness=True),
            helpers.PKH_0_P2WPKH_OUTPUT_SCRIPT)

        riemann.select_network('bitcoin_cash_main')
        with self.assertRaises(ValueError) as context:
            tb.make_pkh_output_script(helpers.PK_0_BYTES, witness=True)

        self.assertIn(
            'Network bitcoin_cash_main does not support witness scripts.',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            tb.make_pkh_output_script('hello world')
        self.assertIn(
            'Unknown pubkey format. Expected bytes. Got: ',
            str(context.exception))

    def test_make_p2sh_output_script(self):
        self.assertEqual(
            tb.make_p2sh_output_script('OP_IF'),
            helpers.OP_IF_OUTPUT_SCRIPT)

    def test_make_p2pkh_output_script(self):
        self.assertEqual(
            tb.make_p2pkh_output_script(helpers.PK_0_BYTES),
            helpers.PKH_0_OUTPUT_SCRIPT)

    def test_make_p2wsh_output_script(self):
        self.assertEqual(
            tb.make_p2wsh_output_script(helpers.P2WSH_SCRIPT),
            helpers.P2WSH_OUTPUT_SCRIPT)

    def test_make_p2wpkh_output_script(self):
        self.assertEqual(
            tb.make_p2wpkh_output_script(helpers.PK_0_BYTES),
            helpers.PKH_0_P2WPKH_OUTPUT_SCRIPT)

    def test_make_output(self):
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
