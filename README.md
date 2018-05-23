## Riemann: bitcoin transactions for humans

[![Build Status](https://travis-ci.org/summa-tx/riemann.svg?branch=master)](https://travis-ci.org/summa-tx/riemann)
[![Coverage Status](https://coveralls.io/repos/github/summa-tx/riemann/badge.svg)](https://coveralls.io/github/summa-tx/riemann)

### Purpose

Riemann is a **dependency-free Python3** library for creating **bitcoin-style transactions**. It is **compatible with many chains** and **supports SegWit**.

Riemann aims to make it easy to create application-specific transactions. It serializes and unserializes scripts from human-readable strings. It contains a complete toolbox for transaction construction, as well as built-in support for ~20 live networks and ~40 testnet or regtest nets.

Riemann is NOT a wallet. It does NOT handle keys or create signatures. Riemann is NOT a protocol or RPC implementation. Riemann does NOT communicate with anything. Ever. Riemann is NOT a Script VM. Riemann does NOT check the validity of your scriptsigs.

Riemann is _almost_ stateless. Before calling functions, you select a network. A list of supported networks is in `riemann/networks/__init__.py`. **No networks have been thoroughly tested.**

### Contributing

Please read CONTRIBUTING.md.

### Installation, Development & Running Tests

```
$ git clone git@github.com:summa-tx/riemann.git
$ cd riemann
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements-test.txt
$ pip install -e .
$ tox
```

### Usage

At a low level, Riemann deals in byte-like objects. However, it provides layers of abstractions on top of this. Notably, scripts are commonly expresses as strings. In script strings, data (like pubkeys) is expressed in unprefixed hex. For example, a P2PKH output script_pubkey might be expressed as follows:

```Python
# Note that the PUSH0x14 for the pubkey is implied
"OP_DUP OP_HASH160 00112233445566778899AABBCCDDEEFF00112233 OP_EQUALVERIFY OP_CHECKSIG"
```

`tx.tx` contains the data structures for the different pieces of a transaction. It deals in bytes and bytearrays.

`tx.tx_builder` provides tools for constructing transactions. It accepts human-readable inputs, like ints and human readable script strings wherever possible, and returns serialized transactions.

`simple` contains a simplified interface to the tx_builder. It accepts human-readable inputs, and guesses parameters like version and lock time based on the contents of the script.

Bitcoin mainnet is the default network. Select a network as follows:

```Python
import riemann
riemann.select_network('network_name')
```

When relevant, segwit is enabled by passing `witness=True`. Example: `make_sh_output(script_string, witness=True)`. There are also convenience functions that provide the same functionality, e.g.,  `make_p2wsh_output(script_string)`.

Data structures are IMMUTABLE. You can not (and definitely should not!) edit an instance of any of the underlying classes. Instead, make a new instance, or use the `copy` method. The `copy` method allows you to make a copy, and takes arguments to override any specific attribute.

### Notes and Bitcoin gotchas:

* For convenience, we separate the script_sig into the stack_script and the redeem_script. For PKH spends, the redeem script MUST BE `b''`.

* If there are any witnesses, all inputs must have a witness. The witness list MUST be the same size as the input list. Use `tx_builder.make_legacy_input_and_empty_witness()` when building your input to also generate a blank witness for your input. It returns `(TxIn, InputWitness)`.

* If all sequence numbers are set to max (0xFFFFFFFF), `lock_time` is disregarded by consensus rules. For this reason, 0xFFFFFFFE is the default sequence number in simple.py.

* Relative lock-time signaling uses a **different time format** than absolute lock-time. See here: https://prestwi.ch/bitcoin-time-locks/

* Not all chains support OP_CHECKSEQUENCEVERIFY and relative lock-times (lookin' at you Zcash).

* Replace-by-fee signaling is also communicated by sequence numbers. If any sequence number is 0xFFFFFFFD or lower, then RBF is enabled. RBF is _NOT_ a consensus feature.

* `lock_time` and `sequence` use different encodings for time.

```Python
# NB:
# script_sig -> Goes in TxIn.
#   - Legacy only
#   - Contains initial stack (stack_script)
#   - Contains p2sh script (redeem_script)
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

# LICENSE

Riemann is released under the LGPL.
Riemann contains some code released under MIT and ISC licenses. The appropriate license is included at the top of these files.

In particular:
* Base58 implementation from the excellent pycoin by Richard Kiss. [Link](https://github.com/richardkiss/pycoin)
* Bech32 implementation from Pieter Wuille. [Link](https://github.com/sipa/bech32/tree/master/ref/python)
* blake256 implementation by Larry Bugbee. [Link](http://www.seanet.com/~bugbee/crypto/blake/)
