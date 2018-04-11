import unittest
from .. import tx
from .. import utils


class TestVarInt(unittest.TestCase):

    def setUp(self):
        pass

    def test_one_byte(self):
        res = tx.VarInt(0xfb)
        self.assertEqual(res, b'\xfb')
        self.assertIsInstance(res, tx.VarInt)

    def test_one_byte_boundary(self):
        res = tx.VarInt(0xff)
        self.assertEqual(res, b'\xfd' + b'\xff')
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


class TestTx(unittest.TestCase):

    def setUp(self):
        pass

    def test_everything(self):
        version = bytearray([0] * 4)
        flag = b'\x00\x01'
        tx_ins = [
            tx.TxIn(
                outpoint=tx.Outpoint(
                    bytearray([0xee] * 32), bytearray([0] * 4)),
                script=bytearray([0xff] * 20),
                sequence=bytearray([0xaa] * 4)
            )
        ]
        tx_outs = [
            tx.TxOut(
                value=bytearray(utils.i2lx(0xccbbccbbccbbccbb)),
                pk_script=bytearray([0xdd] * 32)
            )
        ]
        tx_witnesses = [
            tx.TxWitness(
                [
                    tx.StackItem(bytearray([0x88] * 18)),
                    tx.StackItem(bytearray([0x99] * 18))
                ]
            )
        ]
        lock_time = bytearray([0xff] * 4)

        res = tx.Tx(version, flag, tx_ins, tx_outs, tx_witnesses, lock_time)
        print(res.hex())
