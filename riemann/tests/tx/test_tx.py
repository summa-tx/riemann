import unittest
import riemann
from .. import helpers
from ...tx import tx
from ... import utils


# On chain legacy tx p2sh -> p2pkh tx
# https://blockchain.info/rawtx/0739d0c7b7b7ff5f991e8e3f72a6f5eb56563880df982c4ab813cd71bc7a6a03?format=hex

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

        with self.assertRaises(ValueError) as context:
            tx.VarInt.from_bytes(b'\xfe')
        self.assertIn(
            'Malformed VarInt. Got: fe',
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

        self.assertIn('Expected byte-like object with length 32. ',
                      str(context.exception))

    def test_create_outpoint_str_tx_id(self):
        outpoint_index = helpers.outpoint_index
        outpoint_tx_id = 'Hello world'

        with self.assertRaises(ValueError) as context:
            tx.Outpoint(outpoint_tx_id, outpoint_index)

        self.assertIn('Expected byte-like object. ',
                      str(context.exception))

    def test_create_outpoint_long_index(self):
        outpoint_index = utils.i2le_padded(0, 5)
        outpoint_tx_id = helpers.outpoint_tx_id

        with self.assertRaises(ValueError) as context:
            tx.Outpoint(outpoint_tx_id, outpoint_index)

        self.assertIn('Expected byte-like object with length 4. ',
                      str(context.exception))

    def test_create_outpoint_no_index(self):
        outpoint_index = None
        outpoint_tx_id = helpers.outpoint_tx_id

        with self.assertRaises(ValueError) as context:
            tx.Outpoint(outpoint_tx_id, outpoint_index)

        self.assertIn('Expected byte-like object. ',
                      str(context.exception))

    def test_copy(self):
        outpoint_index = helpers.outpoint_index
        outpoint_tx_id = helpers.outpoint_tx_id

        res = tx.Outpoint(outpoint_tx_id, outpoint_index)
        copy = res.copy()
        self.assertEqual(res, copy)
        self.assertIsNot(res, copy)


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

    def test_long_script_sig(self):
        with self.assertRaises(ValueError) as context:
            tx.TxIn(self.outpoint, b'\x00' * 1000,
                    b'\x00' * 1000, self.sequence)

        self.assertIn(
            'Input script_sig is too long. Expected <= 1650 bytes. '
            'Got 2000 bytes.',
            str(context.exception))


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

    def test_dust_limit_error(self):
        with self.assertRaises(ValueError) as context:
            tx.TxOut(utils.i2le_padded(5, 8), self.output_script)

        self.assertIn(
            'Transaction value below dust limit. '
            'Expected more than 546 sat. Got: 5 sat.',
            str(context.exception))


class TestWitnessStackItem(unittest.TestCase):

    def setUp(self):
        self.stack_item_bytes = helpers.P2WSH_WITNESS_STACK_ITEMS[1]

    def test_create_stack_item(self):
        w = tx.WitnessStackItem(self.stack_item_bytes)
        self.assertEqual(w.item, self.stack_item_bytes)
        self.assertEqual(w.item_len, len(self.stack_item_bytes))
        self.assertEqual(
            w,
            bytes([len(self.stack_item_bytes)]) + self.stack_item_bytes)

    def test_from_bytes(self):
        w = tx.WitnessStackItem.from_bytes(
            bytes([len(self.stack_item_bytes)]) + self.stack_item_bytes)
        self.assertEqual(w.item, self.stack_item_bytes)
        self.assertEqual(w.item_len, len(self.stack_item_bytes))
        self.assertEqual(
            w,
            bytes([len(self.stack_item_bytes)]) + self.stack_item_bytes)


class TestInputWitness(unittest.TestCase):

    def setUp(self):
        self.stack = [tx.WitnessStackItem(b)
                      for b in helpers.P2WSH_WITNESS_STACK_ITEMS]

    def test_create_witness(self):
        iw = tx.InputWitness(self.stack)
        self.assertEqual(len(iw.stack), len(self.stack))
        for item, expected in zip(iw.stack, self.stack):
            self.assertEqual(item, expected)

        bad_stack = [None, 1]
        with self.assertRaises(ValueError) as context:
            tx.InputWitness(bad_stack)

        self.assertIn('Invalid witness stack item. Expected bytes. Got None',
                      str(context.exception))

    def test_from_bytes(self):
        iw = tx.InputWitness.from_bytes(helpers.P2WSH_WITNESS)
        self.assertEqual(len(iw.stack), len(self.stack))
        for item, expected in zip([s.item for s in iw.stack],
                                  [s.item for s in self.stack]):
            self.assertEqual(item, expected)


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
        self.none_flag = None
        self.tx_ins = [self.tx_in]
        self.tx_outs = [self.tx_out_0, self.tx_out_1]
        self.none_witnesses = None
        self.lock_time = helpers.lock_time

        self.segwit_flag = b'\x00\x01'
        self.stack = [tx.WitnessStackItem(b)
                      for b in helpers.P2WSH_WITNESS_STACK_ITEMS]
        self.tx_witnesses = [tx.InputWitness(self.stack)]

    # Convenience monotest
    # Sorta broken.
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
        none_witnesses = [
            tx.InputWitness(
                [
                    tx.WitnessStackItem(bytearray([0x88] * 18)),
                    tx.WitnessStackItem(bytearray([0x99] * 18))
                ]
            )
        ]
        lock_time = bytearray([0xff] * 4)

        tx.Tx(version, flag, tx_ins, tx_outs, none_witnesses, lock_time)

        # TODO: needs assertions

    # Convenience monotest
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

        self.assertEqual(res, helpers.RAW_P2SH_TO_P2PKH)

    # TODO: Break up this monstrosity
    def test_create_tx(self):
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)

        self.assertEqual(t, helpers.P2PKH_SPEND)

        with self.assertRaises(ValueError) as context:
            tx.Tx(self.version, b'\x00\x00', self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)
        self.assertIn(
            'Invald segwit flag. Expected None or ',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.Tx(self.version, self.segwit_flag, self.tx_ins, self.tx_outs,
                  None, self.lock_time)
        self.assertIn(
            'Got segwit flag but no witnesses.',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.Tx(self.version, b'\x00\x01', self.tx_ins, self.tx_outs,
                  [], self.lock_time)
        self.assertIn(
            'Got segwit flag but no witnesses.',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.Tx(self.version, None, self.tx_ins, self.tx_outs,
                  self.tx_witnesses, self.lock_time)
        self.assertIn(
            'Got witnesses but no segwit flag.',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            stack = self.stack + [self.stack[0]]
            witness = tx.InputWitness(stack)
            tx.Tx(self.version, self.segwit_flag, self.tx_ins, self.tx_outs,
                  witness, self.lock_time)
        self.assertIn(
            'Witness and TxIn lists must be same length. ',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.Tx(self.version, self.segwit_flag, self.tx_ins, self.tx_outs,
                  [1 for _ in self.tx_witnesses], self.lock_time)
        self.assertIn(
            'Invalid InputWitness. Expected instance of InputWitness.',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx_ins = [self.tx_ins[0] for _ in range(257)]
            tx.Tx(self.version, self.none_flag, tx_ins, self.tx_outs,
                  None, self.lock_time)
        self.assertIn(
            'Too many inputs or outputs. Stop that.',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx_outs = [self.tx_outs[0] for _ in range(257)]
            tx.Tx(self.version, self.none_flag, self.tx_ins, tx_outs,
                  None, self.lock_time)
        self.assertIn(
            'Too many inputs or outputs. Stop that.',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx_ins = []
            tx.Tx(self.version, self.none_flag, tx_ins, self.tx_outs,
                  None, self.lock_time)
        self.assertIn(
            'Too few inputs or outputs. Stop that.',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx_ins = [1]
            tx.Tx(self.version, self.none_flag, tx_ins, self.tx_outs,
                  None, self.lock_time)
        self.assertIn(
            'Invalid TxIn. Expected instance of TxIn. Got int',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx_outs = [1]
            tx.Tx(self.version, self.none_flag, self.tx_ins, tx_outs,
                  None, self.lock_time)
        self.assertIn(
            'Invalid TxOut. Expected instance of TxOut. Got int',
            str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx_in = self.tx_ins[0].copy(stack_script=b'\x00' * 1616,
                                        redeem_script=None)
            tx_ins = [tx_in for _ in range(255)]
            tx_outs = [self.tx_outs[0] for _ in range(255)]
            tx.Tx(self.version, self.none_flag, tx_ins, tx_outs,
                  None, self.lock_time)

        self.assertIn(
            'Tx is too large. Expect less than 100kB. Got: 440397 bytes',
            str(context.exception))

    def test_tx_id(self):
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)

        self.assertEqual(t.tx_id, helpers.tx_id)
        self.assertEqual(t.tx_id_le, helpers.tx_id_le)

    def test_calculate_fee(self):
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)

        self.assertEqual(t.calculate_fee([10 ** 8]), 57534406)

    def test_sighash_none(self):
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)

        with self.assertRaises(NotImplementedError) as context:
            t.sighash_none()

        self.assertIn('SIGHASH_NONE is a bad idea.', str(context.exception))

    def test_copy(self):
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)

        t_copy = t.copy()

        self.assertEqual(t, t_copy)
        self.assertIsNot(t, t_copy)

    def test_sighash_all(self):
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)
        self.assertEqual(t.sighash_all(0, helpers.prevout_pk_script),
                         helpers.sighash_all)

    def test_sighash_all_anyone_can_pay(self):
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)
        self.assertEqual(
            t.sighash_all(0, helpers.prevout_pk_script, anyone_can_pay=True),
            helpers.sighash_all_anyonecanpay)

    def test_sighash_single(self):
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)
        self.assertEqual(t.sighash_single(0, helpers.prevout_pk_script),
                         helpers.sighash_single)

    def test_sighash_single_anyone_can_pay(self):
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)
        self.assertEqual(
            t.sighash_single(
                0, helpers.prevout_pk_script, anyone_can_pay=True),
            helpers.sighash_single_anyonecanpay)


class DecredTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        riemann.select_network('decred_main')

    def tearDown(self):
        riemann.select_network('bitcoin_main')


class TestDecredByteData(DecredTestCase):

    def test_init_error(self):
        riemann.select_network('bitcoin_main')
        with self.assertRaises(ValueError) as context:
            tx.DecredByteData()

        self.assertIn('Decred classes not supported by network bitcoin_main. '
                      'How did you get here?',
                      str(context.exception))


class TestDecredOutpoint(DecredTestCase):

    def test_create_outpoint(self):
        outpoint_index = helpers.DCR_OUTPOINT_INDEX
        outpoint_tx_id = helpers.DCR_OUTPOINT_TX_ID_LE
        outpoint_tree = helpers.DCR_OUTPOINT_TREE

        outpoint = tx.DecredOutpoint(
            outpoint_tx_id, outpoint_index, outpoint_tree)

        self.assertEqual(outpoint, helpers.DCR_OUTPOINT)

    def test_copy(self):
        outpoint_index = helpers.DCR_OUTPOINT_INDEX
        outpoint_tx_id = helpers.DCR_OUTPOINT_TX_ID_LE
        outpoint_tree = helpers.DCR_OUTPOINT_TREE

        res = tx.DecredOutpoint(
            outpoint_tx_id, outpoint_index, outpoint_tree)

        copy = res.copy()
        self.assertEqual(res, copy)
        self.assertIsNot(res, copy)

    def test_create_outpoint_short_tx_id(self):
        outpoint_index = helpers.DCR_OUTPOINT_INDEX
        outpoint_tx_id = bytearray(b'\xff')
        outpoint_tree = helpers.DCR_OUTPOINT_TREE

        with self.assertRaises(ValueError) as context:
            tx.DecredOutpoint(
                outpoint_tx_id, outpoint_index, outpoint_tree)

        self.assertIn('Expected byte-like object with length 32. ',
                      str(context.exception))

    def test_create_outpoint_string_tx_id(self):
        outpoint_index = helpers.DCR_OUTPOINT_INDEX
        outpoint_tx_id = 'Hello World'
        outpoint_tree = helpers.DCR_OUTPOINT_TREE

        with self.assertRaises(ValueError) as context:
            tx.DecredOutpoint(
                outpoint_tx_id, outpoint_index, outpoint_tree)

        self.assertIn('Expected byte-like object. ',
                      str(context.exception))

    def test_create_outpoint_long_tx_id(self):
        outpoint_index = helpers.DCR_OUTPOINT_INDEX
        outpoint_tx_id = b'00' * 37
        outpoint_tree = helpers.DCR_OUTPOINT_TREE

        with self.assertRaises(ValueError) as context:
            tx.DecredOutpoint(
                outpoint_tx_id, outpoint_index, outpoint_tree)

        self.assertIn('Expected byte-like object with length 32. ',
                      str(context.exception))

    def test_create_outpoint_short_index(self):
        outpoint_index = b'\x00'
        outpoint_tx_id = helpers.DCR_OUTPOINT_TX_ID_LE
        outpoint_tree = helpers.DCR_OUTPOINT_TREE

        with self.assertRaises(ValueError) as context:
            tx.DecredOutpoint(
                outpoint_tx_id, outpoint_index, outpoint_tree)

        self.assertIn('Expected byte-like object with length 4. ',
                      str(context.exception))

    def test_create_outpoint_string_tree(self):
        outpoint_index = helpers.DCR_OUTPOINT_INDEX
        outpoint_tx_id = helpers.DCR_OUTPOINT_TX_ID_LE
        outpoint_tree = 'Hello World'

        with self.assertRaises(ValueError) as context:
            tx.DecredOutpoint(
                outpoint_tx_id, outpoint_index, outpoint_tree)

        self.assertIn('Expected byte-like object. ',
                      str(context.exception))


class TestDecredTxIn(DecredTestCase):

    def setUp(self):
        super().setUp()
        outpoint_index = helpers.DCR_OUTPOINT_INDEX
        outpoint_tx_id = helpers.DCR_OUTPOINT_TX_ID_LE
        outpoint_tree = helpers.DCR_OUTPOINT_TREE

        self.sequence = helpers.DCR_SEQUNCE

        self.outpoint = tx.DecredOutpoint(
            outpoint_tx_id, outpoint_index, outpoint_tree)

    def test_init(self):
        tx_in = tx.DecredTxIn(self.outpoint, self.sequence)

        self.assertEqual(tx_in, helpers.DCR_INPUT)

    def test_init_bad_outpoint(self):
        with self.assertRaises(ValueError) as context:
            tx.DecredTxIn('Hello World', self.sequence)
        self.assertIn('Expected byte-like object. ',
                      str(context.exception))

    def test_init_bad_sequnce(self):
        with self.assertRaises(ValueError) as context:
            tx.DecredTxIn(self.outpoint, 'Hello World')
        self.assertIn('Expected byte-like object. ',
                      str(context.exception))

    def test_copy(self):
        res = tx.DecredTxIn(self.outpoint, self.sequence)
        copy = res.copy()
        self.assertEqual(res, copy)
        self.assertIsNot(res, copy)


class TestDecredTxOut(DecredTestCase):

    def setUp(self):
        super().setUp()
        self.value = helpers.DCR_OUTPUT_VALUE
        self.version = helpers.DCR_OUTPUT_VERSION
        self.output_script = helpers.DCR_OUTPUT_SCRIPT

    def test_init(self):
        tx_out = tx.DecredTxOut(
            self.value, self.version, self.output_script)

        self.assertEqual(tx_out, helpers.DCR_OUTPUT)

    def test_bad_value(self):
        with self.assertRaises(ValueError) as context:
            tx.DecredTxOut('Hello World', self.version, self.output_script)
        self.assertIn('Expected byte-like object. ',
                      str(context.exception))

    def test_bad_version(self):
        with self.assertRaises(ValueError) as context:
            tx.DecredTxOut(self.value, 'Hello World', self.output_script)
        self.assertIn('Expected byte-like object. ',
                      str(context.exception))

    def test_bad_script(self):
        with self.assertRaises(ValueError) as context:
            tx.DecredTxOut(self.value, self.version, 'Hello World')
        self.assertIn('Expected byte-like object. ',
                      str(context.exception))

    def test_copy(self):
        res = tx.DecredTxOut(
            self.value, self.version, self.output_script)
        copy = res.copy()
        self.assertEqual(res, copy)
        self.assertIsNot(res, copy)


class TestDecredInputWitness(DecredTestCase):

    def setUp(self):
        super().setUp()
        self.value = helpers.DCR_WITNESS_VALUE
        self.height = helpers.DCR_WITNESS_HEIGHT
        self.index = helpers.DCR_WITNESS_INDEX
        self.stack_script = helpers.DCR_STACK_SCRIPT
        self.redeem_script = helpers.DCR_REDEEM_SCRIPT

    def test_init(self):
        input_witness = tx.DecredInputWitness(
            value=self.value,
            height=self.height,
            index=self.index,
            stack_script=self.stack_script,
            redeem_script=self.redeem_script)

        self.assertEqual(input_witness, helpers.DCR_WITNESS)

    def test_init_errors(self):

        with self.assertRaises(ValueError) as context:
            tx.DecredInputWitness('Hello World', self.height, self.index,
                                  self.stack_script, self.redeem_script)

        self.assertIn('Expected byte-like object', str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.DecredInputWitness(self.value, 'Hello World', self.index,
                                  self.stack_script, self.redeem_script)

        self.assertIn('Expected byte-like object', str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.DecredInputWitness(self.value, self.height, 'Hello World',
                                  self.stack_script, self.redeem_script)

        self.assertIn('Expected byte-like object', str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.DecredInputWitness(self.value, self.height, self.index,
                                  'Hello World', self.redeem_script)

        self.assertIn('Expected byte-like object', str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.DecredInputWitness(self.value, self.height, self.index,
                                  self.redeem_script, 'Hello World')

        self.assertIn('Expected byte-like object', str(context.exception))

    def test_copy(self):
        res = tx.DecredInputWitness(
            value=self.value,
            height=self.height,
            index=self.index,
            stack_script=self.stack_script,
            redeem_script=self.redeem_script)
        copy = res.copy()

        self.assertEqual(res, copy)
        self.assertIsNot(res, copy)


class TestDecredTx(DecredTestCase):

    def setUp(self):
        super().setUp()

        self.version = helpers.DCR_VERSION

        self.outpoint_index = helpers.DCR_OUTPOINT_INDEX
        self.outpoint_tx_id = helpers.DCR_OUTPOINT_TX_ID_LE
        self.outpoint_tree = helpers.DCR_OUTPOINT_TREE
        self.sequence = helpers.DCR_SEQUNCE

        self.outpoint = tx.DecredOutpoint(
            self.outpoint_tx_id, self.outpoint_index, self.outpoint_tree)
        self.tx_in = tx.DecredTxIn(self.outpoint, self.sequence)

        self.output_value = helpers.DCR_OUTPUT_VALUE
        self.output_version = helpers.DCR_OUTPUT_VERSION
        self.output_script = helpers.DCR_OUTPUT_SCRIPT
        self.tx_out = tx.DecredTxOut(
            self.output_value, self.output_version, self.output_script)

        self.lock_time = helpers.DCR_LOCKTIME
        self.expiry = helpers.DCR_EXPIRY

        self.witness_value = helpers.DCR_WITNESS_VALUE
        self.height = helpers.DCR_WITNESS_HEIGHT
        self.witness_index = helpers.DCR_WITNESS_INDEX
        self.stack_script = helpers.DCR_STACK_SCRIPT
        self.redeem_script = helpers.DCR_REDEEM_SCRIPT
        self.witness = tx.DecredInputWitness(
            value=self.witness_value,
            height=self.height,
            index=self.witness_index,
            stack_script=self.stack_script,
            redeem_script=self.redeem_script)

    def test_init(self):
        transaction = tx.DecredTx(
            version=self.version,
            tx_ins=[self.tx_in],
            tx_outs=[self.tx_out],
            lock_time=self.lock_time,
            expiry=self.expiry,
            tx_witnesses=[self.witness])

        self.assertEqual(transaction, helpers.DCR_RAW_P2SH_TO_P2PKH)

    def test_init_errors(self):
        with self.assertRaises(ValueError) as context:
            tx.DecredTx(
                version='Hello World',
                tx_ins=[self.tx_in],
                tx_outs=[self.tx_out],
                lock_time=self.lock_time,
                expiry=self.expiry,
                tx_witnesses=[self.witness])

            self.assertIn('Expected byte-like object', str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.DecredTx(
                version=self.version,
                tx_ins=['Hello World'],
                tx_outs=[self.tx_out],
                lock_time=self.lock_time,
                expiry=self.expiry,
                tx_witnesses=[self.witness])

        self.assertIn('Invalid TxIn.', str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.DecredTx(
                version=self.version,
                tx_ins=[self.tx_in],
                tx_outs=['Hello World'],
                lock_time=self.lock_time,
                expiry=self.expiry,
                tx_witnesses=[self.witness])

        self.assertIn('Invalid TxOut.', str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.DecredTx(
                version=self.version,
                tx_ins=[self.tx_in],
                tx_outs=[self.tx_out],
                lock_time='Hello World',
                expiry=self.expiry,
                tx_witnesses=[self.witness])

        self.assertIn('Expected byte-like object', str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.DecredTx(
                version=self.version,
                tx_ins=[self.tx_in],
                tx_outs=[self.tx_out],
                lock_time=self.lock_time,
                expiry='Hello World',
                tx_witnesses=[self.witness])

        self.assertIn('Expected byte-like object', str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.DecredTx(
                version=self.version,
                tx_ins=[self.tx_in],
                tx_outs=[self.tx_out],
                lock_time=self.lock_time,
                expiry=self.expiry,
                tx_witnesses=['Hello World'])

        self.assertIn('Invalid TxWitness', str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.DecredTx(
                version=self.version,
                tx_ins=[self.tx_in] * 256,
                tx_outs=[self.tx_out],
                lock_time=self.lock_time,
                expiry=self.expiry,
                tx_witnesses=[self.witness] * 256)

        self.assertIn('Too many inputs or outputs. Stop that.',
                      str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.DecredTx(
                version=self.version,
                tx_ins=[self.tx_in] * 2,
                tx_outs=[self.tx_out],
                lock_time=self.lock_time,
                expiry=self.expiry,
                tx_witnesses=[self.witness])

        self.assertIn('Witness and TxIn lists must be same length. ',
                      str(context.exception))

        with self.assertRaises(ValueError) as context:
            tx.DecredTx(
                version=self.version,
                tx_ins=[],
                tx_outs=[self.tx_out],
                lock_time=self.lock_time,
                expiry=self.expiry,
                tx_witnesses=[])

        self.assertIn('Too few inputs or outputs. Stop that.',
                      str(context.exception))

        long_witness = tx.DecredInputWitness(
            self.witness_value,
            self.height,
            self.witness_index,
            self.stack_script * 64,
            self.redeem_script * 64)
        with self.assertRaises(ValueError) as context:
            tx.DecredTx(
                version=self.version,
                tx_ins=[self.tx_in] * 255,
                tx_outs=[self.tx_out] * 255,
                lock_time=self.lock_time,
                expiry=self.expiry,
                tx_witnesses=[long_witness] * 255)

        self.assertIn('Tx is too large. Expect less than 100kB.',
                      str(context.exception))

    def test_tx_id(self):
        transaction = tx.DecredTx(
            version=self.version,
            tx_ins=[self.tx_in],
            tx_outs=[self.tx_out],
            lock_time=self.lock_time,
            expiry=self.expiry,
            tx_witnesses=[self.witness])

        self.assertEqual(transaction.tx_id, helpers.DCR_TX_ID)
        self.assertEqual(transaction.tx_id_le, helpers.DCR_TX_ID_LE)

    def test_calculate_fee(self):
        transaction = tx.DecredTx(
            version=self.version,
            tx_ins=[self.tx_in],
            tx_outs=[self.tx_out],
            lock_time=self.lock_time,
            expiry=self.expiry,
            tx_witnesses=[self.witness])

        self.assertEqual(transaction.calculate_fee(), 33400)

    def test_witness(self):
        transaction = tx.DecredTx(
            version=self.version,
            tx_ins=[self.tx_in],
            tx_outs=[self.tx_out],
            lock_time=self.lock_time,
            expiry=self.expiry,
            tx_witnesses=[self.witness])

        self.assertEqual(
            transaction.witness(),
            b'\x01\x00' + b'\x02\x00' + b'\x01' + helpers.DCR_WITNESS)

    def test_witness_hash(self):
        transaction = tx.DecredTx(
            version=self.version,
            tx_ins=[self.tx_in],
            tx_outs=[self.tx_out],
            lock_time=self.lock_time,
            expiry=self.expiry,
            tx_witnesses=[self.witness])

        self.assertEqual(
            transaction.witness_hash(),
            helpers.DCR_WITNESS_HASH)  # TODO: check this better

    def test_sighash_none(self):
        transaction = tx.DecredTx(
            version=self.version,
            tx_ins=[self.tx_in],
            tx_outs=[self.tx_out],
            lock_time=self.lock_time,
            expiry=self.expiry,
            tx_witnesses=[self.witness])

        with self.assertRaises(NotImplementedError) as context:
            transaction.sighash_none()

        self.assertIn(
            'SIGHASH_NONE is a bad idea.',
            str(context.exception))

    def test_copy(self):
        res = tx.DecredTx(
            version=self.version,
            tx_ins=[self.tx_in],
            tx_outs=[self.tx_out],
            lock_time=self.lock_time,
            expiry=self.expiry,
            tx_witnesses=[self.witness])

        copy = res.copy()

        self.assertEqual(res, copy)
        self.assertIsNot(res, copy)
