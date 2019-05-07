import unittest
import riemann
from unittest import mock
from riemann.tests import helpers
from riemann.tx import tx_builder as tb


class TestTxBuilder(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        riemann.select_network('bitcoin_main')

    def test_make_sh_output_script(self):
        self.assertEqual(
            tb.make_sh_output_script('OP_IF'),
            helpers.OP_IF['output_script'])
        self.assertEqual(
            tb.make_sh_output_script(
                helpers.P2WSH['human']['witnesses'][0]['wit_script'],
                witness=True),
            helpers.P2WSH['ser']['ins'][0]['pk_script'])

        riemann.select_network('bitcoin_cash_main')
        with self.assertRaises(ValueError) as context:
            tb.make_sh_output_script(
                helpers.P2WSH['human']['witnesses'][0]['wit_script'],
                witness=True)

        self.assertIn(
            'Network bitcoin_cash_main does not support witness scripts.',
            str(context.exception))

    def test_make_pkh_output_script(self):
        self.assertEqual(
            tb.make_pkh_output_script(helpers.PK['ser'][0]['pk']),
            helpers.PK['ser'][0]['pkh_output'])
        self.assertEqual(
            tb.make_pkh_output_script(
                helpers.PK['ser'][0]['pk'],
                witness=True),
            helpers.PK['ser'][0]['pkh_p2wpkh_output'])

        riemann.select_network('bitcoin_cash_main')
        with self.assertRaises(ValueError) as context:
            tb.make_pkh_output_script(helpers.PK['ser'][0]['pk'], witness=True)

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
            helpers.OP_IF['output_script'])

    def test_make_p2pkh_output_script(self):
        self.assertEqual(
            tb.make_p2pkh_output_script(helpers.PK['ser'][0]['pk']),
            helpers.PK['ser'][0]['pkh_output'])

    def test_make_p2wsh_output_script(self):
        self.assertEqual(
            tb.make_p2wsh_output_script(
                helpers.P2WSH['human']['witnesses'][0]['wit_script']),
            helpers.P2WSH['ser']['ins'][0]['pk_script'])

    def test_make_p2wpkh_output_script(self):
        self.assertEqual(
            tb.make_p2wpkh_output_script(helpers.PK['ser'][0]['pk']),
            helpers.PK['ser'][0]['pkh_p2wpkh_output'])

    def test_make_sh_output(self):
        pass  # covered by next two

    def test_make_p2sh_output(self):
        self.assertEqual(
            tb.make_p2sh_output(
                value=helpers.P2PKH1['human']['outs'][0]['value'],
                output_script='OP_IF'),
            helpers.OP_IF['output'])

    def test_make_p2wsh_output(self):
        helper_witness = helpers.P2WSH['human']['witnesses'][0]
        self.assertEqual(
            tb.make_p2wsh_output(
                value=helpers.P2WSH['human']['outs'][3]['value'],
                output_script=helper_witness['wit_script']),
            helpers.P2WSH['ser']['outs'][3]['output'])

    def test_make_pkh_output(self):
        pass  # covered by next 2

    def test_make_p2pkh_output(self):
        self.assertEqual(
            tb.make_p2pkh_output(
                value=helpers.P2PKH1['human']['outs'][0]['value'],
                pubkey=helpers.PK['ser'][0]['pk']),
            helpers.PK['ser'][0]['pk_p2pkh_output'])

    def test_make_p2wpkh_output(self):
        self.assertEqual(
            tb.make_p2wpkh_output(
                value=helpers.P2PKH1['human']['outs'][0]['value'],
                pubkey=helpers.PK['ser'][0]['pk']),
            helpers.PK['ser'][0]['pk_p2wpkh_output'])

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

    def test_make_outpoint(self):
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.P2PKH1['ser']['ins'][0]['hash'],
            index=helpers.P2PKH1['human']['ins'][0]['index'])

        self.assertEqual(
            outpoint,
            helpers.P2PKH1['ser']['ins'][0]['outpoint'])

    def test_make_script_sig(self):
        tx_in = helpers.P2SH_PD1['human']['ins'][0]
        self.assertEqual(
            tb.make_script_sig(
                stack_script=tx_in['stack_script'],
                redeem_script=tx_in['redeem_script']),
            helpers.P2SH_PD1['ser']['ins'][0]['script_sig'])

    def test_make_legacy_input(self):
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.P2PKH1['ser']['ins'][0]['hash'],
            index=helpers.P2PKH1['human']['ins'][0]['index'])

        tx_in = tb.make_legacy_input(
            outpoint=outpoint,
            stack_script=helpers.P2PKH1['ser']['ins'][0]['stack_script'],
            redeem_script=helpers.P2PKH1['ser']['ins'][0]['redeem_script'],
            sequence=helpers.P2PKH1['human']['ins'][0]['sequence'])

        self.assertEqual(tx_in, helpers.P2PKH1['ser']['tx']['in'])

    def test_make_legacy_input_and_empty_witness(self):
        pass

    def test_make_witness_input_and_witness(self):
        pass

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

    @mock.patch('riemann.tx.tx_builder.sprout')
    def test_sprout_snowflake(self, mock_tx):
        # TODO: Improve
        riemann.select_network('zcash_sprout_main')
        mock_tx.SproutTx.return_value = 0
        self.assertEqual(
            tb.make_tx(0, 0, 0, 0, tx_joinsplits=[]),
            0)

    @mock.patch('riemann.tx.tx_builder.overwinter')
    def test_overwinter_snowflake(self, mock_tx):
        # TODO: Improve
        riemann.select_network('zcash_overwinter_main')
        mock_tx.OverwinterTx.return_value = 0
        self.assertEqual(
            tb.make_tx(0, 0, 0, 0, expiry=0),
            0)
