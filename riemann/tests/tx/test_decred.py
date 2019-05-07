import riemann
import unittest
from riemann import tx, utils, simple
from riemann.tx import tx_builder as tb
from riemann.tests.tx.helpers import decred_helpers as helpers


class DecredTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        riemann.select_network('decred_main')

    def tearDown(self):
        riemann.select_network('bitcoin_main')


class TestDecredSimple(unittest.TestCase):

    def test_decred_simple(self):
        outpoint = simple.outpoint(
            tx_id=helpers.DCR['human']['ins'][0]['hash'],
            index=helpers.DCR['human']['ins'][0]['index'],
            tree=helpers.DCR['human']['ins'][0]['tree'])

        self.assertEqual(
            simple.unsigned_input(
                outpoint=outpoint,
                sequence=helpers.DCR['human']['ins'][0]['sequence']),
            helpers.DCR['ser']['tx']['in_unsigned'])


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
        outpoint_index = helpers.DCR['ser']['ins'][0]['index']
        outpoint_tx_id = helpers.DCR['ser']['ins'][0]['hash']
        outpoint_tree = helpers.DCR['ser']['ins'][0]['tree']

        outpoint = tx.DecredOutpoint(
            outpoint_tx_id, outpoint_index, outpoint_tree)

        self.assertEqual(outpoint, helpers.DCR['ser']['ins'][0]['outpoint'])

    def test_copy(self):
        outpoint_index = helpers.DCR['ser']['ins'][0]['index']
        outpoint_tx_id = helpers.DCR['ser']['ins'][0]['hash']
        outpoint_tree = helpers.DCR['ser']['ins'][0]['tree']

        res = tx.DecredOutpoint(
            outpoint_tx_id, outpoint_index, outpoint_tree)

        copy = res.copy()
        self.assertEqual(res, copy)
        self.assertIsNot(res, copy)

    def test_create_outpoint_short_tx_id(self):
        outpoint_index = helpers.DCR['ser']['ins'][0]['index']
        outpoint_tx_id = bytearray(b'\xff')
        outpoint_tree = helpers.DCR['ser']['ins'][0]['tree']

        with self.assertRaises(ValueError) as context:
            tx.DecredOutpoint(
                outpoint_tx_id, outpoint_index, outpoint_tree)

        self.assertIn('Expected byte-like object with length 32. ',
                      str(context.exception))

    def test_create_outpoint_string_tx_id(self):
        outpoint_index = helpers.DCR['ser']['ins'][0]['index']
        outpoint_tx_id = 'Hello World'
        outpoint_tree = helpers.DCR['ser']['ins'][0]['tree']

        with self.assertRaises(ValueError) as context:
            tx.DecredOutpoint(
                outpoint_tx_id, outpoint_index, outpoint_tree)

        self.assertIn('Expected byte-like object. ',
                      str(context.exception))

    def test_create_outpoint_long_tx_id(self):
        outpoint_index = helpers.DCR['ser']['ins'][0]['index']
        outpoint_tx_id = b'00' * 37
        outpoint_tree = helpers.DCR['ser']['ins'][0]['tree']

        with self.assertRaises(ValueError) as context:
            tx.DecredOutpoint(
                outpoint_tx_id, outpoint_index, outpoint_tree)

        self.assertIn('Expected byte-like object with length 32. ',
                      str(context.exception))

    def test_create_outpoint_short_index(self):
        outpoint_index = b'\x00'
        outpoint_tx_id = helpers.DCR['ser']['ins'][0]['hash']
        outpoint_tree = helpers.DCR['ser']['ins'][0]['tree']

        with self.assertRaises(ValueError) as context:
            tx.DecredOutpoint(
                outpoint_tx_id, outpoint_index, outpoint_tree)

        self.assertIn('Expected byte-like object with length 4. ',
                      str(context.exception))

    def test_create_outpoint_string_tree(self):
        outpoint_index = helpers.DCR['ser']['ins'][0]['index']
        outpoint_tx_id = helpers.DCR['ser']['ins'][0]['hash']
        outpoint_tree = 'Hello World'

        with self.assertRaises(ValueError) as context:
            tx.DecredOutpoint(
                outpoint_tx_id, outpoint_index, outpoint_tree)

        self.assertIn('Expected byte-like object. ',
                      str(context.exception))


class TestDecredTxIn(DecredTestCase):

    def setUp(self):
        super().setUp()
        outpoint_index = helpers.DCR['ser']['ins'][0]['index']
        outpoint_tx_id = helpers.DCR['ser']['ins'][0]['hash']
        outpoint_tree = helpers.DCR['ser']['ins'][0]['tree']

        self.sequence = helpers.DCR['ser']['ins'][0]['sequence']

        self.outpoint = tx.DecredOutpoint(
            outpoint_tx_id, outpoint_index, outpoint_tree)

    def test_init(self):
        tx_in = tx.DecredTxIn(self.outpoint, self.sequence)

        self.assertEqual(tx_in, helpers.DCR['ser']['tx']['in_unsigned'])

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
        self.value = helpers.DCR['ser']['outs'][0]['value']
        self.version = helpers.DCR['ser']['outs'][0]['version']
        self.output_script = helpers.DCR['ser']['outs'][0]['pk_script']

    def test_init(self):
        tx_out = tx.DecredTxOut(
            self.value, self.version, self.output_script)

        self.assertEqual(tx_out, helpers.DCR['ser']['outs'][0]['output'])

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

    def test_from_bytes_long(self):
        with self.assertRaises(NotImplementedError) as context:
            tx.DecredTxOut.from_bytes(b'\xff' * 1000)
        self.assertIn(
            'No support for abnormally long pk_scripts.',
            str(context.exception))


class TestDecredInputWitness(DecredTestCase):

    def setUp(self):
        super().setUp()
        helper_witness = helpers.DCR['ser']['witnesses'][0]
        self.value = helper_witness['value']
        self.height = helper_witness['height']
        self.index = helper_witness['index']
        self.stack_script = helper_witness['stack_script']
        self.redeem_script = helper_witness['redeem_script']

    def test_init(self):
        input_witness = tx.DecredInputWitness(
            value=self.value,
            height=self.height,
            index=self.index,
            stack_script=self.stack_script,
            redeem_script=self.redeem_script)

        self.assertEqual(
            input_witness,
            helpers.DCR['ser']['witnesses'][0]['witness'])

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

        self.version = helpers.DCR['ser']['version']

        self.outpoint_index = helpers.DCR['ser']['ins'][0]['index']
        self.outpoint_tx_id = helpers.DCR['ser']['ins'][0]['hash']
        self.outpoint_tree = helpers.DCR['ser']['ins'][0]['tree']
        self.sequence = helpers.DCR['ser']['ins'][0]['sequence']

        self.outpoint = tx.DecredOutpoint(
            self.outpoint_tx_id, self.outpoint_index, self.outpoint_tree)
        self.tx_in = tx.DecredTxIn(self.outpoint, self.sequence)

        self.output_value = helpers.DCR['ser']['outs'][0]['value']
        self.output_version = helpers.DCR['ser']['outs'][0]['version']
        self.output_script = helpers.DCR['ser']['outs'][0]['pk_script']
        self.tx_out = tx.DecredTxOut(
            self.output_value, self.output_version, self.output_script)

        self.lock_time = helpers.DCR['ser']['locktime']
        self.expiry = helpers.DCR['ser']['expiry']

        self.witness_value = helpers.DCR['ser']['witnesses'][0]['value']
        self.height = helpers.DCR['ser']['witnesses'][0]['height']
        self.witness_index = helpers.DCR['ser']['witnesses'][0]['index']
        self.stack_script = helpers.DCR['ser']['witnesses'][0]['stack_script']
        self.redeem_script = \
            helpers.DCR['ser']['witnesses'][0]['redeem_script']
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

        self.assertEqual(transaction, helpers.DCR['ser']['tx']['p2sh_2_p2pkh'])

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

        # with self.assertRaises(ValueError) as context:
        #     tx.DecredTx(
        #         version=self.version,
        #         tx_ins=[self.tx_in] * 2,
        #         tx_outs=[self.tx_out],
        #         lock_time=self.lock_time,
        #         expiry=self.expiry,
        #         tx_witnesses=[self.witness])
        #
        # self.assertIn('Witness and TxIn lists must be same length. ',
        #               str(context.exception))

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

        self.assertEqual(transaction.tx_id, helpers.DCR['ser']['tx']['hash'])
        self.assertEqual(
            transaction.tx_id_le,
            helpers.DCR['ser']['tx']['hash_le'])

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
        tx_wit = b'\x01\x00' + b'\x02\x00' + b'\x01' + \
            helpers.DCR['ser']['witnesses'][0]['witness']
        self.assertEqual(transaction.witness(), tx_wit)

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
            helpers.DCR['ser']['witnesses'][0]['hash'])

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

    def test_txhash(self):
        '''
        https://github.com/decred/dcrd/blob/master/wire/msgtx_test.go#L139-L140
        '''
        outpoint = tx.DecredOutpoint(
            tx_id=b'\x00' * 32,
            index=b'\xff' * 4,
            tree=b'\x00')
        tx_ins = [tx.DecredTxIn(outpoint=outpoint, sequence=b'\xff' * 4)]
        tx_outs = [tx.DecredTxOut(value=utils.i2le_padded(5000000000, 8),
                                  version=b'\xf0\xf0',
                                  output_script=helpers.DCR['ser']['hash_pk'])]
        tx_witnesses = [
            tx.DecredInputWitness(value=utils.i2le_padded(5000000000, 8),
                                  height=b'\x34' * 4,
                                  index=b'\x2E' * 4,
                                  stack_script=bytes([0x04, 0x31, 0xdc, 0x00,
                                                      0x1b, 0x01, 0x62]),
                                  redeem_script=b'')]
        version = helpers.DCR['ser']['version']
        t = tx.DecredTx(
            version=version,
            tx_ins=tx_ins,
            tx_outs=tx_outs,
            lock_time=b'\x00' * 4,
            expiry=b'\x00' * 4,
            tx_witnesses=tx_witnesses)

        self.assertEqual(t.tx_id, helpers.DCR['ser']['tx']['expected_hash'])

    def test_sighash(self):
        tx_in_0 = tx.DecredTxIn.from_bytes(helpers.DCR1['ser']['ins'][0]['in'])
        tx_in_1 = tx.DecredTxIn.from_bytes(helpers.DCR1['ser']['ins'][1]['in'])
        tx_in_2 = tx.DecredTxIn.from_bytes(helpers.DCR1['ser']['ins'][2]['in'])

        tx_ins = [tx_in_0, tx_in_1, tx_in_2]

        tx_out_0 = tx.DecredTxOut.from_bytes(
            helpers.DCR1['ser']['outs'][0]['output'])
        tx_out_1 = tx.DecredTxOut.from_bytes(
            helpers.DCR1['ser']['outs'][1]['output'])

        tx_outs = [tx_out_0, tx_out_1]

        tx_witness_0 = tx.DecredInputWitness(
            value=helpers.DCR1['ser']['witness'][0]['value'],
            height=helpers.DCR1['ser']['witness'][0]['height'],
            index=helpers.DCR1['ser']['witness'][0]['index'],
            stack_script=helpers.DCR1['ser']['witness'][0]['stack_script'],
            redeem_script=b'')
        tx_witness_1 = tx.DecredInputWitness(
            value=helpers.DCR1['ser']['witness'][1]['value'],
            height=helpers.DCR1['ser']['witness'][1]['height'],
            index=helpers.DCR1['ser']['witness'][1]['index'],
            stack_script=helpers.DCR1['ser']['witness'][1]['stack_script'],
            redeem_script=b'')
        tx_witness_2 = tx.DecredInputWitness(
            value=helpers.DCR1['ser']['witness'][2]['value'],
            height=helpers.DCR1['ser']['witness'][2]['height'],
            index=helpers.DCR1['ser']['witness'][2]['index'],
            stack_script=helpers.DCR1['ser']['witness'][2]['stack_script'],
            redeem_script=b'')

        tx_witnesses = [tx_witness_0, tx_witness_1, tx_witness_2]

        tx.DecredTx(
            version=helpers.DCR1['ser']['version'],
            tx_ins=tx_ins,
            tx_outs=tx_outs,
            lock_time=helpers.DCR1['ser']['locktime'],
            expiry=helpers.DCR1['ser']['expiry'],
            tx_witnesses=tx_witnesses)

        # self.assertEqual(
        #     t.sighash_all(
        #         index=0,
        #         prevout_pk_script=SIGHASH_DCR['prevout_pk']),
        #     helpers.SIGHASH_DCR['all'])
        # self.assertEqual(
        #     t.sighash_all(
        #         index=0,
        #         prevout_pk_script=SIGHASH_DCR['prevout_pk'],
        #         anyone_can_pay=True),
        #     helpers.SIGHASH_DCR['all_anyonecanpay'])
        # self.assertEqual(
        #     t.sighash_single(
        #         index=0,
        #         prevout_pk_script=SIGHASH_DCR['prevout_pk']),
        #     helpers.SIGHASH_DCR['single'])
        # self.assertEqual(
        #     t.sighash_single(
        #         index=0,
        #         prevout_pk_script=SIGHASH_DCR['prevout_pk'],
        #         anyone_can_pay=True),
        #     helpers.SIGHASH_DCR['single_anyonecanpay'])


class TestDecredTxBuilder(DecredTestCase):

    def test_make_decred_output(self):
        riemann.select_network('decred_main')
        self.assertEqual(
            tb._make_output(
                value=helpers.DCR['ser']['outs'][0]['value'],
                output_script=helpers.DCR['ser']['outs'][0]['pk_script'],
                version=helpers.DCR['ser']['outs'][0]['version']),
            helpers.DCR['ser']['outs'][0]['output'])

    def test_make_decred_witness(self):
        riemann.select_network('decred_main')
        helper_witness = helpers.DCR['ser']['witnesses'][0]
        self.assertEqual(
            tb.make_decred_witness(
                value=helper_witness['value'],
                height=helper_witness['height'],
                index=helper_witness['index'],
                stack_script=helper_witness['stack_script'],
                redeem_script=helper_witness['redeem_script']),
            helper_witness['witness'])

    def test_make_decred_outpoint(self):
        riemann.select_network('decred_main')
        self.assertEqual(
            tb.make_outpoint(
                tx_id_le=helpers.DCR['ser']['ins'][0]['hash'],
                index=0,
                tree=0),
            helpers.DCR['ser']['ins'][0]['outpoint'])

    def test_make_decred_witness_input(self):
        riemann.select_network('decred_main')
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.DCR['ser']['ins'][0]['hash'],
            index=0,
            tree=0)
        self.assertEqual(
            tb.make_decred_input(
                outpoint=outpoint,
                sequence=helpers.DCR['human']['ins'][0]['sequence']),
            helpers.DCR['ser']['tx']['in_unsigned'])

    def test_make_decred_input(self):
        riemann.select_network('decred_main')
        outpoint = tb.make_outpoint(
            tx_id_le=helpers.DCR['ser']['ins'][0]['hash'],
            index=0,
            tree=0)
        self.assertEqual(
            tb.make_witness_input(
                outpoint=outpoint,
                sequence=helpers.DCR['human']['ins'][0]['sequence']),
            helpers.DCR['ser']['tx']['in_unsigned'])
