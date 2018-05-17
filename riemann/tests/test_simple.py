import unittest
from riemann import simple
from riemann.tx import tx_builder as tb
from riemann.tests import helpers


class TestSimple(unittest.TestCase):

    def setUp(self):
        pass

    def test_p2sh_input(self):

        outpoint = simple.outpoint(
            helpers.P2SH_PUSHDATA1_TX_ID, helpers.P2SH_PUSHDATA1_TX_INDEX)
        tx_p2sh_input = simple.p2sh_input(
            outpoint, helpers.P2SH_PUSHDATA1_STACK_SCRIPT,
            helpers.P2SH_PUSHDATA1_REDEEM_SCRIPT, sequence=0xFFFFFFFF)

        self.assertTrue(tx_p2sh_input.is_p2sh())

        self.assertTrue(isinstance(tx_p2sh_input.stack_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.stack_script,
            helpers.P2SH_PUSHDATA1_SERIALIZED_STACK_SCRIPT)

        self.assertTrue(isinstance(tx_p2sh_input.redeem_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.redeem_script,
            helpers.P2SH_PUSHDATA1_SERIALIZED_REDEEM_SCRIPT)
        self.assertEqual(tx_p2sh_input, helpers.P2SH_PUSHDATA1_INPUT)

    def test_p2sh_input_and_witness(self):

        outpoint = simple.outpoint(
            helpers.P2SH_PUSHDATA1_TX_ID, helpers.P2SH_PUSHDATA1_TX_INDEX)
        (tx_p2sh_input, witness) = simple.p2sh_input_and_witness(
            outpoint, helpers.P2SH_PUSHDATA1_STACK_SCRIPT,
            helpers.P2SH_PUSHDATA1_REDEEM_SCRIPT, sequence=0xFFFFFFFF)

        self.assertTrue(tx_p2sh_input.is_p2sh())
        self.assertEqual(witness, b'\x00')

        self.assertTrue(isinstance(tx_p2sh_input.stack_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.stack_script,
            helpers.P2SH_PUSHDATA1_SERIALIZED_STACK_SCRIPT)

        self.assertTrue(isinstance(tx_p2sh_input.redeem_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.redeem_script,
            helpers.P2SH_PUSHDATA1_SERIALIZED_REDEEM_SCRIPT)

        self.assertEqual(tx_p2sh_input, helpers.P2SH_PUSHDATA1_INPUT)

    def test_p2wsh_input_and_witness(self):

        outpoint = simple.outpoint(helpers.P2WSH_TX_ID, helpers.P2WSH_TX_INDEX)
        (tx_in, witness) = simple.p2wsh_input_and_witness(
            outpoint=outpoint,
            stack=helpers.P2WSH_WITNESS_STACK_STRING,
            witness_script=helpers.P2WSH_SCRIPT,
            sequence=helpers.P2WSH_SPEND_SEQUENCE_INT)

        self.assertTrue(tx_in == helpers.P2WSH_SPEND_TX_IN)
        self.assertTrue(witness == helpers.P2WSH_WITNESS)

    def test_unsigned_legacy_tx(self):

        outpoint = simple.outpoint(
            tx_id=helpers.P2PKH_TX_ID,
            index=helpers.P2PKH_TX_INDEX)
        tx_ins = simple.unsigned_input(
            outpoint=outpoint,
            sequence=helpers.P2PKH_SEQUENCE)
        tx_out = simple.output(
            helpers.P2PKH_VALUE - helpers.P2PKH_FEE,
            helpers.P2PKH_RECEIVE_ADDR)
        tx_return_output = tb.make_op_return_output(helpers.P2PKH_MEMO)
        tx = simple.unsigned_legacy_tx(
            tx_ins=[tx_ins],
            tx_outs=[tx_out, tx_return_output])

        self.assertTrue(tx == helpers.P2PKH_UNSIGNED_TX)

    def test_unsigned_witness_tx(self):

        outpoint = simple.outpoint(
            tx_id=helpers.P2WPKH_TX_ID,
            index=helpers.P2WPKH_TX_INDEX)
        tx_ins = simple.unsigned_input(
            outpoint=outpoint,
            sequence=helpers.P2WPKH_SEQUENCE)
        tx_outs = simple.output(
            helpers.P2WPKH_VALUE - helpers.P2WPKH_FEE,
            helpers.P2WPKH_RECEIVE_ADDR)
        tx = simple.unsigned_witness_tx(
            tx_ins=[tx_ins],
            tx_outs=[tx_outs])

        self.assertTrue(tx == helpers.P2WPKH_UNSIGNED_TX)
