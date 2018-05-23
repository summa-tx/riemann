import unittest
import riemann
from riemann.tests import helpers
from riemann.script import serialization as ser


class TestSerialization(unittest.TestCase):

    def tearDown(self):
        riemann.select_network('bitcoin_main')

    def test_serialize(self):
        self.assertEqual(
            ser.serialize(helpers.MSIG_2_2['redeem_script']),
            helpers.MSIG_2_2['ser_script'])
        self.assertEqual(
            ser.serialize('OP_IF'),
            bytes([99]))

    def test_serialize_error(self):
        with self.assertRaises(NotImplementedError) as context:
            ser.serialize('00' * 65999)
        self.assertIn(
            'Hex string too long to serialize.',
            str(context.exception))

        with self.assertRaises(NotImplementedError) as context:
            ser.serialize('OP_PUSHDATA4')
        self.assertIn(
            'OP_PUSHDATA4 is a bad idea.',
            str(context.exception))

        with self.assertRaises(NotImplementedError) as context:
            ser.serialize('OP_CODESEPARATOR')
        self.assertIn(
            'OP_CODESEPARATOR is a bad idea.',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            ser.serialize('OP_NOTAREALOPCODE')
        self.assertIn(
            'non-hexadecimal number found',
            str(context.exception))

    def test_hex_serialize(self):
        self.assertEqual(
            ser.hex_serialize(helpers.MSIG_2_2['redeem_script']),
            helpers.MSIG_2_2['ser_script'].hex())

        self.assertEqual(
            ser.hex_serialize('OP_IF'),
            bytes([99]).hex())

    def test_hex_serialize_OP_PUSHDATA1(self):
        self.assertEqual(
            ser.hex_serialize(
                helpers.P2SH_PD1['human']['ins'][0]['script_sig']),
            helpers.P2SH_PD1['ser']['ins'][0]['script_sig'].hex())

    def test_hex_deserialize_OP_PUSHDATA1(self):
        self.assertEqual(
            ser.hex_deserialize(
                helpers.P2SH_PD1['ser']['ins'][0]['script_sig'].hex()),
            helpers.P2SH_PD1['human']['ins'][0]['script_sig'])

    def test_hex_serialize_OP_PUSHDATA2(self):
        self.assertEqual(
            ser.hex_serialize(
                helpers.P2SH_PD2['human']['ins'][0]['script_sig']),
            helpers.P2SH_PD2['ser']['ins'][0]['script_sig'].hex())

    def test_hex_deserialize_OP_PUSHDATA2(self):
        self.assertEqual(
            ser.hex_deserialize(
                helpers.P2SH_PD2['ser']['ins'][0]['script_sig'].hex()),
            helpers.P2SH_PD2['human']['ins'][0]['script_sig'])

    def test_deserialize(self):
        self.assertEqual(
            helpers.MSIG_2_2['redeem_script'],
            ser.deserialize(helpers.MSIG_2_2['ser_script']))

        self.assertEqual(
            'OP_IF',
            ser.deserialize(bytes([99])))

    def test_deserialize_error(self):
        with self.assertRaises(IndexError) as context:
            ser.deserialize(b'\x05\x00\x00')
        self.assertIn(
            'Push 5 caused out of bounds exception.',
            str(context.exception))

        with self.assertRaises(NotImplementedError) as context:
            ser.deserialize(b'\xab')
        self.assertIn(
            'OP_CODESEPARATOR is a bad idea.',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            ser.deserialize(b'\xfe')
        self.assertIn(
            'Unsupported opcode. Got 0xfe',
            str(context.exception))

    def test_hex_deserialize(self):
        self.assertEqual(
            helpers.MSIG_2_2['redeem_script'],
            ser.hex_deserialize(helpers.MSIG_2_2['ser_script'].hex()))

        self.assertEqual(
            'OP_IF',
            ser.hex_deserialize('63'))

    def test_overwrites(self):
        riemann.select_network('decred_main')
        self.assertEqual(
            'OP_BLAKE256',
            ser.hex_deserialize('a8'))
        self.assertEqual(
            'a8',
            ser.hex_serialize('OP_BLAKE256'))
        self.assertEqual(
            'OP_SHA256',
            ser.hex_deserialize('c0'))
        self.assertEqual(
            'c0',
            ser.hex_serialize('OP_SHA256'))

    def test_pushdata4_error(self):
        with self.assertRaises(NotImplementedError) as context:
            ser.deserialize(bytes([78]))

        self.assertIn(
            'OP_PUSHDATA4 is a bad idea.',
            str(context.exception))
