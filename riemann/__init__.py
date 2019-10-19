from riemann import networks

network = networks.get_network('bitcoin_main')


def select_network(name: str):
    '''
    Set the library to use a supported network

    Examples:

    - bitcon_main
    - litecoin_test
    - zcash_sapling_main
    '''
    global network
    network = networks.get_network(name)


def get_current_network() -> networks.Network:
    '''Return the current network as a class'''
    return network


def get_current_network_name() -> str:
    '''Return the name of the current network'''
    return '{}_{}'.format(network.NETWORK_NAME, network.SUBNET_NAME)
