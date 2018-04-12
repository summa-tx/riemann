import unittest
import binascii
from .. import tx
from .. import utils


'https://blockchain.info/rawtx/0739d0c7b7b7ff5f991e8e3f72a6f5eb56563880df982c4ab813cd71bc7a6a03?format=hex'
'010000000101d15c2cc4621b2a319ba53714e2709f8ba2dbaf23f8c35a4bddcb203f9b391000000000df473044022000e02ea97289a35181a9bfabd324f12439410db11c4e94978cdade6a665bf1840220458b87c34d8bb5e4d70d01041c7c2d714ea8bfaca2c2d2b1f9e5749c3ee17e3d012102ed0851f0b4c4458f80e0310e57d20e12a84642b8e097fe82be229edbd7dbd53920f6665740b1f950eb58d646b1fae9be28cef842da5e51dc78459ad2b092e7fd6e514c5163a914bb408296de2420403aa79eb61426bb588a08691f8876a91431b31321831520e346b069feebe6e9cf3dd7239c670400925e5ab17576a9140d22433293fe9652ea00d21c5061697aef5ddb296888ac0000000001d0070000000000001976a914f2539f42058da784a9d54615ad074436cf3eb85188ac00000000'


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


class TestTxIn(unittest.TestCase):

    def test_create_input(self):
        outpoint_index = utils.i2le_padded(0, 4)
        outpoint_tx_id = bytearray(binascii.unhexlify(
            '10399b3f20cbdd4b5ac3f823afdba28b'
            '9f70e21437a59b312a1b62c42c5cd101'))[::-1]
        outpoint = tx.Outpoint(outpoint_tx_id, outpoint_index)

        sequence = utils.i2le_padded(0, 4)

        script = bytearray(binascii.unhexlify('473044022000e02ea97289a35181a9bfabd324f12439410db11c4e94978cdade6a665bf1840220458b87c34d8bb5e4d70d01041c7c2d714ea8bfaca2c2d2b1f9e5749c3ee17e3d012102ed0851f0b4c4458f80e0310e57d20e12a84642b8e097fe82be229edbd7dbd53920f6665740b1f950eb58d646b1fae9be28cef842da5e51dc78459ad2b092e7fd6e514c5163a914bb408296de2420403aa79eb61426bb588a08691f8876a91431b31321831520e346b069feebe6e9cf3dd7239c670400925e5ab17576a9140d22433293fe9652ea00d21c5061697aef5ddb296888ac'))


        tx_in = tx.TxIn(outpoint, script, sequence)
        print('')
        print('Printing TxIn')
        print(tx_in.hex())


class TestTx(unittest.TestCase):

    def setUp(self):
        pass

    # Convenience monotest
    def test_everything_witness(self):
        version = bytearray([0] * 4)
        flag = b'\x00\x01'
        outpoint_index = utils.i2le_padded(0, 4)
        outpoint_tx_id = bytearray(binascii.unhexlify(
            '10399b3f20cbdd4b5ac3f823afdba28b'
            '9f70e21437a59b312a1b62c42c5cd101'))[::-1]
        outpoint = tx.Outpoint(outpoint_tx_id, outpoint_index)

        sequence = utils.i2le_padded(0, 4)

        script = bytearray(binascii.unhexlify('473044022000e02ea97289a35181a9bfabd324f12439410db11c4e94978cdade6a665bf1840220458b87c34d8bb5e4d70d01041c7c2d714ea8bfaca2c2d2b1f9e5749c3ee17e3d012102ed0851f0b4c4458f80e0310e57d20e12a84642b8e097fe82be229edbd7dbd53920f6665740b1f950eb58d646b1fae9be28cef842da5e51dc78459ad2b092e7fd6e514c5163a914bb408296de2420403aa79eb61426bb588a08691f8876a91431b31321831520e346b069feebe6e9cf3dd7239c670400925e5ab17576a9140d22433293fe9652ea00d21c5061697aef5ddb296888ac'))

        tx_in = tx.TxIn(outpoint, script, sequence)
        tx_ins = [tx_in]

        tx_outs = [
            tx.TxOut(
                value=bytearray(utils.i2le_padded(2000, 8)),
                pk_script=bytearray(binascii.unhexlify('76a914f2539f42058da784a9d54615ad074436cf3eb85188ac')))
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
        print('printing witness tx hex')
        print(res.hex())
        print('')
        print('print witness tx_id hex')
        print(res.tx_id.hex())
        print('')
        print('printing witness wtx_id hex')
        print(res.wtx_id.hex())

    def test_everything(self):
        version = utils.i2le_padded(1, 4)
        flag = None
        outpoint_index = utils.i2le_padded(0, 4)
        outpoint_tx_id = bytearray(binascii.unhexlify(
            '10399b3f20cbdd4b5ac3f823afdba28b'
            '9f70e21437a59b312a1b62c42c5cd101'))[::-1]
        outpoint = tx.Outpoint(outpoint_tx_id, outpoint_index)

        sequence = utils.i2le_padded(0, 4)

        script = bytearray(binascii.unhexlify('473044022000e02ea97289a35181a9bfabd324f12439410db11c4e94978cdade6a665bf1840220458b87c34d8bb5e4d70d01041c7c2d714ea8bfaca2c2d2b1f9e5749c3ee17e3d012102ed0851f0b4c4458f80e0310e57d20e12a84642b8e097fe82be229edbd7dbd53920f6665740b1f950eb58d646b1fae9be28cef842da5e51dc78459ad2b092e7fd6e514c5163a914bb408296de2420403aa79eb61426bb588a08691f8876a91431b31321831520e346b069feebe6e9cf3dd7239c670400925e5ab17576a9140d22433293fe9652ea00d21c5061697aef5ddb296888ac'))

        tx_in = tx.TxIn(outpoint, script, sequence)
        tx_ins = [tx_in]

        tx_outs = [
            tx.TxOut(
                value=bytearray(utils.i2le_padded(2000, 8)),
                pk_script=bytearray(binascii.unhexlify('76a914f2539f42058da784a9d54615ad074436cf3eb85188ac')))
        ]

        lock_time = utils.i2le_padded(0, 4)

        res = tx.Tx(version, None, tx_ins, tx_outs, None, lock_time)
        print('')
        print('printing legacy tx hex')
        print(res.hex())
        print('')
        print('print legacy tx_id hex')
        print(res.tx_id.hex())














1
