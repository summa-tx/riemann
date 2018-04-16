# To add a new coin
# 1. define a class in networks.py
# 2. add it to SUPPORTED

from .networks import *  # noqa: F403


SUPPORTED = {
    'bitcoin_main': BitcoinMain,  # noqa: F405
    'bitcoin_test': BitcoinTest,  # noqa: F405
    'bitcoin_reg': BitcoinRegtest,  # noqa: F405
    'litecoin_main': LitecoinMain,  # noqa: F405
    'litecoin_test': LitecoinTest,  # noqa: F405
    'litecoin_reg': LitecoinRegtest,  # noqa: F405
    'bitcoin_cash_main': BitcoinCashMain,  # noqa: F405
    'bitcoin_cash_test': BitcoinCashTest,  # noqa: F405
    'bitcoin_cash_reg': BitcoinCashRegtest,  # noqa: F405
    'bitcoin_gold_main': BitcoinGoldMain,  # noqa: F405
    'bitcoin_gold_test': BitcoinGoldTest,  # noqa: F405
    'bitcoin_gold_reg': BitcoinGoldRegtest,  # noqa: F405
    'dogecoin_main': DogecoinMain,  # noqa: F405
    'dogecoin_test': DogecoinTest,  # noqa: F405
    'dogecoin_reg': DogecoinRegtest,  # noqa: F405
    'dash_main': DashMain,  # noqa: F405
    'dash_test': DashTest,  # noqa: F405
    'dash_reg': DashRegtest,  # noqa: F405
    'zcash_main': ZcashMain,  # noqa: F405
    'zcash_test': ZcashTest,  # noqa: F405
    'zcash_reg': ZcashRegtest,  # noqa: F405
    'decred_main': DecredMain,  # noqa: F405
    'decred_test': DecredTest,  # noqa: F405
    'decred_simnet': DecredSimnet,  # noqa: F405
    'pivx_main': PivxMain,  # noqa: F405
    'pivx_test': PivxTest,  # noqa: F405
    'pivx_reg': PivxRegtest,  # noqa: F405
    'viacoin_main': ViacoinMain,  # noqa: F405
    'viacoin_test': ViacoinTest,  # noqa: F405
    'viacoin_simnet': ViacoinSimnet,  # noqa: F405
    'feathercoin_main': FeathercoinMain,  # noqa: F405
    'feathercoin_test': FeathercoinTest,  # noqa: F405
    'feathercoin_reg': FeathercoinRegtest,  # noqa: F405
    'bitcoin_dark_main': BitcoinDarkMain,  # noqa: F405
    'bitcoin_dark_test': BitcoinDarkTest,  # noqa: F405
    'bitcoin_dark_reg': BitcoinDarkRegtest,  # noqa: F405
    'axe_main': AxeMain,  # noqa: F405
    'axe_test': AxeTest,  # noqa: F405
    'axe_reg': AxeRegtest,  # noqa: F405
    'bitcore_main': BitcoreMain,  # noqa: F405
    'bitcore_test': BitcoreTest,  # noqa: F405
    'bitcore_reg': BitcoreRegtest,  # noqa: F405
    'digibyte_main': DigibyteMain,  # noqa: F405
    'digibyte_test': DigibyteTest,  # noqa: F405
    'digibyte_reg': DigibyteRegtest,  # noqa: F405
    'groestlcoin_main': GroestlcoinMain,  # noqa: F405
    'groestlcoin_test': GroestlcoinTest,  # noqa: F405
    'groestlcoin_reg': GroestlcoinRegtest,  # noqa: F405
    'monacoin_main': MonacoinMain,  # noqa: F405
    'monacoin_test': MonacoinTest,  # noqa: F405
    'monacoin_reg': MonacoinRegtest,  # noqa: F405
    'navcoin_main': NavcoinMain,  # noqa: F405
    'navcoin_test': NavcoinTest,  # noqa: F405
    'navcoin_reg': NavcoinRegtest,  # noqa: F405
    'syscoin_main': SyscoinMain,  # noqa: F405
    'syscoin_test': SyscoinTest,  # noqa: F405
    'syscoin_reg': SyscoinRegtest,  # noqa: F405
    'vertcoin_main': VertcoinMain,  # noqa: F405
    'vertcoin_test': VertcoinTest,  # noqa: F405
    'vertcoin_reg': VertcoinRegtest,  # noqa: F405
    'bitcoin_private_main': BitcoinPrivateMain,  # noqa: F405
    'bitcoin_private_test': BitcoinPrivateTest,  # noqa: F405
    'bitcoin_private_reg': BitcoinPrivateRegtest  # noqa: F405
}


def get_network(name):
    '''
    Check by name if network is supported. Then return the class.
    '''
    if name not in SUPPORTED:
        raise ValueError('Unknown chain specifed: {}'.format(name))

    return SUPPORTED[name]
