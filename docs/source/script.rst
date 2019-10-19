Script
======

Riemann provides support for (de)serializing Bitcoin Script. However, it does
not support execution of Script.

In Riemann's Script serialization, opcodes are represented as strings and data
pushes are represented as unprefixed hex strings. E.g. `"0011aabb OP_HASH160"`.
This can be serialized to bytes via `serialization.serialize` or to hex via
`serialization.hex_serialize`.

Some examples are available in `riemann/script/examples.py` and
`riemann/examples`.

Serialization
-------------

.. automodule:: riemann.script.serialization
    :members:
    :undoc-members:
