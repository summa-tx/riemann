Multi-coin transaction generation toolbox.

### Major TODOs

* Many more tests
* Alternate API where the network object is passed to functions (real statelessness)
* Support OP_PUSHDATA1-4
* Fix bug in InputWitness.from_bytes

### Purpose

Multicoin is a **dependency-free Python3** library for creating **bitcoin-style transactions**. It is compatible with many chains and **supports SegWit**.

Multicoin aims to make it easy to create application-specific Bitcoin transactions. It serializes and unserializes scripts from human-readable strings. It contains a complete toolbox for transaction construction, as well as built-in support for >20 live networks and ~40 testnet or regtest nets.

Multicoin is NOT a wallet. It does NOT handle keys or create signatures. Multicoin is NOT a protocol or RPC implementation. Multicoin does NOT communicate with anything. Ever.

Multicoin is _almost_ stateless. Before calling functions, you select a network. A list of supported networks is in `multicoin/networks/__init__.py`. **No networks have been thoroughly tested.**

### Installation, Development & Running Tests

`$ git clone $LIB_URL`
`$ cd python-multicoin`
`$ virtualenv -p python3 venv`
`$ source venv/bin/activate`
`$ pip install -r requirements-test.txt`
`$ pip install -e .`
`$ tox`

### Usage

All objects are immutable

`tx.tx` contains the data structures for the different pieces of a transaction.

`tx.tx_builder` provides tools for constructing

`simple` contains a simplified interface to the tx_builder.

Bitcoin mainnet is the default network. Select a network as follows:

```Python
import multicoin
multicoin.select_network('network_name')
```

At a low level, Multicoin deals in byte-like objects. However, it provides layers of abstractions on top of this. Notably, scripts are commonly expresses as strings. In script strings, data (like pubkeys) is expressed in unprefixed hex. For example, a P2PKH output script_pubkey might be expressed as follows:

```Python
# Note that the PUSH0x14 for the pubkey is implied
"OP_DUP OP_HASH160 00112233445566778899AABBCCDDEEFF00112233 OP_EQUALVERIFY OP_CHECKSIG"
```

Fixed-length bitstrings (version, lock_time, sequence, value, etc.) are expressed as integers.

When relevant, segwit is enabled by passing `witness=True`. Example: `make_sh_output(script_string, witness=True)`. There are also convenience functions like `make_p2wsh_output` that provide the same functionality.

Data structures are IMMUTABLE. You can not (and definitely should not!) edit an instance of any of the underlying classes. Instead, make a new instance, or use the `copy` method. The `copy` method allows you to make a copy, and takes arguments to override any specific attribute.

### Notes and weird little transaction rules:

* If there are any witnesses, all inputs must have a witness. The witness list MUST be the same size as the input list. Use `tx_builder.make_legacy_input_and_empty_witness()` when building your input to also generate a blank witness for your input. It returns `(TxIn, InputWitness)`.

* If all sequence numbers are set to max (0xFFFFFFFF), `lock_time` is disregarded by consensus rules.

* `lock_time` and `sequence` use different encodings for time.

```Python
# NB:
# script_sig -> Goes in TxIn.
#   - Legacy only
#   - Contains initial stack (stack_script)
#   - Contains pubey/script revelation
# stack_script -> Goes in script_sig
#   - Legacy only
#   - Contains script that makes initial stack
# script_pubkey -> Goes in TxOut
#   - Also called pk_script, output_script
#   - P2PKH: OP_DUP OP_HASH160 PUSH14 {pkh} OP_EQUALVERIFY OP_CHECKSIG
#   - P2SH: OP_HASH160 {script_hash} OP_EQUAL
#   - P2WPKH: OP_0 PUSH0x14 {pkh}
#   - P2WSH: OP_0 PUSH0x20 {script_hash}
# WitnessStackItem -> Goes in InputWitness
#   - Witness only
#   - Contains a length-prefixed stack item
# InputWitness -> Goes in Witness
#   - A stack associated with a specific input
#   - If spending from p2wsh, the last item is a serialzed script
#   - If spending from p2wpkh, consists of [signature, pubkey]
```
