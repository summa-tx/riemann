msig_two_two = 'OP_2 {} {} OP_2 OP_CHECKMULTISIG'  # Needs two pubkeys
p2pkh = 'OP_DUP OP_HASH160 {} OP_EQUALVERIFY OP_CHECKSIG'  # Needs one pubkey
p2sh = 'OP_HASH160 {} OP_EQUAL'  # Needs 20 byte scripthash
p2w = 'OP_0 {}'  # Needs length-prefixed witness script
htlc = 'OP_IF ' \
            'OP_SHA256 {} OP_EQUALVERIFY ' \
            'OP_DUP OP_HASH160 {} ' \
       'OP_ELSE ' \
            '{} OP_CHECKLOCKTIMEVERIFY OP_DROP ' \
            'OP_DUP OP_HASH160 {}' \
       'OP_ENDIF' \
       'OP_EQUALVERIFY' \
       'OP_CHECKSIG'
       # Needs a 32 byte hash, alice's pubkey, a timeout, and bob's pubkey
