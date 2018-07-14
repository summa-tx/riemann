# flake8: noqa

# From Dev++ slides
# https://docs.google.com/presentation/d/1YGZf1VKKOnCdpuaVzU35CAXy8uGcztq0OBlTNMGSmkw/edit?usp=sharing
from ..script import examples

# Pay-to-Public-Key-Hash Transaction used in riemann.examples.p2pkh_tx_ex
# UTXOs: https://blockchain.info/rawtx/264b157c1c733bb42c42f2932702921ea23ac93259ca058cdf36311e36295188
# https://blockchain.info/rawtx/1e7acd3d4715054c8fb0fdea25c5c704986006d2c6f30b0782e9b36a7ee072ef
P2PKH = {
        'human': {
            'version': 0,
            'locktime': 00000000,
            'ins': [
                {
                    'id': 0,
                    'sequence': 0xFFFFFFFE,
                    'addr': '18mTD3dVy4Y69knfyRi5vKtDxqtFWmgg7v',
                    'hash': '264b157c1c733bb42c42f2932702921ea23ac93259ca058cdf36311e36295188',
                    'hash_le': '',
                    'index': 0,
                    'value': 100000,
                    'outpoint': '885129361e3136df8c05ca5932c93aa21e92022793f2422cb43b731c7c154b2600000000',
                    'signature': '3045022100969b9b2a0eb72af4018834dc17e7d2eb0a09e8ffa1d620847f85cebc29d6197002203378382cfbfefad6d659fe838c34549dc9a8c2e9e61087d4c648c6c3562e386701',
                    'pubkey': '02bfb0a1108262227c8415aa90edc6c1a10e1e447ae58587c537926ef7069a38ca',
                    'stack_script': '3045022100969b9b2a0eb72af4018834dc17e7d2eb0a09e8ffa1d620847f85cebc29d6197002203378382cfbfefad6d659fe838c34549dc9a8c2e9e61087d4c648c6c3562e386701 02bfb0a1108262227c8415aa90edc6c1a10e1e447ae58587c537926ef7069a38ca'
                    }
                ],
            'outs': [
                {
                    'id': 0,
                    'addr': 'bc1qss5rslea60lftfe7pyk32s9j9dtr7z7mrqud3g',
                    'value': 96900,
                    'pk_script': '00148428387f3dd3fe95a73e092d1540b22b563f0bdb'
                    },
                {
                    'id': 1,
                    'memo': 'made with ❤ by riemann'.encode('utf-8'),
                    'value': 0,
                    'pk_script': '6a4c186d616465207769746820e29da4206279207269656d616e6e'
                    }
                ]
            },
        'ser': {
            'version': bytes.fromhex('00000000'),
            'locktime': bytes.fromhex('00000000'),
            'ins': [
                {
                    'id': 0,
                    'hash': bytes.fromhex('885129361e3136df8c05ca5932c93aa21e92022793f2422cb43b731c7c154b26'),
                    'sequence': bytes.fromhex('feffffff'),
                    'index': bytes.fromhex('00000000'),
                    'pk_script': bytes.fromhex('a91455310f53d91c7a6034b2c9abff3e0b9cf3fcee1e88ac'),
                    'value': bytes.fromhex('a086010000000000'),
                    'outpoint': bytes.fromhex('885129361e3136df8c05ca5932c93aa21e92022793f2422cb43b731c7c154b2600000000'),
                    'stack_script': bytes.fromhex('483045022100969b9b2a0eb72af4018834dc17e7d2eb0a09e8ffa1d620847f85cebc29d6197002203378382cfbfefad6d659fe838c34549dc9a8c2e9e61087d4c648c6c3562e3867012102bfb0a1108262227c8415aa90edc6c1a10e1e447ae58587c537926ef7069a38ca'),
                    'redeem_script': bytes.fromhex(''),
                    'input': bytes.fromhex('885129361e3136df8c05ca5932c93aa21e92022793f2422cb43b731c7c154b26000000006b483045022100969b9b2a0eb72af4018834dc17e7d2eb0a09e8ffa1d620847f85cebc29d6197002203378382cfbfefad6d659fe838c34549dc9a8c2e9e61087d4c648c6c3562e3867012102bfb0a1108262227c8415aa90edc6c1a10e1e447ae58587c537926ef7069a38cafeffffff')
                    }
                ],
            'outs': [
                {
                    'id': 0,
                    'value': bytes.fromhex('847a010000000000'),
                    'pk_script': bytes.fromhex('00148428387f3dd3fe95a73e092d1540b22b563f0bdb'),
                    'output': bytes.fromhex('847a0100000000001600148428387f3dd3fe95a73e092d1540b22b563f0bdb')
                    },
                {
                    'id': 1,
                    'value': bytes.fromhex('0000000000000000'),
                    'pk_script': bytes.fromhex('6a4c186d616465207769746820e29da4206279207269656d616e6e'),
                    'output': bytes.fromhex('00000000000000001b6a4c186d616465207769746820e29da4206279207269656d616e6e')
                    }
                ],
            'tx': {
                'out': bytes.fromhex('847a0100000000001600148428387f3dd3fe95a73e092d1540b22b563f0bdb00000000000000001b6a4c186d616465207769746820e29da4206279207269656d616e6e00000000'),
                'unsigned': bytes.fromhex('0100000001885129361e3136df8c05ca5932c93aa21e92022793f2422cb43b731c7c154b260000000000feffffff02847a0100000000001600148428387f3dd3fe95a73e092d1540b22b563f0bdb00000000000000001b6a4c186d616465207769746820e29da4206279207269656d616e6e00000000'),
                'signed': bytes.fromhex('0100000001885129361e3136df8c05ca5932c93aa21e92022793f2422cb43b731c7c154b26000000006b483045022100969b9b2a0eb72af4018834dc17e7d2eb0a09e8ffa1d620847f85cebc29d6197002203378382cfbfefad6d659fe838c34549dc9a8c2e9e61087d4c648c6c3562e3867012102bfb0a1108262227c8415aa90edc6c1a10e1e447ae58587c537926ef7069a38cafeffffff02847a0100000000001600148428387f3dd3fe95a73e092d1540b22b563f0bdb00000000000000001b6a4c186d616465207769746820e29da4206279207269656d616e6e00000000'),
                'hash': bytes.fromhex(''),
                'hash_le': bytes.fromhex('')
                }
            }
        }

# UTXOs: https://blockchain.info/rawtx/d1c789a9c60383bf715f3f6ad9d14b91fe55f3deb369fe5d9280cb1a01793f81
# https://blockchain.info/rawtx/452c629d67e41baec3ac6f04fe744b4b9617f8f859c63b3002f8684e7a4fee03
# ['ser']['ins'][0]['value'] incorrect, only used in sighashes so leave
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
                ]
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
                    'pk_script': bytes.fromhex('a91424d6008f143af0cca57344069c46661aa4fcea2387'),
                    'value': bytes.fromhex('3af9870200000000'),
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
                ]
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
# https://blockchain.info/rawtx/d2941b532f6d3d54d596345b50972b3995983239884037a52aab799ec84292ee
# https://blockchain.info/rawtx/1d204bc09e183741bf4c8fbe9034067d160e369e373ec9669ea51bfe6d0567df
P2WPKH = {
        'human': {
            'version': 1,
            'locktime': 0,
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
            'version': bytes.fromhex('00000000'),
            'locktime': bytes.fromhex('00000000'),
            'ins': [
                {
                    'id': 0,
                    'hash': bytes.fromhex('d2941b532f6d3d54d596345b50972b3995983239884037a52aab799ec84292ee'),
                    'index': bytes.fromhex('00000000'),
                    'value': bytes.fromhex(''),
                    'pk_script': bytes.fromhex('0014758ce550380d964051086798d6546bebdca27a73'),
                    'sequence': bytes.fromhex('fffffffd'),
                    'input': bytes.fromhex('ee9242c89e79ab2aa537408839329895392b97505b3496d5543d6d2f531b94d20000000000fdffffff')
                    }
                ],
            'outs': [
                {
                    'id': 0,
                    'value': bytes.fromhex(''),
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
            'tx': {
                'unsigned': bytes.fromhex('01000000000101ee9242c89e79ab2aa537408839329895392b97505b3496d5543d6d2f531b94d20000000000fdffffff0173d301000000000017a914bba5acbec4e6e3374a0345bf3609fa7cfea825f1870000000000'),
                'signed': bytes.fromhex('01000000000101ee9242c89e79ab2aa537408839329895392b97505b3496d5543d6d2f531b94d20000000000fdffffff0173d301000000000017a914bba5acbec4e6e3374a0345bf3609fa7cfea825f18702483045022100f746173f184f43e2855fd1b739879a137317ef905cc3b56fd1bcd34158a4721a022031163e6831efe77aa256ecfd65b9b1a9e46cafce8c2611be222194ee985dfd660121027450ee71e5a86f7466720a10811316f79a64e85d5671ee46332f8f7dae4f5d6700000000')
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
                ]
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
        'redeem_script': examples.msig_two_two.format(pk0=PK['human'][0]['pk'], pk1=PK['human'][1]['pk']),
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

# https://zcash.blockexplorer.com/api/rawtx/67b17e92db8c6480df9030177fd5b98120d0455fd86c3bcd27de2ee7db6cdd1a
ZCASH_SPROUT = {
    'human': {},
    'ser': {
        'version': bytes.fromhex('02000000'),
        'ins': [],
        'outs': [{
            'id': 0,
            'value': bytes.fromhex('e0142e0000000000'),
            'pk_script': bytes.fromhex('1976a9140a8ed3e5f90e20658d880ca74233abc5986e1fff88ac')
        }],
        'joinsplits': [{
            'vpub_old': bytes.fromhex('0000000000000000'),
            'vpub_new': bytes.fromhex('f03b2e0000000000'),
            'anchor': bytes.fromhex('9ee80d2801a507e09867d73400daadfcb301dbff28e58ea5008d434c57e71c5c'),
            'nullifiers': bytes.fromhex('10517e16d11c18b628e276dc29513bbeb8a6c904e598ea47dbad2c89efb82b78d3f3583e9c18bbca64700d35adb9af7d5c4867d2ddb00311a71b8d0a76be41ab'),
            'commitments': bytes.fromhex('ea4eb688104ff24f1e7e6015e86458c99c44048ba3a7e12ab86ebd3f59687cec32a6b0f37a850bf298d5b347bb72a71a88152d337800e92987a922176f94ba7f'),
            'ephemeral_key': bytes.fromhex('b0418dce0664330863a91f0a4e76b1401a592ff98e8948966df1e320743d0b55'),
            'random_seed': bytes.fromhex('abbd4590b748c7c544e1a92f2267fd9da8d6ba3dea55bb5e888d86b8be1cf4af'),
            'vmacs': bytes.fromhex('ea4565ddac68725e4154dcaad2d5a992140c08bf7304e81ada4ed2462ef8cb488166d9017409daf4256736959d4ccb59cf618bf90230a870cc3d2265816d8c7e'),
            'zkproof': {
                'pi_sub_a': bytes.fromhex('0305f166bac140c5dea09d126e32d51fce6191c5d842be02654b76aed5508bf693'),
                'pi_prime_sub_a': bytes.fromhex('0310fac4dccaab31efcb6d2cac2ec3a71f82a2af9505694984a66e1ecd27d7b116'),
                'pi_sub_b': bytes.fromhex('0b0275f336881dca40aa49e6ac620cc86e36e05c576e0be5c9d648dfb71027f24114e2f86e4238558feea25bf6b0ebfdcf0f8808e7a661c47d4aa873a532432ce8'),
                'pi_prime_sub_b': bytes.fromhex('02174e19a01ceae668c78612e4905e1a82cea499ceb639d428ccad63464313104e'),
                'pi_sub_c': bytes.fromhex('0201b3b623af03bd728c2b58f05031e87c9f8640373109d03bacca2dae76f4225a'),
                'pi_prime_sub_c': bytes.fromhex('0327fc5792817d5cf86539143e8e8d467b34c380f87bf87bf4939fd7c1bf84f934'),
                'pi_sub_k': bytes.fromhex('031c01f53baefa48fb5a23f2d5c8747ee098ed9746af0a6efeedddf8628a568d91'),
                'pi_sub_h': bytes.fromhex('02268cc9c62c4717e9c486092f5b4263e423fef666b760f4d1e2994bd7b57208cf')
            },
            'proof': bytes.fromhex('0305f166bac140c5dea09d126e32d51fce6191c5d842be02654b76aed5508bf6930310fac4dccaab31efcb6d2cac2ec3a71f82a2af9505694984a66e1ecd27d7b1160b0275f336881dca40aa49e6ac620cc86e36e05c576e0be5c9d648dfb71027f24114e2f86e4238558feea25bf6b0ebfdcf0f8808e7a661c47d4aa873a532432ce802174e19a01ceae668c78612e4905e1a82cea499ceb639d428ccad63464313104e0201b3b623af03bd728c2b58f05031e87c9f8640373109d03bacca2dae76f4225a0327fc5792817d5cf86539143e8e8d467b34c380f87bf87bf4939fd7c1bf84f934031c01f53baefa48fb5a23f2d5c8747ee098ed9746af0a6efeedddf8628a568d9102268cc9c62c4717e9c486092f5b4263e423fef666b760f4d1e2994bd7b57208cf'),
            'encoded_notes': bytes.fromhex('751d83351d74f9514a54cdfbe7fb93ed525c006537573b412cb9a080b8b8026acb77692e28fb5649dca76cfbef1c6e86f6074f83cf5509887a32c2e0242d89cf4cc8825e53520a073e1efb2d439514301accc5e3948e5597e59aeba9c7020898762e6ed3587f90177a057d2e1173c7034b4dce6a209979377469686c0d2d560aaa8236dbe699044181c33f49e4d43b40458684d8c4bd56a2fd89f017eeb63e04f99cf7c29275d0b6eccf229a21d8c89664bff5e2f797b799fd2cf6152960ad700ec85ea6c977cc60442ec76239521603eb6e3611347d48f894eb42cef5b1cb4a59feed7e7fcfabdb0e28b4f382b983e7d82d5cd36f28b1e0a4d986d4590aa3828c654b3b4732a526787bde2ea6b49cec12a81f5071bf872623ced77e78226884955fc8ae9551f8f37f23c45fba90ad1035d54cafa034e36e93772b8e2ceba6609f9d8c70644b570026933b4f177f7fd64b5ba835fc2fa13026485e8e9d72ae353cae97bd5f05187cf8c9326b5b72771a182f43e966620d74a932a0e7bc7bf02ac3d1882391a272bb33169404c8b1d50deb5105e55bec3ccd15a6bfcbd1f19c17ad337cff0ce55225018230420ab08018ea3781f07a79a71acfcf7742cebb20c24817d998025935517a60b092eb3a564a63c72dd68a4555eee0319d3c36229067b740eb42df4e6ec7465aef5d264d1c578785d3a2ee4b6e8f3f50c0ffd29b051e1f7f2895a098a3dba2319c0b6c3cf527e5dbf1f87c14201e58568fddecd86fbf3f6a23b23223e0db25a09e9e33d3d3b56ac4e167733021beeeb503329fee8d9e309ebcc4d5d903b6ba935b796c4a69455785d8971cdc8a81c017f54bdbea0599f85a99f9c30d427f3a4147c01bee75937905888c58867be2982cca4b3260e44daa753d2d56dcb3e5e77763048a16754dd1b11adf41d8549fd6f341005f83e323e13b54a087b7a025e6c5d6ce96c1e1d6343cff657abed3fb7f20f33f843adfcade21df5c686d23f8c14e81ef6a4830ba7c772ed491367a39531d04f9a2c7a969cc8fbaabbfccf854279f7bbbe2aac89252cc294ce86c4d88c6db81a5337bca4ec9484b0ce3276ed86911649430e2df697d1ee6f1ff33090c28d49d729a65393083d978dfe7ac85976a255f44a9b5199312b426a2eb682e59c1599ac837bd7ccb766884d2b35a49ac1a52a298920178941e0ae7d8d235467b2290f178811c2f76a91e5396768053176098c708f6253bb6c7d2aa93eace91d8ea7158e7a3f1e0dae49b737f628224b16403f7b9a37c1122e8c24e2eae0e2c315fbf8bb0a3fe7836de61aa0708a10f421e7aa068f2480ab37c0d5084f9c85d5c0963084ca78a7aa10f526db8486d7b7eccb8d34c60bf53763ac03a0033c8da9e78b4e7e91a42169abc551f52df351fa69555bcafb7cfde8a4c36cd9a5eb66215c1da2b10471f5bbca5a4547d3f608e1d38c455c582c4a1f0624ef5b302a75d75332c720d2144a86d174d9b8b78deeb93b205e2483de152845443275458b632a5d0641b2ba2119c0a35396f3f25c7b0141e5d7261fbce557bec9aec19dbebcfcbaf9012d7c45d027ff99909e0d3a6811701e63de1a939d6c163dc5f9a4d950cabeb070f642c8c162e00693f89051348c241e8cb0129e4bf4591522df667cd2910b3b8346382f3f6c0ef5e8e392d9cca8164e959a71ab55b6517ac')
        }],
        'lock_time': bytes.fromhex('00000000'),
        'joinsplit_pubkey': bytes.fromhex('abe1da14bd6ffb08c4015e1bd8d43d305605697c8d67aae2331144f9e98b6634'),
        'joinsplit_sig': bytes.fromhex('ab3f349909c98d946b13450e1fa49d6877895545c8ef9b13454411067b16ff94a900c288361372f03bf03447ebe7ce098498bfcb41940b4a01b6449290738406'),
        'joinsplit_0': bytes.fromhex('0000000000000000f03b2e00000000009ee80d2801a507e09867d73400daadfcb301dbff28e58ea5008d434c57e71c5c10517e16d11c18b628e276dc29513bbeb8a6c904e598ea47dbad2c89efb82b78d3f3583e9c18bbca64700d35adb9af7d5c4867d2ddb00311a71b8d0a76be41abea4eb688104ff24f1e7e6015e86458c99c44048ba3a7e12ab86ebd3f59687cec32a6b0f37a850bf298d5b347bb72a71a88152d337800e92987a922176f94ba7fb0418dce0664330863a91f0a4e76b1401a592ff98e8948966df1e320743d0b55abbd4590b748c7c544e1a92f2267fd9da8d6ba3dea55bb5e888d86b8be1cf4afea4565ddac68725e4154dcaad2d5a992140c08bf7304e81ada4ed2462ef8cb488166d9017409daf4256736959d4ccb59cf618bf90230a870cc3d2265816d8c7e0305f166bac140c5dea09d126e32d51fce6191c5d842be02654b76aed5508bf6930310fac4dccaab31efcb6d2cac2ec3a71f82a2af9505694984a66e1ecd27d7b1160b0275f336881dca40aa49e6ac620cc86e36e05c576e0be5c9d648dfb71027f24114e2f86e4238558feea25bf6b0ebfdcf0f8808e7a661c47d4aa873a532432ce802174e19a01ceae668c78612e4905e1a82cea499ceb639d428ccad63464313104e0201b3b623af03bd728c2b58f05031e87c9f8640373109d03bacca2dae76f4225a0327fc5792817d5cf86539143e8e8d467b34c380f87bf87bf4939fd7c1bf84f934031c01f53baefa48fb5a23f2d5c8747ee098ed9746af0a6efeedddf8628a568d9102268cc9c62c4717e9c486092f5b4263e423fef666b760f4d1e2994bd7b57208cf751d83351d74f9514a54cdfbe7fb93ed525c006537573b412cb9a080b8b8026acb77692e28fb5649dca76cfbef1c6e86f6074f83cf5509887a32c2e0242d89cf4cc8825e53520a073e1efb2d439514301accc5e3948e5597e59aeba9c7020898762e6ed3587f90177a057d2e1173c7034b4dce6a209979377469686c0d2d560aaa8236dbe699044181c33f49e4d43b40458684d8c4bd56a2fd89f017eeb63e04f99cf7c29275d0b6eccf229a21d8c89664bff5e2f797b799fd2cf6152960ad700ec85ea6c977cc60442ec76239521603eb6e3611347d48f894eb42cef5b1cb4a59feed7e7fcfabdb0e28b4f382b983e7d82d5cd36f28b1e0a4d986d4590aa3828c654b3b4732a526787bde2ea6b49cec12a81f5071bf872623ced77e78226884955fc8ae9551f8f37f23c45fba90ad1035d54cafa034e36e93772b8e2ceba6609f9d8c70644b570026933b4f177f7fd64b5ba835fc2fa13026485e8e9d72ae353cae97bd5f05187cf8c9326b5b72771a182f43e966620d74a932a0e7bc7bf02ac3d1882391a272bb33169404c8b1d50deb5105e55bec3ccd15a6bfcbd1f19c17ad337cff0ce55225018230420ab08018ea3781f07a79a71acfcf7742cebb20c24817d998025935517a60b092eb3a564a63c72dd68a4555eee0319d3c36229067b740eb42df4e6ec7465aef5d264d1c578785d3a2ee4b6e8f3f50c0ffd29b051e1f7f2895a098a3dba2319c0b6c3cf527e5dbf1f87c14201e58568fddecd86fbf3f6a23b23223e0db25a09e9e33d3d3b56ac4e167733021beeeb503329fee8d9e309ebcc4d5d903b6ba935b796c4a69455785d8971cdc8a81c017f54bdbea0599f85a99f9c30d427f3a4147c01bee75937905888c58867be2982cca4b3260e44daa753d2d56dcb3e5e77763048a16754dd1b11adf41d8549fd6f341005f83e323e13b54a087b7a025e6c5d6ce96c1e1d6343cff657abed3fb7f20f33f843adfcade21df5c686d23f8c14e81ef6a4830ba7c772ed491367a39531d04f9a2c7a969cc8fbaabbfccf854279f7bbbe2aac89252cc294ce86c4d88c6db81a5337bca4ec9484b0ce3276ed86911649430e2df697d1ee6f1ff33090c28d49d729a65393083d978dfe7ac85976a255f44a9b5199312b426a2eb682e59c1599ac837bd7ccb766884d2b35a49ac1a52a298920178941e0ae7d8d235467b2290f178811c2f76a91e5396768053176098c708f6253bb6c7d2aa93eace91d8ea7158e7a3f1e0dae49b737f628224b16403f7b9a37c1122e8c24e2eae0e2c315fbf8bb0a3fe7836de61aa0708a10f421e7aa068f2480ab37c0d5084f9c85d5c0963084ca78a7aa10f526db8486d7b7eccb8d34c60bf53763ac03a0033c8da9e78b4e7e91a42169abc551f52df351fa69555bcafb7cfde8a4c36cd9a5eb66215c1da2b10471f5bbca5a4547d3f608e1d38c455c582c4a1f0624ef5b302a75d75332c720d2144a86d174d9b8b78deeb93b205e2483de152845443275458b632a5d0641b2ba2119c0a35396f3f25c7b0141e5d7261fbce557bec9aec19dbebcfcbaf9012d7c45d027ff99909e0d3a6811701e63de1a939d6c163dc5f9a4d950cabeb070f642c8c162e00693f89051348c241e8cb0129e4bf4591522df667cd2910b3b8346382f3f6c0ef5e8e392d9cca8164e959a71ab55b6517ac'),
        'tx_out_0': bytes.fromhex('e0142e00000000001976a9140a8ed3e5f90e20658d880ca74233abc5986e1fff88ac'),
        'tx': bytes.fromhex('020000000001e0142e00000000001976a9140a8ed3e5f90e20658d880ca74233abc5986e1fff88ac00000000010000000000000000f03b2e00000000009ee80d2801a507e09867d73400daadfcb301dbff28e58ea5008d434c57e71c5c10517e16d11c18b628e276dc29513bbeb8a6c904e598ea47dbad2c89efb82b78d3f3583e9c18bbca64700d35adb9af7d5c4867d2ddb00311a71b8d0a76be41abea4eb688104ff24f1e7e6015e86458c99c44048ba3a7e12ab86ebd3f59687cec32a6b0f37a850bf298d5b347bb72a71a88152d337800e92987a922176f94ba7fb0418dce0664330863a91f0a4e76b1401a592ff98e8948966df1e320743d0b55abbd4590b748c7c544e1a92f2267fd9da8d6ba3dea55bb5e888d86b8be1cf4afea4565ddac68725e4154dcaad2d5a992140c08bf7304e81ada4ed2462ef8cb488166d9017409daf4256736959d4ccb59cf618bf90230a870cc3d2265816d8c7e0305f166bac140c5dea09d126e32d51fce6191c5d842be02654b76aed5508bf6930310fac4dccaab31efcb6d2cac2ec3a71f82a2af9505694984a66e1ecd27d7b1160b0275f336881dca40aa49e6ac620cc86e36e05c576e0be5c9d648dfb71027f24114e2f86e4238558feea25bf6b0ebfdcf0f8808e7a661c47d4aa873a532432ce802174e19a01ceae668c78612e4905e1a82cea499ceb639d428ccad63464313104e0201b3b623af03bd728c2b58f05031e87c9f8640373109d03bacca2dae76f4225a0327fc5792817d5cf86539143e8e8d467b34c380f87bf87bf4939fd7c1bf84f934031c01f53baefa48fb5a23f2d5c8747ee098ed9746af0a6efeedddf8628a568d9102268cc9c62c4717e9c486092f5b4263e423fef666b760f4d1e2994bd7b57208cf751d83351d74f9514a54cdfbe7fb93ed525c006537573b412cb9a080b8b8026acb77692e28fb5649dca76cfbef1c6e86f6074f83cf5509887a32c2e0242d89cf4cc8825e53520a073e1efb2d439514301accc5e3948e5597e59aeba9c7020898762e6ed3587f90177a057d2e1173c7034b4dce6a209979377469686c0d2d560aaa8236dbe699044181c33f49e4d43b40458684d8c4bd56a2fd89f017eeb63e04f99cf7c29275d0b6eccf229a21d8c89664bff5e2f797b799fd2cf6152960ad700ec85ea6c977cc60442ec76239521603eb6e3611347d48f894eb42cef5b1cb4a59feed7e7fcfabdb0e28b4f382b983e7d82d5cd36f28b1e0a4d986d4590aa3828c654b3b4732a526787bde2ea6b49cec12a81f5071bf872623ced77e78226884955fc8ae9551f8f37f23c45fba90ad1035d54cafa034e36e93772b8e2ceba6609f9d8c70644b570026933b4f177f7fd64b5ba835fc2fa13026485e8e9d72ae353cae97bd5f05187cf8c9326b5b72771a182f43e966620d74a932a0e7bc7bf02ac3d1882391a272bb33169404c8b1d50deb5105e55bec3ccd15a6bfcbd1f19c17ad337cff0ce55225018230420ab08018ea3781f07a79a71acfcf7742cebb20c24817d998025935517a60b092eb3a564a63c72dd68a4555eee0319d3c36229067b740eb42df4e6ec7465aef5d264d1c578785d3a2ee4b6e8f3f50c0ffd29b051e1f7f2895a098a3dba2319c0b6c3cf527e5dbf1f87c14201e58568fddecd86fbf3f6a23b23223e0db25a09e9e33d3d3b56ac4e167733021beeeb503329fee8d9e309ebcc4d5d903b6ba935b796c4a69455785d8971cdc8a81c017f54bdbea0599f85a99f9c30d427f3a4147c01bee75937905888c58867be2982cca4b3260e44daa753d2d56dcb3e5e77763048a16754dd1b11adf41d8549fd6f341005f83e323e13b54a087b7a025e6c5d6ce96c1e1d6343cff657abed3fb7f20f33f843adfcade21df5c686d23f8c14e81ef6a4830ba7c772ed491367a39531d04f9a2c7a969cc8fbaabbfccf854279f7bbbe2aac89252cc294ce86c4d88c6db81a5337bca4ec9484b0ce3276ed86911649430e2df697d1ee6f1ff33090c28d49d729a65393083d978dfe7ac85976a255f44a9b5199312b426a2eb682e59c1599ac837bd7ccb766884d2b35a49ac1a52a298920178941e0ae7d8d235467b2290f178811c2f76a91e5396768053176098c708f6253bb6c7d2aa93eace91d8ea7158e7a3f1e0dae49b737f628224b16403f7b9a37c1122e8c24e2eae0e2c315fbf8bb0a3fe7836de61aa0708a10f421e7aa068f2480ab37c0d5084f9c85d5c0963084ca78a7aa10f526db8486d7b7eccb8d34c60bf53763ac03a0033c8da9e78b4e7e91a42169abc551f52df351fa69555bcafb7cfde8a4c36cd9a5eb66215c1da2b10471f5bbca5a4547d3f608e1d38c455c582c4a1f0624ef5b302a75d75332c720d2144a86d174d9b8b78deeb93b205e2483de152845443275458b632a5d0641b2ba2119c0a35396f3f25c7b0141e5d7261fbce557bec9aec19dbebcfcbaf9012d7c45d027ff99909e0d3a6811701e63de1a939d6c163dc5f9a4d950cabeb070f642c8c162e00693f89051348c241e8cb0129e4bf4591522df667cd2910b3b8346382f3f6c0ef5e8e392d9cca8164e959a71ab55b6517acabe1da14bd6ffb08c4015e1bd8d43d305605697c8d67aae2331144f9e98b6634ab3f349909c98d946b13450e1fa49d6877895545c8ef9b13454411067b16ff94a900c288361372f03bf03447ebe7ce098498bfcb41940b4a01b6449290738406')
    }
}
# https://zcash.blockexplorer.com/api/rawtx/92423ae0b69c1f2dd911671264933e576ac1c205467145544e5cc650184e32a3
ZCASH_OVERWINTER_NO_JS = {
    'human': {},
    'ser': {
        'tx': bytes.fromhex('030000807082c403010000000000000000000000000000000000000000000000000000000000000000ffffffff050306760500ffffffff0200ca9a3b000000001976a914361683f47d7dfc6a8d17f8f7b9413ff1a27ec62988ac80b2e60e0000000017a914ee16b664f7bca502cad662e5e36bad071423951987000000000000000000')
    }
}
