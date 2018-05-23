# flake8: noqa

import unittest
import riemann
from .. import helpers
from ...encoding import base58

# https://github.com/decred/dcrd/blob/dcc58786d33e557641948e1ac3f48785b2d11609/dcrutil/address_test.go
DCR_ADDR = (
    ('DsU7xcg53nxaKLLcAUSKyRndjG78Z2VZnX9', b'\x07\x3f', bytes([0x22, 0x9e, 0xba, 0xc3, 0x0e, 0xfd, 0x6a, 0x69, 0xee, 0xc9, 0xc1, 0xa4, 0x8e, 0x04, 0x8b, 0x7c, 0x97, 0x5c, 0x25, 0xf2])),
    ('DsUZxxoHJSty8DCfwfartwTYbuhmVct7tJu', b'\x07\x3f', bytes([0x27, 0x89, 0xd5, 0x8c, 0xfa, 0x09, 0x57, 0xd2, 0x06, 0xf0, 0x25, 0xc2, 0xaf, 0x05, 0x6f, 0xc8, 0xa7, 0x7c, 0xeb, 0xb0])),
    ('DcuQKx8BES9wU7C6Q5VmLBjw436r27hayjS', b'\x07\x1a', bytes([0xf0, 0xb4, 0xe8, 0x51, 0x00, 0xae, 0xe1, 0xa9, 0x96, 0xf2, 0x29, 0x15, 0xeb, 0x3c, 0x3f, 0x76, 0x4d, 0x53, 0x77, 0x9a]))
)


class TestBase58(unittest.TestCase):

    def tearDown(self):
        riemann.select_network('bitcoin_main')

    def test_decode_error(self):
        with self.assertRaises(ValueError) as context:
            base58.decode('13VmALKHkCdSN1JULkP6RqW3LcbpWvgryW')

        self.assertIn(
            'hashed base58 has bad checksum ',
            str(context.exception))

    def test_decode_without_checksum(self):
        self.assertEqual(
            base58.decode('1P86rvoC4bTympTEdXnw9HhWVxb4', False),
            b'\x00' + helpers.PK['ser'][0]['pkh'])

    def test_encode_with_checksum(self):
        self.assertEqual(
            base58.encode_with_checksum(b'\x00' + helpers.PK['ser'][0]['pkh']),
            helpers.ADDR[0]['p2pkh'])

    def test_decode_with_checksum(self):
        self.assertEqual(
            b'\x00' + helpers.PK['ser'][0]['pkh'],
            base58.decode_with_checksum(helpers.ADDR[0]['p2pkh']))

    def test_has_checksum(self):
        self.assertTrue(
            base58.has_checksum(helpers.ADDR[0]['p2pkh']))
        self.assertFalse(base58.has_checksum('1P86rvoC4bTympTEdXnw9HhWVxb4'))

    def test_from_long_error(self):
        with self.assertRaises(ValueError) as context:
            base58.from_long(56, 1, 5, lambda: 1 / 0)  # lambda always raises

        self.assertIn(
            "can't convert to character corresponding to",
            str(context.exception))

    def test_decred_addresses(self):
        riemann.select_network('decred_main')
        for addr in DCR_ADDR:
            expected = addr[0]
            addr_hash = bytearray()
            addr_hash.extend(addr[1])
            addr_hash.extend(addr[2])
            self.assertEqual(expected, base58.encode(addr_hash))
