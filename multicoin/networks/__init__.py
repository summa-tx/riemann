# To add a new coin
# 1. define a class
# 2. add it to get_network
# 3. add it to SUPPORTED

SUPPORTED = [
    'bitcoin_main',
    'bitcoin_test',
    'litecoin_main',
    'litecoin_test',
    'bitcoin_cash_main',
    'bitcoin_gold_main',
    'bitcoin_gold_test',
    'dogecoin_main',
    'dogecoin_test',
    'dash_main',
    'dash_test',
    'zcash_main',
    'decred_main',
    'decred_test',
    'pivx_main',
    'pivx_test',
    'viacoin_main',
    'viacoin_test',
    'feathercoin_main',
    'feathercoin_test',
    'unobtanium_main',
    'faircoin_main',
    'bitcoin_dark_main'
    # TODO add more()
]


def get_network(name):
    if name not in SUPPORTED:
        raise ValueError('Unknown chain specifed: {}'.format(name))
    if name == 'bitcoin_main':
        return BitcoinMain
    if name == 'bitcoin_test':
        return BitcoinTest
    if name == 'litecoin_main':
        return LitecoinMain
    if name == 'litecoin_test':
        return LitecoinTest
    if name == 'bitcoin_cash_main':
        return BitcoinCashMain
    if name == 'bitcoin_gold_main':
        return BitcoinGoldMain
    if name == 'bitcoin_gold_test':
        return BitcoinGoldTest
    if name == 'dogecoin_main':
        return DogecoinMain
    if name == 'dogecoin_test':
        return DogecoinTest
    if name == 'dash_main':
        return DashMain
    if name == 'dash_test':
        return DashTest
    if name == 'zcash_main':
        return ZcashMain
    if name == 'decred_main':
        return DecredMain
    if name == 'decred_test':
        return DecredTest
    if name == 'pivx_main':
        return PivxMain
    if name == 'pivx_test':
        return PivxTest
    if name == 'viacoin_main':
        return ViacoinMain
    if name == 'viacoin_test':
        return ViacoinTest
    if name == 'feathercoin_main':
        return FeathercoinMain
    if name == 'feathercoin_test':
        return FeathercoinTest
    if name == 'unobtanium_main':
        return UnobtaniumMain
    if name == 'faircoin_main':
        return FaircoinMain
    if name == 'bitcoin_dark_main':
        return BitcoinDarkMain
    # TODO add more


class Network:
    SYMBOL = None
    NETWORK_NAME = None
    SUBNET_NAME = None
    P2PKH = None
    P2SH = None
    SEGWIT = None


class BitcoinMain(Network):
    SYMBOL = 'BTC'
    NETWORK_NAME = 'bitcoin'
    SUBNET_NAME = 'mainnet'
    P2PKH = b'\x00'
    P2SH = b'\x05'
    SEGWIT = True


class BitcoinTest(Network):
    SYMBOL = 'tBTC'
    NETWORK_NAME = 'bitcoin'
    SUBNET_NAME = 'testnet'
    P2PKH = b'o'  # 0x6f
    P2SH = b'\xc4'
    SEGWIT = True


class LitecoinMain(Network):
    SYMBOL = 'LTC'
    NETWORK_NAME = 'litecoin'
    SUBNET_NAME = 'mainnet'
    P2PKH = b'0'
    P2SH = b'\x05'
    SEGWIT = True


class LitecoinTest(Network):
    SYMBOL = 'tLTC'
    NETWORK_NAME = 'litecoin'
    SUBNET_NAME = 'testnet'
    P2PKH = b'o'
    P2SH = b'\xc4'
    SEGWIT = True


class BitcoinCashMain(Network):
    SYMBOL = 'BCH'
    NETWORK_NAME = 'bitcoin_cash'
    SUBNET_NAME = 'mainnet'
    P2PKH = b'\x00'
    P2SH = b'\x05'
    SEGWIT = False


class BitcoinGoldMain(Network):
    SYMBOL = 'BTG'
    NETWORK_NAME = 'bitcoin_gold'
    SUBNET_NAME = 'mainnet'
    P2PKH = b'&'
    P2SH = b'\x17'
    SEGWIT = True


class BitcoinGoldTest(Network):
    SYMBOL = 'tBTG'
    NETWORK_NAME = 'bitcoin_gold'
    SUBNET_NAME = 'testnet'
    P2PKH = b'o'
    P2SH = b'\xc4'
    SEGWIT = True


class DogecoinMain(Network):
    SYMBOL = 'DOGE'
    NETWORK_NAME = 'dogecoin'
    SUBNET_NAME = 'mainnet'
    P2PKH = b'\x1e'
    P2SH = b'\x16'
    SEGWIT = False  # as of 4/2018, at least; dogewit is a-comin', they say


class DogecoinTest(Network):
    SYMBOL = 'tDOGE'
    NETWORK_NAME = 'dogecoin'
    SUBNET_NAME = 'testnet'
    P2PKH = b'q'
    P2SH = b'\xc4'
    SEGWIT = False


class DashMain(Network):
    SYMBOL = 'DASH'
    NETWORK_NAME = 'dash'
    SUBNET_NAME = 'mainnet'
    P2PKH = b'L'
    P2SH = b'\x10'
    SEGWIT = False


class DashTest(Network):
    SYMBOL = 'tDASH'
    NETWORK_NAME = 'dash'
    SUBNET_NAME = 'testnet'
    P2PKH = b'\x8c'
    P2SH = b'\x13'
    SEGWIT = False


class ZcashMain(Network):
    SYMBOL = 'ZEC'
    NETWORK_NAME = 'zcash'
    SUBNET_NAME = 'mainnet'
    P2PKH = b'\x1c\xb8'
    P2SH = b'\x1c\xbd'
    SEGWIT = False


class DecredMain(Network):
    SYMBOL = 'DCR'
    NETWORK_NAME = 'decred'
    SUBNET_NAME = 'mainnet'
    P2PKH = b'\x07?'
    P2SH = b'\x07\x1a'
    SEGWIT = False


class DecredTest(Network):
    SYMBOL = 'tDCR'
    NETWORK_NAME = 'decred'
    SUBNET_NAME = 'testnet'
    P2PKH = b'\x0f!'
    P2SH = b'\x0el'
    SEGWIT = False


class PivxMain(Network):
    SYMBOL = 'PIVX'
    NETWORK_NAME = 'pivx'
    SUBNET_NAME = 'mainnet'
    P2PKH = b'\x1e'
    P2SH = b'\x00d'
    SEGWIT = False


class PivxTest(Network):
    SYMBOL = 'tPIVX'
    NETWORK_NAME = 'pivx'
    SUBNET_NAME = 'testnet'
    P2PKH = b'\x8b'
    P2SH = b'\x13'
    SEGWIT = False


# from here down, are those coins in top 100 ~coins~ on coinmarketcap
# rather than the true front page, which is top 100 coins and tokens
class ViacoinMain(Network):
    SYMBOL = 'VIA'
    NETWORK_NAME = 'viacoin'
    SUBNET_NAME = 'mainnet'
    P2PKH = b'G'
    P2SH = b'!'
    SEGWIT = True


class ViacoinTest(Network):
    SYMBOL = 'tVIA'
    NETWORK_NAME = 'viacoin'
    SUBNET_NAME = 'testnet'
    P2PKH = b'\x7f'
    P2SH = b'\xc4'
    SEGWIT = True


class FeathercoinMain(Network):
    SYMBOL = 'FTC'
    NETWORK_NAME = 'feathercoin'
    SUBNET_NAME = 'mainnet'
    P2PKH = b'\x0e'
    P2SH = b'`'
    SEGWIT = True


class FeathercoinTest(Network):
    SYMBOL = 'tFTC'
    NETWORK_NAME = 'feathercoin'
    SUBNET_NAME = 'testnet'
    P2PKH = b'A'
    P2SH = b'\xc4'
    SEGWIT = True


class UnobtaniumMain(Network):
    SYMBOL = 'UNO'  # or else draw two!
    NETWORK_NAME = 'unobtanium'  # still can't with that spelling
    SUBNET_NAME = 'testnet'
    P2PKH = b'\x82'
    P2SH = b'\x1e'
    SEGWIT = True


class FaircoinMain(Network):
    SYMBOL = 'FAI'
    NETWORK_NAME = 'faircoin'
    SUBNET_NAME = 'mainnet'
    P2PKH = b'_'  # ('_')b it approves!
    P2SH = b'$'
    SEGWIT = False  # no information exists


class BitcoinDarkMain(Network):
    SYMBOL = 'BTCD'
    NETWORK_NAME = 'bitcoin_dark'
    SUBNET_NAME = 'mainnet'
    P2PKH = b'<'
    P2SH = b'-'
    SEGWIT = False

# TODO add more
