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

    def test_make_decred_output(self):
        riemann.select_network('decred_main')
        self.assertEqual(
            tb._make_output(
                value=helpers.DCR['ser']['outs'][0]['value'],
                output_script=helpers.DCR['ser']['outs'][0]['pk_script'],
                version=helpers.DCR['ser']['outs'][0]['version']),
            helpers.DCR['ser']['outs'][0]['output'])

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

    def test_make_decred_witness(self):
        riemann.select_network('decred_main')
        helper_witness = helpers.DCR['ser']['witnesses'][0]
        self.assertEqual(
            tb.make_decred_witness(
                value=helper_witness['value'],
                height=helper_witness['height'],
                index=helper_witness['index'],
                stack_script=helper_witness['stack_script'],
                redeem_script=helper_witness['redeem_script']),
            helper_witness['witness'])

    def test_make_outpoint(self):
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.P2PKH1['ser']['ins'][0]['hash'],
            index=helpers.P2PKH1['human']['ins'][0]['index'])

        self.assertEqual(
            outpoint,
            helpers.P2PKH1['ser']['ins'][0]['outpoint'])

    def test_make_decred_outpoint(self):
        riemann.select_network('decred_main')
        self.assertEqual(
            tb.make_outpoint(
                tx_id_le=helpers.DCR['ser']['ins'][0]['hash'],
                index=0,
                tree=0),
            helpers.DCR['ser']['ins'][0]['outpoint'])

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

    def test_make_decred_witness_input(self):
        riemann.select_network('decred_main')
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.DCR['ser']['ins'][0]['hash'],
            index=0,
            tree=0)
        self.assertEqual(
            tb.make_decred_input(
                outpoint=outpoint,
                sequence=helpers.DCR['human']['ins'][0]['sequence']),
            helpers.DCR['ser']['tx']['in_unsigned'])

    def test_make_decred_input(self):
        riemann.select_network('decred_main')
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.DCR['ser']['ins'][0]['hash'],
            index=0,
            tree=0)
        self.assertEqual(
            tb.make_witness_input(
                outpoint=outpoint,
                sequence=helpers.DCR['human']['ins'][0]['sequence']),
            helpers.DCR['ser']['tx']['in_unsigned'])

    def test_make_witness_input_and_witness(self):
        pass

    def test_make_decred_input_and_witness(self):
        riemann.select_network('decred_main')
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.DCR['ser']['ins'][0]['hash'],
            index=0,
            tree=0)
        tx_in, witness = tb.make_witness_input_and_witness(
            outpoint=outpoint,
            sequence=helpers.DCR['human']['ins'][0]['sequence'],
            value=helpers.DCR['ser']['witnesses'][0]['value'],
            height=helpers.DCR['ser']['witnesses'][0]['height'],
            index=helpers.DCR['ser']['witnesses'][0]['index'],
            stack_script=helpers.DCR['ser']['witnesses'][0]['stack_script'],
            redeem_script=helpers.DCR['ser']['witnesses'][0]['redeem_script'])
        self.assertEqual(
            tx_in,
            helpers.DCR['ser']['tx']['in_unsigned'])
        self.assertEqual(
            witness,
            helpers.DCR['ser']['witnesses'][0]['witness'])

    def test_make_decred_tx(self):
        riemann.select_network('decred_main')
        helper_witness = helpers.DCR['ser']['witnesses'][0]
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.DCR['ser']['ins'][0]['hash'],
            index=0,
            tree=0)
        tx_in, witness = tb.make_witness_input_and_witness(
            outpoint=outpoint,
            sequence=helpers.DCR['human']['ins'][0]['sequence'],
            value=helper_witness['value'],
            height=helper_witness['height'],
            index=helper_witness['index'],
            stack_script=helper_witness['stack_script'],
            redeem_script=helper_witness['redeem_script'])
        tx_out = tb._make_output(
            value=helpers.DCR['ser']['outs'][0]['value'],
            output_script=helpers.DCR['ser']['outs'][0]['pk_script'],
            version=helpers.DCR['ser']['outs'][0]['version'])
        self.assertEqual(
            tb.make_tx(
                version=1,
                tx_ins=[tx_in],
                tx_outs=[tx_out],
                lock_time=helpers.DCR['human']['locktime'],
                expiry=helpers.DCR['human']['expiry'],
                tx_witnesses=witness),
            helpers.DCR['ser']['tx']['p2sh_2_p2pkh'])

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

    @mock.patch('riemann.tx.tx_builder.tx')
    def test_sprout_snowflake(self, mock_tx):
        # TODO: Improve
        riemann.select_network('zcash_sprout_main')
        mock_tx.SproutTx.return_value = 0
        self.assertEqual(
            tb.make_tx(0, 0, 0, 0, tx_joinsplits=[]),
            0)

    @mock.patch('riemann.tx.tx_builder.tx')
    def test_overwinter_snowflake(self, mock_tx):
        # TODO: Improve
        riemann.select_network('zcash_overwinter_main')
        mock_tx.OverwinterTx.return_value = 0
        self.assertEqual(
            tb.make_tx(0, 0, 0, 0, expiry=0),
            0)
