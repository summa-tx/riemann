# flake8: noqa

# Needs two pubkeys
msig_two_two = 'OP_2 {pk0} {pk1} OP_2 OP_CHECKMULTISIG'

# Needs two signatures and the redeem_script
msig_two_two_stack_script = 'OP_0 {sig0} {sig1}'

# Needs signature and pubkey
p2pkh_script_sig = '{sig} {pk}'

# Needs one pubkey
p2pkh_script_pubkey = 'OP_DUP OP_HASH160 {pk} OP_EQUALVERIFY OP_CHECKSIG'

# Needs 20 byte scripthash
p2sh_script_pubkey = 'OP_HASH160 {sh} OP_EQUAL'


# Needs length-prefixed witness script
p2w = 'OP_0 {}'

# Needs a 32 byte hash, alice's pubkey, a timeout, and bob's pubkey
htlc_redeem_script = \
    'OP_IF ' \
        'OP_SHA256 {secret_hash} OP_EQUALVERIFY ' \
        'OP_DUP OP_HASH160 {pkh0} ' \
    'OP_ELSE ' \
        '{timeout} OP_CHECKLOCKTIMEVERIFY OP_DROP ' \
        'OP_DUP OP_HASH160 {pkh1} ' \
    'OP_ENDIF ' \
    'OP_EQUALVERIFY ' \
    'OP_CHECKSIG'

# Needs (signature, pubkey, secret)
# IN THAT ORDER!
htlc_stack_script_execute = '{sig} {pk} {secret} OP_TRUE'

# Needs (signature, pubkey, serialized_redeem_script)
# IN THAT ORDER!
htlc_stack_script_refund = '{sig} {pk} OP_FALSE'

# Don't forget to attach the script hash to the end of the p2sh script sigs
