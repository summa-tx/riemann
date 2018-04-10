import multicoin.networks as networks

network = networks.get_network('bitcoin_main')


def SelectNetwork(name, subnet):
    global network
    if name not in networks.SUPPORTED:
        raise ValueError('Unknown chain specifed: {}'.format(name))
    network = networks.get_network(name)
