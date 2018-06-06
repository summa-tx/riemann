# flake8: noqa

# To add a new coin
# 1. define a class in networks.py
# 2. add it to SUPPORTED

from .networks import *


SUPPORTED = {
    'bitcoin_main': BitcoinMain,
    'bitcoin_test': BitcoinTest,
    'bitcoin_reg': BitcoinRegtest,
    'litecoin_main': LitecoinMain,
    'litecoin_test': LitecoinTest,
    'litecoin_reg': LitecoinRegtest,
    'bitcoin_cash_main': BitcoinCashMain,
    'bitcoin_cash_test': BitcoinCashTest,
    'bitcoin_cash_reg': BitcoinCashRegtest,
    'bitcoin_gold_main': BitcoinGoldMain,
    'bitcoin_gold_test': BitcoinGoldTest,
    'bitcoin_gold_reg': BitcoinGoldRegtest,
    'dogecoin_main': DogecoinMain,
    'dogecoin_test': DogecoinTest,
    'dogecoin_reg': DogecoinRegtest,
    'dash_main': DashMain,
    'dash_test': DashTest,
    'dash_reg': DashRegtest,
    'zcash_sprout_main': ZcashSproutMain,
    'zcash_sprout_test': ZcashSproutTest,
    'zcash_sprout_reg': ZcashSproutRegtest,
    'zcash_overwinter_main': ZcashOverwinterMain,
    'zcash_overwinter_test': ZcashOverwinterTest,
    'zcash_overwinter_reg': ZcashOverwinterRegtest,
    'zcash_sapling_main': ZcashSaplingMain,
    'zcash_sapling_test': ZcashSaplingTest,
    'zcash_sapling_reg': ZcashSaplingRegtest,
    'decred_main': DecredMain,
    'decred_test': DecredTest,
    'decred_simnet': DecredSimnet,
    'pivx_main': PivxMain,
    'pivx_test': PivxTest,
    'pivx_reg': PivxRegtest,
    'viacoin_main': ViacoinMain,
    'viacoin_test': ViacoinTest,
    'viacoin_simnet': ViacoinSimnet,
    'feathercoin_main': FeathercoinMain,
    'feathercoin_test': FeathercoinTest,
    'feathercoin_reg': FeathercoinRegtest,
    'bitcoin_dark_main': BitcoinDarkMain,
    'bitcoin_dark_test': BitcoinDarkTest,
    'bitcoin_dark_reg': BitcoinDarkRegtest,
    'axe_main': AxeMain,
    'axe_test': AxeTest,
    'axe_reg': AxeRegtest,
    'bitcore_main': BitcoreMain,
    'bitcore_test': BitcoreTest,
    'bitcore_reg': BitcoreRegtest,
    'digibyte_main': DigibyteMain,
    'digibyte_test': DigibyteTest,
    'digibyte_reg': DigibyteRegtest,
    'groestlcoin_main': GroestlcoinMain,
    'groestlcoin_test': GroestlcoinTest,
    'groestlcoin_reg': GroestlcoinRegtest,
    'monacoin_main': MonacoinMain,
    'monacoin_test': MonacoinTest,
    'monacoin_reg': MonacoinRegtest,
    'navcoin_main': NavcoinMain,
    'navcoin_test': NavcoinTest,
    'navcoin_reg': NavcoinRegtest,
    'syscoin_main': SyscoinMain,
    'syscoin_test': SyscoinTest,
    'syscoin_reg': SyscoinRegtest,
    'vertcoin_main': VertcoinMain,
    'vertcoin_test': VertcoinTest,
    'vertcoin_reg': VertcoinRegtest,
    'bitcoin_private_main': BitcoinPrivateMain,
    'bitcoin_private_test': BitcoinPrivateTest,
    'bitcoin_private_reg': BitcoinPrivateRegtest,
    'verge_main': VergeMain,
    'verge_test': VergeTest,
    'verge_reg': VergeRegtest
}


def get_network(name):
    '''
    Check by name if network is supported. Then return the class.
    '''
    if name not in SUPPORTED:
        raise ValueError('Unknown chain specifed: {}'.format(name))

    return SUPPORTED[name]
