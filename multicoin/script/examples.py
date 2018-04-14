# Needs two pubkeys
msig_two_two = 'OP_2 {} {} OP_2 OP_CHECKMULTISIG'

# Needs two SignatureHash
msig_two_two_script_sig = 'OP_0 {} {}'

# Needs one pubkey
p2pkh_script_pubkey = 'OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG'

# Needs signature
p2pkh_script_sig = '{}'

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

# Needs (signature, pubkey, secret)
# IN THAT ORDER!
htlc_script_sig_execute = '{} {} {} OP_TRUE'

# Needs (signature, pubkey, serialized_redeem_script)
# IN THAT ORDER!
htlc_script_sig_execute = '{} {} OP_FALSE'

# Don't forget to attach the script hash to the end of the p2sh script sigs
