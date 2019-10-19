InputWitness
============

An `InputWitness` is the SegWit datastructure containing spend authorization
for a specific input. It consists of a tuple (the `stack`) of
:ref:`WitnessStackItem` objects.

Within a `Tx` the list of `InputWitness` objects is called `tx_witnesses`. Each
witness and each item in its stack can be indexed by its position, e.g.
`my_tx.tx_witnesses[0].stack[4]`. In the case of p2wsh inputs, the last stack
item `my_input_witness.stack[-1]` is called the Witness Script, and contains a
serialized Script program.

.. autoclass:: riemann.tx.InputWitness
    :members:
    :undoc-members:
