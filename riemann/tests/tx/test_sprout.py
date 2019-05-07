import riemann
import unittest
from riemann import tx
from riemann.tests.helpers import P2SH
from riemann.tests.tx.helpers import overwinter_helpers as helpers


class SproutTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        riemann.select_network('zcash_sprout_main')

    def tearDown(self):
        riemann.select_network('bitcoin_main')


class TestZcashByteData(SproutTestCase):

    def test_init_error(self):
        riemann.select_network('bitcoin_main')
        with self.assertRaises(ValueError) as context:
            tx.ZcashByteData()

        self.assertIn('Zcash classes not supported by network bitcoin_main. '
                      'How did you get here?',
                      str(context.exception))


class TestSpoutZkproof(SproutTestCase):

    def setUp(self):
        super().setUp()
        self.zkproof = helpers.ZCASH_SPROUT['ser']['joinsplits'][0]['zkproof']
        self.ser_proof = helpers.ZCASH_SPROUT['ser']['joinsplits'][0]['proof']

    def attr_assert(self, attr_name, replacement, err_text):
        # Removes a named key from a dictionary and replaces it with b'\x00'
        temp_dict = dict((a, self.zkproof[a])
                         for a in self.zkproof
                         if a != attr_name)
        temp_dict[attr_name] = replacement
        with self.assertRaises(ValueError) as context:
            tx.SproutZkproof(**temp_dict)

        self.assertIn(err_text, str(context.exception))

    def test_init_errors(self):
        self.attr_assert('pi_sub_a', b'', 'Expected byte-like object')
        self.attr_assert('pi_prime_sub_a', b'', 'Expected byte-like object')
        self.attr_assert('pi_sub_b', b'', 'Expected byte-like object')
        self.attr_assert('pi_prime_sub_b', b'', 'Expected byte-like object')
        self.attr_assert('pi_sub_c', b'', 'Expected byte-like object')
        self.attr_assert('pi_prime_sub_c', b'', 'Expected byte-like object')
        self.attr_assert('pi_sub_k', b'', 'Expected byte-like object')
        self.attr_assert('pi_sub_h', b'', 'Expected byte-like object')

    def test_from_bytes(self):
        self.assertEqual(
            tx.SproutZkproof.from_bytes(self.ser_proof),
            tx.SproutZkproof(**self.zkproof))


class TestSproutJoinsplit(SproutTestCase):

    def setUp(self):
        super().setUp()
        self.joinsplit_ser = helpers.ZCASH_SPROUT['ser']['joinsplit_0']
        self.zkproof = tx.SproutZkproof.from_bytes(
            helpers.ZCASH_SPROUT['ser']['joinsplits'][0]['proof'])
        self.joinsplit = helpers.ZCASH_SPROUT['ser']['joinsplits'][0].copy()
        self.joinsplit['zkproof'] = self.zkproof
        self.joinsplit.pop('proof')  # remove this entry from the dict

    def attr_assert(self, attr_name, replacement, err_text):
        # Removes a named key from a dictionary and replaces it with b'\x00'
        temp_dict = dict((a, self.joinsplit[a])
                         for a in self.joinsplit
                         if a != attr_name)
        temp_dict[attr_name] = replacement
        with self.assertRaises(ValueError) as context:
            tx.SproutJoinsplit(**temp_dict)

        self.assertIn(err_text, str(context.exception))

    def test_init_errors(self):
        self.attr_assert('vpub_old', b'', 'Expected byte-like object')
        self.attr_assert('vpub_new', b'', 'Expected byte-like object')
        self.attr_assert('anchor', b'', 'Expected byte-like object')
        self.attr_assert('nullifiers', b'', 'Expected byte-like object')
        self.attr_assert('commitments', b'', 'Expected byte-like object')
        self.attr_assert('ephemeral_key', b'', 'Expected byte-like object')
        self.attr_assert('random_seed', b'', 'Expected byte-like object')
        self.attr_assert('vmacs', b'', 'Expected byte-like object')
        self.attr_assert('zkproof', b'', 'Invalid zkproof. ')
        self.attr_assert('encoded_notes', b'', 'Expected byte-like object')

    def test_from_bytes(self):
        self.assertEqual(
            tx.SproutJoinsplit.from_bytes(self.joinsplit_ser),
            tx.SproutJoinsplit(**self.joinsplit))

    def test_vpub_zero(self):
        self.attr_assert(
            'vpub_old', b'\xff' * 8, 'vpub_old or vpub_new must be zero')


class TestSproutTx(SproutTestCase):

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

        self.tx['version'] = helpers.ZCASH_SPROUT['ser']['version']
        self.tx['tx_ins'] = []
        self.tx_out = tx.TxOut.from_bytes(
            helpers.ZCASH_SPROUT['ser']['tx_out_0'])
        self.tx['tx_outs'] = [self.tx_out]
        self.tx['lock_time'] = helpers.ZCASH_SPROUT['ser']['lock_time']
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
            tx.SproutTx(**temp_dict)

        self.assertIn(err_text, str(context.exception))

    def test_init_errors(self):
        self.attr_assert('version', b'', 'Expected byte-like object')
        self.attr_assert('lock_time', b'', 'Expected byte-like object')
        self.attr_assert('tx_ins', [b''], 'Invalid TxIn. ')
        self.attr_assert('tx_outs', [b''], 'Invalid TxOut. ')
        self.attr_assert(
            'version', b'\x01\x00\x00\x00', 'Joinsplits not allowed')
        self.attr_assert('tx_joinsplits', [b''] * 6, 'Too many joinsplits.')
        self.attr_assert('tx_joinsplits', [b''], 'Invalid Joinsplit. ')
        self.attr_assert('joinsplit_pubkey', b'', 'Expected byte-like object')
        self.attr_assert('joinsplit_sig', b'\x00', 'Expected byte-like object')
        self.attr_assert(
            'version', b'\x04\x00\x00\x00', 'Version must be 1 or 2. ')

    def test_no_inputs(self):
        temp_dict = self.tx.copy()
        temp_dict['version'] = b'\x01\x00\x00\x00'
        temp_dict['tx_joinsplits'] = []

        with self.assertRaises(ValueError) as context:
            tx.SproutTx(**temp_dict)

        self.assertIn(
            'Version 1 txns must have at least 1 input',
            str(context.exception))

    def test_from_bytes(self):
        self.assertEqual(
            tx.SproutTx.from_bytes(self.tx_ser),
            tx.SproutTx(**self.tx))

    def test_tx_ids(self):
        t = tx.SproutTx(**self.tx)
        self.assertEqual(
            t.tx_id_le,
            bytes.fromhex('1add6cdbe72ede27cd3b6cd85f45d02081b9d57f173090df80648cdb927eb167'))  # noqa: E501
        self.assertEqual(
            t.tx_id,
            bytes.fromhex('67b17e92db8c6480df9030177fd5b98120d0455fd86c3bcd27de2ee7db6cdd1a'))  # noqa: E501

    def test_from_bytes_with_tx_in(self):
        # This is a bit hard to read
        temp_dict = self.tx.copy()
        temp_dict['tx_ins'] = \
            [tx.TxIn.from_bytes(P2SH['ser']['ins'][0]['input'])]

        # Take the current serialization's version,
        # Add b'\x01' for 1 tx_in
        # Add the tx_in from another transaction
        # Add back the rest of the serialization
        temp_ser = \
            self.tx_ser[0:4] \
            + b'\x01' \
            + P2SH['ser']['ins'][0]['input'] \
            + self.tx_ser[5:]

        self.assertEqual(
            tx.SproutTx.from_bytes(temp_ser),
            tx.SproutTx(**temp_dict))

    def test_copy(self):
        t = tx.SproutTx(**self.tx)
        t_copy = t.copy()

        self.assertEqual(t, t_copy)
        self.assertIsNot(t, t_copy)

    def test_print_sighash(self):
        t = tx.SproutTx(**self.tx)
        print('SproutTx Test Sighash:',
              t.sighash_all(index=0, script=b'\x0100'))

    def test_calculate_fee(self):
        t = tx.SproutTx(**self.tx)
        self.assertEqual(
            t.calculate_fee([]),
            10000)
