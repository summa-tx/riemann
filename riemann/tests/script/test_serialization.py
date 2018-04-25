import unittest
import riemann
from riemann.tests import helpers
from riemann.script import serialization as ser


class TestSerialization(unittest.TestCase):

    def tearDown(self):
        riemann.select_network('bitcoin_main')

    def test_serialize(self):
        self.assertEqual(
            ser.serialize(helpers.MSIG_TWO_TWO_SCRIPT),
            helpers.MSIG_TWO_TWO_SERIALIZED_SCRIPT)
        self.assertEqual(
            ser.serialize('OP_IF'),
            bytes([99]))

    def test_serialize_error(self):
        with self.assertRaises(NotImplementedError) as context:
            ser.serialize('00' * 77)
        self.assertIn(
            'OP_PUSHDATA1-4 not supported yet.',
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
            ser.hex_serialize(helpers.MSIG_TWO_TWO_SCRIPT),
            helpers.MSIG_TWO_TWO_SERIALIZED_SCRIPT.hex())

        self.assertEqual(
            ser.hex_serialize('OP_IF'),
            bytes([99]).hex())

    def test_deserialize(self):
        self.assertEqual(
            helpers.MSIG_TWO_TWO_SCRIPT,
            ser.deserialize(helpers.MSIG_TWO_TWO_SERIALIZED_SCRIPT))

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
            helpers.MSIG_TWO_TWO_SCRIPT,
            ser.hex_deserialize(helpers.MSIG_TWO_TWO_SERIALIZED_SCRIPT.hex()))

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
