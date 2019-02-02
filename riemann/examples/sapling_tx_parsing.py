import riemann
from riemann import tx

from riemann import utils

riemann.select_network('zcash_sapling_main')

tx_hex = 'YOUR_TX_HEX_HERE'

# Parse the transaction blob into an object
sapling_tx = tx.SaplingTx.from_hex(tx_hex)

# Interact with it easily
print(utils.le2i(sapling_tx.expiry_height))
print(sapling_tx.tx_shielded_outputs[0].enc_ciphertext.hex())
print(sapling_tx.tx_joinsplits[0].zkproof.pi_sub_c.hex())

# Change some part of it
new_tx = sapling_tx.copy(expiry_height=77)

print(new_tx.hex())

# Calculate the sighash
new_tx.sighash_all(
    joinsplit=False,  # True if you're signing a joinsplit
    script_code=b'\x19\x76\x00\x88\xac',  # the script code to sign
    anyone_can_pay=False,  # Anyone can pay can't be used with JSs
    prevout_value=b'\x00' * 8)  # little-endian 8 byte value in zatoshi
