SUPPORTED = [
    'bitcoin_main',
    # TODO add more
]


def get_network(name):
    if name not in SUPPORTED:
        raise ValueError('Unknown chain specifed: {}'.format(name))
    if name == 'bitcoin_main':
        return BitcoinMain
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

# TODO add more
