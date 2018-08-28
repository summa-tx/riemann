# # Generates sighash values from available information on a raw transaction,
# using python-bitcoinlib by Peter Todd and Merry Friends
# https://github.com/petertodd/python-bitcoinlib/blob/master/LICENSE
# Complies with BIP143.
# Full title was "sighashgeneratorviapython-bitcoinlib.py", abbreviated to SPQR
# pip install python-bitcoinlib

import binascii
from io import BytesIO
from riemann.tests import helpers
from bitcoin.core import CMutableTransaction
from bitcoin.core.script import SIGHASH_ANYONECANPAY, CScript
from bitcoin.core.script import SignatureHash, SIGHASH_ALL, SIGHASH_SINGLE


def parse_tx(hex_tx):
    # NB: The deserialize function reads from a stream.
    raw_tx = BytesIO(binascii.unhexlify(hex_tx))
    tx = CMutableTransaction.stream_deserialize(raw_tx)
    return tx


prevout_pk_script = \
    CScript(helpers.P2WPKH['ser']['ins'][0]['pk_script'])  # bytes
tx_hex = helpers.P2WPKH['ser']['tx']['unsigned'].hex()  # raw hex
index = helpers.P2WPKH['human']['ins'][0]['index']  # integer
a = parse_tx(tx_hex)

int_value = helpers.P2WPKH['human']['ins'][0]['value']  # integer of tx value

print('Sighash All:')
print(SignatureHash(prevout_pk_script, a, index,
                    SIGHASH_ALL, sigversion=1, amount=(int_value)).hex())
print('Sighash All, Anyone Can Pay:')
print(SignatureHash(prevout_pk_script, a, index,
                    SIGHASH_ALL | SIGHASH_ANYONECANPAY,
                    sigversion=1, amount=(int_value)).hex())
print('Sighash Single:')
print(SignatureHash(prevout_pk_script, a, index,
                    SIGHASH_SINGLE, sigversion=1, amount=(int_value)).hex())
print('Sighash Single, Anyone Can Pay:')
print(SignatureHash(prevout_pk_script, a, index,
                    SIGHASH_SINGLE | SIGHASH_ANYONECANPAY,
                    sigversion=1, amount=(int_value)).hex())
