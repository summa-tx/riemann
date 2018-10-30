import unittest
import riemann
from riemann import utils
from riemann.tx import sapling
from riemann.tests.tx.helpers import sapling_helpers


class SaplingTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        riemann.select_network('zcash_sapling_main')

    def tearDown(self):
        riemann.select_network('bitcoin_main')

    def attr_assert(self, Class, data_dict, attr_name, replacement, err_text):
        # Removes a named key from a dictionary and replaces it with b'\x00'
        temp_dict = dict((a, data_dict[a])
                         for a in data_dict
                         if a != attr_name)
        temp_dict[attr_name] = replacement
        with self.assertRaises(ValueError) as context:
            Class(**temp_dict)

        self.assertIn(err_text, str(context.exception))


class TestSaplingShieldedSpend(SaplingTestCase):

    def test_from_hex(self):
        for ss in sapling_helpers.TXNS[0]['vShieldedSpend']:
            spend = sapling.SaplingShieldedSpend.from_hex(ss['full'])
            self.assertEqual(
                spend.cv.hex(),
                ss['cv'])
            self.assertEqual(
                spend.anchor.hex(),
                ss['anchor'])
            self.assertEqual(
                spend.nullifier.hex(),
                ss['nullifier'])
            self.assertEqual(
                spend.rk.hex(),
                ss['rk'])
            self.assertEqual(
                spend.zkproof.hex(),
                ss['zkproof'])
            self.assertEqual(
                spend.spend_auth_sig.hex(),
                ss['spend_auth_sig'])

    def test_init_errors(self):
        ss = sapling_helpers.TXNS[0]['vShieldedSpend'][0].copy()
        ss.pop('full')
        for k, v in ss.items():
            ss[k] = bytes.fromhex(v)

        S = sapling.SaplingShieldedSpend

        self.attr_assert(S, ss, 'cv', b'', 'Expected byte-like')
        self.attr_assert(S, ss, 'anchor', b'', 'Expected byte-like')
        self.attr_assert(S, ss, 'nullifier', b'', 'Expected byte-like')
        self.attr_assert(S, ss, 'rk', b'', 'Expected byte-like')
        self.attr_assert(S, ss, 'zkproof', b'', 'Invalid zkproof')
        self.attr_assert(S, ss, 'spend_auth_sig', b'', 'Expected byte-like')


class TestSaplingShieldedOutput(SaplingTestCase):

    def test_from_hex(self):
        for so in sapling_helpers.TXNS[0]['vShieldedOutput']:
            output = sapling.SaplingShieldedOutput.from_hex(so['full'])
            self.assertEqual(
                output.cv.hex(),
                so['cv'].hex())
            self.assertEqual(
                output.cmu.hex(),
                so['cmu'].hex())
            self.assertEqual(
                output.ephemeral_key.hex(),
                so['ephemeral_key'].hex())
            self.assertEqual(
                output.enc_ciphertext.hex(),
                so['enc_ciphertext'].hex())
            self.assertEqual(
                output.out_ciphertext.hex(),
                so['out_ciphertext'].hex())
            self.assertEqual(
                output.zkproof.hex(),
                so['zkproof'].hex())

    def test_init_errors(self):
        S = sapling.SaplingShieldedOutput
        so = sapling_helpers.TXNS[0]['vShieldedOutput'][0].copy()
        so.pop('full')
        self.attr_assert(S, so, 'cv', b'', 'Expected byte-like')
        self.attr_assert(S, so, 'cmu', b'', 'Expected byte-like')
        self.attr_assert(S, so, 'ephemeral_key', b'', 'Expected byte-like')
        self.attr_assert(S, so, 'enc_ciphertext', b'', 'Expected byte-like')
        self.attr_assert(S, so, 'zkproof', b'', 'Invalid zkproof')


class TestSaplingZkproof(SaplingTestCase):

    def test_from_hex(self):
        zk = sapling_helpers.ZKPROOF
        zkproof = sapling.SaplingZkproof.from_hex(zk['full'])
        self.assertEqual(
            zkproof.pi_sub_a.hex(),
            zk['pi_sub_a'].hex())
        self.assertEqual(
            zkproof.pi_sub_b.hex(),
            zk['pi_sub_b'].hex())
        self.assertEqual(
            zkproof.pi_sub_c.hex(),
            zk['pi_sub_c'].hex())

    def test_init_errors(self):
        Z = sapling.SaplingZkproof
        zk = sapling_helpers.ZKPROOF.copy()
        zk.pop('full')
        self.attr_assert(Z, zk, 'pi_sub_a', b'', 'Expected byte-like')
        self.attr_assert(Z, zk, 'pi_sub_b', b'', 'Expected byte-like')
        self.attr_assert(Z, zk, 'pi_sub_c', b'', 'Expected byte-like')


class TestSaplingJoinsplit(SaplingTestCase):

    def test_from_hex(self):
        for js in sapling_helpers.TXNS[0]['vJoinsplits']:
            output = sapling.SaplingJoinsplit.from_hex(js['full'])
            self.assertEqual(
                output.vpub_old.hex(),
                js['vpub_old'].hex())
            self.assertEqual(
                output.vpub_new.hex(),
                js['vpub_new'].hex())
            self.assertEqual(
                output.anchor.hex(),
                js['anchor'].hex())
            self.assertEqual(
                output.nullifiers.hex(),
                js['nullifiers'].hex())
            self.assertEqual(
                output.commitments.hex(),
                js['commitments'].hex())
            self.assertEqual(
                output.ephemeral_key.hex(),
                js['ephemeral_key'].hex())
            self.assertEqual(
                output.random_seed.hex(),
                js['random_seed'].hex())
            self.assertEqual(
                output.vmacs.hex(),
                js['vmacs'].hex())
            self.assertEqual(
                output.zkproof.hex(),
                js['zkproof'].hex())
            self.assertEqual(
                output.encoded_notes.hex(),
                js['encoded_notes'].hex())

    def test_init_errors(self):
        J = sapling.SaplingJoinsplit
        js = sapling_helpers.TXNS[0]['vJoinsplits'][0].copy()
        js.pop('full')

        self.attr_assert(J, js, 'vpub_old', b'', 'Expected byte-like')
        self.attr_assert(J, js, 'vpub_new', b'', 'Expected byte-like')
        self.attr_assert(J, js, 'anchor', b'', 'Expected byte-like')
        self.attr_assert(J, js, 'nullifiers', b'', 'Expected byte-like')
        self.attr_assert(J, js, 'commitments', b'', 'Expected byte-like')
        self.attr_assert(J, js, 'ephemeral_key', b'', 'Expected byte-like')
        self.attr_assert(J, js, 'random_seed', b'', 'Expected byte-like')
        self.attr_assert(J, js, 'vmacs', b'', 'Expected byte-like')
        self.attr_assert(J, js, 'zkproof', b'', 'Invalid zkproof')
        self.attr_assert(J, js, 'encoded_notes', b'', 'Expected byte-like')

        js['vpub_old'] = b'\xff' * 8
        self.attr_assert(J, js, 'vpub_new', b'\xff' * 8, 'must be zero')


class TestSaplingTx(SaplingTestCase):

    def setUp(self):
        super().setUp()
        self.tx_dict = sapling_helpers.TXNS[0]['as_dict'].copy()
        self.tx = sapling.SaplingTx(**self.tx_dict)

    def test_from_hex(self):
        for txn in sapling_helpers.TXNS:
            test_tx = sapling.SaplingTx.from_hex(txn['hex'])
            self.assertEqual(
                test_tx.binding_sig.hex(),
                txn['bindingSig'])
            self.assertEqual(
                utils.le2i(test_tx.expiry_height),
                txn['expiryHeight'])
            for pair in zip(test_tx.tx_shielded_spends, txn['vShieldedSpend']):
                self.assertEqual(
                    pair[0].cv.hex(),
                    pair[1]['cv'])
                self.assertEqual(
                    pair[0].anchor.hex(),
                    pair[1]['anchor'])
                self.assertEqual(
                    pair[0].nullifier.hex(),
                    pair[1]['nullifier'])
                self.assertEqual(
                    pair[0].zkproof.hex(),
                    pair[1]['zkproof'])
                self.assertEqual(
                    pair[0].spend_auth_sig.hex(),
                    pair[1]['spend_auth_sig'])

    def test_init_network_error(self):
        riemann.select_network('zcash_sprout_main')
        with self.assertRaises(ValueError) as context:
            sapling.SaplingTx(**self.tx_dict)

        self.assertIn('SaplingTx not supported', str(context.exception))

    def test_init_value_balance_error(self):
        temp_dict = self.tx_dict.copy()
        temp_dict['value_balance'] = b'\x01' * 8
        temp_dict['tx_shielded_spends'] = []
        temp_dict['tx_shielded_outputs'] = []
        with self.assertRaises(ValueError) as context:
            sapling.SaplingTx(**temp_dict)

        self.assertIn('must be 8 0-bytes', str(context.exception))

    def test_no_input_value(self):
        temp_dict = self.tx_dict.copy()
        temp_dict['tx_ins'] = []
        temp_dict['tx_shielded_spends'] = []
        temp_dict['tx_joinsplits'] = []
        with self.assertRaises(ValueError) as context:
            sapling.SaplingTx(**temp_dict)

        self.assertIn('Transaction must have some input value',
                      str(context.exception))

    def test_misc_init_errors(self):
        td = self.tx_dict
        T = sapling.SaplingTx
        self.attr_assert(T, td, 'lock_time', b'', 'Expected byte-like')
        self.attr_assert(T, td, 'expiry_height', b'', 'Expected byte-like')
        self.attr_assert(T, td, 'value_balance', b'', 'Expected byte-like')
        self.attr_assert(T, td, 'expiry_height', b'\xff' * 4, '499999999')
        self.attr_assert(T, td, 'binding_sig', b'', 'Expected byte-like')
        self.attr_assert(T, td, 'tx_ins', [b''], 'Invalid TxIn')
        self.attr_assert(T, td, 'tx_outs', [b''], 'Invalid TxOut')
        self.attr_assert(T, td, 'tx_joinsplits', [b''] * 6, 'Too many join')
        self.attr_assert(
            T, td, 'tx_shielded_spends', [b''] * 3, 'Invalid shielded spend')
        self.attr_assert(
            T, td, 'tx_shielded_outputs', [b''] * 3, 'Invalid shielded output')
        self.attr_assert(T, td, 'tx_joinsplits', [b''], 'Invalid Joinsplit')
        self.attr_assert(T, td, 'joinsplit_pubkey', b'', 'Expected byte-like')
        self.attr_assert(T, td, 'joinsplit_sig', b'', 'Expected byte-like')

    def test_sighash(self):
        for txn in sapling_helpers.SIGHASH:
            test_tx = sapling.SaplingTx.from_hex(txn['hex'])
            self.assertEqual(
                test_tx._hash_prevouts(anyone_can_pay=False).hex(),
                txn['hashPrevouts'])
            self.assertEqual(
                test_tx._hash_sequence(
                    sighash_type=txn['sighash_type'],
                    anyone_can_pay=False).hex(),
                txn['hashSequence'])
            self.assertEqual(
                test_tx._hash_outputs(
                    sighash_type=txn['sighash_type'],
                    index=txn['index']).hex(),
                txn['hashOutputs'])
            self.assertEqual(
                test_tx._hash_joinsplits().hex(),
                txn['hashJoinSplits'])
            self.assertEqual(
                test_tx._hash_shielded_spends().hex(),
                txn['hashShieldedSpends'])
            self.assertEqual(
                test_tx._hash_shielded_outputs().hex(),
                txn['hashShieldedOutputs'])
            self.assertEqual(
                test_tx.sighash(
                    sighash_type=txn['sighash_type'],
                    index=txn['index'],
                    joinsplit=txn['joinsplit'],
                    script_code=bytes.fromhex(txn['script_code']),
                    anyone_can_pay=txn['anyone_can_pay'],
                    prevout_value=bytes.fromhex(txn['amount'])).hex(),
                txn['sighash'])
