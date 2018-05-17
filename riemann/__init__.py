from . import networks

network = networks.get_network('bitcoin_main')


def select_network(name):
    global network
    network = networks.get_network(name)


def get_current_network():
    return network


def get_current_network_name():
    return '{}_{}'.format(network.NETWORK_NAME, network.SUBNET_NAME)
