import multicoin.networks as networks

network = networks.get_network('bitcoin_main')


def select_network(name):
    global network
    network = networks.get_network(name)


def get_current_network():
    return '{}_{}'.format(network.NETWORK_NAME, network.SUBNET_NAME)
