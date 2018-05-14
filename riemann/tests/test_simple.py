import unittest
from riemann import simple
from riemann.tests import helpers
from riemann.script import serialization as script_ser


class TestSimple(unittest.TestCase):

    def setUp(self):
        pass

    def test_p2sh_input(self):

        outpoint = simple.outpoint(
            helpers.P2SH_PUSHDATA1_TX_ID, helpers.P2SH_PUSHDATA1_TX_INDEX)
        tx_p2sh_input = simple.p2sh_input(
            outpoint, helpers.P2SH_PUSHDATA1_STACK_SCRIPT,
            helpers.P2SH_PUSHDATA1_REDEEM_SCRIPT, sequence=None)

        self.assertTrue(tx_p2sh_input.is_p2sh())

        self.assertTrue(isinstance(tx_p2sh_input.stack_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.stack_script,
            script_ser.serialize(helpers.P2SH_PUSHDATA1_STACK_SCRIPT))

        self.assertTrue(isinstance(tx_p2sh_input.redeem_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.redeem_script,
            script_ser.serialize(script_ser.hex_serialize(
                helpers.P2SH_PUSHDATA1_REDEEM_SCRIPT)))

        self.assertTrue(isinstance(tx_p2sh_input.outpoint.tx_id, bytes))
        self.assertEqual(
            tx_p2sh_input.outpoint.tx_id[::-1].hex(),
            helpers.P2SH_PUSHDATA1_TX_ID)

        self.assertTrue(isinstance(tx_p2sh_input.outpoint.index, bytes))
        self.assertEqual(
            int(tx_p2sh_input.outpoint.index.hex()),
            helpers.P2SH_PUSHDATA1_TX_INDEX)

    def test_p2sh_input_and_witness(self):

        outpoint = simple.outpoint(
            helpers.P2SH_PUSHDATA1_TX_ID, helpers.P2SH_PUSHDATA1_TX_INDEX)
        (tx_p2sh_input, witness) = simple.p2sh_input_and_witness(
            outpoint, helpers.P2SH_PUSHDATA1_STACK_SCRIPT,
            helpers.P2SH_PUSHDATA1_REDEEM_SCRIPT, sequence=None)

        self.assertTrue(tx_p2sh_input.is_p2sh())
        self.assertEqual(witness, b'\x00')

        self.assertTrue(isinstance(tx_p2sh_input.stack_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.stack_script,
            script_ser.serialize(helpers.P2SH_PUSHDATA1_STACK_SCRIPT))

        self.assertTrue(isinstance(tx_p2sh_input.redeem_script, bytearray))
        self.assertEqual(
            tx_p2sh_input.redeem_script,
            script_ser.serialize(script_ser.hex_serialize(
                helpers.P2SH_PUSHDATA1_REDEEM_SCRIPT)))

        self.assertTrue(isinstance(tx_p2sh_input.outpoint.tx_id, bytes))
        self.assertEqual(
            tx_p2sh_input.outpoint.tx_id[::-1].hex(),
            helpers.P2SH_PUSHDATA1_TX_ID)

        self.assertTrue(isinstance(tx_p2sh_input.outpoint.index, bytes))
        self.assertEqual(
            int(tx_p2sh_input.outpoint.index.hex()),
            helpers.P2SH_PUSHDATA1_TX_INDEX)

    def test_p2wsh_input_and_witness(self):
        pass
