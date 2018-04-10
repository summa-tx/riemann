SUPPORTED = [
    'bitcoin_main',
    'bitcoin_test'
]

REQUIRED_ARGS = (
    'network_name', 'subnet_name',
    'p2sh_prefix', 'address_prefix',
    'segwit')


class Network:
    NETWORK_NAME = None
    SUBNET_NAME = None
    P2PKH = None
    P2SH = None
    SEGWIT = None


class BitcoinMain(Network):
    NETWORK_NAME = 'bitcoin'
    SUBNET_NAME = 'mainnet'
    P2PKH = b'\x00'
    P2SH = b'\x05'
    SEGWIT = True

# TODO
