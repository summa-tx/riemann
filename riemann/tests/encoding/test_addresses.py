import unittest
import riemann
from riemann import utils
from .. import helpers
from ...encoding import addresses as addr

# NB:
# How to make more of these.
# 1. Install python-bitcoinlib
# 2. Compile a script to an array of ints (same as input to bytes class)
# 3. Follow procedure below
#
# from bitcoin.core.script import CScript
# from bitcoin.wallet import CBitcoinAddress
# a = CScript(bytes.fromhex('HEX SCRIPT'))
# CBitcoinAddress.from_scriptPubKey(a.to_p2sh_scriptPubKey()
#
# For more P2PKH addresses:
# P2PKHBitcoinAddress.from_pubkey(PUBKEY_BYTES, accept_invalid=True)


class TestAddresses(unittest.TestCase):

    def tearDown(self):
        riemann.select_network('bitcoin_main')

    def test_make_p2sh_address(self):
        a = addr.make_p2sh_address('OP_IF')
        self.assertEqual(a, helpers.OP_IF['p2sh'])

    def test_make_p2sh_address_msig(self):
        a = addr.make_p2sh_address(helpers.MSIG_2_2['redeem_script'])
        self.assertEqual(a, helpers.MSIG_2_2['p2sh'])

    def test_make_p2wsh_address(self):
        a = addr.make_p2wsh_address(
            helpers.P2WSH['human']['witnesses'][0]['wit_script'])
        self.assertEqual(a, helpers.P2WSH['human']['ins'][0]['addr'])

    def test_make_p2pkh_address(self):
        a = addr.make_p2pkh_address(b'\x00' * 65)
        self.assertEqual(a, helpers.ADDR[0]['p2pkh'])
        b = addr.make_p2pkh_address(b'\x11' * 65)
        self.assertEqual(b, helpers.ADDR[1]['p2pkh'])

    def test_make_p2wpkh_address(self):
        a = addr.make_p2wpkh_address(helpers.P2WPKH_ADDR['pubkey'])
        self.assertEqual(a, helpers.P2WPKH_ADDR['address'])

    def test_parse(self):
        self.assertEqual(addr.parse(helpers.OP_IF['p2sh']),
                         b'\x05' + helpers.OP_IF['script_hash'])
        self.assertEqual(addr.parse(helpers.MSIG_2_2['p2sh']),
                         b'\x05' + helpers.MSIG_2_2['script_hash'])
        self.assertEqual(addr.parse(
            helpers.P2WSH['human']['ins'][0]['addr']),
            b'\x00\x20' + helpers.P2WSH['ser']['ins'][0]['pk_script'][2:])
        self.assertEqual(addr.parse(helpers.P2WPKH_ADDR['address']),
                         b'\x00\x14' + helpers.P2WPKH_ADDR['pkh'])
        self.assertEqual(addr.parse(helpers.ADDR[0]['p2pkh']),
                         b'\x00' + helpers.PK['ser'][0]['pkh'])

        with self.assertRaises(ValueError) as context:
            addr.parse('This is not a valid address.')

        self.assertIn('Unsupported address format. Got: ',
                      str(context.exception))

    def test_parse_hash(self):
        self.assertEqual(addr.parse_hash(helpers.OP_IF['p2sh']),
                         helpers.OP_IF['script_hash'])
        self.assertEqual(addr.parse_hash(helpers.MSIG_2_2['p2sh']),
                         helpers.MSIG_2_2['script_hash'])
        self.assertEqual(
            addr.parse_hash(
                helpers.P2WSH['human']['ins'][0]['addr']),
            helpers.P2WSH['ser']['ins'][0]['pk_script'][2:])
        self.assertEqual(addr.parse_hash(helpers.P2WPKH_ADDR['address']),
                         helpers.P2WPKH_ADDR['pkh'])
        self.assertEqual(addr.parse_hash(helpers.ADDR[0]['p2pkh']),
                         helpers.PK['ser'][0]['pkh'])

        with self.assertRaises(ValueError) as context:
            addr.parse('bc1blahblahblah')

        self.assertIn('Unsupported address format. Got: ',
                      str(context.exception))

        # Test cash addr code
        riemann.select_network('bitcoin_cash_main')
        self.assertEqual(
            addr.parse_hash(helpers.OP_IF['p2sh']),
            helpers.OP_IF['script_hash'])

        self.assertEqual(
            addr.parse_hash(helpers.OP_IF['cashaddr']),
            helpers.OP_IF['script_hash'])

        self.assertEqual(
            addr.parse_hash(helpers.CASHADDR['p2pkh']),
            utils.hash160(helpers.CASHADDR['pubkey']))

    def test_cashaddrs(self):
        riemann.select_network('bitcoin_cash_main')

        self.assertEqual(
            addr.make_legacy_p2sh_address('OP_IF'),
            helpers.OP_IF['p2sh'])

        self.assertEqual(
            addr.make_sh_address('OP_IF'),
            helpers.OP_IF['cashaddr'])

        self.assertEqual(
            addr.make_legacy_p2pkh_address(helpers.CASHADDR['pubkey']),
            helpers.CASHADDR['legacy_p2pkh'])

        self.assertEqual(
            addr.make_pkh_address(helpers.CASHADDR['pubkey']),
            helpers.CASHADDR['p2pkh'])

    def test_from_output_script(self):

        self.assertEqual(
            addr.from_output_script(helpers.OP_IF['output_script']),
            helpers.OP_IF['p2sh'])
        self.assertEqual(
            addr.from_output_script(
                helpers.P2WSH['ser']['ins'][0]['pk_script']),
            helpers.P2WSH['human']['ins'][0]['addr'])
        self.assertEqual(
            addr.from_output_script(helpers.PK['ser'][0]['pkh_output']),
            helpers.ADDR[0]['p2pkh'])
        self.assertEqual(
            addr.from_output_script(helpers.P2WPKH_ADDR['output']),
            helpers.P2WPKH_ADDR['address'])

        with self.assertRaises(ValueError) as context:
            addr.from_output_script(b'\x8e' * 34)
        self.assertIn(
            'Cannot parse address from script.',
            str(context.exception))

    def test_cashaddr_from_output_script(self):
        riemann.select_network('bitcoin_cash_main')
        self.assertEqual(
            addr.from_output_script(helpers.PK['ser'][0]['pkh_output']),
            helpers.ADDR[0]['p2pkh_cashaddr'])
        self.assertEqual(
            addr.from_output_script(helpers.OP_IF['output_script']),
            helpers.OP_IF['cashaddr'])

    def test_to_output_script(self):
        self.assertEqual(
            addr.to_output_script(helpers.OP_IF['p2sh']),
            helpers.OP_IF['output_script'])
        self.assertEqual(
            addr.to_output_script(helpers.P2WSH['human']['ins'][0]['addr']),
            helpers.P2WSH['ser']['ins'][0]['pk_script'])
        self.assertEqual(
            addr.to_output_script(helpers.ADDR[0]['p2pkh']),
            helpers.PK['ser'][0]['pkh_output'])
        self.assertEqual(
            addr.to_output_script(helpers.P2WPKH_ADDR['address']),
            helpers.P2WPKH_ADDR['output'])

        with self.assertRaises(ValueError) as context:
            # Junk B58 w valid checksum
            addr.to_output_script('1111111111111111111111111111111111177fdsQ')

        self.assertIn(
            'Cannot parse output script from address.',
            str(context.exception))

    def test_cashaddr_to_output_script(self):
        riemann.select_network('bitcoin_cash_main')

        self.assertEqual(
            addr.to_output_script(helpers.OP_IF['cashaddr']),
            helpers.OP_IF['output_script'])

        self.assertEqual(
            addr.to_output_script(helpers.ADDR[0]['p2pkh_cashaddr']),
            helpers.PK['ser'][0]['pkh_output'])
