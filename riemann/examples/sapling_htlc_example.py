import riemann
from riemann import simple, utils
from riemann.encoding import addresses as addr


riemann.select_network('zcash_sapling_main')

# Needs a 32 byte hash, alice's pubkey, a timeout, and bob's pubkey
htlc_redeem_script = (
    'OP_IF '
        'OP_SHA256 {secret_hash} OP_EQUALVERIFY '   # noqa: E131
        'OP_DUP OP_HASH160 {pkh0} '
    'OP_ELSE '
        '{timeout} OP_CHECKLOCKTIMEVERIFY OP_DROP '
        'OP_DUP OP_HASH160 {pkh1} '
    'OP_ENDIF '
    'OP_EQUALVERIFY '
    'OP_CHECKSIG')

# this spends via the HTLC secret revelation path
# Needs (signature, pubkey, secret, TRUE)
# IN THAT ORDER!
htlc_stack_script_execute = '{sig} {pk} {secret} OP_1'

# this spends via the timelocked refund path
# Needs (signature, pubkey, FALSE serialized_redeem_script)
# IN THAT ORDER!
htlc_stack_script_refund = '{sig} {pk} OP_0'

# Worst secret in the world :D
secret = '32' * 32
secret_hash = utils.sha256(bytes.fromhex(secret)).hex()

# Use real pubkeys!
fake_pk_execute = '02' * 32
fake_pk_refund = '03' * 32

# Use a real sig!
fake_sig = '04' * 32

# Use a real timelock!
timeout = 'deadbeef'

# string formatting to fill parameters
filled_in_redeem_script = htlc_redeem_script.format(
    secret_hash=secret_hash,
    pkh0=utils.hash160(bytes.fromhex(fake_pk_execute)).hex(),
    timeout=timeout,
    pkh1=utils.hash160(bytes.fromhex(fake_pk_refund)).hex())

# DON'T SEND MONEY TO THIS EXAMPLE ADDRESS!!!
# t 3fKPy737rsshnQJ7iRoXw3XujCB7tjuiUt
htlc_address = addr.make_sh_address(filled_in_redeem_script)

# how to send money there
output = simple.output(500000, htlc_address)

# --- HOW TO SPEND ---
# fill in the sig/pubkey/secret
filled_in_execute_script = htlc_stack_script_execute.format(
    sig=fake_sig,
    pk=fake_pk_execute,
    secret=secret)
filled_in_refund_script = htlc_stack_script_refund.format(
    sig=fake_sig,
    pk=fake_pk_refund)

# make inputs with the stack script and redeem script
fake_outpoint = simple.empty_outpoint()
execute_input = simple.p2sh_input(
    outpoint=fake_outpoint,
    stack_script=filled_in_execute_script,
    redeem_script=filled_in_redeem_script)
refund_input = simple.p2sh_input(
    outpoint=fake_outpoint,
    stack_script=filled_in_refund_script,
    redeem_script=filled_in_redeem_script)
