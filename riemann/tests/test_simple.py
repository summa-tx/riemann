import unittest
from riemann import simple
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
