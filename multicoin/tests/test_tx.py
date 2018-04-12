import unittest
import binascii
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

    # Convenience monotest
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
                value=bytearray(utils.i2le(21000000) + (b'\x00' * 4)),
                pk_script=bytearray(binascii.unhexlify('5221022626e955ea6ea6d98850c994f9107b036b1334f18ca8830bfff1295d21cfdb702103b287eaf122eea69030a0e9feed096bed8045c8b98bec453e1ffac7fbdbd4bb7152ae'))
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
        print('')
        print(res.hex())
        print('')
        print(res.tx_id.hex())
        print('')
        print(res.wtx_id.hex())


class TestOutpoint(unittest.TestCase):

    def test_create_outpoint(self):
        outpoint_index = utils.i2le_padded(0, 4)
        outpoint_tx_id = bytearray(binascii.unhexlify(
            '51b78168d94ec307e2855697209275d4'
            '77e05d8647caf29cb9e38fb6a4661145'))[::-1]
        outpoint = tx.Outpoint(outpoint_tx_id, outpoint_index)

        self.assertEqual(
            outpoint.hex(),
            '451166a4b68fe3b99cf2ca47865de077d475'
            '9220975685e207c34ed96881b75100000000')
