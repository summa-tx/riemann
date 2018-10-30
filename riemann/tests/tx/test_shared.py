import riemann
import unittest
from riemann import tx


class TestByteData(unittest.TestCase):

    def setUp(self):
        pass

    def test_iter(self):
        bd = tx.ByteData()
        bd._bytes.extend(b'\x00\x00')
        i = iter(bd)
        next(i)
        next(i)
        self.assertRaises(StopIteration, i.__next__)

    def test_iadd_error(self):
        bd = tx.ByteData()
        with self.assertRaises(TypeError) as context:
            bd += 'alphabet'

        self.assertIn('unsupported operand type(s) for +=: '
                      'ByteData and str', str(context.exception))

    def test_setattr_error(self):
        bd = tx.ByteData()
        bd._make_immutable()
        with self.assertRaises(TypeError) as context:
            bd.a = 'aaaaa'

        self.assertIn('cannot be written to.', str(context.exception))

    def test_repr(self):
        bd = tx.ByteData()
        bd._bytes.extend(b'\xff')

        self.assertEqual(bd.__repr__(), "ByteData: bytearray(b'\\xff')")

    def test_find(self):
        bd = tx.ByteData()
        bd._bytes.extend(b'\xff\xdd\x88')

        self.assertEqual(bd.find(b'\xff'), 0)
        self.assertEqual(bd.find(b'\xdd'), 1)
        self.assertEqual(bd.find(b'\x88'), 2)
        self.assertEqual(bd.find(b'\x00'), -1)

        bd2 = tx.ByteData()
        bd2._bytes.extend(b'\xaa')

        self.assertEqual(bd.find(bd2), -1)

    def test_hex(self):
        t = b'\xff\xdd\x88'
        bd = tx.ByteData()
        bd._bytes.extend(t)

        self.assertEqual(bd.hex(), t.hex())

    def test_ne_error(self):
        with self.assertRaises(TypeError) as context:
            bd = tx.ByteData()
            bd == 'hello world'

        self.assertIn(
            'Equality not supported for ByteData and ',
            str(context.exception))


class TestVarInt(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        riemann.select_network('bitcoin_main')

    def test_one_byte(self):
        res = tx.VarInt(0xfb)
        self.assertEqual(res, b'\xfb')
        self.assertIsInstance(res, tx.VarInt)

    def test_one_byte_boundary(self):
        res = tx.VarInt(0xff)
        self.assertEqual(res, b'\xfd' + b'\xff\x00')
        self.assertIsInstance(res, tx.VarInt)

    def test_two_bytes(self):
        res = tx.VarInt(0xffff)
        self.assertEqual(res, b'\xfd' + (b'\xff' * 2))
        self.assertIsInstance(res, tx.VarInt)

    def test_four_bytes(self):
        res = tx.VarInt(0xffffffff)
        self.assertEqual(res, b'\xfe' + (b'\xff' * 4))
        self.assertIsInstance(res, tx.VarInt)

    def test_eight_bytes(self):
        res = tx.VarInt(0xffffffffffffffff)
        self.assertEqual(res, b'\xff' + (b'\xff' * 8))
        self.assertIsInstance(res, tx.VarInt)

        res = tx.VarInt(0x0123456789abcdef)
        self.assertEqual(res, b'\xff' + b'\xef\xcd\xab\x89\x67\x45\x23\x01')

        res = tx.VarInt(0x234000000000)  # 6 bytes to test padding
        self.assertEqual(res, b'\xff' + b'\x00\x00\x00\x00\x40\x23\x00\x00')

    def test_negative(self):
        with self.assertRaises(ValueError) as context:
            tx.VarInt(-5)

        self.assertIn('VarInt cannot be less than 0.',
                      str(context.exception))

    def test_too_high(self):
        with self.assertRaises(ValueError) as context:
            tx.VarInt(2 ** 64 + 1)

        self.assertIn('VarInt cannot be greater than (2 ** 64) - 1.',
                      str(context.exception))

    def test_copy(self):
        res = tx.VarInt(0xffffffffffffffff)
        copy = res.copy()
        self.assertEqual(res, copy)
        self.assertIsNot(res, copy)

    def test_from_bytes(self):

        # This test is kinda a joke
        self.assertEqual(tx.VarInt.from_bytes(b'\xfd\x91#'), b'\xfd\x91#')
        self.assertEqual(tx.VarInt.from_bytes(b'\x00'), b'\x00')
        self.assertEqual(tx.VarInt.from_bytes(b'\xff' * 9), b'\xff' * 9)

        with self.assertRaises(ValueError) as context:
            tx.VarInt.from_bytes(b'\xfe')
        self.assertIn(
            'Malformed VarInt. Got: fe',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.VarInt.from_bytes(b'\xfe\x00\x00\x00')
        self.assertIn(
            'Malformed VarInt. Got: fe',
            str(context.exception))

    def test_zcash_compact_enforcement(self):
        riemann.select_network('zcash_overwinter_main')

        with self.assertRaises(ValueError) as context:
            tx.VarInt.from_bytes(b'\xfd\x00\x00')

        self.assertIn(
            'VarInt must be compact. Got:',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.VarInt.from_bytes(b'\xfe\x00\x00\x00\x00')

        self.assertIn(
            'VarInt must be compact. Got:',
            str(context.exception))
