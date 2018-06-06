import unittest
import riemann
from .. import utils
from . import helpers


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        riemann.select_network('bitcoin_main')

    def test_i2le(self):
        self.assertEqual(utils.i2le(0), b'\x00')
        self.assertEqual(utils.i2le(0xff), b'\xff')
        self.assertEqual(utils.i2le(0x0100), b'\x00\x01')
        self.assertEqual(utils.i2le(0xabcdef), b'\xef\xcd\xab')

    def test_i2le_padded(self):
        self.assertEqual(utils.i2le_padded(0, 4), b'\x00' * 4)
        self.assertEqual(utils.i2le_padded(0xff, 1), b'\xff')
        self.assertEqual(utils.i2le_padded(0x0100, 8),
                         b'\x00\x01\x00\x00\x00\x00\x00\x00')
        self.assertEqual(utils.i2le_padded(0xabcdef, 5),
                         b'\xef\xcd\xab\x00\x00')

    def test_le2i(self):
        self.assertEqual(utils.le2i(b'\x00' * 4), 0)
        self.assertEqual(utils.le2i(b'\xff'), 0xff)
        self.assertEqual(utils.le2i(b'\x00\x01\x00\x00\x00\x00\x00\x00'),
                         0x0100)
        self.assertEqual(utils.le2i(b'\xef\xcd\xab\x00\x00'), 0xabcdef)

    def test_be2i(self):
        self.assertEqual(utils.be2i(b'\x00' * 4), 0)
        self.assertEqual(utils.be2i(b'\xff'), 0xff)
        self.assertEqual(utils.be2i(b'\x00\x01\x00\x00\x00\x00\x00\x00'),
                         0x01000000000000)
        self.assertEqual(utils.be2i(b'\xef\xcd\xab\x00\x00'), 0xefcdab0000)

    def test_i2be(self):
        self.assertEqual(
            utils.i2be(0),
            b'\x00')
        self.assertEqual(
            utils.i2be(0xff),
            b'\xff')
        self.assertEqual(
            utils.i2be(0xffff),
            b'\xff\xff')

    def test_i2be_padded(self):
        self.assertEqual(
            utils.i2be_padded(0, 5),
            b'\x00' * 5)
        self.assertEqual(
            utils.i2be_padded(0xff, 3),
            b'\x00\x00\xff')
        self.assertEqual(
            utils.i2be_padded(0xffff, 2),
            b'\xff\xff')

    def test_change_endianness(self):
        self.assertEqual(utils.change_endianness(b'\x00'), b'\x00')
        self.assertEqual(utils.change_endianness(b'\x00\xaa'), b'\xaa\x00')
        self.assertEqual(utils.change_endianness(b'\xff'), b'\xff')
        self.assertEqual(utils.change_endianness(b'\x00\xab\xcd\xef'),
                         b'\xef\xcd\xab\x00')

    def test_rmd160(self):
        '''
        https://homes.esat.kuleuven.be/~bosselae/ripemd160.html
        '''
        self.assertEqual(
            utils.rmd160(b''),
            bytes.fromhex('9c1185a5c5e9fc54612808977ee8f548b2258d31'))
        self.assertEqual(
            utils.rmd160('message digest'.encode('utf-8')),
            bytes.fromhex('5d0689ef49d2fae572b881b123a85ffa21595f36'))

    def test_sha256(self):
        '''
        https://www.di-mgt.com.au/sha_testvectors.html
        '''
        self.assertEqual(
            utils.sha256(b''),
            bytes.fromhex('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'))  # noqa: E501
        self.assertEqual(
            utils.sha256('abc'.encode('utf-8')),
            bytes.fromhex('ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'))  # noqa: E501
        self.assertEqual(
            utils.sha256(helpers.P2WSH['ser']['witnesses'][0]['wit_script']),
            helpers.P2WSH['ser']['ins'][0]['pk_script'][2:])

    def test_hash160(self):
        self.assertEqual(
            utils.hash160(bytes.fromhex(helpers.PK['human'][0]['pk'])),
            helpers.PK['ser'][0]['pkh'])
        self.assertEqual(
            utils.hash160(bytes.fromhex(helpers.PK['human'][1]['pk'])),
            helpers.PK['ser'][1]['pkh'])
        self.assertEqual(
            utils.hash160(helpers.P2WPKH_ADDR['pubkey']),
            helpers.P2WPKH_ADDR['pkh'])

    def test_hash256(self):
        '''
        http://www.herongyang.com/Bitcoin/Block-Data-Calculate-Double-SHA256-with-Python.html
        '''
        self.assertEqual(
            utils.hash256(b'\x00'),
            bytes.fromhex('1406e05881e299367766d313e26c05564ec91bf721d31726bd6e46e60689539a'))  # noqa: E501
        self.assertEqual(
            utils.hash256('abc'.encode('utf-8')),
            bytes.fromhex('4f8b42c22dd3729b519ba6f68d2da7cc5b2d606d05daed5ad5128cc03e6c6358'))  # noqa: E501
        self.assertEqual(
            utils.hash256('The quick brown fox jumps over the lazy dog'.encode('utf-8')),  # noqa: E501
            bytes.fromhex('6d37795021e544d82b41850edf7aabab9a0ebe274e54a519840c4666f35b3937'))  # noqa: E501

    def test_blake256(self):
        self.assertEqual(
            utils.blake256('').hex(),
            '716f6e863f744b9ac22c97ec7b76ea5f5908bc5b2f67c61510bfc4751384ea7a')
        self.assertEqual(
            utils.blake256('a').hex(),
            '43234ff894a9c0590d0246cfc574eb781a80958b01d7a2fa1ac73c673ba5e311')

    def test_decred_snowflakes(self):
        riemann.select_network('decred_main')
        self.assertEqual(utils.hash160(b'\x00'),
                         utils.rmd160(utils.blake256(b'\x00')))

        self.assertEqual(utils.hash256(b'\x00'),
                         utils.blake256(utils.blake256(b'\x00')))

    def test_blake2b(self):
        '''
        https://github.com/BLAKE2/BLAKE2/blob/master/testvectors/blake2b-kat.txt
        '''
        self.assertEqual(
            utils.blake2b(b'',
                          key=bytes.fromhex('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f')),  # noqa: E501
            bytes.fromhex('10ebb67700b1868efb4417987acf4690ae9d972fb7a590c2f02871799aaa4786b5e996e8f0f4eb981fc214b005f42d2ff4233499391653df7aefcbc13fc51568'))  # noqa: E501

        self.assertEqual(
            utils.blake2b(b'\x00',
                          key=bytes.fromhex('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f')),  # noqa: E501
            bytes.fromhex('961f6dd1e4dd30f63901690c512e78e4b45e4742ed197c3c5e45c549fd25f2e4187b0bc9fe30492b16b0d0bc4ef9b0f34c7003fac09a5ef1532e69430234cebd'))  # noqa: E501

        self.assertEqual(
            utils.blake2b(bytes.fromhex('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f6061'),  # noqa: E501
                          key=bytes.fromhex('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f')),  # noqa: E501
            bytes.fromhex('bb2039ec287091bcc9642fc90049e73732e02e577e2862b32216ae9bedcd730c4c284ef3968c368b7d37584f97bd4b4dc6ef6127acfe2e6ae2509124e66c8af4'))  # noqa: E501

    def test_blake2s(self):
        self.assertEqual(
            utils.blake2s(b'',
                          key=bytes.fromhex('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f')),  # noqa: E501
            bytes.fromhex('48a8997da407876b3d79c0d92325ad3b89cbb754d86ab71aee047ad345fd2c49'))  # noqa: E501

        self.assertEqual(
            utils.blake2s(b'\x00',
                          key=bytes.fromhex('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f')),  # noqa: E501
            bytes.fromhex('40d15fee7c328830166ac3f918650f807e7e01e177258cdc0a39b11f598066f1'))  # noqa: E501

        self.assertEqual(
            utils.blake2s(bytes.fromhex('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f'),  # noqa: E501
                          key=bytes.fromhex('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f')),  # noqa: E501
            bytes.fromhex('8975b0577fd35566d750b362b0897a26c399136df07bababbde6203ff2954ed4'))  # noqa: E501
