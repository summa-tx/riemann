SUPPORTED = [
    'bitcoin_main',
    'bitcoin_test'
    # TODO add more
]


def get_network(name):
    if name not in SUPPORTED:
        raise ValueError('Unknown chain specifed: {}'.format(name))
    if name == 'bitcoin_main':
        return BitcoinMain
    if name == 'bitcoin_test':
        return BitcoinTest
    # TODO add more


class Network:
    SYMBOL = 'BTC'
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
