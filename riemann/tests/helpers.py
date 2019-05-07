# flake8: noqa

# From Dev++ slides
# https://docs.google.com/presentation/d/1YGZf1VKKOnCdpuaVzU35CAXy8uGcztq0OBlTNMGSmkw/edit?usp=sharing
from ..script import examples

# Pay-to-Public-Key-Hash Transaction
P2PKH = {
        'human': {
            'version': 1,
            'locktime': 00000000,
            'ins': [
                {
                    'id': 0,
                    'sequence': 0xFFFFFFFE,
                    'addr': 'bc1q0py7d067fvd6wg64wtgmpj7qjnczz0nv6e2wgq',
                    'hash': 'ff7ff97060bfa1763dd9d4101b322157e841a4de865ddc28b1f71500f45c8135',
                    'hash_le': '',
                    'index': 0,
                    'value': 1000,
                    'outpoint': '35815cf40015f7b128dc5d86dea441e85721321b10d4d93d76a1bf6070f97fff00000000',
                    'signature': '30450221009e8c7f85d6491169df139f25d26633efe48e98738331a37a1694d655dccebdbd02201a6444cfb364e91279f8c9a8b09cdbdeb4bf6cc0f00f53b9356f852c3b3151dc01',
                    'pubkey': '02a004b949e4769ed341064829137b18992be884da5932c755e48f9465c1069dc2',
                    'stack_script': '30450221009e8c7f85d6491169df139f25d26633efe48e98738331a37a1694d655dccebdbd02201a6444cfb364e91279f8c9a8b09cdbdeb4bf6cc0f00f53b9356f852c3b3151dc01 02a004b949e4769ed341064829137b18992be884da5932c755e48f9465c1069dc2'
                    }
                ],
            'outs': [
                {
                    'id': 0,
                    'addr': 'bc1qp037f2sk26acz8dn9knp6s8fzuwg390zqxh966',
                    'value': 990,
                    'pk_script': '02ef21caa25eca974d3bdd73c034d6943cbf145a700d493adaa6f496bd87c5b33b'
                    },
                {
                    'id': 1,
                    'memo': 'made with ❤ by riemann'.encode('utf-8'),
                    'value': 0,
                    'pk_script': '6a186d616465207769746820e29da4206279207269656d616e6e'
                    }
                ]
            },
        'ser': {
            'version': bytes.fromhex('00000000'),
            'locktime': bytes.fromhex('00000000'),
            'ins': [
                {
                    'id': 0,
                    'hash': bytes.fromhex('ff7ff97060bfa1763dd9d4101b322157e841a4de865ddc28b1f71500f45c8135'),
                    'sequence': bytes.fromhex('feffffff'),
                    'index': bytes.fromhex('00000000'),
                    'pk_script': bytes.fromhex('02ef21caa25eca974d3bdd73c034d6943cbf145a700d493adaa6f496bd87c5b33b'),
                    'value': bytes.fromhex('e803000000000000'),
                    'outpoint': bytes.fromhex('35815cf40015f7b128dc5d86dea441e85721321b10d4d93d76a1bf6070f97fff00000000'),
                    'stack_script': bytes.fromhex('4830450221009e8c7f85d6491169df139f25d26633efe48e98738331a37a1694d655dccebdbd02201a6444cfb364e91279f8c9a8b09cdbdeb4bf6cc0f00f53b9356f852c3b3151dc012102a004b949e4769ed341064829137b18992be884da5932c755e48f9465c1069dc2'),
                    'redeem_script': bytes.fromhex(''),
                    'input': bytes.fromhex('35815cf40015f7b128dc5d86dea441e85721321b10d4d93d76a1bf6070f97fff000000006b4830450221009e8c7f85d6491169df139f25d26633efe48e98738331a37a1694d655dccebdbd02201a6444cfb364e91279f8c9a8b09cdbdeb4bf6cc0f00f53b9356f852c3b3151dc012102a004b949e4769ed341064829137b18992be884da5932c755e48f9465c1069dc2feffffff')
                    }
                ],
            'outs': [
                {
                    'id': 0,
                    'value': bytes.fromhex('de03000000000000'),
                    'pk_script': bytes.fromhex('02ef21caa25eca974d3bdd73c034d6943cbf145a700d493adaa6f496bd87c5b33b'),
                    'output': bytes.fromhex('de030000000000001600140be3e4aa1656bb811db32da61d40e9171c8895e2')
                    },
                {
                    'id': 1,
                    'value': bytes.fromhex('0000000000000000'),
                    'pk_script': bytes.fromhex('6a186d616465207769746820e29da4206279207269656d616e6e'),
                    'output': bytes.fromhex('00000000000000001a6a186d616465207769746820e29da4206279207269656d616e6e')
                    }
                ],
            'tx': {
                'out': bytes.fromhex('de030000000000001600140be3e4aa1656bb811db32da61d40e9171c8895e200000000000000001a6a186d616465207769746820e29da4206279207269656d616e6e00000000'),
                'unsigned': bytes.fromhex('020000000135815cf40015f7b128dc5d86dea441e85721321b10d4d93d76a1bf6070f97fff0000000000feffffff02de030000000000001600140be3e4aa1656bb811db32da61d40e9171c8895e200000000000000001a6a186d616465207769746820e29da4206279207269656d616e6e00000000'),
                'signed': bytes.fromhex('020000000135815cf40015f7b128dc5d86dea441e85721321b10d4d93d76a1bf6070f97fff000000006b4830450221009e8c7f85d6491169df139f25d26633efe48e98738331a37a1694d655dccebdbd02201a6444cfb364e91279f8c9a8b09cdbdeb4bf6cc0f00f53b9356f852c3b3151dc012102a004b949e4769ed341064829137b18992be884da5932c755e48f9465c1069dc2feffffff02de030000000000001600140be3e4aa1656bb811db32da61d40e9171c8895e200000000000000001a6a186d616465207769746820e29da4206279207269656d616e6e00000000')
                }
            }
        }

# UTXOs: https://blockchain.info/rawtx/d1c789a9c60383bf715f3f6ad9d14b91fe55f3deb369fe5d9280cb1a01793f81
# https://blockchain.info/rawtx/452c629d67e41baec3ac6f04fe744b4b9617f8f859c63b3002f8684e7a4fee03
# ['ser']['ins'][0]['value'] incorrect (fee is already deducted), only used in sighashes so leave
P2PKH1 = {
        'human': {
            'version': 1,
            'locktime': 19430600,
            'ins': [
                {
                    'id': 0,
                    'sequence': 0xFFFFFFFE,
                    'addr': '1GKN6gJBgvet8S92qiQjVxEaVJ5eoJE9s2',
                    'hash': 'd1c789a9c60383bf715f3f6ad9d14b91fe55f3deb369fe5d9280cb1a01793f81',
                    'hash_le': '813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1',
                    'index': 0,
                    'outpoint': '813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c700000000',
                    'stack_script': '483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a',
                    'redeem_script': '',
                    }
                ],
            'outs': [
                {
                    'id': 0,
                    'addr': '1JAHBxA51vwp5C2zpSB15VbxSZK3hVJs2H',
                    'value': 32454049,
                    'pk_script': '76a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac'
                    },
                {
                    'id': 1,
                    'addr': '13achaY7hdFTEHCzWC1Cvuo1FDKzDtAvRt',
                    'value': 10011545,
                    'pk_script': '76a9141c4bc762dd5423e332166702cb75f40df79fea1288ac'
                    }
                ],
            'tx': {
                'signed': '0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600'
                }
            },
        'ser': {
            'version': bytes.fromhex('01000000'),
            'locktime': bytes.fromhex('19430600'),
            'ins': [
                {
                    'id': 0,
                    'sequence': bytes.fromhex('feffffff'),
                    'hash': bytes.fromhex('813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1'),
                    'index': bytes.fromhex('00000000'),
                    'pk_script': bytes.fromhex('17a91424d6008f143af0cca57344069c46661aa4fcea2387'),
                    'value': bytes.fromhex('3af9870200000000'), # 42465594; fee is already deducted from this value
                    'outpoint': bytes.fromhex('813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d100000000'),
                    'stack_script_len': bytes.fromhex('6b'),
                    'stack_script': bytes.fromhex('483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a'),
                    'redeem_script': bytes.fromhex(''),
                    }
                ],
            'outs': [
                {
                    'id': 0,
                    'value': bytes.fromhex('a135ef0100000000'),
                    'pk_script': bytes.fromhex('76a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac'),
                    'out': bytes.fromhex('a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac')
                    },
                {
                    'id': 1,
                    'value': bytes.fromhex('99c3980000000000'),
                    'pk_script': bytes.fromhex('76a9141c4bc762dd5423e332166702cb75f40df79fea1288ac'),
                    'out': bytes.fromhex('99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac')
                    }
                ],
            'sighash': {
                'all': bytes.fromhex('b85c4f8d1377cc138225dd9b319d0a4ca547f7884270640f44c5fcdf269e0fe8'),
                'all_anyonecanpay': bytes.fromhex('3b67a5114cc9fc837ddd6f6ec11bde38db5f68c34ab6ece2a043d7b25f2cf8bb'),
                'single': bytes.fromhex('1dab67d768be0380fc800098005d1f61744ffe585b0852f8d7adc12121a86938'),
                'single_anyonecanpay': bytes.fromhex('d4687b93c0a9090dc0a3384cd3a594ce613834bb37abc56f6032e96c597547e3')
                },
            'tx': {
                'in': bytes.fromhex('813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff'),
                'signed': bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600'),
                'hash': bytes.fromhex('452c629d67e41baec3ac6f04fe744b4b9617f8f859c63b3002f8684e7a4fee03'),
                'hash_le': bytes.fromhex('03ee4f7a4e68f802303bc659f8f817964b4b74fe046facc3ae1be4679d622c45')
                }
            }
        }

# Pay-to-Script-Hash Transaction
#  UTXO: https://blockchain.info/rawtx/adbd01a9a2e9cae0d601061e73c5b3dbb635bb6b9e9b63dd555f88355ff28407
#  https://blockchain.info/rawtx/348231565
P2SH = {
    'human': {
        'version': 1,
        'locktime': 00000000,
        'ins': [
            {
                'sequence': 0xFFFFFFFE,
                'id': 0,
                'addr': '',
                'hash': '',
                'hash_le': '',
                'index': 0,
                'value': 0,
                'outpoint': ''
                }
            ],
        'outs': [
            {
                'id': 0,
                'addr': '',
                'value': 0,
                'pk_script': ''
                },
            {
                'id': 1,
                'addr': '',
                'value': 0,
                'pk_script': ''
                }
            ],
        'tx': {
            'signed': '01000000010784f25f35885f55dd639b9e6bbb35b6dbb3c5731e0601d6e0cae9a2a901bdad01000000d900473044022006ef6bf5880315420936e7c1bdeb7d68e67706d183b69ea3437966fb817da9bc02203446effcdf377e913ed145423088b9acf86b09ad0d608dfffd0bfaca5a396f2f01473044022022b990a3765a4418dc7e600a33a9b4019eeb6d5ed1ba8ab056533c6a50aadedb02202577803366dd13f2003bf90bf4ec463b6201ea70ea7b8ed414e8c385debacff501475221024c122c7dc3c539eaf657e254bb30a25ccc6efc17c1f58e4e448b3b9305b27dab21031d46936f30c89bb975a96c531ddebb256c6965235dc5383f36317953f10ea48952aeffffffff0270c579000000000017a914ec8c50e0db21e67a1c07eca87d1018a4e825275e870c93be000000000017a914aea8d2f5708ff4257169233664bd776806170b4d8700000000'
            }
        },
    'ser': {
        'version': bytes.fromhex('01000000'),
        'locktime': bytes.fromhex('00000000'),
        'ins': [
            {
                'sequence': bytes.fromhex('ffffffff'),
                'id': 0,
                'hash': bytes.fromhex(''),
                'index': bytes.fromhex(''),
                'pk_script': bytes.fromhex(''),
                'value': bytes.fromhex(''),
                'outpoint': bytes.fromhex('0784f25f35885f55dd639b9e6bbb35b6dbb3c5731e0601d6e0cae9a2a901bdad01000000'),
                'stack_script_len': bytes.fromhex(''),
                'stack_script': bytes.fromhex('00473044022006ef6bf5880315420936e7c1bdeb7d68e67706d183b69ea3437966fb817da9bc02203446effcdf377e913ed145423088b9acf86b09ad0d608dfffd0bfaca5a396f2f01473044022022b990a3765a4418dc7e600a33a9b4019eeb6d5ed1ba8ab056533c6a50aadedb02202577803366dd13f2003bf90bf4ec463b6201ea70ea7b8ed414e8c385debacff501'),
                'redeem_script': bytes.fromhex('475221024c122c7dc3c539eaf657e254bb30a25ccc6efc17c1f58e4e448b3b9305b27dab21031d46936f30c89bb975a96c531ddebb256c6965235dc5383f36317953f10ea48952ae'),
                'script_sig': bytes.fromhex('00473044022006ef6bf5880315420936e7c1bdeb7d68e67706d183b69ea3437966fb817da9bc02203446effcdf377e913ed145423088b9acf86b09ad0d608dfffd0bfaca5a396f2f01473044022022b990a3765a4418dc7e600a33a9b4019eeb6d5ed1ba8ab056533c6a50aadedb02202577803366dd13f2003bf90bf4ec463b6201ea70ea7b8ed414e8c385debacff501475221024c122c7dc3c539eaf657e254bb30a25ccc6efc17c1f58e4e448b3b9305b27dab21031d46936f30c89bb975a96c531ddebb256c6965235dc5383f36317953f10ea48952ae'),
                'input': bytes.fromhex('0784f25f35885f55dd639b9e6bbb35b6dbb3c5731e0601d6e0cae9a2a901bdad01000000d900473044022006ef6bf5880315420936e7c1bdeb7d68e67706d183b69ea3437966fb817da9bc02203446effcdf377e913ed145423088b9acf86b09ad0d608dfffd0bfaca5a396f2f01473044022022b990a3765a4418dc7e600a33a9b4019eeb6d5ed1ba8ab056533c6a50aadedb02202577803366dd13f2003bf90bf4ec463b6201ea70ea7b8ed414e8c385debacff501475221024c122c7dc3c539eaf657e254bb30a25ccc6efc17c1f58e4e448b3b9305b27dab21031d46936f30c89bb975a96c531ddebb256c6965235dc5383f36317953f10ea48952aeffffffff'),
                }
            ],
        'outs': [
            {
                'id': 0,
                'value': bytes.fromhex(''),
                'pk_script': bytes.fromhex(''),
                'output': bytes.fromhex('70c579000000000017a914ec8c50e0db21e67a1c07eca87d1018a4e825275e87')
                },
            {
                'id': 1,
                'value': bytes.fromhex(''),
                'pk_script': bytes.fromhex(''),
                'output': bytes.fromhex('0c93be000000000017a914aea8d2f5708ff4257169233664bd776806170b4d87')
                }
            ],
        'tx': {
            'out': bytes.fromhex(''),
            'unsigned': bytes.fromhex(''),
            'signed': bytes.fromhex('01000000010784f25f35885f55dd639b9e6bbb35b6dbb3c5731e0601d6e0cae9a2a901bdad01000000d900473044022006ef6bf5880315420936e7c1bdeb7d68e67706d183b69ea3437966fb817da9bc02203446effcdf377e913ed145423088b9acf86b09ad0d608dfffd0bfaca5a396f2f01473044022022b990a3765a4418dc7e600a33a9b4019eeb6d5ed1ba8ab056533c6a50aadedb02202577803366dd13f2003bf90bf4ec463b6201ea70ea7b8ed414e8c385debacff501475221024c122c7dc3c539eaf657e254bb30a25ccc6efc17c1f58e4e448b3b9305b27dab21031d46936f30c89bb975a96c531ddebb256c6965235dc5383f36317953f10ea48952aeffffffff0270c579000000000017a914ec8c50e0db21e67a1c07eca87d1018a4e825275e870c93be000000000017a914aea8d2f5708ff4257169233664bd776806170b4d8700000000'),
            'hash': bytes.fromhex(''),
            'hash_le': bytes.fromhex('')
            }
        }
    }

# Pay-to-Witness-Public-Key-Hash
# https://blockchain.info/rawtx/d2941b532f6d3d54d596345b50972b3995983239884037a52aab799ec84292ee (parent)
# https://blockchain.info/rawtx/1d204bc09e183741bf4c8fbe9034067d160e369e373ec9669ea51bfe6d0567df (child)
P2WPKH = {
        'human': {
            'version': 1,
            'locktime': 523722,
            'ins': [
                {
                    'id': 0,
                    'addr': 'bc1qwkxw25pcpktyq5ggv7vdv4rta0w2y7nnhtq88f',
                    'hash': 'd2941b532f6d3d54d596345b50972b3995983239884037a52aab799ec84292ee',
                    'index': 0,
                    'value': 120000,
                    'pk_script': '0014758ce550380d964051086798d6546bebdca27a73',
                    'sequence': 0xFFFFFFFd
                    }
                ],
            'outs': [
                {
                    'id': 0,
                    'addr': '3JoCkhfh6juGAp43jWftoSqJwoPptJ7GwF',
                    'value': 119667,
                    'pk_script': 'a914bba5acbec4e6e3374a0345bf3609fa7cfea825f187',
                    'output': '73d301000000000017a914bba5acbec4e6e3374a0345bf3609fa7cfea825f187'
                    },
                ],
            'witnesses': [
                {
                    'signature': '3045022100f746173f184f43e2855fd1b739879a137317ef905cc3b56fd1bcd34158a4721a022031163e6831efe77aa256ecfd65b9b1a9e46cafce8c2611be222194ee985dfd6601',
                    'pubkey': '027450ee71e5a86f7466720a10811316f79a64e85d5671ee46332f8f7dae4f5d67',
                    'stack': '3045022100f746173f184f43e2855fd1b739879a137317ef905cc3b56fd1bcd34158a4721a022031163e6831efe77aa256ecfd65b9b1a9e46cafce8c2611be222194ee985dfd6601 027450ee71e5a86f7466720a10811316f79a64e85d5671ee46332f8f7dae4f5d67'
                    }
                ]
            },
        'ser': {
            'version': bytes.fromhex('01000000'),
            'locktime': bytes.fromhex('cafd0700'),
            'ins': [
                {
                    'id': 0,
                    'hash': bytes.fromhex('d2941b532f6d3d54d596345b50972b3995983239884037a52aab799ec84292ee'),
                    'index': bytes.fromhex('00000000'),
                    'value': bytes.fromhex('c0d4010000000000'),
                    'pk_script': bytes.fromhex('160014758ce550380d964051086798d6546bebdca27a73'),
                    'sequence': bytes.fromhex('fffffffd'),
                    'input': bytes.fromhex('ee9242c89e79ab2aa537408839329895392b97505b3496d5543d6d2f531b94d20000000000fdffffff')
                    }
                ],
            'outs': [
                {
                    'id': 0,
                    'value': bytes.fromhex('73d3010000000000'),
                    'pk_script': bytes.fromhex('a914bba5acbec4e6e3374a0345bf3609fa7cfea825f187'),
                    'output': bytes.fromhex('73d301000000000017a914bba5acbec4e6e3374a0345bf3609fa7cfea825f187')
                    },
                ],
            'witnesses': [
                {
                    'signature': bytes.fromhex('3045022100f746173f184f43e2855fd1b739879a137317ef905cc3b56fd1bcd34158a4721a022031163e6831efe77aa256ecfd65b9b1a9e46cafce8c2611be222194ee985dfd6601'),
                    'pubkey': bytes.fromhex('027450ee71e5a86f7466720a10811316f79a64e85d5671ee46332f8f7dae4f5d67'),
                    'stack': bytes.fromhex('483045022100f746173f184f43e2855fd1b739879a137317ef905cc3b56fd1bcd34158a4721a022031163e6831efe77aa256ecfd65b9b1a9e46cafce8c2611be222194ee985dfd660121027450ee71e5a86f7466720a10811316f79a64e85d5671ee46332f8f7dae4f5d67'),
                    'witness': bytes.fromhex('02483045022100f746173f184f43e2855fd1b739879a137317ef905cc3b56fd1bcd34158a4721a022031163e6831efe77aa256ecfd65b9b1a9e46cafce8c2611be222194ee985dfd660121027450ee71e5a86f7466720a10811316f79a64e85d5671ee46332f8f7dae4f5d67'),
                    }
                ],
            'segwit_sighash': {
                'all': bytes.fromhex('135754ab872e4943f7a9c30d6143c4c7187e33d0f63c75ec82a7f9a15e2f2d00'),
                'all_anyonecanpay': bytes.fromhex('cc7438d5b15e93ba612dcd227cf1937c35273675b3aa7d1b771573667376ddf6'),
                'single': bytes.fromhex('d04631d2742e6fd8e80e2e4309dece65becca41d37fd6bc0bcba041c52d824d5'),
                'single_anyonecanpay': bytes.fromhex('ffea9cdda07170af9bc9967cedf485e9fe15b78a622e0c196c0b6fc64f40c615')
                },
            'tx': {
                'unsigned': bytes.fromhex('02000000000101ee9242c89e79ab2aa537408839329895392b97505b3496d5543d6d2f531b94d20000000000fdffffff0173d301000000000017a914bba5acbec4e6e3374a0345bf3609fa7cfea825f18700cafd0700'),
                'signed': bytes.fromhex('02000000000101ee9242c89e79ab2aa537408839329895392b97505b3496d5543d6d2f531b94d20000000000fdffffff0173d301000000000017a914bba5acbec4e6e3374a0345bf3609fa7cfea825f18702483045022100f746173f184f43e2855fd1b739879a137317ef905cc3b56fd1bcd34158a4721a022031163e6831efe77aa256ecfd65b9b1a9e46cafce8c2611be222194ee985dfd660121027450ee71e5a86f7466720a10811316f79a64e85d5671ee46332f8f7dae4f5d67cafd0700')
                }
            }
        }

# P2WSH
# UTXOs: https://blockchain.info/rawtx/3e28c6fa977034c2035ddede799ae32bc301efa03b5b033eaf983ac9c1aece1f
# https://blockchain.info/rawtx/264814c57c76694c752bcb800d7edaf210ef3a2c199c4db44485a15eb3429691
P2WSH = {
        'human': {
            'version': 1,
            'locktime': 0,
            'ins': [
                {
                    'sequence': 0xFFFFFFFF,
                    'id': 0,
                    'hash': '3e28c6fa977034c2035ddede799ae32bc301efa03b5b033eaf983ac9c1aece1f',
                    'index': 1,
                    'outpoint': '1fceaec1c93a98af3e035b3ba0ef01c32be39a79dede5d03c2347097fac6283e01000000',
                    'addr': 'bc1qwqdg6squsna38e46795at95yu9atm8azzmyvckulcc7kytlcckxswvvzej',
                    'value': 18661939,
                    'pk_script': '0020701a8d401c84fb13e6baf169d59684e17abd9fa216c8cc5b9fc63d622ff8c58d'
                    }
                ],
            'outs': [
                {
                    'id': 0,
                    'addr': '19u4AHtrWf4YfABuo1vCKcpizdngMxNJcF',
                    'value': 9000000,
                    'pk_script': '76a9146199463742d1359a505881821d82f5d4148e3fc588ac',
                    'output': '40548900000000001976a9146199463742d1359a505881821d82f5d4148e3fc588ac'
                    },
                {
                    'id': 1,
                    'addr': '32xum18WdAepEed6DNEBbNKBDU1gPUusqr',
                    'value': 1980000,
                    'pk_script': 'a9140df9a2a3c14a223733908e3e9127e2f6a9e2878e87',
                    'output': '60361e000000000017a9140df9a2a3c14a223733908e3e9127e2f6a9e2878e87'
                    },
                {
                    'id': 2,
                    'addr': '1PGd2WtYtEXNb6mFjesZr5WV7NXyAeb5Nj',
                    'value': 7351120,
                    'pk_script': '76a914f447146b86373c781a946d7ebd88cbbb79ec810288ac',
                    'output': '502b7000000000001976a914f447146b86373c781a946d7ebd88cbbb79ec810288ac'
                    },
                {
                    'id': 3,
                    'addr': 'bc1qwqdg6squsna38e46795at95yu9atm8azzmyvckulcc7kytlcckxswvvzej',
                    'value': 290819,
                    'pk_script': '0020701a8d401c84fb13e6baf169d59684e17abd9fa216c8cc5b9fc63d622ff8c58d',
                    'output': '0370040000000000220020701a8d401c84fb13e6baf169d59684e17abd9fa216c8cc5b9fc63d622ff8c58d'
                    }
                ],
            'witnesses': [
                {
                    'stack': 'NONE 304402201b1c2fc7d58870004c379575a47db60c3833174033f891ad5030cbf0c37c50c302206087d3ddc6f38da40e7eaf8c2af3f934a577de10e6ca75e00b4cdfbb34f5d40601 3045022100a7ecde342ccacd1159e385bcd41c947723a7ae3fcea66c76b5b09d02fee310f7022058ca21324fcd0c90e69630f13975d993e11f62ec8d7aa1a9a49036b9607e58fe01',
                    'wit_script': 'OP_2 0375e00eb72e29da82b89367947f29ef34afb75e8654f6ea368e0acdfd92976b7c 03a1b26313f430c4b15bb1fdce663207659d8cac749a0e53d70eff01874496feff 03c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f880 OP_3 OP_CHECKMULTISIG',
                    }
                ],
            'tx': {
                'signed': '010000000001011fceaec1c93a98af3e035b3ba0ef01c32be39a79dede5d03c2347097fac6283e0100000000ffffffff0440548900000000001976a9146199463742d1359a505881821d82f5d4148e3fc588ac60361e000000000017a9140df9a2a3c14a223733908e3e9127e2f6a9e2878e87502b7000000000001976a914f447146b86373c781a946d7ebd88cbbb79ec810288ac0370040000000000220020701a8d401c84fb13e6baf169d59684e17abd9fa216c8cc5b9fc63d622ff8c58d040047304402201b1c2fc7d58870004c379575a47db60c3833174033f891ad5030cbf0c37c50c302206087d3ddc6f38da40e7eaf8c2af3f934a577de10e6ca75e00b4cdfbb34f5d40601483045022100a7ecde342ccacd1159e385bcd41c947723a7ae3fcea66c76b5b09d02fee310f7022058ca21324fcd0c90e69630f13975d993e11f62ec8d7aa1a9a49036b9607e58fe016952210375e00eb72e29da82b89367947f29ef34afb75e8654f6ea368e0acdfd92976b7c2103a1b26313f430c4b15bb1fdce663207659d8cac749a0e53d70eff01874496feff2103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f88053ae00000000'
                }
            },
        'ser': {
            'version': bytes.fromhex('01000000'),
            'locktime': bytes.fromhex('00000000'),
            'segwit_flag': bytes.fromhex('0001'),
            'ins': [
                {
                    'sequence': bytes.fromhex('ffffffff'),
                    'id': 0,
                    'hash': bytes.fromhex('3e28c6fa977034c2035ddede799ae32bc301efa03b5b033eaf983ac9c1aece1f'),
                    'index': bytes.fromhex('01000000'),
                    'outpoint': bytes.fromhex('1fceaec1c93a98af3e035b3ba0ef01c32be39a79dede5d03c2347097fac6283e01000000'),
                    'value': bytes.fromhex(''),
                    'pk_script': bytes.fromhex('0020701a8d401c84fb13e6baf169d59684e17abd9fa216c8cc5b9fc63d622ff8c58d'),
                    'input': bytes.fromhex('1fceaec1c93a98af3e035b3ba0ef01c32be39a79dede5d03c2347097fac6283e0100000000ffffffff'),
                    }
                ],
            'outs': [
                {
                    'id': 0,
                    'value': bytes.fromhex(''),
                    'pk_script': bytes.fromhex('76a9146199463742d1359a505881821d82f5d4148e3fc588ac'),
                    'output': bytes.fromhex('40548900000000001976a9146199463742d1359a505881821d82f5d4148e3fc588ac')
                    },
                {
                    'id': 1,
                    'value': bytes.fromhex(''),
                    'pk_script': bytes.fromhex('a9140df9a2a3c14a223733908e3e9127e2f6a9e2878e87'),
                    'output': bytes.fromhex('60361e000000000017a9140df9a2a3c14a223733908e3e9127e2f6a9e2878e87')
                    },
                {
                    'id': 2,
                    'value': bytes.fromhex(''),
                    'pk_script': bytes.fromhex('76a914f447146b86373c781a946d7ebd88cbbb79ec810288ac'),
                    'output': bytes.fromhex('502b7000000000001976a914f447146b86373c781a946d7ebd88cbbb79ec810288ac')
                    },
                {
                    'id': 3,
                    'value': bytes.fromhex(''),
                    'pk_script': bytes.fromhex('0020701a8d401c84fb13e6baf169d59684e17abd9fa216c8cc5b9fc63d622ff8c58d'),
                    'output': bytes.fromhex('0370040000000000220020701a8d401c84fb13e6baf169d59684e17abd9fa216c8cc5b9fc63d622ff8c58d')
                    }
                ],
            'witnesses': [
                {
                    'wit_stack_items': [
                        bytes.fromhex(''),
                        bytes.fromhex('304402201b1c2fc7d58870004c379575a47db60c3833174033f891ad5030cbf0c37c50c302206087d3ddc6f38da40e7eaf8c2af3f934a577de10e6ca75e00b4cdfbb34f5d40601'),
                        bytes.fromhex('3045022100a7ecde342ccacd1159e385bcd41c947723a7ae3fcea66c76b5b09d02fee310f7022058ca21324fcd0c90e69630f13975d993e11f62ec8d7aa1a9a49036b9607e58fe01'),
                        bytes.fromhex('52210375e00eb72e29da82b89367947f29ef34afb75e8654f6ea368e0acdfd92976b7c2103a1b26313f430c4b15bb1fdce663207659d8cac749a0e53d70eff01874496feff2103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f88053ae')
                        ],
                    'wit_script': bytes.fromhex('52210375e00eb72e29da82b89367947f29ef34afb75e8654f6ea368e0acdfd92976b7c2103a1b26313f430c4b15bb1fdce663207659d8cac749a0e53d70eff01874496feff2103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f88053ae'),
                    }
                ],
            'tx': {
                'witness': bytes.fromhex('040047304402201b1c2fc7d58870004c379575a47db60c3833174033f891ad5030cbf0c37c50c302206087d3ddc6f38da40e7eaf8c2af3f934a577de10e6ca75e00b4cdfbb34f5d40601483045022100a7ecde342ccacd1159e385bcd41c947723a7ae3fcea66c76b5b09d02fee310f7022058ca21324fcd0c90e69630f13975d993e11f62ec8d7aa1a9a49036b9607e58fe016952210375e00eb72e29da82b89367947f29ef34afb75e8654f6ea368e0acdfd92976b7c2103a1b26313f430c4b15bb1fdce663207659d8cac749a0e53d70eff01874496feff2103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f88053ae'),
                'signed': bytes.fromhex('010000000001011fceaec1c93a98af3e035b3ba0ef01c32be39a79dede5d03c2347097fac6283e0100000000ffffffff0440548900000000001976a9146199463742d1359a505881821d82f5d4148e3fc588ac60361e000000000017a9140df9a2a3c14a223733908e3e9127e2f6a9e2878e87502b7000000000001976a914f447146b86373c781a946d7ebd88cbbb79ec810288ac0370040000000000220020701a8d401c84fb13e6baf169d59684e17abd9fa216c8cc5b9fc63d622ff8c58d040047304402201b1c2fc7d58870004c379575a47db60c3833174033f891ad5030cbf0c37c50c302206087d3ddc6f38da40e7eaf8c2af3f934a577de10e6ca75e00b4cdfbb34f5d40601483045022100a7ecde342ccacd1159e385bcd41c947723a7ae3fcea66c76b5b09d02fee310f7022058ca21324fcd0c90e69630f13975d993e11f62ec8d7aa1a9a49036b9607e58fe016952210375e00eb72e29da82b89367947f29ef34afb75e8654f6ea368e0acdfd92976b7c2103a1b26313f430c4b15bb1fdce663207659d8cac749a0e53d70eff01874496feff2103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f88053ae00000000')
                }
            }
    }

INPUT_FOR_WITNESS_SEQUENCE_GUESSING = bytes.fromhex('1fceaec1c93a98af3e035b3ba0ef01c32be39a79dede5d03c2347097fac6283e0100000000feffffff')

# P2SH OP_PUSHDATA1
# UTXOs: https://blockchain.info/rawtx/6293ab0c51e73fd12c20ea93de23005966f651556fa745f8b139833328f53e12
# https://blockchain.info/rawtx/967ea903705887766b02834c13e0f3de43030ec19b5a3e568676be3557a41c39
P2SH_PD1 = {
        'human': {
            'version': 0,
            'locktime': 0,
            'ins': [
                {
                    'sequence': 0xFFFFFFFF,
                    'id': 0,
                    'hash': '6293ab0c51e73fd12c20ea93de23005966f651556fa745f8b139833328f53e12',
                    'index': 0,
                    'addr': '3Hd8JLLJVFw9sNhzaxPfp5t13gMfoJEVqG',
                    'value': 938948354,
                    'pk_script': 'a914aec5abbd414bb04de2dd55dd8048b05c3a76ec6387',
                    'stack_script': 'OP_0 3044022024bb241b26586a4c614ba38fec83a50904d5daeed0975e25eae095e5e911989e022073d99364454fc572a189a2dcf11c6b182a45c5177e746b731448abe3d9e4fe5001 30440220319dbd5a69bcaa73e569c5e068edb03f6c52344cd9068d248925256463608c8f02201b4f35ee176d85395aa1eb49aa80adc22cad820d26d62cf462889b791b98aaf801',
                    'redeem_script': 'OP_2 02975ddf75126ef880d1b56ea194141ea0ceb2d9e12298b74d54432cbd83535854 03c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f880 03e5dc75b59e4c67bfea266314d0b1da1e317f5b7d1e4cf1975442b79e542de748 OP_3 OP_CHECKMULTISIG',
                    'script_sig': 'OP_0 3044022024bb241b26586a4c614ba38fec83a50904d5daeed0975e25eae095e5e911989e022073d99364454fc572a189a2dcf11c6b182a45c5177e746b731448abe3d9e4fe5001 30440220319dbd5a69bcaa73e569c5e068edb03f6c52344cd9068d248925256463608c8f02201b4f35ee176d85395aa1eb49aa80adc22cad820d26d62cf462889b791b98aaf801 522102975ddf75126ef880d1b56ea194141ea0ceb2d9e12298b74d54432cbd835358542103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f8802103e5dc75b59e4c67bfea266314d0b1da1e317f5b7d1e4cf1975442b79e542de74853ae',
                    }
                ],
            'outs': [
                {
                    'id': 0,
                    'addr': 'bc1qwqdg6squsna38e46795at95yu9atm8azzmyvckulcc7kytlcckxswvvzej',
                    'value': 904975000,
                    'pk_script': '0020701a8d401c84fb13e6baf169d59684e17abd9fa216c8cc5b9fc63d622ff8c58d',
                    },
                {
                    'id': 1,
                    'addr': 'bc1qyy30guv6m5ez7ntj0ayr08u23w3k5s8vg3elmxdzlh8a3xskupyqn2lp5w',
                    'value': 33915754,
                    'pk_script': '00202122f4719add322f4d727f48379f8a8ba36a40ec4473fd99a2fdcfd89a16e048',
                    }
                ],
            },
        'ser': {
            'version': bytes.fromhex('00000000'),
            'locktime': bytes.fromhex('00000000'),
            'ins': [
                {
                    'id': 0,
                    'sequence': bytes.fromhex('ffffffff'),
                    'hash': bytes.fromhex('6293ab0c51e73fd12c20ea93de23005966f651556fa745f8b139833328f53e12'),
                    'index': bytes.fromhex('01000000'),
                    'value': bytes.fromhex(''),
                    'pk_script': bytes.fromhex('a914aec5abbd414bb04de2dd55dd8048b05c3a76ec6387'),
                    'stack_script': bytes.fromhex('00473044022024bb241b26586a4c614ba38fec83a50904d5daeed0975e25eae095e5e911989e022073d99364454fc572a189a2dcf11c6b182a45c5177e746b731448abe3d9e4fe50014730440220319dbd5a69bcaa73e569c5e068edb03f6c52344cd9068d248925256463608c8f02201b4f35ee176d85395aa1eb49aa80adc22cad820d26d62cf462889b791b98aaf801'),
                    'redeem_script': bytes.fromhex('4c69522102975ddf75126ef880d1b56ea194141ea0ceb2d9e12298b74d54432cbd835358542103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f8802103e5dc75b59e4c67bfea266314d0b1da1e317f5b7d1e4cf1975442b79e542de74853ae'),
                    'script_sig': bytes.fromhex('00473044022024bb241b26586a4c614ba38fec83a50904d5daeed0975e25eae095e5e911989e022073d99364454fc572a189a2dcf11c6b182a45c5177e746b731448abe3d9e4fe50014730440220319dbd5a69bcaa73e569c5e068edb03f6c52344cd9068d248925256463608c8f02201b4f35ee176d85395aa1eb49aa80adc22cad820d26d62cf462889b791b98aaf8014c69522102975ddf75126ef880d1b56ea194141ea0ceb2d9e12298b74d54432cbd835358542103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f8802103e5dc75b59e4c67bfea266314d0b1da1e317f5b7d1e4cf1975442b79e542de74853ae'),
                    'input': bytes.fromhex('123ef528338339b1f845a76f5551f666590023de93ea202cd13fe7510cab936200000000fc00473044022024bb241b26586a4c614ba38fec83a50904d5daeed0975e25eae095e5e911989e022073d99364454fc572a189a2dcf11c6b182a45c5177e746b731448abe3d9e4fe50014730440220319dbd5a69bcaa73e569c5e068edb03f6c52344cd9068d248925256463608c8f02201b4f35ee176d85395aa1eb49aa80adc22cad820d26d62cf462889b791b98aaf8014c69522102975ddf75126ef880d1b56ea194141ea0ceb2d9e12298b74d54432cbd835358542103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f8802103e5dc75b59e4c67bfea266314d0b1da1e317f5b7d1e4cf1975442b79e542de74853aeffffffff'),
                    }
                ],
            'outs': [
                {
                    'id': 0,
                    'value': bytes.fromhex(''),
                    'pk_script': bytes.fromhex('0020701a8d401c84fb13e6baf169d59684e17abd9fa216c8cc5b9fc63d622ff8c58d'),
                    'output': bytes.fromhex('')
                    },
                {
                    'id': 1,
                    'value': bytes.fromhex(''),
                    'pk_script': bytes.fromhex('00202122f4719add322f4d727f48379f8a8ba36a40ec4473fd99a2fdcfd89a16e048'),
                    'output': bytes.fromhex('')
                    }
                ],
            'tx': {
                'unsinged': bytes.fromhex('')
                }
            }
        }

# P2SH OP_PUSHDATA2 (contructed by modifying the transaction shown in the P2SH_PD1 dictionary)
P2SH_PD2 = {
        'human': {
            'version': 0,
            'locktime': 0,
            'ins': [
                {
                    'id': 0,
                    'sequence': 0xFFFFFFFF,
                    'addr': '3Hd8JLLJVFw9sNhzaxPfp5t13gMfoJEVqG',
                    'index': 0,
                    'value': 938948354,
                    'script_sig': 'OP_0 3044022024bb241b26586a4c614ba38fec83a50904d5daeed0975e25eae095e5e911989e022073d99364454fc572a189a2dcf11c6b182a45c5177e746b731448abe3d9e4fe5001 30440220319dbd5a69bcaa73e569c5e068edb03f6c52344cd9068d248925256463608c8f02201b4f35ee176d85395aa1eb49aa80adc22cad820d26d62cf462889b791b98aaf801 522102975ddf75126ef880d1b56ea194141ea0ceb2d9e12298b74d54432cbd835358542103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f8802103e5dc75b59e4c67bfea266314d0b1da1e317f5b7d1e4cf1975442b79e542de74853ae2102975ddf75126ef880d1b56ea194141ea0ceb2d9e12298b74d54432cbd835358542103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f8802103e5dc75b59e4c67bfea266314d0b1da1e317f5b7d1e4cf1975442b79e542de74853ae2102975ddf75126ef880d1b56ea194141ea0ceb2d9e12298b74d54432cbd835358542103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f8802103e5dc75b59e4c67bfea266314d0b1da1e317f5b7d1e4cf1975442b79e542de74853ae',
                    }
                ],
            },
        'ser': {
            'version': bytes.fromhex('00000000'),
            'locktime': bytes.fromhex('00000000'),
            'ins': [
                {
                    'id': 0,
                    'sequence': bytes.fromhex('ffffffff'),
                    'hash': bytes.fromhex(''),
                    'index': bytes.fromhex('01000000'),
                    'value': bytes.fromhex(''),
                    'script_sig': bytes.fromhex('00473044022024bb241b26586a4c614ba38fec83a50904d5daeed0975e25eae095e5e911989e022073d99364454fc572a189a2dcf11c6b182a45c5177e746b731448abe3d9e4fe50014730440220319dbd5a69bcaa73e569c5e068edb03f6c52344cd9068d248925256463608c8f02201b4f35ee176d85395aa1eb49aa80adc22cad820d26d62cf462889b791b98aaf8014d3901522102975ddf75126ef880d1b56ea194141ea0ceb2d9e12298b74d54432cbd835358542103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f8802103e5dc75b59e4c67bfea266314d0b1da1e317f5b7d1e4cf1975442b79e542de74853ae2102975ddf75126ef880d1b56ea194141ea0ceb2d9e12298b74d54432cbd835358542103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f8802103e5dc75b59e4c67bfea266314d0b1da1e317f5b7d1e4cf1975442b79e542de74853ae2102975ddf75126ef880d1b56ea194141ea0ceb2d9e12298b74d54432cbd835358542103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f8802103e5dc75b59e4c67bfea266314d0b1da1e317f5b7d1e4cf1975442b79e542de74853ae'),
                    }
                ],
            'tx': {
                'unsigned': bytes.fromhex('123ef528338339b1f845a76f5551f666590023de93ea202cd13fe7510cab936200000000fc00473044022024bb241b26586a4c614ba38fec83a50904d5daeed0975e25eae095e5e911989e022073d99364454fc572a189a2dcf11c6b182a45c5177e746b731448abe3d9e4fe50014730440220319dbd5a69bcaa73e569c5e068edb03f6c52344cd9068d248925256463608c8f02201b4f35ee176d85395aa1eb49aa80adc22cad820d26d62cf462889b791b98aaf8014c69522102975ddf75126ef880d1b56ea194141ea0ceb2d9e12298b74d54432cbd835358542103c96d495bfdd5ba4145e3e046fee45e84a8a48ad05bd8dbb395c011a32cf9f8802103e5dc75b59e4c67bfea266314d0b1da1e317f5b7d1e4cf1975442b79e542de74853aeffffffff')
                }
            }
        }
# Notes
# Unsure if python-bitcoinlib supports witness txns yet.
# To make more sighash tests:
#
# 1. install python-bitcoinlib
# 2. As follows:
# ««NB: (for BIP143 witness sighash, one can use riemann/tests/scripts/SPQR.py)»»
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
# a = parse_tx(tx_hex)
#
# # for legacy sighash:
# print(SignatureHash(prevout_pk_script, a, index, SIGHASH_ALL))
# print(SignatureHash(prevout_pk_script, a, index,
#                     SIGHASH_ALL | SIGHASH_ANYONECANPAY))
# print(SignatureHash(prevout_pk_script, a, index, SIGHASH_SINGLE))
# print(SignatureHash(prevout_pk_script, a, index,
#                     SIGHASH_SINGLE | SIGHASH_ANYONECANPAY))
#
# # for BIP143 witness sighash:
# print(SignatureHash(prevout_pk_script, a, index,
#                     SIGHASH_ALL, sigversion=1, amount=(INT_VALUE)).hex())
# print(SignatureHash(prevout_pk_script, a, index,
#                     SIGHASH_ALL | SIGHASH_ANYONECANPAY,
#                     sigversion=1, amount=(INT_VALUE)).hex())
# print(SignatureHash(prevout_pk_script, a, index,
#                     SIGHASH_SINGLE, sigversion=1, amount=(INT_VALUE)).hex())
# print(SignatureHash(prevout_pk_script, a, index,
#                     SIGHASH_SINGLE | SIGHASH_ANYONECANPAY,
#                     sigversion=1, amount=(INT_VALUE)).hex())

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
SIGHASH_FORKID = {
        'all': bytes.fromhex('450a16c7b1d6f913acb2460665a6fdc7dc7d351af5a3358c537278ffa4d125ea'),
        'single': bytes.fromhex('1a8ad1cebbd419fe5a53092fa6c272d8456829e871bf46be93906e859e42890e'),
        'all_anyone_can_pay': bytes.fromhex('f1a7a88eb953c86381f50ed223b8dd06e45b86437747ad83886f0529da9f3323'),
        'single_anyone_can_pay': bytes.fromhex('4ad1e69f172960c7ce26b993a0696fb618cf41104898b93b9fd66be465d1d38d')
        }
OP_IF = {
        'p2sh': '3MpTk145zbm5odhRALfT9BnUs8DB5w4ydw',
        'cashaddr': 'bitcoincash:prwv474e2d35xuf77ju6r4zr5xmv4ryd6ynr4c5mld',
        'script_hash': bytes.fromhex('dccafab9536343713ef4b9a1d443a1b6ca8c8dd1'),
        'output_script': b'\xa9\x14' + bytes.fromhex('dccafab9536343713ef4b9a1d443a1b6ca8c8dd1') + b'\x87',
        'output': bytes.fromhex('a135ef0100000000') + b'\x17' + b'\xa9\x14' + bytes.fromhex('dccafab9536343713ef4b9a1d443a1b6ca8c8dd1') + b'\x87'
        }

PK = {
        'human': [
            {
                'pk': '00' * 65,
                'pkh': '1b60c31dba9403c74d81af255f0c300bfed5faa3'
                },
            {
                'pk': '11' * 65,
                'pkh': 'e723a0f62396b8b03dbd9e48e9b9efe2eb704aab'
                }
            ],
        'ser': [
            {
                'pk': bytes.fromhex('00' * 65),
                'pkh': bytes.fromhex('1b60c31dba9403c74d81af255f0c300bfed5faa3'),
                'pkh_output': b'\x76\xa9\x14' + bytes.fromhex('1b60c31dba9403c74d81af255f0c300bfed5faa3') + b'\x88\xac',
                'pkh_p2wpkh_output': b'\x00\x14' + bytes.fromhex('1b60c31dba9403c74d81af255f0c300bfed5faa3'),
                'pk_p2pkh_output': bytes.fromhex('a135ef0100000000') + b'\x19' + b'\x76\xa9\x14' + bytes.fromhex('1b60c31dba9403c74d81af255f0c300bfed5faa3') + b'\x88\xac',
                'pk_p2wpkh_output': bytes.fromhex('a135ef0100000000') + b'\x16' + b'\x00\x14' + bytes.fromhex('1b60c31dba9403c74d81af255f0c300bfed5faa3')
                },
            {
                'pk': bytes.fromhex('11' * 65),
                'pkh': bytes.fromhex('e723a0f62396b8b03dbd9e48e9b9efe2eb704aab')
                }
            ]
        }



MSIG_2_2 = {
        'redeem_script': examples.msig_two_two.format(pk0=PK['human'][0]['pk'], pk1=PK['human'][1]['pk']),  # type: ignore
        'ser_script': bytes.fromhex('5241000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000041111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111152ae'),
        'p2sh': '3R23EEkAzy7HPWKN8rcL4ZzSjEWNsipxWV',
        'script_hash': bytes.fromhex('ffe3e2be6ba8d465041d3da1cdfe472b901b215a'),
        'output': b'\xa9' + bytes.fromhex('ffe3e2be6ba8d465041d3da1cdfe472b901b215a') + b'\x87'
        }

# https://blockchain.info/rawtx/2b6d004f685cf6515faf5d5a508853a5d9cda2c589fcf49a5781cb38be06029b
# https://blockchain.info/rawtx/bb35ff9adf914ce9263b75fbd1f8c1f706dd4f0389f4a39c2efe5f272381ead5
# https://blockchain.info/rawtx/7e7399b59e04c5cd0701642d4f40e48deb791a1fabda0e48ad267696571014b7
P2WPKH_ADDR = {
        'address': 'bc1q8cqttds2dej9zht7vupd3467ndhur92fudlyql',
        'pubkey': bytes.fromhex('03dc3dbabbf8c5e15d1eb3606a6a42c6d3a8c546f2a196a80a08b9a9021e2be33d'),
        'pkh': bytes.fromhex('3e00b5b60a6e64515d7e6702d8d75e9b6fc19549'),
        'output': b'\x00\x14' + bytes.fromhex('3e00b5b60a6e64515d7e6702d8d75e9b6fc19549')
        }

ADDR = [
        {
            'p2pkh': '13VmALKHkCdSN1JULkP6RqW3LcbpWvgryV',
            'p2pkh_cashaddr': 'bitcoincash:qqdkpscah22q836dsxhj2hcvxq9la4065v92pm9f84',
            'p2wpkh': 'bc1qrdsvx8d6jspuwnvp4uj47rpsp0ldt74r72cx4u'
            },
        {
            'p2pkh': '1N59mqr5yg38K11PTY2HdZTN7KmAHeCyHE'
            }
        ]

CASHADDR = {
        'pubkey': bytes.fromhex('02f0899f0bbd104a12efa06d10eece1584887a6cfaf31cd168c78d0c15d8357aa7'),
        'p2pkh': 'bitcoincash:qr4l2ykm7qw4rwg0yqtxwrt4mp0m4wsn4qv4sm4l62',
        'legacy_p2pkh': '1NWdP6dqMUjK5VCDELo6vFhaGkJFLEY5Gw'
        }

# From blockchain.info
# https://blockchain.info/rawtx/0739d0c7b7b7ff5f991e8e3f72a6f5eb56563880df982c4ab813cd71bc7a6a03?format=hex

RAW_P2SH_TO_P2PKH = bytes.fromhex( '010000000101d15c2cc4621b2a319ba53714e2709f8ba2dbaf23f8c35a4bddcb203f9b391000000000df473044022000e02ea97289a35181a9bfabd324f12439410db11c4e94978cdade6a665bf1840220458b87c34d8bb5e4d70d01041c7c2d714ea8bfaca2c2d2b1f9e5749c3ee17e3d012102ed0851f0b4c4458f80e0310e57d20e12a84642b8e097fe82be229edbd7dbd53920f6665740b1f950eb58d646b1fae9be28cef842da5e51dc78459ad2b092e7fd6e514c5163a914bb408296de2420403aa79eb61426bb588a08691f8876a91431b31321831520e346b069feebe6e9cf3dd7239c670400925e5ab17576a9140d22433293fe9652ea00d21c5061697aef5ddb296888ac0000000001d0070000000000001976a914f2539f42058da784a9d54615ad074436cf3eb85188ac00000000')
