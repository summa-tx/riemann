import unittest
import riemann
from riemann import simple
from riemann import tx as txn
from riemann.tests import helpers


class TestSimple(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        riemann.select_network('bitcoin_main')

    def test_guess_version(self):
        self.assertEqual(
            simple.guess_version('OP_IF'),
            1)
        self.assertEqual(
            simple.guess_version('OP_CHECKSEQUENCEVERIFY'),
            2)

        riemann.select_network('zcash_sprout_main')
        self.assertEqual(
            simple.guess_version('OP_IF'),
            1)

        riemann.select_network('zcash_overwinter_main')
        self.assertEqual(
            simple.guess_version('OP_IF'),
            3)

        riemann.select_network('zcash_sapling_main')
        self.assertEqual(
            simple.guess_version('OP_IF'),
            4)

    def test_guess_sequence(self):
        self.assertEqual(
            simple.guess_sequence('OP_IF'),
            0xFFFFFFFE)
        self.assertEqual(
            simple.guess_sequence('0000FFEE OP_CHECKSEQUENCEVERIFY'),
            0x0000FFEE)

    def test_guess_locktime(self):
        self.assertEqual(
            simple.guess_locktime('OP_IF'),
            0)
        self.assertEqual(
            simple.guess_locktime('0000FFEE OP_CHECKLOCKTIMEVERIFY'),
            0x0000FFEE)

    def test_output(self):
        for i in range(len(helpers.P2WSH['human']['outs'])):
            self.assertEqual(
                simple.output(
                    value=helpers.P2WSH['human']['outs'][i]['value'],
                    address=helpers.P2WSH['human']['outs'][i]['addr']),
                helpers.P2WSH['ser']['outs'][i]['output'])

    def test_empty_output(self):
        self.assertEqual(
            simple.empty_output(),
            b'\xff' * 8 + b'\x00')

    def test_outpoint(self):
        self.assertEqual(
            simple.outpoint(
                tx_id=helpers.P2PKH['human']['ins'][0]['hash'],
                index=helpers.P2PKH['human']['ins'][0]['index']),
            helpers.P2PKH['ser']['ins'][0]['outpoint'])

    def test_empty_outpoint(self):
        self.assertEqual(
            simple.empty_outpoint(),
            b'\x00' * 36)

    def test_unsigned_input(self):
        outpoint = simple.outpoint(
            tx_id=helpers.P2PKH['human']['ins'][0]['hash'],
            index=helpers.P2PKH['human']['ins'][0]['index'])

        self.assertEqual(
            simple.unsigned_input(
                outpoint=outpoint),
            outpoint.to_bytes() + b'\x00' + b'\xFE\xFF\xFF\xFF')

        self.assertEqual(
            simple.unsigned_input(
                outpoint=outpoint,
                sequence=0x1234abcd),
            outpoint.to_bytes() + b'\x00' + b'\xcd\xab\x34\x12')

        self.assertEqual(
            simple.unsigned_input(
                outpoint=outpoint,
                redeem_script='11AA OP_CHECKSEQUENCEVERIFY'),
            outpoint.to_bytes() + b'\x00' + b'\xaa\x11\x00\x00')

        self.assertEqual(
            simple.unsigned_input(
                outpoint=outpoint,
                redeem_script='11AA OP_CHECKSEQUENCEVERIFY',
                sequence=0x1234abcd),
            outpoint.to_bytes() + b'\x00' + b'\xcd\xab\x34\x12')

        riemann.select_network('decred_main')

        outpoint = simple.outpoint(
            tx_id=helpers.DCR['human']['ins'][0]['hash'],
            index=helpers.DCR['human']['ins'][0]['index'],
            tree=helpers.DCR['human']['ins'][0]['tree'])

        self.assertEqual(
            simple.unsigned_input(
                outpoint=outpoint,
                sequence=helpers.DCR['human']['ins'][0]['sequence']),
            helpers.DCR['ser']['tx']['in_unsigned'])

    def test_empty_input(self):
        self.assertEqual(
            simple.empty_input(),
            b'\x00' * 41)

    def test_p2pkh_input(self):
        outpoint = simple.outpoint(
            tx_id=helpers.P2PKH['human']['ins'][0]['hash'],
            index=helpers.P2PKH['human']['ins'][0]['index'])

        self.assertEqual(
            simple.p2pkh_input(
                outpoint=outpoint,
                sig=helpers.P2PKH['human']['ins'][0]['signature'],
                pubkey=helpers.P2PKH['human']['ins'][0]['pubkey'],
            ),
            helpers.P2PKH['ser']['ins'][0]['input']
        )

    def test_p2pkh_input_and_witness(self):
        outpoint = simple.outpoint(
            tx_id=helpers.P2PKH['human']['ins'][0]['hash'],
            index=helpers.P2PKH['human']['ins'][0]['index'])

        (tx_in, witness) = simple.p2pkh_input_and_witness(
            outpoint=outpoint,
            sig=helpers.P2PKH['human']['ins'][0]['signature'],
            pubkey=helpers.P2PKH['human']['ins'][0]['pubkey'],
            sequence=helpers.P2PKH['human']['ins'][0]['sequence'])

        self.assertEqual(
            tx_in,
            helpers.P2PKH['ser']['ins'][0]['input'])
        self.assertEqual(
            witness,
            b'\x00')

    def test_p2sh_input(self):

        outpoint = simple.outpoint(
            tx_id=helpers.P2SH_PD1['human']['ins'][0]['hash'],
            index=helpers.P2SH_PD1['human']['ins'][0]['index'])
        tx_p2sh_input = simple.p2sh_input(
            outpoint=outpoint,
            stack_script=helpers.P2SH_PD1['human']['ins'][0]['stack_script'],
            redeem_script=helpers.P2SH_PD1['human']['ins'][0]['redeem_script'],
            sequence=helpers.P2SH_PD1['human']['ins'][0]['sequence'])

        self.assertTrue(tx_p2sh_input.is_p2sh())

        self.assertEqual(
            tx_p2sh_input.stack_script,
            helpers.P2SH_PD1['ser']['ins'][0]['stack_script'])
        self.assertEqual(
            tx_p2sh_input.redeem_script,
            helpers.P2SH_PD1['ser']['ins'][0]['redeem_script'])
        self.assertEqual(
            tx_p2sh_input,
            helpers.P2SH_PD1['ser']['ins'][0]['input'])

        # Seems weird, but tests sequence guessing
        outpoint = simple.outpoint(
            tx_id=helpers.P2PKH['human']['ins'][0]['hash'],
            index=helpers.P2PKH['human']['ins'][0]['index'])
        tx_p2sh_input = simple.p2sh_input(
            outpoint=outpoint,
            stack_script=helpers.P2PKH['human']['ins'][0]['stack_script'],
            redeem_script='',
            sequence=None)

        self.assertEqual(
            tx_p2sh_input,
            helpers.P2PKH['ser']['ins'][0]['input'])

    def test_p2sh_input_and_witness(self):

        outpoint = simple.outpoint(
            helpers.P2SH_PD1['human']['ins'][0]['hash'],
            helpers.P2SH_PD1['human']['ins'][0]['index'])
        (tx_p2sh_input, witness) = simple.p2sh_input_and_witness(
            outpoint=outpoint,
            stack_script=helpers.P2SH_PD1['human']['ins'][0]['stack_script'],
            redeem_script=helpers.P2SH_PD1['human']['ins'][0]['redeem_script'],
            sequence=helpers.P2SH_PD1['human']['ins'][0]['sequence'])

        self.assertTrue(tx_p2sh_input.is_p2sh())
        self.assertEqual(witness, b'\x00')
        self.assertEqual(
            tx_p2sh_input.stack_script,
            helpers.P2SH_PD1['ser']['ins'][0]['stack_script'])
        self.assertEqual(
            tx_p2sh_input.redeem_script,
            helpers.P2SH_PD1['ser']['ins'][0]['redeem_script'])
        self.assertEqual(
            tx_p2sh_input,
            helpers.P2SH_PD1['ser']['ins'][0]['input'])

        # Seems weird but tests sequence guessing
        outpoint = simple.outpoint(
            tx_id=helpers.P2PKH['human']['ins'][0]['hash'],
            index=helpers.P2PKH['human']['ins'][0]['index'])
        (tx_in, witness) = simple.p2sh_input_and_witness(
            outpoint=outpoint,
            stack_script=helpers.P2PKH['human']['ins'][0]['stack_script'],
            redeem_script='',
            sequence=None)

        self.assertEqual(
            tx_in,
            helpers.P2PKH['ser']['ins'][0]['input'])

        self.assertEqual(
            witness,
            b'\x00')

    def test_p2wpkh_input_and_witness(self):
        outpoint = simple.outpoint(
            tx_id=helpers.P2WPKH['human']['ins'][0]['hash'],
            index=helpers.P2WPKH['human']['ins'][0]['index'])

        (tx_in, witness) = simple.p2wpkh_input_and_witness(
            outpoint=outpoint,
            sig=helpers.P2WPKH['human']['witnesses'][0]['signature'],
            pubkey=helpers.P2WPKH['human']['witnesses'][0]['pubkey'],
            sequence=helpers.P2WPKH['human']['ins'][0]['sequence'])

        self.assertEqual(
            tx_in,
            helpers.P2WPKH['ser']['ins'][0]['input'])
        self.assertEqual(
            witness,
            helpers.P2WPKH['ser']['witnesses'][0]['witness'])

    def test_p2wsh_input_and_witness(self):
        helper_witness = helpers.P2WSH['human']['witnesses'][0]
        outpoint = simple.outpoint(
            tx_id=helpers.P2WSH['human']['ins'][0]['hash'],
            index=helpers.P2WSH['human']['ins'][0]['index'])
        (tx_in, witness) = simple.p2wsh_input_and_witness(
            outpoint=outpoint,
            stack=helper_witness['stack'],
            witness_script=helper_witness['wit_script'],
            sequence=helpers.P2WSH['human']['ins'][0]['sequence'])

        self.assertEqual(tx_in, helpers.P2WSH['ser']['ins'][0]['input'])
        self.assertEqual(witness, helpers.P2WSH['ser']['tx']['witness'])

        helper_witness = helpers.P2WSH['human']['witnesses'][0]
        outpoint = simple.outpoint(
            tx_id=helpers.P2WSH['human']['ins'][0]['hash'],
            index=helpers.P2WSH['human']['ins'][0]['index'])

        (tx_in, witness) = simple.p2wsh_input_and_witness(
            outpoint=outpoint,
            stack=helper_witness['stack'],
            witness_script=helper_witness['wit_script'],
            sequence=None)

        self.assertEqual(
            tx_in,
            helpers.INPUT_FOR_WITNESS_SEQUENCE_GUESSING)

    def test_empty_input_witness(self):
        self.assertEqual(
            simple.empty_input_witness(),
            b'\x00')

    def test_unsigned_legacy_tx(self):

        outpoint = simple.outpoint(
            tx_id=helpers.P2PKH['human']['ins'][0]['hash'],
            index=helpers.P2PKH['human']['ins'][0]['index'])
        tx_in = simple.unsigned_input(
            outpoint=outpoint,
            sequence=helpers.P2PKH['human']['ins'][0]['sequence'])
        tx_out = simple.output(
            helpers.P2PKH['human']['outs'][0]['value'],
            helpers.P2PKH['human']['outs'][0]['addr'])
        tx_return_output = txn.make_op_return_output(
            helpers.P2PKH['human']['outs'][1]['memo'])
        tx = simple.unsigned_legacy_tx(
            tx_ins=[tx_in],
            tx_outs=[tx_out, tx_return_output])

        self.assertEqual(tx, helpers.P2PKH['ser']['tx']['unsigned'])

    def test_unsigned_witness_tx(self):
        outpoint = simple.outpoint(
            tx_id=helpers.P2WPKH['human']['ins'][0]['hash'],
            index=helpers.P2WPKH['human']['ins'][0]['index'])
        tx_in = simple.unsigned_input(
            outpoint=outpoint,
            sequence=helpers.P2WPKH['human']['ins'][0]['sequence'])
        tx_out = simple.output(
            helpers.P2WPKH['human']['outs'][0]['value'],
            helpers.P2WPKH['human']['outs'][0]['addr'])
        tx = simple.unsigned_witness_tx(
            tx_ins=[tx_in],
            tx_outs=[tx_out])

        self.assertEqual(tx, helpers.P2WPKH['ser']['tx']['unsigned'])

    def test_legacy_tx(self):
        outpoint = simple.outpoint(
            tx_id=helpers.P2PKH['human']['ins'][0]['hash'],
            index=helpers.P2PKH['human']['ins'][0]['index'])
        tx_in = simple.p2pkh_input(
            outpoint=outpoint,
            sig=helpers.P2PKH['human']['ins'][0]['signature'],
            pubkey=helpers.P2PKH['human']['ins'][0]['pubkey'],
            sequence=helpers.P2PKH['human']['ins'][0]['sequence'])
        tx_out = simple.output(
            helpers.P2PKH['human']['outs'][0]['value'],
            helpers.P2PKH['human']['outs'][0]['addr'])
        tx_return_output = txn.make_op_return_output(
            helpers.P2PKH['human']['outs'][1]['memo'])

        tx = simple.legacy_tx([tx_in], [tx_out, tx_return_output])

        self.assertEqual(tx, helpers.P2PKH['ser']['tx']['signed'])

    def test_witness_tx(self):
        outpoint = simple.outpoint(
            tx_id=helpers.P2WPKH['human']['ins'][0]['hash'],
            index=helpers.P2WPKH['human']['ins'][0]['index'])
        (tx_in, witness) = simple.p2wpkh_input_and_witness(
            outpoint=outpoint,
            sig=helpers.P2WPKH['human']['witnesses'][0]['signature'],
            pubkey=helpers.P2WPKH['human']['witnesses'][0]['pubkey'],
            sequence=helpers.P2WPKH['human']['ins'][0]['sequence'])
        tx_out = simple.output(
            value=helpers.P2WPKH['human']['outs'][0]['value'],
            address=helpers.P2WPKH['human']['outs'][0]['addr'])
        tx = simple.witness_tx(
            tx_ins=[tx_in],
            tx_outs=[tx_out],
            tx_witnesses=[witness])

        self.assertEqual(
            tx,
            helpers.P2WPKH['ser']['tx']['signed'])

    def test_witness_tx_exception(self):
        outpoint = simple.outpoint(
            tx_id=helpers.P2WPKH['human']['ins'][0]['hash'],
            index=helpers.P2WPKH['human']['ins'][0]['index'])
        (tx_in, witness) = simple.p2wpkh_input_and_witness(
            outpoint=outpoint,
            sig=helpers.P2WPKH['human']['witnesses'][0]['signature'],
            pubkey=helpers.P2WPKH['human']['witnesses'][0]['pubkey'],
            sequence=helpers.P2WPKH['human']['ins'][0]['sequence'])
        tx_out = simple.output(
            value=helpers.P2WPKH['human']['outs'][0]['value'],
            address=helpers.P2WPKH['human']['outs'][0]['addr'])
        witness = txn.InputWitness.from_bytes(b'\x02\x02\xab\xab\x01\xab')

        tx = simple.witness_tx(
            tx_ins=[tx_in],
            tx_outs=[tx_out],
            tx_witnesses=[witness])

        self.assertEqual(
            tx.lock_time,
            b'\x00' * 4)

        self.assertEqual(
            tx.version,
            b'\x01' + b'\x00' * 3)
