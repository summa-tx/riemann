Encoding
========

Riemann provides support for encoding addresses for all supported chains,
including native SegWit and cashaddrs. Typically, we recommend using the high
level `addresses` module, but the encoders themselves are also available.

We recommend generally using the `addresses` module. Addresses may be encoded
by type (e.g. `make_p2wsh_address`) or you may allow Riemann to select for you
(e.g. `make_sh_address`). Riemann prefers `cashaddr` where available, and
legacy elsewhere. Developers wanting Segwit addresses should be careful to use
Segwit specific methods.

Note: Compatibility Segwit addresses (witness-over-p2sh) are not first-class
address types in Riemann. You'll have to make script-sigs yourself.

.. toctree::
   :maxdepth: 2
   :caption: Encoder Info:

   encoders


Addresses
---------

.. automodule:: riemann.encoding.addresses
    :members:
    :undoc-members:
