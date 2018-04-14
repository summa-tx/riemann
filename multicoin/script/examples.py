# Needs two pubkeys
msig_two_two = 'OP_2 {} {} OP_2 OP_CHECKMULTISIG'

# Needs one pubkey
p2pkh_script_pubkey = 'OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG'

# Needs 20 byte scripthash
p2sh_script_pubkey = 'OP_HASH160 {} OP_EQUAL'

# Needs length-prefixed witness script
p2w = 'OP_0 {}'

# Needs a 32 byte hash, alice's pubkey, a timeout, and bob's pubkey
htlc = \
    'OP_IF ' \
        'OP_SHA256 {} OP_EQUALVERIFY ' \
        'OP_DUP OP_HASH160 {} ' \
    'OP_ELSE ' \
        '{} OP_CHECKLOCKTIMEVERIFY OP_DROP ' \
        'OP_DUP OP_HASH160 {} ' \
    'OP_ENDIF ' \
    'OP_EQUALVERIFY ' \
    'OP_CHECKSIG'
