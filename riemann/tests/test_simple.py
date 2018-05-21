import unittest
from riemann import simple
from riemann.tx import tx_builder as tb
from riemann.tests import helpers


class TestSimple(unittest.TestCase):

    def setUp(self):
        pass

    def test_p2sh_input(self):

        outpoint = simple.outpoint(
            tx_id=helpers.P2SH_PD1['ins'][0]['hash'].hex(),
            index=helpers.P2SH_PD1['ins'][0]['index'])
        tx_p2sh_input = simple.p2sh_input(
            outpoint=outpoint,
            stack_script=helpers.P2SH_PD1['stack_script']['human'],
            redeem_script=helpers.P2SH_PD1['redeem_script']['human'],
            sequence=helpers.P2SH_PD1['sequence'])

        self.assertTrue(tx_p2sh_input.is_p2sh())

        self.assertTrue(isinstance(tx_p2sh_input.stack_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.stack_script,
            helpers.P2SH_PD1['stack_script']['serialized'])

        self.assertTrue(isinstance(tx_p2sh_input.redeem_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.redeem_script,
            helpers.P2SH_PD1['redeem_script']['serialized'])
        self.assertEqual(tx_p2sh_input, helpers.P2SH_PD1['tx']['in'])

    def test_p2sh_input_and_witness(self):

        outpoint = simple.outpoint(
            helpers.P2SH_PD1['ins'][0]['hash'].hex(),
            helpers.P2SH_PD1['ins'][0]['index'])
        (tx_p2sh_input, witness) = simple.p2sh_input_and_witness(
            outpoint=outpoint,
            stack_script=helpers.P2SH_PD1['stack_script']['human'],
            redeem_script=helpers.P2SH_PD1['redeem_script']['human'],
            sequence=helpers.P2SH_PD1['sequence'])

        self.assertTrue(tx_p2sh_input.is_p2sh())
        self.assertEqual(witness, b'\x00')

        self.assertTrue(isinstance(tx_p2sh_input.stack_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.stack_script,
            helpers.P2SH_PD1['stack_script']['serialized'])

        self.assertTrue(isinstance(tx_p2sh_input.redeem_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.redeem_script,
            helpers.P2SH_PD1['redeem_script']['serialized'])

        self.assertEqual(tx_p2sh_input, helpers.P2SH_PD1['tx']['in'])

    def test_p2wsh_input_and_witness(self):

        outpoint = simple.outpoint(
            tx_id=helpers.P2WSH['ins'][0]['hash'].hex(),
            index=helpers.P2WSH['ins'][0]['index'])
        (tx_in, witness) = simple.p2wsh_input_and_witness(
            outpoint=outpoint,
            stack=helpers.P2WSH['wit']['stack_script']['human'],
            witness_script=helpers.P2WSH['wit']['wit_script']['human'],
            sequence=helpers.P2WSH['sequence'])

        self.assertTrue(tx_in == helpers.P2WSH['tx']['in'])
        self.assertTrue(witness == helpers.P2WSH['tx']['witness'])

    def test_unsigned_legacy_tx(self):

        outpoint = simple.outpoint(
            tx_id=helpers.P2PKH['ins'][0]['hash'].hex(),
            index=helpers.P2PKH['ins'][0]['index'])
        tx_ins = simple.unsigned_input(
            outpoint=outpoint,
            sequence=helpers.P2PKH['sequence'])
        tx_out = simple.output(
            helpers.P2PKH['outs'][0]['value'],
            helpers.P2PKH['outs'][0]['addr'])
        tx_return_output = tb.make_op_return_output(
            helpers.P2PKH['outs'][1]['memo'])
        tx = simple.unsigned_legacy_tx(
            tx_ins=[tx_ins],
            tx_outs=[tx_out, tx_return_output])

        self.assertTrue(tx == helpers.P2PKH['tx']['unsigned'])

    def test_unsigned_witness_tx(self):
        outpoint = simple.outpoint(
            tx_id=helpers.P2WPKH['ins'][0]['hash'].hex(),
            index=helpers.P2WPKH['ins'][0]['index'])
        tx_ins = simple.unsigned_input(
            outpoint=outpoint,
            sequence=helpers.P2WPKH['sequence'])
        tx_outs = simple.output(
            helpers.P2WPKH['outs'][0]['value'],
            helpers.P2WPKH['outs'][0]['addr'])
        tx = simple.unsigned_witness_tx(
            tx_ins=[tx_ins],
            tx_outs=[tx_outs])

        self.assertTrue(tx == helpers.P2WPKH['tx']['unsigned'])
