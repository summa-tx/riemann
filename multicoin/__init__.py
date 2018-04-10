import multicoin.networks as networks

network = networks.get_network('bitcoin_main')


def SelectNetwork(name, subnet):
    global network
    network = networks.get_network(name)
