Riemann Transactions
====================

Riemann supports transactions in many chains. See :ref:`Networks` for a
complete list.

Riemann represents transactions as bytestrings with some additional sugar on
top. All elements of a transaction inherit from the `ByteData` class. This
provides indexing `version = my_tx[:4]`, formatting `print(my_tx)` and
`f'{my_tx:x}'`, as well as equality and other useful operators.

Generally, developers want to interact with the `Tx` class and its components,
`TxIn`, `TxOut`, and `InputWitness`.


.. toctree::
   :maxdepth: 2
   :caption: Tx Classes:

   bytedata
   outpoint
   txin
   txout
   witnessstackitem
   inputwitness
   tx
