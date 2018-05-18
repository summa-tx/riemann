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

    def test_make_decred_output(self):
        riemann.select_network('decred_main')
        self.assertEqual(
            tb._make_output(
                value=helpers.DCR_OUTPUT_VALUE,
                output_script=helpers.DCR_OUTPUT_SCRIPT,
                version=helpers.DCR_OUTPUT_VERSION),
            helpers.DCR_OUTPUT)

    def test_make_sh_output(self):
        pass  # covered by next two

    def test_make_p2sh_output(self):
        self.assertEqual(
            tb.make_p2sh_output(
                value=helpers.output_value_0_int,
                output_script='OP_IF'),
            helpers.OP_IF_OUTPUT)

    def test_make_p2wsh_output(self):
        self.assertEqual(
            tb.make_p2wsh_output(
                value=helpers.P2WSH_OUTPUT_3_VALUE_INT,
                output_script=helpers.P2WSH_SCRIPT),
            helpers.P2WSH_OUTPUT_3)

    def test_make_pkh_output(self):
        pass  # covered by next 2

    def test_make_p2pkh_output(self):
        self.assertEqual(
            tb.make_p2pkh_output(
                value=helpers.output_value_0_int,
                pubkey=helpers.PK_0_BYTES),
            helpers.PK_0_P2PKH_OUTPUT)

    def test_make_p2wpkh_output(self):
        self.assertEqual(
            tb.make_p2wpkh_output(
                value=helpers.output_value_0_int,
                pubkey=helpers.PK_0_BYTES),
            helpers.PK_0_P2WPKH_OUTPUT)

    def test_make_op_return_output_error(self):
        with self.assertRaises(ValueError) as context:
            tb.make_op_return_output(b'\x00' * 78)

        self.assertIn(
            'Data is too long. Expected <= 77 bytes',
            str(context.exception))

    def test_make_empty_witness(self):
        pass

    def test_make_witness_stack_item(self):
        pass

    def test_make_witness(self):
        pass

    def test_make_decred_witness(self):
        riemann.select_network('decred_main')
        self.assertEqual(
            tb.make_decred_witness(
                value=helpers.DCR_WITNESS_VALUE,
                height=helpers.DCR_WITNESS_HEIGHT,
                index=helpers.DCR_WITNESS_INDEX,
                stack_script=helpers.DCR_STACK_SCRIPT,
                redeem_script=helpers.DCR_REDEEM_SCRIPT),
            helpers.DCR_WITNESS)

    def test_make_outpoint(self):
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.outpoint_tx_id,
            index=helpers.outpoint_index_int)

        self.assertEqual(
            outpoint,
            helpers.outpoint)

    def test_make_decred_outpoint(self):
        riemann.select_network('decred_main')
        self.assertEqual(
            tb.make_outpoint(
                tx_id_le=helpers.DCR_OUTPOINT_TX_ID_LE,
                index=0,
                tree=0),
            helpers.DCR_OUTPOINT)

    def test_make_script_sig(self):
        self.assertEqual(
            tb.make_script_sig(
                stack_script=helpers.P2SH_PUSHDATA1_STACK_SCRIPT,
                redeem_script=helpers.P2SH_PUSHDATA1_REDEEM_SCRIPT),
            helpers.P2SH_PUSHDATA1_SERIALIZED)

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

    def test_make_decred_witness_input(self):
        riemann.select_network('decred_main')
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.DCR_OUTPOINT_TX_ID_LE,
            index=0,
            tree=0)
        self.assertEqual(
            tb.make_decred_input(
                outpoint=outpoint,
                sequence=helpers.DCR_SEQUNCE_INT),
            helpers.DCR_INPUT)

    def test_make_decred_input(self):
        riemann.select_network('decred_main')
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.DCR_OUTPOINT_TX_ID_LE,
            index=0,
            tree=0)
        self.assertEqual(
            tb.make_witness_input(
                outpoint=outpoint,
                sequence=helpers.DCR_SEQUNCE_INT),
            helpers.DCR_INPUT)

    def test_make_witness_input_and_witness(self):
        pass

    def test_make_decred_input_and_witness(self):
        riemann.select_network('decred_main')
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.DCR_OUTPOINT_TX_ID_LE,
            index=0,
            tree=0)
        tx_in, witness = tb.make_witness_input_and_witness(
            outpoint=outpoint,
            sequence=helpers.DCR_SEQUNCE_INT,
            value=helpers.DCR_WITNESS_VALUE,
            height=helpers.DCR_WITNESS_HEIGHT,
            index=helpers.DCR_WITNESS_INDEX,
            stack_script=helpers.DCR_STACK_SCRIPT,
            redeem_script=helpers.DCR_REDEEM_SCRIPT)
        self.assertEqual(
            tx_in,
            helpers.DCR_INPUT)
        self.assertEqual(
            witness,
            helpers.DCR_WITNESS)

    def test_make_decred_tx(self):
        riemann.select_network('decred_main')
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.DCR_OUTPOINT_TX_ID_LE,
            index=0,
            tree=0)
        tx_in, witness = tb.make_witness_input_and_witness(
            outpoint=outpoint,
            sequence=helpers.DCR_SEQUNCE_INT,
            value=helpers.DCR_WITNESS_VALUE,
            height=helpers.DCR_WITNESS_HEIGHT,
            index=helpers.DCR_WITNESS_INDEX,
            stack_script=helpers.DCR_STACK_SCRIPT,
            redeem_script=helpers.DCR_REDEEM_SCRIPT)
        tx_out = tb._make_output(
            value=helpers.DCR_OUTPUT_VALUE,
            output_script=helpers.DCR_OUTPUT_SCRIPT,
            version=helpers.DCR_OUTPUT_VERSION)
        self.assertEqual(
            tb.make_tx(
                version=1,
                tx_ins=[tx_in],
                tx_outs=[tx_out],
                lock_time=helpers.DCR_LOCKTIME_INT,
                expiry=helpers.DCR_EXPIRY_INT,
                tx_witnesses=witness),
            helpers.DCR_RAW_P2SH_TO_P2PKH)

    def test_length_prepend(self):
        self.assertEqual(
            tb.length_prepend(b'\x00'),
            b'\x01\x00')
        self.assertEqual(
            tb.length_prepend(b'\x00' * 99),
            b'\x63' + b'\x00' * 99)
        self.assertEqual(
            tb.length_prepend(b'\x00' * 256),
            b'\xfd\x00\x01' + b'\x00' * 256)
