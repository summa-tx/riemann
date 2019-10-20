Riemann Transactions
====================

Riemann supports transactions in many chains. See :ref:`Networks` for a
complete list.

Riemann represents transactions as bytestrings with some additional sugar on
top. All elements of a transaction inherit from the `ByteData` class. The
ByteData class provides useful syntactic sugar:

.. code-block:: python

    # indexing
    version = my_tx[:4]

    # formatting
    f'{my_tx:x}'

    # equality
    my_tx == some_other_tx



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
