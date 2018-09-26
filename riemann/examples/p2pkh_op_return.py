from riemann import simple
from riemann.tx import tx_builder
from riemann.encoding import addresses as addr

# For signing these example transactions, python-bitcoinlib is used:

# from bitcoin.wallet import CKey
# receiver = CKey(bytes.fromhex(receiver_privkey))
# receiver_pubkey = receiver.pub.hex()
# sender = CKey(bytes.fromhex(sender_privkey))
# sender_pubkey = sender.pub.hex()


version = 1
sequence = 0xFFFFFFFE
locktime = 0x00000000


# Sender (made up private key that controls absolutely nothing)
sender_privkey_hex = '372f913c52d7a6dfdfda9261e666a70e60f694f47c83fae388035fabbb168d63'     # noqa: E501
sender_pubkey = '02a004b949e4769ed341064829137b18992be884da5932c755e48f9465c1069dc2'        # noqa: E501
sender_addr = addr.make_p2wpkh_address(bytes.fromhex(sender_pubkey))

# Receiver (made up private key that controls absolutely nothing)
receiver_privkey_hex = '9a597c337b95fb037e3e1e4b719b1fd8d3914e69c22464bee63954eda03b56c3'   # noqa: E501
receiver_pubkey = '02ef21caa25eca974d3bdd73c034d6943cbf145a700d493adaa6f496bd87c5b33b'      # noqa: E501
receiver_addr = addr.make_p2wpkh_address(bytes.fromhex(receiver_pubkey))

# Sender Input
tx_id = 'ff7ff97060bfa1763dd9d4101b322157e841a4de865ddc28b1f71500f45c8135'
index = 0
sender_outpoint = simple.outpoint(tx_id, index)
sender_value = 1000
fee = 10
sender_input = simple.unsigned_input(sender_outpoint, sequence=sequence)

# Sender Output
sender_output = simple.output(value=sender_value - fee, address=receiver_addr)

# OP_RETURN output
riemann_note = 'made with ❤ by riemann'.encode('utf-8')
op_return_output = tx_builder.make_op_return_output(riemann_note)

unsigned_tx = simple.unsigned_legacy_tx(
    tx_ins=[sender_input],
    tx_outs=[sender_output, op_return_output],
    version=version,
    lock_time=locktime)

sighash_all = 0x01
sighash = unsigned_tx.sighash_all(
    index=0,
    script=addr.to_output_script(sender_addr))

# Using instance of CKey from python-bitcoinlib to sign:
# sig = sender.sign(sighash) + bytes([sighash_all])
# sig = sig.hex()
sig = '30450221009e8c7f85d6491169df139f25d26633efe48e98738331a37a1694d655dccebdbd02201a6444cfb364e91279f8c9a8b09cdbdeb4bf6cc0f00f53b9356f852c3b3151dc01'    # noqa: E501

signed_input = simple.p2pkh_input(
    outpoint=sender_outpoint,
    sig=sig,
    pubkey=sender_pubkey,
    sequence=sequence)

tx_signed = unsigned_tx.copy(tx_ins=[signed_input])
print('tx_signed')
print(tx_signed.hex())
print()
print(tx_signed.tx_id.hex())
print()
print(tx_signed.tx_id_le.hex())
print()
