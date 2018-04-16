import unittest
from .. import helpers
from ...tx import tx
from ... import utils


# On chain legacy tx p2sh -> p2pkh tx
# https://blockchain.info/rawtx/0739d0c7b7b7ff5f991e8e3f72a6f5eb56563880df982c4ab813cd71bc7a6a03?format=hex

class TestByteData(unittest.TestCase):

    def setUp(self):
        pass


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

    def setUp(self):
        pass

    def test_create_outpoint(self):
        outpoint_index = helpers.outpoint_index
        outpoint_tx_id = helpers.outpoint_tx_id

        outpoint = tx.Outpoint(outpoint_tx_id, outpoint_index)

        self.assertEqual(outpoint.tx_id, outpoint_tx_id)
        self.assertEqual(outpoint.index, outpoint_index)
        self.assertEqual(outpoint, outpoint_tx_id + outpoint_index)

    def test_create_outpoint_short_tx_id(self):
        outpoint_index = helpers.outpoint_index
        outpoint_tx_id = bytearray(b'\xff')

        with self.assertRaises(ValueError) as context:
            tx.Outpoint(outpoint_tx_id, outpoint_index)

        self.assertIn('Expected bytes-like object with length 32. ',
                      str(context.exception))

    def test_create_outpoint_str_tx_id(self):
        outpoint_index = helpers.outpoint_index
        outpoint_tx_id = 'Hello world'

        with self.assertRaises(ValueError) as context:
            tx.Outpoint(outpoint_tx_id, outpoint_index)

        self.assertIn('Expected bytes-like object. ',
                      str(context.exception))

    def test_create_outpoint_long_index(self):
        outpoint_index = utils.i2le_padded(0, 5)
        outpoint_tx_id = helpers.outpoint_tx_id

        with self.assertRaises(ValueError) as context:
            tx.Outpoint(outpoint_tx_id, outpoint_index)

        self.assertIn('Expected bytes-like object with length 4. ',
                      str(context.exception))

    def test_create_outpoint_no_index(self):
        outpoint_index = None
        outpoint_tx_id = helpers.outpoint_tx_id

        with self.assertRaises(ValueError) as context:
            tx.Outpoint(outpoint_tx_id, outpoint_index)

        self.assertIn('Expected bytes-like object. ',
                      str(context.exception))


class TestTxIn(unittest.TestCase):

    def setUp(self):
        outpoint_index = helpers.outpoint_index
        outpoint_tx_id = helpers.outpoint_tx_id

        self.stack_script = helpers.stack_script
        self.redeem_script = helpers.redeem_script
        self.sequence = helpers.sequence
        self.outpoint = tx.Outpoint(outpoint_tx_id, outpoint_index)

    def test_create_input(self):
        tx_in = tx.TxIn(self.outpoint, self.stack_script,
                        self.redeem_script, self.sequence)

        self.assertEqual(tx_in.outpoint, self.outpoint)
        self.assertEqual(tx_in.stack_script, self.stack_script)
        self.assertEqual(tx_in.redeem_script, self.redeem_script)
        self.assertEqual(tx_in.sequence, self.sequence)
        self.assertEqual(tx_in, helpers.tx_in)

    def test_copy(self):
        tx_in = tx.TxIn(self.outpoint, self.stack_script,
                        self.redeem_script, self.sequence)

        tx_in_copy = tx_in.copy()

        self.assertEqual(tx_in, tx_in_copy)  # They should be equal
        self.assertIsNot(tx_in, tx_in_copy)  # But not the same object


class TestTxOut(unittest.TestCase):

    def setUp(self):
        self.value = helpers.output_value_0
        self.output_script = helpers.output_script_0

    def test_create_output(self):
        tx_out = tx.TxOut(self.value, self.output_script)
        self.assertEqual(tx_out, helpers.tx_out_0)

    def test_copy(self):
        tx_out = tx.TxOut(self.value, self.output_script)
        tx_out_copy = tx_out.copy()

        self.assertEqual(tx_out, tx_out_copy)  # They should be equal
        self.assertIsNot(tx_out, tx_out_copy)  # But not the same object


class TestWitnessStackItem(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_stack_item(self):
        pass


class TestInputWitness(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_witness(self):
        pass


class TestTx(unittest.TestCase):

    def setUp(self):
        self.outpoint_index = helpers.outpoint_index
        self.outpoint_tx_id = helpers.outpoint_tx_id

        self.stack_script = helpers.stack_script
        self.redeem_script = helpers.redeem_script
        self.sequence = helpers.sequence
        self.outpoint = tx.Outpoint(self.outpoint_tx_id, self.outpoint_index)

        self.tx_in = tx.TxIn(self.outpoint, self.stack_script,
                             self.redeem_script, self.sequence)

        self.value_0 = helpers.output_value_0
        self.output_script_0 = helpers.output_script_0
        self.value_1 = helpers.output_value_1
        self.output_script_1 = helpers.output_script_1

        self.tx_out_0 = tx.TxOut(self.value_0, self.output_script_0)
        self.tx_out_1 = tx.TxOut(self.value_1, self.output_script_1)

        self.version = helpers.version
        self.flag = None
        self.tx_ins = [self.tx_in]
        self.tx_outs = [self.tx_out_0, self.tx_out_1]
        self.tx_witnesses = None
        self.lock_time = helpers.lock_time

    # Convenience monotest
    def test_everything_witness(self):
        version = bytearray([0] * 4)
        flag = b'\x00\x01'
        outpoint_index = utils.i2le_padded(0, 4)
        outpoint_tx_id = bytearray(bytearray.fromhex(
            '10399b3f20cbdd4b5ac3f823afdba28b'
            '9f70e21437a59b312a1b62c42c5cd101'))[::-1]
        outpoint = tx.Outpoint(outpoint_tx_id, outpoint_index)

        sequence = utils.i2le_padded(0, 4)

        script = bytearray(bytearray.fromhex('473044022000e02ea97289a35181a9bfabd324f12439410db11c4e94978cdade6a665bf1840220458b87c34d8bb5e4d70d01041c7c2d714ea8bfaca2c2d2b1f9e5749c3ee17e3d012102ed0851f0b4c4458f80e0310e57d20e12a84642b8e097fe82be229edbd7dbd53920f6665740b1f950eb58d646b1fae9be28cef842da5e51dc78459ad2b092e7fd6e514c5163a914bb408296de2420403aa79eb61426bb588a08691f8876a91431b31321831520e346b069feebe6e9cf3dd7239c670400925e5ab17576a9140d22433293fe9652ea00d21c5061697aef5ddb296888ac'))  # noqa: E501

        tx_in = tx.TxIn(outpoint, script, bytearray(), sequence)
        tx_ins = [tx_in]

        tx_outs = [
            tx.TxOut(
                value=bytearray(utils.i2le_padded(2000, 8)),
                output_script=bytearray(bytearray.fromhex('76a914f2539f42058da784a9d54615ad074436cf3eb85188ac')))  # noqa: E501
        ]
        tx_witnesses = [
            tx.InputWitness(
                [
                    tx.WitnessStackItem(bytearray([0x88] * 18)),
                    tx.WitnessStackItem(bytearray([0x99] * 18))
                ]
            )
        ]
        lock_time = bytearray([0xff] * 4)

        tx.Tx(version, flag, tx_ins, tx_outs, tx_witnesses, lock_time)

        # TODO: needs assertions

    def test_everything(self):
        version = utils.i2le_padded(1, 4)
        outpoint_index = utils.i2le_padded(0, 4)
        outpoint_tx_id = bytearray(bytearray.fromhex(
            '10399b3f20cbdd4b5ac3f823afdba28b'
            '9f70e21437a59b312a1b62c42c5cd101'))[::-1]
        outpoint = tx.Outpoint(outpoint_tx_id, outpoint_index)

        sequence = utils.i2le_padded(0, 4)

        script = bytearray(bytearray.fromhex('473044022000e02ea97289a35181a9bfabd324f12439410db11c4e94978cdade6a665bf1840220458b87c34d8bb5e4d70d01041c7c2d714ea8bfaca2c2d2b1f9e5749c3ee17e3d012102ed0851f0b4c4458f80e0310e57d20e12a84642b8e097fe82be229edbd7dbd53920f6665740b1f950eb58d646b1fae9be28cef842da5e51dc78459ad2b092e7fd6e514c5163a914bb408296de2420403aa79eb61426bb588a08691f8876a91431b31321831520e346b069feebe6e9cf3dd7239c670400925e5ab17576a9140d22433293fe9652ea00d21c5061697aef5ddb296888ac'))  # noqa: E501

        tx_in = tx.TxIn(outpoint, script, bytearray(), sequence)
        tx_ins = [tx_in]

        tx_outs = [
            tx.TxOut(
                value=bytearray(utils.i2le_padded(2000, 8)),
                output_script=bytearray(bytearray.fromhex('76a914f2539f42058da784a9d54615ad074436cf3eb85188ac')))  # noqa: E501
        ]

        lock_time = utils.i2le_padded(0, 4)

        res = tx.Tx(version, None, tx_ins, tx_outs, None, lock_time)

        self.assertEqual(res.hex(), helpers.RAW_P2SH_TO_P2PKH)

    def test_create_tx(self):
        t = tx.Tx(self.version, self.flag, self.tx_ins, self.tx_outs,
                  self.tx_witnesses, self.lock_time)

        self.assertEqual(t, helpers.P2PKH_SPEND)

    def test_copy(self):
        t = tx.Tx(self.version, self.flag, self.tx_ins, self.tx_outs,
                  self.tx_witnesses, self.lock_time)

        t_copy = t.copy()

        self.assertEqual(t, t_copy)
        self.assertIsNot(t, t_copy)
