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

    def test_output(self):
        for i in range(len(helpers.P2WSH['human']['outs'])):
            self.assertEqual(
                simple.output(
                    value=helpers.P2WSH['human']['outs'][i]['value'],
                    address=helpers.P2WSH['human']['outs'][i]['addr']),
                helpers.P2WSH['ser']['outs'][i]['output'])

    def test_outpoint(self):
        self.assertEqual(
            simple.outpoint(
                tx_id=helpers.P2PKH['human']['ins'][0]['hash'],
                index=helpers.P2PKH['human']['ins'][0]['index']),
            helpers.P2PKH['ser']['ins'][0]['outpoint'])

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
            tx_outs=[tx_out],
            lock_time=helpers.P2WPKH['human']['locktime'])

        self.assertEqual(tx, helpers.P2WPKH['ser']['tx']['unsigned'])
