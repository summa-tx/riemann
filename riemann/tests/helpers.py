# flake8: noqa

# From Dev++ slides
# https://docs.google.com/presentation/d/1YGZf1VKKOnCdpuaVzU35CAXy8uGcztq0OBlTNMGSmkw/edit?usp=sharing
from ..script import examples

version = bytes.fromhex('01000000')
num_inputs = bytes.fromhex('01')
outpoint_tx_id = bytes.fromhex('813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1')
outpoint_index = bytes.fromhex('00000000')
script_sig_len = bytes.fromhex('6b')
stack_script = bytes.fromhex('483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')
redeem_script = bytes.fromhex('')
sequence = bytes.fromhex('feffffff')
num_outputs = bytes.fromhex('02')
output_value_0 = bytes.fromhex('a135ef0100000000')
output_script_0 = bytes.fromhex('76a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac')
output_value_1 = bytes.fromhex('99c3980000000000')
output_script_1 = bytes.fromhex('76a9141c4bc762dd5423e332166702cb75f40df79fea1288ac')
lock_time = bytes.fromhex('19430600')

prevout_pk_script = bytes.fromhex('a91424d6008f143af0cca57344069c46661aa4fcea2387')
prevout_value = bytes.fromhex('3af9870200000000')

# Notes
# Unsure if python-bitcoinlib supports witness txns yet.
# To make more sighash tests:
#
# 1. install python-bitcoinlib
# 2. As follows:
#
# ```Python
# import binascii
# from io import BytesIO
# from bitcoin.core import CMutableTransaction
# from bitcoin.core.script import SIGHASH_ANYONECANPAY, CScript
# from bitcoin.core.script import SignatureHash, SIGHASH_ALL, SIGHASH_SINGLE
#
# def parse_tx(hex_tx):
#      # NB: The deserialize function reads from a stream.
#      raw_tx = BytesIO(binascii.unhexlify(hex_tx))
#      tx = CMutableTransaction.stream_deserialize(raw_tx)
#      return tx
#
# prevout_pk_script = CScript(bytes.fromhex(HEX_ENCODED_PK_SCRIPT))
# tx_hex = 'SOME HEX ENCODED TX'
# index = THE_INDEX_OF_THE_INPUT
# a = parse_tx(HEX_ENCODED_TX)
#
# print(SignatureHash(prevout_pk_script, a, index, SIGHASH_ALL))
# print(SignatureHash(prevout_pk_script, a, index,
#                     SIGHASH_ALL | SIGHASH_ANYONECANPAY))
# print(SignatureHash(prevout_pk_script, a, index, SIGHASH_SINGLE))
# print(SignatureHash(prevout_pk_script, a, index,
#                     SIGHASH_SINGLE | SIGHASH_ANYONECANPAY))
sighash_all = bytes.fromhex('b85c4f8d1377cc138225dd9b319d0a4ca547f7884270640f44c5fcdf269e0fe8')
sighash_all_anyonecanpay = bytes.fromhex('3b67a5114cc9fc837ddd6f6ec11bde38db5f68c34ab6ece2a043d7b25f2cf8bb')
sighash_single = bytes.fromhex('1dab67d768be0380fc800098005d1f61744ffe585b0852f8d7adc12121a86938')
sighash_single_anyonecanpay = bytes.fromhex('d4687b93c0a9090dc0a3384cd3a594ce613834bb37abc56f6032e96c597547e3')

script_sig = bytes.fromhex('483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')
outpoint = bytes.fromhex('813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d100000000')
tx_in = '813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff'
tx_out_0 = 'a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac'
tx_out_1 = '99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac'

tx_id = bytes.fromhex('452c629d67e41baec3ac6f04fe744b4b9617f8f859c63b3002f8684e7a4fee03')
tx_id_le = tx_id[::-1]
P2PKH_SPEND = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')


# Forkid tests generated with pycoin
# To Produce More:
# Install pycoin
# from pycoin.coins.bcash.Tx import Tx
# a = Tx.from_bin(P2PKH_SPEND)
# class p():
#    pass
# c = p()
# c.coin_value = int.from_bytes(prevout_value, 'little')
# a.set_unspents([c])
# hex(a.SolutionChecker(a)._signature_hash(prevout_pk_script, 0, SIGHASH TYPE AS INT))

sighash_forkid_all = bytes.fromhex('450a16c7b1d6f913acb2460665a6fdc7dc7d351af5a3358c537278ffa4d125ea')
sighash_forkid_single = bytes.fromhex('1a8ad1cebbd419fe5a53092fa6c272d8456829e871bf46be93906e859e42890e')
sighash_forkid_all_anyone_can_pay = bytes.fromhex('f1a7a88eb953c86381f50ed223b8dd06e45b86437747ad83886f0529da9f3323')
sighash_forkid_single_anyone_can_pay = bytes.fromhex('4ad1e69f172960c7ce26b993a0696fb618cf41104898b93b9fd66be465d1d38d')

# From blockchain.info
# https://blockchain.info/rawtx/0739d0c7b7b7ff5f991e8e3f72a6f5eb56563880df982c4ab813cd71bc7a6a03?format=hex

RAW_P2SH_TO_P2PKH = bytes.fromhex( '010000000101d15c2cc4621b2a319ba53714e2709f8ba2dbaf23f8c35a4bddcb203f9b391000000000df473044022000e02ea97289a35181a9bfabd324f12439410db11c4e94978cdade6a665bf1840220458b87c34d8bb5e4d70d01041c7c2d714ea8bfaca2c2d2b1f9e5749c3ee17e3d012102ed0851f0b4c4458f80e0310e57d20e12a84642b8e097fe82be229edbd7dbd53920f6665740b1f950eb58d646b1fae9be28cef842da5e51dc78459ad2b092e7fd6e514c5163a914bb408296de2420403aa79eb61426bb588a08691f8876a91431b31321831520e346b069feebe6e9cf3dd7239c670400925e5ab17576a9140d22433293fe9652ea00d21c5061697aef5ddb296888ac0000000001d0070000000000001976a914f2539f42058da784a9d54615ad074436cf3eb85188ac00000000')


OP_IF_P2SH = '3MpTk145zbm5odhRALfT9BnUs8DB5w4ydw'
OP_IF_SCRIPT_HASH = bytes.fromhex('dccafab9536343713ef4b9a1d443a1b6ca8c8dd1')
OP_IF_OUTPUT_SCRIPT = b'\xa9' + OP_IF_SCRIPT_HASH + b'\x87'

# Use '00' * 65 and '11' * 65 as pubkeys
PK_0 = '00' * 65
PK_1 = '11' * 65
PKH_0 = bytes.fromhex('1b60c31dba9403c74d81af255f0c300bfed5faa3')
PKH_1 = bytes.fromhex('e723a0f62396b8b03dbd9e48e9b9efe2eb704aab')
P2PKH_0 = '13VmALKHkCdSN1JULkP6RqW3LcbpWvgryV'
P2PKH_1 = '1N59mqr5yg38K11PTY2HdZTN7KmAHeCyHE'

MSIG_TWO_TWO_SCRIPT = examples.msig_two_two.format(PK_0, PK_1)
MSIG_TWO_TWO_SERIALIZED_SCRIPT = bytes.fromhex('5241000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000041111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111152ae')
MSIG_TWO_TWO_P2SH = '3R23EEkAzy7HPWKN8rcL4ZzSjEWNsipxWV'
MSIG_TWO_TWO_SCRIPT_HASH = bytes.fromhex('ffe3e2be6ba8d465041d3da1cdfe472b901b215a')
MSIG_TWO_TWO_OUTPUT_SCRIPT = b'\xa9' + MSIG_TWO_TWO_SCRIPT_HASH + b'\x87'


# https://blockchain.info/rawtx/264814c57c76694c752bcb800d7edaf210ef3a2c199c4db44485a15eb3429691
P2WSH_SPEND = bytes.fromhex('010000000001011fceaec1c93a98af3e035b3ba0ef01c32be39a79dede5d03c2347097fac6283e0100000000ffffffff0440548900000000001976a9146199463742d1359a505881821d82f5d4148e3fc588ac60361e000000000017a9140df9a2a3c14a223733908e3e9127e2f6a9e2878e87502b7000000000001976a914f447146b86373c781a946d7ebd88cbbb79ec810288ac0370040000000000220020701a8d401c84fb13e6baf169d59684e17abd9fa216c8cc5b9fc63d622ff8c58d040047304402201b1c2fc7d58870004c379575a47db60c3833174033f891ad5030cbf0c37c50c302206087d3ddc6f38da40e7eaf8c2af3f934a577de10e6ca75e00b4cdfbb34f5d40601483045022100a7ecde342ccacd1159e385bcd41c947723a7ae3fcea66c76b5b09d02fee310f7022058ca21324fcd0c90e69630f13975d993e11f62ec8d7aa1a9a49036b9607e58fe016952210375e00eb72e29da82b89367947f29ef34afb75e8654f6ea368e0acdfd92976b7c2103a1b26313f430c4b15bb1fdce663207659d8cac749a0e53d70eff01874496feff2103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f88053ae00000000')
P2WSH_SCRIPT = 'OP_2 0375e00eb72e29da82b89367947f29ef34afb75e8654f6ea368e0acdfd92976b7c 03a1b26313f430c4b15bb1fdce663207659d8cac749a0e53d70eff01874496feff 03c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f880 OP_3 OP_CHECKMULTISIG'
P2WSH_SERIALIZED_SCRIPT = bytes.fromhex('52210375e00eb72e29da82b89367947f29ef34afb75e8654f6ea368e0acdfd92976b7c2103a1b26313f430c4b15bb1fdce663207659d8cac749a0e53d70eff01874496feff2103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f88053ae')
P2WSH_SCRIPT_HASH = bytes.fromhex('701a8d401c84fb13e6baf169d59684e17abd9fa216c8cc5b9fc63d622ff8c58d')
P2WSH_ADDRESS = 'bc1qwqdg6squsna38e46795at95yu9atm8azzmyvckulcc7kytlcckxswvvzej'
P2WSH_WITNESS = bytes.fromhex('040047304402201b1c2fc7d58870004c379575a47db60c3833174033f891ad5030cbf0c37c50c302206087d3ddc6f38da40e7eaf8c2af3f934a577de10e6ca75e00b4cdfbb34f5d40601483045022100a7ecde342ccacd1159e385bcd41c947723a7ae3fcea66c76b5b09d02fee310f7022058ca21324fcd0c90e69630f13975d993e11f62ec8d7aa1a9a49036b9607e58fe016952210375e00eb72e29da82b89367947f29ef34afb75e8654f6ea368e0acdfd92976b7c2103a1b26313f430c4b15bb1fdce663207659d8cac749a0e53d70eff01874496feff2103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f88053ae')
P2WSH_WITNESS_STACK_ITEMS = [
    bytes.fromhex(''),
    bytes.fromhex('304402201b1c2fc7d58870004c379575a47db60c3833174033f891ad5030cbf0c37c50c302206087d3ddc6f38da40e7eaf8c2af3f934a577de10e6ca75e00b4cdfbb34f5d40601'),
    bytes.fromhex('3045022100a7ecde342ccacd1159e385bcd41c947723a7ae3fcea66c76b5b09d02fee310f7022058ca21324fcd0c90e69630f13975d993e11f62ec8d7aa1a9a49036b9607e58fe01'),
    bytes.fromhex('52210375e00eb72e29da82b89367947f29ef34afb75e8654f6ea368e0acdfd92976b7c2103a1b26313f430c4b15bb1fdce663207659d8cac749a0e53d70eff01874496feff2103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f88053ae')
]

# https://blockchain.info/rawtx/2b6d004f685cf6515faf5d5a508853a5d9cda2c589fcf49a5781cb38be06029b
P2WPKH_ADDRESS = 'bc1q8cqttds2dej9zht7vupd3467ndhur92fudlyql'
P2WPKH_PUBKEY = bytes.fromhex('03dc3dbabbf8c5e15d1eb3606a6a42c6d3a8c546f2a196a80a08b9a9021e2be33d')
P2WPKH_PKH = bytes.fromhex('3e00b5b60a6e64515d7e6702d8d75e9b6fc19549')




# DCR helpers
# http://explorer.dcrdata.org/api/tx/decoded/49245425967b7e39c1eb27d261c7fe972675cccacff19ae9cc21f434ccddd986?indent=true
DCR_RAW_P2SH_TO_P2PKH = bytes.fromhex('01000000010ce98a1ee5669ad51e0e121c4ef898df84d4a4988a184a8b9c4a4141582fd7fd0000000000ffffffff01a8ab570e0000000000001976a9145688f515dcf3453ca9b7a2a93aa441158a0b482c88accde2c2590000000001202e580e000000009797020006000000e0483045022100d1c4e15834d1c405446d6ed6c05b5969483151b6b0401994a13e5bda5b73c36f022076bb7b6f00586ae8eb4b1590a4c670b13c66d04608a632b9d81da1f66470d7920121033f0306ce76970a7bd4506e0d243f571c7dd2d01d3747d9aa9081d89936cb7c1e20a9fc91d0a774083ba8016cac3254d35a99a815e632a7ee7d7d163b5f6723eed9514c5163a6147c0aef5c26e923e27336b945363f9939b97623598876a91410a35ba5323e7d6ac41d0400a7384d6d0767de3d6704cde2c259b17576a9147b5acb92ad78a9f983baa69c4434aa52499815826888ac')

DCR_TX_ID = bytes.fromhex('49245425967b7e39c1eb27d261c7fe972675cccacff19ae9cc21f434ccddd986')
DCR_TX_ID_LE = bytes.fromhex('49245425967b7e39c1eb27d261c7fe972675cccacff19ae9cc21f434ccddd986')[::-1]
DCR_WITNESS_HASH = bytes.fromhex('ef6ea13e5e65874ef767eed3e3b93af63121b3c63207bdfff980b01d9878572e')

DCR_VERSION = bytes.fromhex('01000000')
DCR_NUM_INPUTS = bytes.fromhex('01')
DCR_INPUT = bytes.fromhex('0ce98a1ee5669ad51e0e121c4ef898df84d4a4988a184a8b9c4a4141582fd7fd0000000000ffffffff')
DCR_OUTPOINT = bytes.fromhex('0ce98a1ee5669ad51e0e121c4ef898df84d4a4988a184a8b9c4a4141582fd7fd0000000000')
DCR_OUTPOINT_TX_ID_LE = bytes.fromhex('0ce98a1ee5669ad51e0e121c4ef898df84d4a4988a184a8b9c4a4141582fd7fd')
DCR_OUTPOINT_INDEX = bytes.fromhex('00000000')
DCR_OUTPOINT_TREE = bytes.fromhex('00')
DCR_SEQUNCE = bytes.fromhex('ffffffff')
DCR_NUM_OUTPUTS = bytes.fromhex('01')
DCR_OUTPUT = bytes.fromhex('a8ab570e0000000000001976a9145688f515dcf3453ca9b7a2a93aa441158a0b482c88ac')
DCR_OUTPUT_VALUE = bytes.fromhex('a8ab570e00000000')
DCR_OUTPUT_VERSION = bytes.fromhex('0000')
DCR_OUTPUT_SCRIPT_LEN = bytes.fromhex('19')
DCR_OUTPUT_SCRIPT = bytes.fromhex('76a9145688f515dcf3453ca9b7a2a93aa441158a0b482c88ac')
DCR_LOCKTIME = bytes.fromhex('cde2c259')
DCR_EXPIRY = bytes.fromhex('00000000')
DCR_NUM_WITNESSES = bytes.fromhex('01')
DCR_WITNESS = bytes.fromhex('202e580e000000009797020006000000e0483045022100d1c4e15834d1c405446d6ed6c05b5969483151b6b0401994a13e5bda5b73c36f022076bb7b6f00586ae8eb4b1590a4c670b13c66d04608a632b9d81da1f66470d7920121033f0306ce76970a7bd4506e0d243f571c7dd2d01d3747d9aa9081d89936cb7c1e20a9fc91d0a774083ba8016cac3254d35a99a815e632a7ee7d7d163b5f6723eed9514c5163a6147c0aef5c26e923e27336b945363f9939b97623598876a91410a35ba5323e7d6ac41d0400a7384d6d0767de3d6704cde2c259b17576a9147b5acb92ad78a9f983baa69c4434aa52499815826888ac')
DCR_WITNESS_VALUE = bytes.fromhex('202e580e00000000')
DCR_WITNESS_HEIGHT = bytes.fromhex('97970200')
DCR_WITNESS_INDEX = bytes.fromhex('06000000')
DCR_SIG_SCRIPT_LEN = bytes.fromhex('e0')
DCR_SIG_SCRIPT = bytes.fromhex('483045022100d1c4e15834d1c405446d6ed6c05b5969483151b6b0401994a13e5bda5b73c36f022076bb7b6f00586ae8eb4b1590a4c670b13c66d04608a632b9d81da1f66470d7920121033f0306ce76970a7bd4506e0d243f571c7dd2d01d3747d9aa9081d89936cb7c1e20a9fc91d0a774083ba8016cac3254d35a99a815e632a7ee7d7d163b5f6723eed9514c5163a6147c0aef5c26e923e27336b945363f9939b97623598876a91410a35ba5323e7d6ac41d0400a7384d6d0767de3d6704cde2c259b17576a9147b5acb92ad78a9f983baa69c4434aa52499815826888ac')
DCR_STACK_SCRIPT = bytes.fromhex('483045022100d1c4e15834d1c405446d6ed6c05b5969483151b6b0401994a13e5bda5b73c36f022076bb7b6f00586ae8eb4b1590a4c670b13c66d04608a632b9d81da1f66470d7920121033f0306ce76970a7bd4506e0d243f571c7dd2d01d3747d9aa9081d89936cb7c1e20a9fc91d0a774083ba8016cac3254d35a99a815e632a7ee7d7d163b5f6723eed951')
DCR_REDEEM_SCRIPT = bytes.fromhex('4c5163a6147c0aef5c26e923e27336b945363f9939b97623598876a91410a35ba5323e7d6ac41d0400a7384d6d0767de3d6704cde2c259b17576a9147b5acb92ad78a9f983baa69c4434aa52499815826888ac')

# https://github.com/decred/dcrd/blob/1e42b8524db5e0cbcd5bf5f4893786b4986d17b6/txscript/script_test.go

DCR_EXPECTED_SIGHASH = bytes.fromhex('4ce2cd042d64e35b36fdbd16aff0d38a5abebff0e5e8f6b6b31fcd4ac6957905')

DCR_EXPECTED_TX_HASH = bytes.fromhex('4538fc1618badd058ee88fd020984451024858796be0a1ed111877f887e1bd53')
DCR_TX_HASH_PK_SCRIPT = bytes([0x41, 0x04, 0xd6, 0x4b, 0xdf, 0xd0, 0x9e, 0xb1, 0xc5, 0xfe, 0x29, 0x5a, 0xbd, 0xeb, 0x1d, 0xca, 0x42, 0x81, 0xbe, 0x98, 0x8e, 0x2d, 0xa0, 0xb6, 0xc1, 0xc6, 0xa5, 0x9d, 0xc2, 0x26, 0xc2, 0x86, 0x24, 0xe1, 0x81, 0x75, 0xe8, 0x51, 0xc9, 0x6b, 0x97, 0x3d, 0x81, 0xb0, 0x1c, 0xc3, 0x1f, 0x04, 0x78, 0x34, 0xbc, 0x06, 0xd6, 0xd6, 0xed, 0xf6, 0x20, 0xd1, 0x84, 0x24, 0x1a, 0x6a, 0xed, 0x8b, 0x63, 0xa6, 0xac])


# https://github.com/davecgh/btcd/blob/79fd35832fa39324c74b6022be092a5227f3fc0a/txscript/data/sighash.json
DCR_2 = bytes.fromhex( '010000000304aacce7ca34e1f59e55d957f4d27aa6f54c5dd4046665840797ffe88b27320a0100000000ffffffff0785b51df7d46512ebd63c4dd17f391360c9d6fc5c8846a0684184a601c30c790100000000ffffffff0998d992230ab4b6ab112923bf8fd4db6bd977292ec52e722d27e389e229d1e10000000000ffffffff02e05d6a2f0000000000001976a9142fc06df75ec010d3ff25c3de77713fca4e731d4088ace09cede90500000000001976a914c2a65fb57cd570a53ff6cc721d854d5d7549f23f88ac00000000000000000300e40b540200000051010000040000006a47304402203162d5cea243874539bb6e35c9515342fcfa3fc7b8fa77ca9a17cef541c8957302204e00f31091c8f982eff563b805d1909679741c02c851919a709fce40dcd452ad012103ee327661befce7e68046a18aab5d2a566b0425069ad6b7b1951a737d40abd9cb0012c2e8010000003f010000010000006a4730440220557f6069906bc945c9139f4d2d222abc30e521a20845513897d9ddcee3cb819002205edbda2708bb8df15c3a6f6b28144247544044e320448ff4ac766630bd6532aa012103d7502318c3205e4df6d0b2e9afa4c721526421914783fb33ce2aec9d40f0b4490050d6dc010000000d010000020000006b48304502210099f5cb0ca36e68f7f815e17538706b374e24ec9e61795984f767f230ee08dea802204c908c38e647e5d551dba5054adfd0430dde19ca94d83b68a795678d5246a90d012103ee327661befce7e68046a18aab5d2a566b0425069ad6b7b1951a737d40abd9cb')

DCR_2_VERSION = bytes.fromhex('01000000')
DCR_2_NUM_INPUTS = bytes.fromhex('03')
DCR_2_INPUT_0 = bytes.fromhex('04aacce7ca34e1f59e55d957f4d27aa6f54c5dd4046665840797ffe88b27320a0100000000ffffffff')
DCR_2_INPUT_1 = bytes.fromhex('0785b51df7d46512ebd63c4dd17f391360c9d6fc5c8846a0684184a601c30c790100000000ffffffff')
DCR_2_INPUT_2 = bytes.fromhex('0998d992230ab4b6ab112923bf8fd4db6bd977292ec52e722d27e389e229d1e10000000000ffffffff')
DCR_2_NUM_OUTPUTS = bytes.fromhex('02')
DCR_2_OUTPUT_0 = bytes.fromhex('e05d6a2f0000000000001976a9142fc06df75ec010d3ff25c3de77713fca4e731d4088ac')
DCR_2_OUTPUT_1 = bytes.fromhex('e09cede90500000000001976a914c2a65fb57cd570a53ff6cc721d854d5d7549f23f88ac')
DCR_2_LOCKTIME = bytes.fromhex('00000000')
DCR_2_EXPIRTY = bytes.fromhex('00000000')
DCR_2_NUM_WITNESSES = bytes.fromhex('03')
DCR_2_WITNESS_0 = bytes.fromhex('00e40b540200000051010000040000006a47304402203162d5cea243874539bb6e35c9515342fcfa3fc7b8fa77ca9a17cef541c8957302204e00f31091c8f982eff563b805d1909679741c02c851919a709fce40dcd452ad012103ee327661befce7e68046a18aab5d2a566b0425069ad6b7b1951a737d40abd9cb')
DCR_2_WITNESS_0_SCRIPT_SIG = bytes.fromhex('6a47304402203162d5cea243874539bb6e35c9515342fcfa3fc7b8fa77ca9a17cef541c8957302204e00f31091c8f982eff563b805d1909679741c02c851919a709fce40dcd452ad012103ee327661befce7e68046a18aab5d2a566b0425069ad6b7b1951a737d40abd9cb')
DCR_2_WITNESS_0_STACK_SCRIPT = DCR_2_WITNESS_0_SCRIPT_SIG[1:]
DCR_2_WITNESS_1 = bytes.fromhex('0012c2e8010000003f010000010000006a4730440220557f6069906bc945c9139f4d2d222abc30e521a20845513897d9ddcee3cb819002205edbda2708bb8df15c3a6f6b28144247544044e320448ff4ac766630bd6532aa012103d7502318c3205e4df6d0b2e9afa4c721526421914783fb33ce2aec9d40f0b449')
DCR_2_WITNESS_1_SCRIPT_SIG = bytes.fromhex('6a4730440220557f6069906bc945c9139f4d2d222abc30e521a20845513897d9ddcee3cb819002205edbda2708bb8df15c3a6f6b28144247544044e320448ff4ac766630bd6532aa012103d7502318c3205e4df6d0b2e9afa4c721526421914783fb33ce2aec9d40f0b449')
DCR_2_WITNESS_1_STACK_SCRIPT = DCR_2_WITNESS_1_SCRIPT_SIG[1:]
DCR_2_WITNESS_2 = bytes.fromhex('0050d6dc010000000d010000020000006b48304502210099f5cb0ca36e68f7f815e17538706b374e24ec9e61795984f767f230ee08dea802204c908c38e647e5d551dba5054adfd0430dde19ca94d83b68a795678d5246a90d012103ee327661befce7e68046a18aab5d2a566b0425069ad6b7b1951a737d40abd9cb')
DCR_2_WITNESS_2_SCRIPT_SIG = bytes.fromhex('6b48304502210099f5cb0ca36e68f7f815e17538706b374e24ec9e61795984f767f230ee08dea802204c908c38e647e5d551dba5054adfd0430dde19ca94d83b68a795678d5246a90d012103ee327661befce7e68046a18aab5d2a566b0425069ad6b7b1951a737d40abd9cb')
DCR_2_WITNESS_2_STACK_SCRIPT = DCR_2_WITNESS_1_SCRIPT_SIG[1:]

DCR_2_PREVOUT_PK = bytes.fromhex('76a91478807bd86b22a9f23bb4e026705c3e52824d7f3e88ac')
DCR_2_EXPECTED_SIGHASH_ALL = bytes.fromhex('569f23573cd279d9fea347ed16d86984b271b0b4b4270cc7122201683fcd7708')
DCR_2_EXPECTED_SIGHASH_ALL_ANYONECANPAY = bytes.fromhex('c75779c947b3c0e8828db370c8d5597c6dd91a48e287d1bfca705637943d200e')
DCR_2_EXPECTED_SIGHASH_SINGLE = bytes.fromhex('a1f4f2ced71352153ffee5dd570da5d609ecd5ce04e1db808c238554d758fb13')
DCR_2_EXPECTED_SIGHASH_SINGLE_ANYONECANPAY = bytes.fromhex('1b83a4d2a1a70204587491f7f6e110704e98e1b8da04219efba5dde14eaccf1f')
