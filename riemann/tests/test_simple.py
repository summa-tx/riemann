import unittest
from riemann import simple
from riemann.tx import tx_builder as tb
from riemann.tests import helpers


class TestSimple(unittest.TestCase):

    def setUp(self):
        pass

    def test_p2sh_input(self):

        outpoint = simple.outpoint(
            tx_id=helpers.P2SH_PD1['human']['ins'][0]['hash'],
            index=helpers.P2SH_PD1['human']['ins'][0]['index'])
        tx_p2sh_input = simple.p2sh_input(
            outpoint=outpoint,
            stack_script=helpers.P2SH_PD1['human']['stack_script'],
            redeem_script=helpers.P2SH_PD1['human']['redeem_script'],
            sequence=helpers.P2SH_PD1['human']['sequence'])

        self.assertTrue(tx_p2sh_input.is_p2sh())

        self.assertTrue(isinstance(tx_p2sh_input.stack_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.stack_script,
            helpers.P2SH_PD1['ser']['stack_script'])

        self.assertTrue(isinstance(tx_p2sh_input.redeem_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.redeem_script,
            helpers.P2SH_PD1['ser']['redeem_script'])
        self.assertEqual(tx_p2sh_input, helpers.P2SH_PD1['ser']['tx']['in'])

    def test_p2sh_input_and_witness(self):

        outpoint = simple.outpoint(
            helpers.P2SH_PD1['human']['ins'][0]['hash'],
            helpers.P2SH_PD1['human']['ins'][0]['index'])
        (tx_p2sh_input, witness) = simple.p2sh_input_and_witness(
            outpoint=outpoint,
            stack_script=helpers.P2SH_PD1['human']['stack_script'],
            redeem_script=helpers.P2SH_PD1['human']['redeem_script'],
            sequence=helpers.P2SH_PD1['human']['sequence'])

        self.assertTrue(tx_p2sh_input.is_p2sh())
        self.assertEqual(witness, b'\x00')

        self.assertTrue(isinstance(tx_p2sh_input.stack_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.stack_script,
            helpers.P2SH_PD1['ser']['stack_script'])

        self.assertTrue(isinstance(tx_p2sh_input.redeem_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.redeem_script,
            helpers.P2SH_PD1['ser']['redeem_script'])

        self.assertEqual(tx_p2sh_input, helpers.P2SH_PD1['ser']['tx']['in'])

    def test_p2wsh_input_and_witness(self):

        outpoint = simple.outpoint(
            tx_id=helpers.P2WSH['human']['ins'][0]['hash'],
            index=helpers.P2WSH['human']['ins'][0]['index'])
        (tx_in, witness) = simple.p2wsh_input_and_witness(
            outpoint=outpoint,
            stack=helpers.P2WSH['human']['stack_script'],
            witness_script=helpers.P2WSH['human']['wit_script'],
            sequence=helpers.P2WSH['human']['sequence'])

        self.assertTrue(tx_in == helpers.P2WSH['ser']['tx']['in'])
        self.assertTrue(witness == helpers.P2WSH['ser']['tx']['witness'])

    def test_unsigned_legacy_tx(self):

        outpoint = simple.outpoint(
            tx_id=helpers.P2PKH['human']['ins'][0]['hash'],
            index=helpers.P2PKH['human']['ins'][0]['index'])
        tx_ins = simple.unsigned_input(
            outpoint=outpoint,
            sequence=helpers.P2PKH['human']['sequence'])
        tx_out = simple.output(
            helpers.P2PKH['human']['outs'][0]['value'],
            helpers.P2PKH['human']['outs'][0]['addr'])
        tx_return_output = tb.make_op_return_output(
            helpers.P2PKH['human']['outs'][1]['memo'])
        tx = simple.unsigned_legacy_tx(
            tx_ins=[tx_ins],
            tx_outs=[tx_out, tx_return_output])

        self.assertTrue(tx == helpers.P2PKH['ser']['tx']['unsigned'])

    def test_unsigned_witness_tx(self):
        outpoint = simple.outpoint(
            tx_id=helpers.P2WPKH['human']['ins'][0]['hash'],
            index=helpers.P2WPKH['human']['ins'][0]['index'])
        tx_ins = simple.unsigned_input(
            outpoint=outpoint,
            sequence=helpers.P2WPKH['human']['sequence'])
        tx_outs = simple.output(
            helpers.P2WPKH['human']['outs'][0]['value'],
            helpers.P2WPKH['human']['outs'][0]['addr'])
        tx = simple.unsigned_witness_tx(
            tx_ins=[tx_ins],
            tx_outs=[tx_outs])

        self.assertTrue(tx == helpers.P2WPKH['ser']['tx']['unsigned'])
