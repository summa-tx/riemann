import riemann
import unittest
from riemann import tx
from riemann import utils
from riemann.tests import helpers


class TestOutpoint(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_outpoint(self):
        outpoint_index = helpers.P2PKH1['ser']['ins'][0]['index']
        outpoint_tx_id = helpers.P2PKH1['ser']['ins'][0]['hash']

        outpoint = tx.Outpoint(outpoint_tx_id, outpoint_index)

        self.assertEqual(outpoint.tx_id, outpoint_tx_id)
        self.assertEqual(outpoint.index, outpoint_index)
        self.assertEqual(outpoint, outpoint_tx_id + outpoint_index)

    def test_create_outpoint_short_tx_id(self):
        outpoint_index = helpers.P2PKH1['ser']['ins'][0]['index']
        outpoint_tx_id = bytearray(b'\xff')

        with self.assertRaises(ValueError) as context:
            tx.Outpoint(outpoint_tx_id, outpoint_index)

        self.assertIn('Expected byte-like object with length 32. ',
                      str(context.exception))

    def test_create_outpoint_str_tx_id(self):
        outpoint_index = helpers.P2PKH1['ser']['ins'][0]['index']
        outpoint_tx_id = 'Hello world'

        with self.assertRaises(ValueError) as context:
            tx.Outpoint(outpoint_tx_id, outpoint_index)

        self.assertIn('Expected byte-like object. ',
                      str(context.exception))

    def test_create_outpoint_long_index(self):
        outpoint_index = utils.i2le_padded(0, 5)
        outpoint_tx_id = helpers.P2PKH1['ser']['ins'][0]['hash']

        with self.assertRaises(ValueError) as context:
            tx.Outpoint(outpoint_tx_id, outpoint_index)

        self.assertIn('Expected byte-like object with length 4. ',
                      str(context.exception))

    def test_create_outpoint_no_index(self):
        outpoint_index = None
        outpoint_tx_id = helpers.P2PKH1['ser']['ins'][0]['hash']

        with self.assertRaises(ValueError) as context:
            tx.Outpoint(outpoint_tx_id, outpoint_index)

        self.assertIn('Expected byte-like object. ',
                      str(context.exception))

    def test_copy(self):
        outpoint_index = helpers.P2PKH1['ser']['ins'][0]['index']
        outpoint_tx_id = helpers.P2PKH1['ser']['ins'][0]['hash']

        res = tx.Outpoint(outpoint_tx_id, outpoint_index)
        copy = res.copy()
        self.assertEqual(res, copy)
        self.assertIsNot(res, copy)

    def test_from_bytes(self):
        outpoint = tx.Outpoint.from_bytes(
            helpers.P2PKH1['ser']['ins'][0]['outpoint'])
        self.assertEqual(outpoint, helpers.P2PKH1['ser']['ins'][0]['outpoint'])
        self.assertEqual(
            outpoint.tx_id,
            helpers.P2PKH1['ser']['ins'][0]['hash'])
        self.assertEqual(
            outpoint.index,
            helpers.P2PKH1['ser']['ins'][0]['index'])


class TestTxIn(unittest.TestCase):

    def setUp(self):
        outpoint_index = helpers.P2PKH1['ser']['ins'][0]['index']
        outpoint_tx_id = helpers.P2PKH1['ser']['ins'][0]['hash']

        self.stack_script = helpers.P2PKH1['ser']['ins'][0]['stack_script']
        self.redeem_script = helpers.P2PKH1['ser']['ins'][0]['redeem_script']
        self.sequence = helpers.P2PKH1['ser']['ins'][0]['sequence']
        self.outpoint = tx.Outpoint(outpoint_tx_id, outpoint_index)

    def test_create_input(self):
        tx_in = tx.TxIn(self.outpoint, self.stack_script,
                        self.redeem_script, self.sequence)

        self.assertEqual(tx_in.outpoint, self.outpoint)
        self.assertEqual(tx_in.stack_script, self.stack_script)
        self.assertEqual(tx_in.redeem_script, self.redeem_script)
        self.assertEqual(tx_in.sequence, self.sequence)
        self.assertEqual(tx_in,  helpers.P2PKH1['ser']['tx']['in'])

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

    def test_from_bytes_pkh(self):
        tx_in = tx.TxIn.from_bytes(helpers.P2PKH1['ser']['tx']['in'])
        self.assertEqual(tx_in,  helpers.P2PKH1['ser']['tx']['in'])
        self.assertEqual(
            tx_in.outpoint,
            helpers.P2PKH1['ser']['ins'][0]['outpoint'])
        self.assertEqual(
            tx_in.sequence,
            helpers.P2PKH1['ser']['ins'][0]['sequence'])
        self.assertEqual(
            tx_in.stack_script,
            helpers.P2PKH1['ser']['ins'][0]['stack_script'])
        self.assertEqual(
            tx_in.redeem_script,
            helpers.P2PKH1['ser']['ins'][0]['redeem_script'])

    def test_from_bytes_sh(self):
        tx_in = tx.TxIn.from_bytes(helpers.P2SH['ser']['ins'][0]['input'])
        self.assertEqual(tx_in, helpers.P2SH['ser']['ins'][0]['input'])
        self.assertEqual(
            tx_in.outpoint,
            helpers.P2SH['ser']['ins'][0]['outpoint'])
        self.assertEqual(
            tx_in.sequence,
            helpers.P2SH['ser']['ins'][0]['sequence'])
        self.assertEqual(
            tx_in.stack_script,
            helpers.P2SH['ser']['ins'][0]['stack_script'])
        self.assertEqual(
            tx_in.redeem_script,
            helpers.P2SH['ser']['ins'][0]['redeem_script'])

    def test_from_bytes_wsh(self):
        tx_in = tx.TxIn.from_bytes(helpers.P2WSH['ser']['ins'][0]['input'])
        self.assertEqual(tx_in, helpers.P2WSH['ser']['ins'][0]['input'])
        self.assertEqual(
            tx_in.outpoint,
            helpers.P2WSH['ser']['ins'][0]['outpoint'])
        self.assertEqual(
            tx_in.sequence,
            utils.i2be(helpers.P2WSH['human']['ins'][0]['sequence']))
        self.assertEqual(tx_in.stack_script, b'')
        self.assertEqual(tx_in.redeem_script, b'')


class TestTxOut(unittest.TestCase):

    def setUp(self):
        self.value = helpers.P2PKH1['ser']['outs'][0]['value']
        self.output_script = helpers.P2PKH1['ser']['outs'][0]['pk_script']

    def test_create_output(self):
        tx_out = tx.TxOut(self.value, self.output_script)
        self.assertEqual(tx_out, helpers.P2PKH1['ser']['outs'][0]['out'])

    def test_copy(self):
        tx_out = tx.TxOut(self.value, self.output_script)
        tx_out_copy = tx_out.copy()

        self.assertEqual(tx_out, tx_out_copy)  # They should be equal
        self.assertIsNot(tx_out, tx_out_copy)  # But not the same object

    def test_from_bytes(self):
        output = helpers.P2PKH1['ser']['outs'][0]['value'] + \
            b'\x19' + helpers.P2PKH1['ser']['outs'][0]['pk_script']
        tx_out = tx.TxOut.from_bytes(output)
        self.assertEqual(
            tx_out.value,
            helpers.P2PKH1['ser']['outs'][0]['value'])
        self.assertEqual(
            tx_out.output_script,
            helpers.P2PKH1['ser']['outs'][0]['pk_script'])

    def test_from_bytes_long(self):
        with self.assertRaises(NotImplementedError) as context:
            tx.TxOut.from_bytes(b'\xff' * 10)
        self.assertIn(
            'No support for abnormally long pk_scripts.',
            str(context.exception))


class TestWitnessStackItem(unittest.TestCase):

    def setUp(self):
        self.stack_item_bytes = \
            helpers.P2WSH['ser']['witnesses'][0]['wit_stack_items'][1]

    def test_create_stack_item(self):
        w = tx.WitnessStackItem(self.stack_item_bytes)
        self.assertEqual(w.item, self.stack_item_bytes)
        self.assertEqual(
            w,
            bytes([len(self.stack_item_bytes)]) + self.stack_item_bytes)

    def test_from_bytes(self):
        w = tx.WitnessStackItem.from_bytes(
            bytes([len(self.stack_item_bytes)]) + self.stack_item_bytes)
        self.assertEqual(w.item, self.stack_item_bytes)
        self.assertEqual(
            w,
            bytes([len(self.stack_item_bytes)]) + self.stack_item_bytes)

    # def test_item_too_long(self):
    #     with self.assertRaises(ValueError) as context:
    #         tx.WitnessStackItem(b'\xff' * 521)
    #     self.assertIn(
    #         'Item is too large. Expected <=520 bytes. ',
    #         str(context.exception))

    def test_null_item_from_bytes(self):
        w = tx.WitnessStackItem.from_bytes(b'\x00')
        self.assertEqual(w, b'\x00')


class TestInputWitness(unittest.TestCase):

    def setUp(self):
        self.stack = [tx.WitnessStackItem(b)
                      for b in
                      helpers.P2WSH['ser']['witnesses'][0]['wit_stack_items']]

    def test_create_witness(self):
        iw = tx.InputWitness(self.stack)
        self.assertEqual(len(iw.stack), len(self.stack))
        for item, expected in zip(iw.stack, self.stack):
            self.assertEqual(item, expected)

        bad_stack = [None, 1]
        with self.assertRaises(ValueError) as context:
            tx.InputWitness(bad_stack)

        self.assertIn('Invalid witness stack item. '
                      'Expected WitnessStackItem. Got None',
                      str(context.exception))

    def test_from_bytes(self):
        iw = tx.InputWitness.from_bytes(helpers.P2WSH['ser']['tx']['witness'])
        self.assertEqual(len(iw.stack), len(self.stack))
        for item, expected in zip([s.item for s in iw.stack],
                                  [s.item for s in self.stack]):
            self.assertEqual(item, expected)


class TestTx(unittest.TestCase):

    def setUp(self):
        self.outpoint_index = helpers.P2PKH1['ser']['ins'][0]['index']
        self.outpoint_tx_id = helpers.P2PKH1['ser']['ins'][0]['hash']

        self.stack_script = helpers.P2PKH1['ser']['ins'][0]['stack_script']
        self.redeem_script = helpers.P2PKH1['ser']['ins'][0]['redeem_script']
        self.sequence = helpers.P2PKH1['ser']['ins'][0]['sequence']
        self.outpoint = tx.Outpoint(self.outpoint_tx_id, self.outpoint_index)

        self.tx_in = tx.TxIn(self.outpoint, self.stack_script,
                             self.redeem_script, self.sequence)

        self.value_0 = helpers.P2PKH1['ser']['outs'][0]['value']
        self.output_script_0 = \
            helpers.P2PKH1['ser']['outs'][0]['pk_script']
        self.value_1 = helpers.P2PKH1['ser']['outs'][1]['value']
        self.output_script_1 = \
            helpers.P2PKH1['ser']['outs'][1]['pk_script']

        self.tx_out_0 = tx.TxOut(self.value_0, self.output_script_0)
        self.tx_out_1 = tx.TxOut(self.value_1, self.output_script_1)

        self.version = helpers.P2PKH1['ser']['version']
        self.none_flag = None
        self.tx_ins = [self.tx_in]
        self.tx_outs = [self.tx_out_0, self.tx_out_1]
        self.none_witnesses = None
        self.lock_time = helpers.P2PKH1['ser']['locktime']

        self.segwit_flag = b'\x00\x01'
        self.stack = [tx.WitnessStackItem(b)
                      for b in
                      helpers.P2WSH['ser']['witnesses'][0]['wit_stack_items']]
        self.tx_witnesses = [tx.InputWitness(self.stack)]

    def tearDown(self):
        riemann.select_network('bitcoin_main')

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

    # TODO: Break up this monstrosity (further)
    def test_tx_witness(self):
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)

        self.assertEqual(t, helpers.P2PKH1['ser']['tx']['signed'])

        with self.assertRaises(ValueError) as context:
            tx.Tx(self.version, b'\x00\x00', self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)
        self.assertIn(
            'Invald segwit flag. Expected None or ',
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

    def test_tx_inandout(self):
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)

        self.assertEqual(t, helpers.P2PKH1['ser']['tx']['signed'])

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

    def test_tx_inout_mutation(self):
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)

        with self.assertRaises(TypeError, msg='That\'s immutable, honey'):
            t.tx_ins = t.tx_ins + (1,)

        with self.assertRaises(TypeError, msg='That\'s immutable, honey'):
            t.tx_outs = t.tx_outs + (1,)

    def test_tx_id(self):
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)

        self.assertEqual(t.tx_id, helpers.P2PKH1['ser']['tx']['hash'])
        self.assertEqual(t.tx_id_le, helpers.P2PKH1['ser']['tx']['hash_le'])

    def test_from_hex_pkh(self):
        t = tx.Tx.from_hex(helpers.P2PKH1['human']['tx']['signed'])
        self.assertEqual(t.version, helpers.P2PKH1['ser']['version'])
        self.assertEqual(t.tx_ins[0],  helpers.P2PKH1['ser']['tx']['in'])
        self.assertEqual(t.tx_outs[0], helpers.P2PKH1['ser']['outs'][0]['out'])
        self.assertEqual(t.tx_outs[1], helpers.P2PKH1['ser']['outs'][1]['out'])
        self.assertEqual(t.lock_time, helpers.P2PKH1['ser']['locktime'])
        self.assertEqual(t, helpers.P2PKH1['ser']['tx']['signed'])

    def test_from_hex_sh(self):
        t = tx.Tx.from_hex(helpers.P2SH['human']['tx']['signed'])
        self.assertEqual(t.version, helpers.P2SH['ser']['version'])
        self.assertEqual(
            t.tx_ins[0],
            helpers.P2SH['ser']['ins'][0]['input'])
        self.assertEqual(
            t.tx_outs[0],
            helpers.P2SH['ser']['outs'][0]['output'])
        self.assertEqual(
            t.tx_outs[1],
            helpers.P2SH['ser']['outs'][1]['output'])
        self.assertEqual(t.lock_time, helpers.P2SH['ser']['locktime'])
        self.assertEqual(t, helpers.P2SH['ser']['tx']['signed'])

    def test_from_hex_wsh(self):
        t = tx.Tx.from_hex(helpers.P2WSH['human']['tx']['signed'])
        self.assertEqual(t.version, helpers.P2WSH['ser']['version'])
        self.assertEqual(t.tx_ins[0], helpers.P2WSH['ser']['ins'][0]['input'])
        self.assertEqual(
            t.tx_outs[0],
            helpers.P2WSH['ser']['outs'][0]['output'])
        self.assertEqual(
            t.tx_outs[1],
            helpers.P2WSH['ser']['outs'][1]['output'])
        self.assertEqual(
            t.tx_outs[2],
            helpers.P2WSH['ser']['outs'][2]['output'])
        self.assertEqual(
            t.tx_outs[3],
            helpers.P2WSH['ser']['outs'][3]['output'])
        self.assertEqual(
            t.tx_witnesses[0],
            helpers.P2WSH['ser']['tx']['witness'])
        self.assertEqual(t.lock_time, helpers.P2WSH['ser']['locktime'])
        self.assertEqual(t, helpers.P2WSH['ser']['tx']['signed'])

    def test_from_bytes_pkh(self):
        t = tx.Tx.from_bytes(helpers.P2PKH1['ser']['tx']['signed'])
        self.assertEqual(t.version, helpers.P2PKH1['ser']['version'])
        self.assertEqual(t.tx_ins[0],  helpers.P2PKH1['ser']['tx']['in'])
        self.assertEqual(t.tx_outs[0], helpers.P2PKH1['ser']['outs'][0]['out'])
        self.assertEqual(t.tx_outs[1], helpers.P2PKH1['ser']['outs'][1]['out'])
        self.assertEqual(t.lock_time, helpers.P2PKH1['ser']['locktime'])
        self.assertEqual(t, helpers.P2PKH1['ser']['tx']['signed'])

    def test_from_bytes_sh(self):
        t = tx.Tx.from_bytes(helpers.P2SH['ser']['tx']['signed'])
        self.assertEqual(t.version, helpers.P2SH['ser']['version'])
        self.assertEqual(
            t.tx_ins[0],
            helpers.P2SH['ser']['ins'][0]['input'])
        self.assertEqual(
            t.tx_outs[0],
            helpers.P2SH['ser']['outs'][0]['output'])
        self.assertEqual(
            t.tx_outs[1],
            helpers.P2SH['ser']['outs'][1]['output'])
        self.assertEqual(t.lock_time, helpers.P2SH['ser']['locktime'])
        self.assertEqual(t, helpers.P2SH['ser']['tx']['signed'])

    def test_from_bytes_wsh(self):
        t = tx.Tx.from_bytes(helpers.P2WSH['ser']['tx']['signed'])
        self.assertEqual(t.version, helpers.P2WSH['ser']['version'])
        self.assertEqual(t.tx_ins[0], helpers.P2WSH['ser']['ins'][0]['input'])
        self.assertEqual(
            t.tx_outs[0],
            helpers.P2WSH['ser']['outs'][0]['output'])
        self.assertEqual(
            t.tx_outs[1],
            helpers.P2WSH['ser']['outs'][1]['output'])
        self.assertEqual(
            t.tx_outs[2],
            helpers.P2WSH['ser']['outs'][2]['output'])
        self.assertEqual(
            t.tx_outs[3],
            helpers.P2WSH['ser']['outs'][3]['output'])
        self.assertEqual(
            t.tx_witnesses[0],
            helpers.P2WSH['ser']['tx']['witness'])
        self.assertEqual(t.lock_time, helpers.P2WSH['ser']['locktime'])
        self.assertEqual(t, helpers.P2WSH['ser']['tx']['signed'])

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

    def test_is_witness(self):
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)

        self.assertFalse(t.is_witness())

        t = tx.Tx.from_bytes(helpers.P2WSH['ser']['tx']['signed'])

        self.assertTrue(t.is_witness())

    def test_segwit_sighash_all(self):
        t = tx.Tx.from_bytes(helpers.P2WPKH['ser']['tx']['signed'])
        self.assertEqual(
            t.sighash_all(
                0,
                helpers.P2WPKH['ser']['ins'][0]['pk_script'],
                prevout_value=helpers.P2WPKH['ser']['ins'][0]['value']
                ),
            helpers.P2WPKH['ser']['segwit_sighash']['all'])

    def test_segwit_sighash_all_anyonecanpay(self):
        t = tx.Tx.from_bytes(helpers.P2WPKH['ser']['tx']['signed'])

        self.assertEqual(
            t.sighash_all(
                0,
                helpers.P2WPKH['ser']['ins'][0]['pk_script'],
                prevout_value=helpers.P2WPKH['ser']['ins'][0]['value'],
                anyone_can_pay=True),
            helpers.P2WPKH['ser']['segwit_sighash']['all_anyonecanpay'])

    def test_segwit_sighash_single(self):
        t = tx.Tx.from_bytes(helpers.P2WPKH['ser']['tx']['signed'])
        self.assertEqual(
            t.sighash_single(
                0,
                helpers.P2WPKH['ser']['ins'][0]['pk_script'],
                prevout_value=helpers.P2WPKH['ser']['ins'][0]['value']),
            helpers.P2WPKH['ser']['segwit_sighash']['single'])

    def test_segwit_sighash_single_anyonecanpay(self):
        t = tx.Tx.from_bytes(helpers.P2WPKH['ser']['tx']['signed'])
        self.assertEqual(
            t.sighash_single(
                0,
                helpers.P2WPKH['ser']['ins'][0]['pk_script'],
                prevout_value=helpers.P2WPKH['ser']['ins'][0]['value'],
                anyone_can_pay=True),
            helpers.P2WPKH['ser']['segwit_sighash']['single_anyonecanpay'])

    def test_presegwit_sighashes(self):
        ''' all, all anyonecanpay, single, single_anyonecanpay.
        Marks transaction as pre- or non-segwit in a segwit network.
        '''
        t = tx.Tx(self.version, None, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)

        self.assertEqual(
            t.sighash_all(
                0,
                helpers.P2PKH1['ser']['ins'][0]['pk_script'],
                ),
            helpers.P2PKH1['ser']['sighash']['all'])

        self.assertEqual(
            t.sighash_all(
                0,
                helpers.P2PKH1['ser']['ins'][0]['pk_script'],
                anyone_can_pay=True),
            helpers.P2PKH1['ser']['sighash']['all_anyonecanpay'])

        self.assertEqual(
                t.sighash_single(
                    0,
                    helpers.P2PKH1['ser']['ins'][0]['pk_script']),
                helpers.P2PKH1['ser']['sighash']['single'])

        self.assertEqual(
            t.sighash_single(
                0,
                helpers.P2PKH1['ser']['ins'][0]['pk_script'],
                anyone_can_pay=True),
            helpers.P2PKH1['ser']['sighash']['single_anyonecanpay'])

    def test_sighash_single_bug(self):
        with self.assertRaises(NotImplementedError) as context:
            t = tx.Tx(self.version, self.none_flag, self.tx_ins * 3,
                      self.tx_outs, self.none_witnesses, self.lock_time)
            t.sighash_single(2, helpers.P2PKH1['ser']['ins'][0]['pk_script'])

        self.assertIn(
            'I refuse to implement the SIGHASH_SINGLE bug.',
            str(context.exception))

    def test_sighash_forkid_single(self):
        riemann.select_network('bitcoin_cash_main')
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)

        sighash = t.sighash_single(
            index=0,
            script=helpers.P2PKH1['ser']['ins'][0]['pk_script'],
            prevout_value=helpers.P2PKH1['ser']['ins'][0]['value'])

        self.assertEqual(
            sighash,
            helpers.SIGHASH_FORKID['single'])

    def test_sighash_forkid_single_anyone_can_pay(self):
        riemann.select_network('bitcoin_cash_main')
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)

        sighash = t.sighash_single(
            index=0,
            script=helpers.P2PKH1['ser']['ins'][0]['pk_script'],
            prevout_value=helpers.P2PKH1['ser']['ins'][0]['value'],
            anyone_can_pay=True)

        self.assertEqual(
            sighash,
            helpers.SIGHASH_FORKID['single_anyone_can_pay'])

    def test_sighash_forkid_all(self):
        riemann.select_network('bitcoin_cash_main')
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)

        sighash = t.sighash_all(
            index=0,
            script=helpers.P2PKH1['ser']['ins'][0]['pk_script'],
            prevout_value=helpers.P2PKH1['ser']['ins'][0]['value'])

        self.assertEqual(
            sighash,
            helpers.SIGHASH_FORKID['all'])

    def test_sighash_forkid_all_anyone_can_pay(self):
        riemann.select_network('bitcoin_cash_main')
        t = tx.Tx(self.version, self.none_flag, self.tx_ins, self.tx_outs,
                  self.none_witnesses, self.lock_time)

        sighash = t.sighash_all(
            index=0,
            script=helpers.P2PKH1['ser']['ins'][0]['pk_script'],
            prevout_value=helpers.P2PKH1['ser']['ins'][0]['value'],
            anyone_can_pay=True)

        self.assertEqual(
            sighash,
            helpers.SIGHASH_FORKID['all_anyone_can_pay'])
