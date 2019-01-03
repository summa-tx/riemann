import riemann
from riemann import simple, utils
from riemann.encoding import addresses as addr
from riemann.script import serialization as ser

riemann.select_network('zcash_sapling_main')

prevout_addr_1 = 't1S3kN4zusjHtDEwfdaCMgk132bqo9DaYW4'
prevout_addr_2 = 't1VQCUYzApF5eWf4UFAGdWwaFEpBfG2su1A'

# This is the script code of the prevout being spent
# We length prefix it
# Needed for sighash later
script_code_1 = b'\x19' + addr.to_output_script(prevout_addr_1)
script_code_2 = b'\x19' + addr.to_output_script(prevout_addr_2)

# Make inputs for our tx
# We're spending the 1st output of a45216...
#            And the 0th output of ae9ee9...
tx_in_1 = simple.unsigned_input(simple.outpoint('a45216a60855f053d63eb78a91429f85c6218541e876be95b17f8743635a0d3e', 1))  # noqa: E501
tx_in_2 = simple.unsigned_input(simple.outpoint('ae9ee9ddeae0f0de07837f25b638ac8a723104753008d9c672e57b1d58e1c863', 0))  # noqa: E501

# Make an output for our tx.
# Our prevouts are worth 0.01845001 and 0.00002 ZEC
# We want to pay 0.0001 ZEC
tx_out = simple.output(1845001 + 2000 - 10000, 't1fRswMu1vopHpWVisgxTtkJSVs8ZCrDZtz')  # noqa: E501

# Make the transaction
unsigned_tx = simple.unsigned_legacy_tx([tx_in_1, tx_in_2], [tx_out])

# Calculate the sighashes
sighash_1 = unsigned_tx.sighash_all(
    index=0,
    script_code=script_code_1,
    prevout_value=utils.i2le_padded(1845001, 8))
sighash_2 = unsigned_tx.sighash_all(
    index=1,
    script_code=script_code_2,
    prevout_value=utils.i2le_padded(2000, 8))

# Sign the transaction with your private keys elsewhere
pubkey_1 = ''
pubkey_2 = ''

sig_1 = ''
sig_2 = ''

# Build the stack scripts
# For P2PKH this is the signature, then the pubkey
stack_script_1 = '{} {}'.format(sig_1, pubkey_1)
stack_script_2 = '{} {}'.format(sig_2, pubkey_2)

# Add serialized stack scripts to the inputs
signed_tx_in_1 = tx_in_1.copy(stack_script=ser.serialize(stack_script_1))
signed_tx_in_2 = tx_in_2.copy(stack_script=ser.serialize(stack_script_2))

# Add the signed inputs
signed_tx = unsigned_tx.copy(tx_ins=[signed_tx_in_1, signed_tx_in_2])

# Print the hex-serialized transaction, ready for broadcast
print(signed_tx.hex())
