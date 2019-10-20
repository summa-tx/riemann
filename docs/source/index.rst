Riemann: Cryptocurrency Transactions for Humans
===============================================

.. code-block:: bash

    $ pip install riemann-tx

Riemann is a **dependency-free Python3** library for creating **bitcoin-style
transactions**. It is **compatible with many chains** and **supports SegWit**.

Riemann aims to make it easy to create application-specific transactions. It
serializes and unserializes scripts from human-readable strings. It contains
a complete toolbox for transaction construction, as well as built-in support
for ~20 live networks and ~40 testnet or regtest nets.

Riemann is NOT a wallet. It does NOT handle keys or create signatures.
Riemann is NOT a protocol or RPC implementation. Riemann does NOT communicate
with anything. Ever. Riemann is NOT a Script VM. Riemann does NOT check the
validity of your scriptsigs.

Riemann is _almost_ stateless. Before calling functions, you select from a list
of :ref:`networks`. Tests are made using on-chain transactions, primarily from
Bitcoin.

.. toctree::
   :maxdepth: 2
   :caption: Submodules:

   simple
   tx builder
   transactions
   encoding
   script
   networks
   utils

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
