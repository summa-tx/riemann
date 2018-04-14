from ..encoding import base58, bech32


class Network:
    '''basic Network class, holding space for the various prefixes.
    Not all prefixes are used by all coins.'''
    SYMBOL = None
    NETWORK_NAME = None
    SUBNET_NAME = None
    P2PKH_PREFIX = None
    P2SH_PREFIX = None
    SEGWIT = False
    P2WSH_PREFIX = None
    P2WPKH_PREFIX = None
    BECH32_HRP = None
    WITNESS_SCRIPT_VERSION = '\x00'
    SEGWIT_ENCODER = bech32
    LEGACY_ENCODER = base58
    SEGWIT_TX_FLAG = b'\x00\x01'


class BitcoinMain(Network):
    SYMBOL = 'BTC'
    NETWORK_NAME = 'bitcoin'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x00'
    P2SH_PREFIX = b'\x05'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'bc'


class BitcoinTest(Network):
    SYMBOL = 'tBTC'
    NETWORK_NAME = 'bitcoin'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    BECH32_HRP = 'tb'
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'


class BitcoinRegtest(Network):
    SYMBOL = 'rBTC'
    NETWORK_NAME = 'bitcoin'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'bcrt'


class LitecoinMain(Network):
    SYMBOL = 'LTC'
    NETWORK_NAME = 'litecoin'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x30'
    P2SH_PREFIX = b'\x32'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'ltc'


class LitecoinTest(Network):
    SYMBOL = 'tLTC'
    NETWORK_NAME = 'litecoin'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\x3a'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'tltc'


class LitecoinRegtest(Network):
    SYMBOL = 'rLTC'
    NETWORK_NAME = 'litecoin'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\x3a'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'tltc'  # no specific reg bech32 hrp specifed


class BitcoinCashMain(Network):
    SYMBOL = 'BCH'
    NETWORK_NAME = 'bitcoin_cash'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x00'
    P2SH_PREFIX = b'\x05'
    SEGWIT = False


class BitcoinCashTest(Network):
    SYMBOL = 'tBCH'
    NETWORK_NAME = 'bitcoin_cash'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = False


class BitcoinCashRegtest(Network):
    SYMBOL = 'rBCH'
    NETWORK_NAME = 'bitcoin_cash'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = False


class BitcoinGoldMain(Network):
    SYMBOL = 'BTG'
    NETWORK_NAME = 'bitcoin_gold'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x26'
    P2SH_PREFIX = b'\x17'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'btg'


class BitcoinGoldTest(Network):
    SYMBOL = 'tBTG'
    NETWORK_NAME = 'bitcoin_gold'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'tbtg'


class BitcoinGoldRegtest(Network):
    SYMBOL = 'rBTG'
    NETWORK_NAME = 'bitcoin_gold'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'tbtg'  # no specific reg bech32 hrp specifed


class DogecoinMain(Network):
    SYMBOL = 'DOGE'
    NETWORK_NAME = 'dogecoin'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x1e'
    P2SH_PREFIX = b'\x16'
    SEGWIT = False  # as of 4/2018, at least; dogewit is a-comin', they say


class DogecoinTest(Network):
    SYMBOL = 'tDOGE'
    NETWORK_NAME = 'dogecoin'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x71'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = False


class DogecoinRegtest(Network):
    ''' I can detect no sign of a Doge reg network;
    for most coins, the reg values are the same as test'''
    SYMBOL = 'rDOGE'
    NETWORK_NAME = 'dogecoin'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x71'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = False


class DashMain(Network):
    SYMBOL = 'DASH'
    NETWORK_NAME = 'dash'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x4c'
    P2SH_PREFIX = b'\x10'
    SEGWIT = False


class DashTest(Network):
    SYMBOL = 'tDASH'
    NETWORK_NAME = 'dash'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x8c'
    P2SH_PREFIX = b'\x13'
    SEGWIT = False


class DashRegtest(Network):
    SYMBOL = 'rDASH'
    NETWORK_NAME = 'dash'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x8c'
    P2SH_PREFIX = b'\x13'
    SEGWIT = False


class ZcashMain(Network):
    SYMBOL = 'ZEC'
    NETWORK_NAME = 'zcash'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x1c\xb8'
    P2SH_PREFIX = b'\x1c\xbd'
    SEGWIT = False


class ZcashTest(Network):
    SYMBOL = 'tZEC'
    NETWORK_NAME = 'zcash'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x1d\x25'
    P2SH_PREFIX = b'\x1c\xba'
    SEGWIT = False


class ZcashRegtest(Network):
    SYMBOL = 'rZEC'
    NETWORK_NAME = 'zcash'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x1d\x25'
    P2SH_PREFIX = b'\x1c\xba'
    SEGWIT = False


class DecredMain(Network):
    SYMBOL = 'DCR'
    NETWORK_NAME = 'decred'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x13\x86'
    P2SH_PREFIX = b'\x07\x1a'
    SEGWIT = False


class DecredTest(Network):
    SYMBOL = 'DCRT'
    NETWORK_NAME = 'decred'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x28\xf7'
    P2SH_PREFIX = b'\x0e\xfc'
    SEGWIT = False


class DecredSimnet(Network):
    SYMBOL = 'DCRS'
    NETWORK_NAME = 'decred'
    SUBNET_NAME = 'simnet'
    P2PKH_PREFIX = b'\x28\xf7'
    P2SH_PREFIX = b'\x0e\xfc'
    SEGWIT = False


class PivxMain(Network):
    SYMBOL = 'PIVX'
    NETWORK_NAME = 'pivx'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x1e'
    P2SH_PREFIX = b'\x0d'
    SEGWIT = False


class PivxTest(Network):
    SYMBOL = 'tPIVX'
    NETWORK_NAME = 'pivx'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x8b'
    P2SH_PREFIX = b'\x13'
    SEGWIT = False


class PivxRegtest(Network):
    SYMBOL = 'rPIVX'
    NETWORK_NAME = 'pivx'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x8b'
    P2SH_PREFIX = b'\x13'
    SEGWIT = False


class ViacoinMain(Network):
    SYMBOL = 'VIA'
    NETWORK_NAME = 'viacoin'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x47'
    P2SH_PREFIX = b'\x21'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'via'


class ViacoinTest(Network):
    SYMBOL = 'tVIA'
    NETWORK_NAME = 'viacoin'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x7f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'tvia'


class ViacoinSimnet(Network):
    SYMBOL = 'sVIA'
    NETWORK_NAME = 'viacoin'
    SUBNET_NAME = 'simnet'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'svia'


class FeathercoinMain(Network):
    SYMBOL = 'FTC'
    NETWORK_NAME = 'feathercoin'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x0e'
    P2SH_PREFIX = b'\x60'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'fc'


class FeathercoinTest(Network):
    SYMBOL = 'tFTC'
    NETWORK_NAME = 'feathercoin'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'tf'


class FeathercoinRegtest(Network):
    SYMBOL = 'rFTC'
    NETWORK_NAME = 'feathercoin'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'fcrt'


class BitcoinDarkMain(Network):
    SYMBOL = 'BTCD'
    NETWORK_NAME = 'bitcoin_dark'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x3c'
    P2SH_PREFIX = b'\x55'
    SEGWIT = False


class BitcoinDarkTest(Network):
    SYMBOL = 'tBTCD'
    NETWORK_NAME = 'bitcoin_dark'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = False


class BitcoinDarkRegtest(Network):
    # like DOGE, I can find no BTCD regnet. Also the code is really old.
    SYMBOL = 'rBTCD'
    NETWORK_NAME = 'bitcoin_dark'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = False


class AxeMain(Network):
    SYMBOL = 'AXE'
    NETWORK_NAME = 'axe'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x37'
    P2SH_PREFIX = b'\x10'
    SEGWIT = False


class AxeTest(Network):
    SYMBOL = 'tAXE'
    NETWORK_NAME = 'axe'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x8c'
    P2SH_PREFIX = b'\x13'
    SEGWIT = False


class AxeRegtest(Network):
    SYMBOL = 'rAXE'
    NETWORK_NAME = 'axe'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x8c'
    P2SH_PREFIX = b'\x13'
    SEGWIT = False


class BitcoreMain(Network):
    SYMBOL = 'BTX'
    NETWORK_NAME = 'bitcore'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x00'
    P2SH_PREFIX = b'\x32'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'


class BitcoreTest(Network):
    SYMBOL = 'tBTX'
    NETWORK_NAME = 'bitcore'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\x3a'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'


class BitcoreRegtest(Network):
    SYMBOL = 'rBTX'
    NETWORK_NAME = 'bitcore'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\x3a'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'


class DigibyteMain(Network):
    SYMBOL = 'DGB'
    NETWORK_NAME = 'digibyte'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x1e'
    P2SH_PREFIX = b'\x3f'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'dgb'


class DigibyteTest(Network):
    SYMBOL = 'tDGB'
    NETWORK_NAME = 'digibyte'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x7e'
    P2SH_PREFIX = b'\x8c'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'dgbt'


class DigibyteRegtest(Network):
    SYMBOL = 'rDGB'
    NETWORK_NAME = 'digibyte'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x7e'
    P2SH_PREFIX = b'\x8c'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'dgbrt'


class GroestlcoinMain(Network):
    SYMBOL = 'GRS'
    NETWORK_NAME = 'groestlcoin'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x24'
    P2SH_PREFIX = b'\x05'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'grs'
    # some wallets have bech32 addresses w/prefix 'grs',
    # but bech32 is not active in groestl at this time.
    # no value for testnet/regnet exists


class GroestlcoinTest(Network):
    SYMBOL = 'tGRS'
    NETWORK_NAME = 'groestl'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'


class GroestlcoinRegtest(Network):
    SYMBOL = 'rGRS'
    NETWORK_NAME = 'groestl'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'


class MonacoinMain(Network):
    SYMBOL = 'MONA'
    NETWORK_NAME = 'monacoin'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x32'
    P2SH_PREFIX = b'\x37'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    # BECH32_HRP = 'mona'
    # bech32 isn't active yet but the team has chosen hrps.


class MonacoinTest(Network):
    SYMBOL = 'tMONA'
    NETWORK_NAME = 'monacoin'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    # BECH32_HRP = 'tmona'


class MonacoinRegtest(Network):
    SYMBOL = 'rMONA'
    NETWORK_NAME = 'digibyte'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    # BECH32_HRP = 'tmona'


class NavcoinMain(Network):
    SYMBOL = 'NAV'
    NETWORK_NAME = 'navcoin'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x35'
    P2SH_PREFIX = b'\x55'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    # bech32 is not yet active on Navcoin


class NavcoinTest(Network):
    SYMBOL = 'tNAV'
    NETWORK_NAME = 'navcoin'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x36'
    P2SH_PREFIX = b'\x56'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'


class NavcoinRegtest(Network):
    SYMBOL = 'rNAV'
    NETWORK_NAME = 'navcoin'
    SUBNET_NAME = 'reg'
    # one of the only coins with different prefixes for reg and test
    P2PKH_PREFIX = b'\x14'
    P2SH_PREFIX = b'\x60'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'


class SyscoinMain(Network):
    SYMBOL = 'SYS'
    NETWORK_NAME = 'syscoin'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x3f'
    P2SH_PREFIX = b'\x05'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'


class SyscoinTest(Network):
    SYMBOL = 'tSYS'
    NETWORK_NAME = 'syscoin'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x41'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'


class SyscoinRegtest(Network):
    SYMBOL = 'rSYS'
    NETWORK_NAME = 'syscoin'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x41'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'


class VertcoinMain(Network):
    SYMBOL = 'VTC'
    NETWORK_NAME = 'vertcoin'
    SUBNET_NAME = 'main'
    P2PKH_PREFIX = b'\x47'
    P2SH_PREFIX = b'\x05'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'vtc'


class VertcoinTest(Network):
    SYMBOL = 'tVTC'
    NETWORK_NAME = 'vertcoin'
    SUBNET_NAME = 'test'
    P2PKH_PREFIX = b'\x4a'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'tvtc'


class VertcoinRegtest(Network):
    SYMBOL = 'rVTC'
    NETWORK_NAME = 'vertcoin'
    SUBNET_NAME = 'reg'
    P2PKH_PREFIX = b'\x6f'
    P2SH_PREFIX = b'\xc4'
    SEGWIT = True
    P2WSH_PREFIX = b'\x00\x20'
    P2WPKH_PREFIX = b'\x00\x14'
    BECH32_HRP = 'bcrt'  # That's the same as Bitcoin's reg.

# Well kids, that's a bundle.
