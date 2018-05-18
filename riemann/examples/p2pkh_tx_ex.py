# flake8: noqa
import riemann
from riemann import simple
from riemann.encoding import addresses
from riemann.tx import tx_builder as tb

'''Creates an example pay to public key hash transaction.'''


# Generate private key, public key, and address.

# Generate private key (not shown) and use to generate public key
# Consider using python-bitcoinlib to generate public_key
# https://github.com/petertodd/python-bitcoinlib

#       private_key_bytes = bytes.fromhex('YOUR PRIVATE KEY GOES HERE')
#       private_key = bitcoin.wallet.CKey(private_key_bytes)
#       public_key = bitcoin.wallet.CKey(private_key_bytes)

# Public key
public_key = '02bfb0a1108262227c8415aa90edc6c1a10e1e447ae58587c537926ef7069a38ca'

# Generate address from public key
address = addresses.make_pkh_address(bytes.fromhex(public_key))


# Generate Unsigned TxIn
# https://blockchain.info/tx/264b157c1c733bb42c42f2932702921ea23ac93259ca058cdf36311e36295188

# Previous transaction hash
tx_id = '264b157c1c733bb42c42f2932702921ea23ac93259ca058cdf36311e36295188'

# UTXO index to use
tx_index = 0

# Generate outpoint
tx_outpoint = simple.outpoint(tx_id, tx_index)

# Generate TxIn
tx_in = simple.unsigned_input(tx_outpoint, sequence=0xFFFFFFFE)


# Generate TxOut

# Address to receive bitcoin
receiving_address = 'bc1qss5rslea60lftfe7pyk32s9j9dtr7z7mrqud3g'

# Bitcoin (satoshis) to send
input_value = 100000

# Allocate Bitcoin (satoshis) for miner
tx_fee = 3100
tx_out = simple.output(input_value - tx_fee, receiving_address)

# Completely optional memo
tx_return_output = tb.make_op_return_output('made with ❤ by riemann'.encode('utf-8'))


# Generate Unsigned Tx 

# Create unsigned transaction
tx = simple.unsigned_tx([tx_in], [tx_out, tx_return_output])


# Generate Signed Tx
# https://blockchain.info/tx/1e7acd3d4715054c8fb0fdea25c5c704986006d2c6f30b0782e9b36a7ee072ef

# With the p2pkh output script from address, create the the sighash to be signed
sighash = tx.sighash_all(index=0, script=addresses.to_output_script(address))

# Declare SIGHASH_ALL type
SIGHASH_ALL = 0x01

# Sign the tx with private key
# Assumes private_key is of type class bitcoin.wallet.CKey from python-bitcoinlib
sig = private_key.sign(sighash) + bytes([SIGHASH_ALL])

# Recreate tx input with script signature
tx_signed_input = simple.p2pkh_input(
        outpoint=tx_outpoint,
        sig=sig.hex(),
        pubkey=public_key,
        sequence=0xFFFFFFFE)

# Recreate tx with the signed tx input
tx_signed = tx.copy(tx_ins=[tx_signed_input])
tx_signed_hex = tx_signed.hex()
print(tx_signed_hex)

# Transaction hash
tx_hash = tx_signed.tx_id.hex()

# Resources to decode transaction (tx_signed_hex)
#       https://blockchain.info/decode-tx
#       https://live.blockcypher.com/btc/decodetx/

# Resources to broadcast transaction (tx_signed_hex)
#       https://blockchain.info/pushtx
#       https://live.blockcypher.com/btc/pushtx/
