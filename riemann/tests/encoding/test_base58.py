import unittest
from .. import helpers
from ...encoding import base58


class TestBase58(unittest.TestCase):

    def test_decode_error(self):
        with self.assertRaises(ValueError) as context:
            base58.decode('13VmALKHkCdSN1JULkP6RqW3LcbpWvgryW')

        self.assertIn(
            'hashed base58 has bad checksum ',
            str(context.exception))

    def test_decode_without_checksum(self):
        self.assertEqual(
            base58.decode('1P86rvoC4bTympTEdXnw9HhWVxb4', False),
            b'\x00' + helpers.PKH_0)

    def test_encode_with_checksum(self):
        self.assertEqual(
            base58.encode_with_checksum(b'\x00' + helpers.PKH_0),
            helpers.P2PKH_0)

    def test_decode_with_checksum(self):
        self.assertEqual(
            b'\x00' + helpers.PKH_0,
            base58.decode_with_checksum(helpers.P2PKH_0))

    def test_has_checksum(self):
        self.assertTrue(
            base58.has_checksum(helpers.P2PKH_0))
        self.assertFalse(base58.has_checksum('1P86rvoC4bTympTEdXnw9HhWVxb4'))

    def test_from_long_error(self):
        with self.assertRaises(ValueError) as context:
            base58.from_long(56, 1, 5, lambda: 1 / 0)  # lambda always raises

        self.assertIn(
            "can't convert to character corresponding to",
            str(context.exception))
