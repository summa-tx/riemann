import riemann
import unittest
from riemann import tx
from riemann.tests.tx.helpers import overwinter_helpers as helpers


class OverwinterTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        riemann.select_network('zcash_overwinter_main')

    def tearDown(self):
        riemann.select_network('bitcoin_main')


class TestOverwinterTx(OverwinterTestCase):

    def setUp(self):
        super().setUp()
        self.joinsplit_ser = helpers.ZCASH_SPROUT['ser']['joinsplit_0']
        self.zkproof = tx.SproutZkproof.from_bytes(
            helpers.ZCASH_SPROUT['ser']['joinsplits'][0]['proof'])
        self.joinsplit = helpers.ZCASH_SPROUT['ser']['joinsplits'][0].copy()
        self.joinsplit['zkproof'] = self.zkproof
        self.joinsplit.pop('proof')  # remove this entry from the dict
        self.joinsplit = tx.SproutJoinsplit(**self.joinsplit)

        self.tx_ser = helpers.ZCASH_SPROUT['ser']['tx']

        self.tx = {}

        self.tx['tx_ins'] = []
        self.tx_out = tx.TxOut.from_bytes(
            helpers.ZCASH_SPROUT['ser']['tx_out_0'])
        self.tx['tx_outs'] = [self.tx_out]
        self.tx['lock_time'] = helpers.ZCASH_SPROUT['ser']['lock_time']
        self.tx['expiry_height'] = helpers.ZCASH_SPROUT['ser']['lock_time']
        self.tx['tx_joinsplits'] = [self.joinsplit]
        self.tx['joinsplit_pubkey'] = \
            helpers.ZCASH_SPROUT['ser']['joinsplit_pubkey']
        self.tx['joinsplit_sig'] = helpers.ZCASH_SPROUT['ser']['joinsplit_sig']

    def attr_assert(self, attr_name, replacement, err_text):
        # Removes a named key from a dictionary and replaces it with b'\x00'
        temp_dict = dict((a, self.tx[a])
                         for a in self.tx
                         if a != attr_name)
        temp_dict[attr_name] = replacement
        with self.assertRaises(ValueError) as context:
            tx.OverwinterTx(**temp_dict)

        self.assertIn(err_text, str(context.exception))

    def test_init_errors(self):
        self.attr_assert('lock_time', b'', 'Expected byte-like object')
        self.attr_assert('expiry_height', b'', 'Expected byte-like object')
        self.attr_assert('expiry_height', b'\xff' * 4, 'Expiry time too high')
        self.attr_assert('tx_ins', [b''], 'Invalid TxIn. ')
        self.attr_assert('tx_outs', [b''], 'Invalid TxOut. ')
        self.attr_assert('tx_joinsplits', [b''] * 6, 'Too many joinsplits.')
        self.attr_assert('tx_joinsplits', [b''], 'Invalid Joinsplit. ')
        self.attr_assert('tx_joinsplits', [], 'Transaction must have ')
        self.attr_assert('joinsplit_pubkey', b'', 'Expected byte-like object')
        self.attr_assert('joinsplit_sig', b'\x00', 'Expected byte-like object')

    def test_calculate_fee(self):
        t = tx.OverwinterTx(**self.tx)
        self.assertEqual(
            t.calculate_fee([]),
            10000)

    def test_not_overwinter(self):
        riemann.select_network('zcash_sprout_main')
        with self.assertRaises(ValueError) as context:
            tx.OverwinterTx(None, None, None, None,
                            None, None, None)
        self.assertIn(
            'OverwinterTx not supported by network ',
            str(context.exception))

    def test_from_bytes_no_js(self):
        self.assertIsInstance(
            tx.OverwinterTx.from_bytes(
                helpers.ZCASH_OVERWINTER_NO_JS['ser']['tx']),
            tx.OverwinterTx)


class OverwinterSighash(unittest.TestCase):

    def setUp(self):
        riemann.select_network('zcash_overwinter_main')
        self.tx = tx.OverwinterTx.from_bytes(helpers.RAW_TX)

    def test_hash_prevouts(self):
        self.assertEqual(
            self.tx._hash_prevouts(anyone_can_pay=False),
            helpers.HASH_PREVOUTS)

    def test_hash_outputs(self):
        self.assertEqual(
            self.tx._hash_outputs(tx.SIGHASH_SINGLE, index=1),
            helpers.HASH_OUTPUTS)

    def test_hash_joinsplits(self):
        self.assertEqual(
            self.tx._hash_joinsplits(),
            helpers.HASH_JOINSPLITS)

    def test_sighash(self):
        self.assertEqual(
            self.tx.sighash_single(
                tx.SIGHASH_SINGLE,
                index=1,
                script_code=helpers.SCRIPT_CODE,
                prevout_value=helpers.PREVOUT_VALUE),
            helpers.SIGHASH)
