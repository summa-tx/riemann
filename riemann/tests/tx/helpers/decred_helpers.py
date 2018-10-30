# flake8: noqa

#  DCR helpers
#  UTXO: http://explorer.dcrdata.org/api/tx/decoded/49245425967b7e39c1eb27d261c7fe972675cccacff19ae9cc21f434ccddd986?indent=true
#  http://explorer.dcrdata.org/api/tx/decoded/fdd72f5841414a9c8b4a188a98a4d484df98f84e1c120e1ed59a66e51e8ae90c?indent=true

DCR = {
        'human': {
            'version': '01000000',
            'locktime': 0x59c2e2cd,
            'expiry': 0,
            'ins': [
                {
                    'id': 0,
                    'sequence': 0xFFFFFFFF,
                    'hash': 'fdd72f5841414a9c8b4a188a98a4d484df98f84e1c120e1ed59a66e51e8ae90c',
                    'index': 0,
                    'tree': 0,
                    'outpoint': '0ce98a1ee5669ad51e0e121c4ef898df84d4a4988a184a8b9c4a4141582fd7fd0000000000'
                    }
                ]
            },
        'ser': {
            'version': bytes.fromhex('01000000'),
            'locktime': bytes.fromhex('cde2c259'),
            'expiry': bytes.fromhex('00000000'),
            'ins': [
                {
                    'id': 0,
                    'sequence': bytes.fromhex('ffffffff'),
                    'hash': bytes.fromhex('0ce98a1ee5669ad51e0e121c4ef898df84d4a4988a184a8b9c4a4141582fd7fd'),
                    'index': bytes.fromhex('00000000'),
                    'tree': bytes.fromhex('00'),
                    'outpoint': bytes.fromhex('0ce98a1ee5669ad51e0e121c4ef898df84d4a4988a184a8b9c4a4141582fd7fd0000000000'),
                    }
                ],
            'outs': [
                {
                    'id': 0,
                    'version': bytes.fromhex('0000'),
                    'value': bytes.fromhex('a8ab570e00000000'),
                    'output': bytes.fromhex('a8ab570e0000000000001976a9145688f515dcf3453ca9b7a2a93aa441158a0b482c88ac'),
                    'script_len': bytes.fromhex('19'),
                    'pk_script': bytes.fromhex('76a9145688f515dcf3453ca9b7a2a93aa441158a0b482c88ac')
                    }
                ],
            'witnesses': [
                {
                    'value': bytes.fromhex('202e580e00000000'),
                    'height': bytes.fromhex('97970200'),
                    'index': bytes.fromhex('06000000'),
                    'witness': bytes.fromhex('202e580e000000009797020006000000e0483045022100d1c4e15834d1c405446d6ed6c05b5969483151b6b0401994a13e5bda5b73c36f022076bb7b6f00586ae8eb4b1590a4c670b13c66d04608a632b9d81da1f66470d7920121033f0306ce76970a7bd4506e0d243f571c7dd2d01d3747d9aa9081d89936cb7c1e20a9fc91d0a774083ba8016cac3254d35a99a815e632a7ee7d7d163b5f6723eed9514c5163a6147c0aef5c26e923e27336b945363f9939b97623598876a91410a35ba5323e7d6ac41d0400a7384d6d0767de3d6704cde2c259b17576a9147b5acb92ad78a9f983baa69c4434aa52499815826888ac'),
                    'hash': bytes.fromhex('ef6ea13e5e65874ef767eed3e3b93af63121b3c63207bdfff980b01d9878572e'),
                    'stack_script': bytes.fromhex('483045022100d1c4e15834d1c405446d6ed6c05b5969483151b6b0401994a13e5bda5b73c36f022076bb7b6f00586ae8eb4b1590a4c670b13c66d04608a632b9d81da1f66470d7920121033f0306ce76970a7bd4506e0d243f571c7dd2d01d3747d9aa9081d89936cb7c1e20a9fc91d0a774083ba8016cac3254d35a99a815e632a7ee7d7d163b5f6723eed951'),
                    'redeem_script': bytes.fromhex('4c5163a6147c0aef5c26e923e27336b945363f9939b97623598876a91410a35ba5323e7d6ac41d0400a7384d6d0767de3d6704cde2c259b17576a9147b5acb92ad78a9f983baa69c4434aa52499815826888ac'),
                    'script_sig_len': bytes.fromhex('e0'),
                    'script_sig': bytes.fromhex('483045022100d1c4e15834d1c405446d6ed6c05b5969483151b6b0401994a13e5bda5b73c36f022076bb7b6f00586ae8eb4b1590a4c670b13c66d04608a632b9d81da1f66470d7920121033f0306ce76970a7bd4506e0d243f571c7dd2d01d3747d9aa9081d89936cb7c1e20a9fc91d0a774083ba8016cac3254d35a99a815e632a7ee7d7d163b5f6723eed9514c5163a6147c0aef5c26e923e27336b945363f9939b97623598876a91410a35ba5323e7d6ac41d0400a7384d6d0767de3d6704cde2c259b17576a9147b5acb92ad78a9f983baa69c4434aa52499815826888ac'),
                    }
                ],
            'hash_pk': bytes([0x41, 0x04, 0xd6, 0x4b, 0xdf, 0xd0, 0x9e, 0xb1, 0xc5, 0xfe, 0x29, 0x5a, 0xbd, 0xeb, 0x1d, 0xca, 0x42, 0x81, 0xbe, 0x98, 0x8e, 0x2d, 0xa0, 0xb6, 0xc1, 0xc6, 0xa5, 0x9d, 0xc2, 0x26, 0xc2, 0x86, 0x24, 0xe1, 0x81, 0x75, 0xe8, 0x51, 0xc9, 0x6b, 0x97, 0x3d, 0x81, 0xb0, 0x1c, 0xc3, 0x1f, 0x04, 0x78, 0x34, 0xbc, 0x06, 0xd6, 0xd6, 0xed, 0xf6, 0x20, 0xd1, 0x84, 0x24, 0x1a, 0x6a, 0xed, 0x8b, 0x63, 0xa6, 0xac]),
            'tx': {
                'in_unsigned': bytes.fromhex('0ce98a1ee5669ad51e0e121c4ef898df84d4a4988a184a8b9c4a4141582fd7fd0000000000ffffffff'),
                'p2sh_2_p2pkh': bytes.fromhex('01000000010ce98a1ee5669ad51e0e121c4ef898df84d4a4988a184a8b9c4a4141582fd7fd0000000000ffffffff01a8ab570e0000000000001976a9145688f515dcf3453ca9b7a2a93aa441158a0b482c88accde2c2590000000001202e580e000000009797020006000000e0483045022100d1c4e15834d1c405446d6ed6c05b5969483151b6b0401994a13e5bda5b73c36f022076bb7b6f00586ae8eb4b1590a4c670b13c66d04608a632b9d81da1f66470d7920121033f0306ce76970a7bd4506e0d243f571c7dd2d01d3747d9aa9081d89936cb7c1e20a9fc91d0a774083ba8016cac3254d35a99a815e632a7ee7d7d163b5f6723eed9514c5163a6147c0aef5c26e923e27336b945363f9939b97623598876a91410a35ba5323e7d6ac41d0400a7384d6d0767de3d6704cde2c259b17576a9147b5acb92ad78a9f983baa69c4434aa52499815826888ac'),
                'expected_hash': bytes.fromhex('4538fc1618badd058ee88fd020984451024858796be0a1ed111877f887e1bd53'),
                'hash': bytes.fromhex('49245425967b7e39c1eb27d261c7fe972675cccacff19ae9cc21f434ccddd986'),
                'hash_le': bytes.fromhex('49245425967b7e39c1eb27d261c7fe972675cccacff19ae9cc21f434ccddd986')[::-1]
                }
            }
        }

# https://github.com/davecgh/btcd/blob/79fd35832fa39324c74b6022be092a5227f3fc0a/txscript/data/sighash.json
DCR1 = {
        'human': {
            'version': '01000000',
            'locktime': 0x00000000,
            'expiry': 0,
            'ins': [
                {
                    'id': 0,
                    'hash': '',
                    'index': 0,
                    'outpoint': ''
                    }
                ]
            },
        'ser': {
            'version': bytes.fromhex('01000000'),
            'locktime': bytes.fromhex('00000000'),
            'expiry': bytes.fromhex('00000000'),
            'ins': [
                {
                    'id': 0,
                    'hash': bytes.fromhex(''),
                    'index': bytes.fromhex(''),
                    'tree': bytes.fromhex(''),
                    'outpoint': bytes.fromhex(''),
                    'in': bytes.fromhex('04aacce7ca34e1f59e55d957f4d27aa6f54c5dd4046665840797ffe88b27320a0100000000ffffffff')
                    },
                {
                    'id': 1,
                    'hash': bytes.fromhex(''),
                    'index': bytes.fromhex(''),
                    'tree': bytes.fromhex(''),
                    'outpoint': bytes.fromhex(''),
                    'in': bytes.fromhex('0785b51df7d46512ebd63c4dd17f391360c9d6fc5c8846a0684184a601c30c790100000000ffffffff')
                    },
                {
                    'id': 2,
                    'hash': bytes.fromhex(''),
                    'index': bytes.fromhex(''),
                    'tree': bytes.fromhex(''),
                    'outpoint': bytes.fromhex(''),
                    'in': bytes.fromhex('0998d992230ab4b6ab112923bf8fd4db6bd977292ec52e722d27e389e229d1e10000000000ffffffff')
                    }
                ],
            'outs': [
                {
                    'id': 0,
                    'version': bytes.fromhex(''),
                    'value': bytes.fromhex(''),
                    'output': bytes.fromhex('e05d6a2f0000000000001976a9142fc06df75ec010d3ff25c3de77713fca4e731d4088ac'),
                    'script_len': bytes.fromhex(''),
                    'pk_script': bytes.fromhex('')
                    },
                {
                    'id': 1,
                    'version': bytes.fromhex(''),
                    'value': bytes.fromhex(''),
                    'output': bytes.fromhex('e09cede90500000000001976a914c2a65fb57cd570a53ff6cc721d854d5d7549f23f88ac'),
                    'script_len': bytes.fromhex(''),
                    'pk_script': bytes.fromhex('')
                    }
                ],
            'witness': [
                {
                    'id': 0,
                    'value': bytes.fromhex('00e40b5402000000'),
                    'height': bytes.fromhex('51010000'),
                    'index': bytes.fromhex('04000000'),
                    'witness': bytes.fromhex('00e40b540200000051010000040000006a47304402203162d5cea243874539bb6e35c9515342fcfa3fc7b8fa77ca9a17cef541c8957302204e00f31091c8f982eff563b805d1909679741c02c851919a709fce40dcd452ad012103ee327661befce7e68046a18aab5d2a566b0425069ad6b7b1951a737d40abd9cb'),
                    'stack_script': bytes.fromhex('47304402203162d5cea243874539bb6e35c9515342fcfa3fc7b8fa77ca9a17cef541c8957302204e00f31091c8f982eff563b805d1909679741c02c851919a709fce40dcd452ad012103ee327661befce7e68046a18aab5d2a566b0425069ad6b7b1951a737d40abd9cb'),
                    'script_sig': bytes.fromhex('6a47304402203162d5cea243874539bb6e35c9515342fcfa3fc7b8fa77ca9a17cef541c8957302204e00f31091c8f982eff563b805d1909679741c02c851919a709fce40dcd452ad012103ee327661befce7e68046a18aab5d2a566b0425069ad6b7b1951a737d40abd9cb')
                    },
                {
                    'id': 1,
                    'value': bytes.fromhex('0012c2e801000000'),
                    'height': bytes.fromhex('3f010000'),
                    'index': bytes.fromhex('01000000'),
                    'witness': bytes.fromhex('0012c2e8010000003f010000010000006a4730440220557f6069906bc945c9139f4d2d222abc30e521a20845513897d9ddcee3cb819002205edbda2708bb8df15c3a6f6b28144247544044e320448ff4ac766630bd6532aa012103d7502318c3205e4df6d0b2e9afa4c721526421914783fb33ce2aec9d40f0b449'),
                    'stack_script': bytes.fromhex('4730440220557f6069906bc945c9139f4d2d222abc30e521a20845513897d9ddcee3cb819002205edbda2708bb8df15c3a6f6b28144247544044e320448ff4ac766630bd6532aa012103d7502318c3205e4df6d0b2e9afa4c721526421914783fb33ce2aec9d40f0b449'),
                    'script_sig': bytes.fromhex('6a4730440220557f6069906bc945c9139f4d2d222abc30e521a20845513897d9ddcee3cb819002205edbda2708bb8df15c3a6f6b28144247544044e320448ff4ac766630bd6532aa012103d7502318c3205e4df6d0b2e9afa4c721526421914783fb33ce2aec9d40f0b449'),
                    },
                {
                    'id': 2,
                    'value': bytes.fromhex('0050d6dc01000000'),
                    'height': bytes.fromhex('0d010000'),
                    'index': bytes.fromhex('02000000'),
                    'witness': bytes.fromhex('0050d6dc010000000d010000020000006b48304502210099f5cb0ca36e68f7f815e17538706b374e24ec9e61795984f767f230ee08dea802204c908c38e647e5d551dba5054adfd0430dde19ca94d83b68a795678d5246a90d012103ee327661befce7e68046a18aab5d2a566b0425069ad6b7b1951a737d40abd9cb'),
                    'stack_script': bytes.fromhex('48304502210099f5cb0ca36e68f7f815e17538706b374e24ec9e61795984f767f230ee08dea802204c908c38e647e5d551dba5054adfd0430dde19ca94d83b68a795678d5246a90d012103ee327661befce7e68046a18aab5d2a566b0425069ad6b7b1951a737d40abd9cb'),
                    'script_sig': bytes.fromhex('6b48304502210099f5cb0ca36e68f7f815e17538706b374e24ec9e61795984f767f230ee08dea802204c908c38e647e5d551dba5054adfd0430dde19ca94d83b68a795678d5246a90d012103ee327661befce7e68046a18aab5d2a566b0425069ad6b7b1951a737d40abd9cb')
                    }
                ],
            'tx': {
                    'p2sh_2_p2pkh': bytes.fromhex('010000000304aacce7ca34e1f59e55d957f4d27aa6f54c5dd4046665840797ffe88b27320a0100000000ffffffff0785b51df7d46512ebd63c4dd17f391360c9d6fc5c8846a0684184a601c30c790100000000ffffffff0998d992230ab4b6ab112923bf8fd4db6bd977292ec52e722d27e389e229d1e10000000000ffffffff02e05d6a2f0000000000001976a9142fc06df75ec010d3ff25c3de77713fca4e731d4088ace09cede90500000000001976a914c2a65fb57cd570a53ff6cc721d854d5d7549f23f88ac00000000000000000300e40b540200000051010000040000006a47304402203162d5cea243874539bb6e35c9515342fcfa3fc7b8fa77ca9a17cef541c8957302204e00f31091c8f982eff563b805d1909679741c02c851919a709fce40dcd452ad012103ee327661befce7e68046a18aab5d2a566b0425069ad6b7b1951a737d40abd9cb0012c2e8010000003f010000010000006a4730440220557f6069906bc945c9139f4d2d222abc30e521a20845513897d9ddcee3cb819002205edbda2708bb8df15c3a6f6b28144247544044e320448ff4ac766630bd6532aa012103d7502318c3205e4df6d0b2e9afa4c721526421914783fb33ce2aec9d40f0b4490050d6dc010000000d010000020000006b48304502210099f5cb0ca36e68f7f815e17538706b374e24ec9e61795984f767f230ee08dea802204c908c38e647e5d551dba5054adfd0430dde19ca94d83b68a795678d5246a90d012103ee327661befce7e68046a18aab5d2a566b0425069ad6b7b1951a737d40abd9cb')
                    }
            }
        }

# Not used:
SIGHASH_DCR = {
        'prevout_pk': bytes.fromhex('76a91478807bd86b22a9f23bb4e026705c3e52824d7f3e88ac'),
        'all': bytes.fromhex('569f23573cd279d9fea347ed16d86984b271b0b4b4270cc7122201683fcd7708'),
        'all_anyonecanpay': bytes.fromhex('c75779c947b3c0e8828db370c8d5597c6dd91a48e287d1bfca705637943d200e'),
        'single': bytes.fromhex('a1f4f2ced71352153ffee5dd570da5d609ecd5ce04e1db808c238554d758fb13'),
        'single_anyonecanpay': bytes.fromhex('1b83a4d2a1a70204587491f7f6e110704e98e1b8da04219efba5dde14eaccf1f')
}
