# flake8: noqa

from riemann import simple

# Spend a P2PKH output:
tx_ins = [simple.unsigned_input(outpoint)]

# Spend a P2SH output
tx_ins += [simple.unsigned_input(
    outpoint=outpoint,
    redeem_script=redeem_script)]

# Make an output
tx_outs = [simple.output(value, address)]

# Build the transaction
tx = simple.unsigned_tx(tx_ins, tx_outs)

sighash_0 = tx.sighash_single(0, p2pkh_pk_script)
sighash_1 tx.sighash_all(1, redeem_script, anyone_can_pay=True)
