import riemann
from riemann import utils
from riemann.script import serialization
from riemann.tx import tx, decred, overwinter, sapling, sprout, zcash_shared

from typing import cast, List, Optional, overload


def make_sh_script_pubkey(script_bytes: bytes, witness: bool = False) -> bytes:
    output_script = bytearray()
    if witness:
        script_hash = utils.sha256(script_bytes)
        output_script.extend(riemann.network.P2WSH_PREFIX)
        output_script.extend(script_hash)
    else:
        script_hash = utils.hash160(script_bytes)
        output_script.extend(b'\xa9\x14')  # OP_HASH160 PUSH0x14
        output_script.extend(script_hash)
        output_script.extend(b'\x87')  # OP_EQUAL

    return bytes(output_script)


def make_sh_output_script(script_string: str, witness: bool = False) -> bytes:
    '''
    str -> bytearray
    '''
    if witness and not riemann.network.SEGWIT:
        raise ValueError(
            'Network {} does not support witness scripts.'
            .format(riemann.get_current_network_name()))

    script_bytes = serialization.serialize(script_string)
    return make_sh_script_pubkey(script_bytes=script_bytes, witness=witness)


def make_pkh_output_script(pubkey: bytes, witness: bool = False) -> bytes:
    '''Makes a pkh pubkey script'''
    if witness and not riemann.network.SEGWIT:
        raise ValueError(
            'Network {} does not support witness scripts.'
            .format(riemann.get_current_network_name()))

    output_script = bytearray()

    if type(pubkey) is not bytearray and type(pubkey) is not bytes:
        raise ValueError('Unknown pubkey format. '
                         'Expected bytes. Got: {}'.format(type(pubkey)))

    pubkey_hash = utils.hash160(pubkey)

    if witness:
        output_script.extend(riemann.network.P2WPKH_PREFIX)
        output_script.extend(pubkey_hash)
    else:
        output_script.extend(b'\x76\xa9\x14')  # OP_DUP OP_HASH160 PUSH14
        output_script.extend(pubkey_hash)
        output_script.extend(b'\x88\xac')  # OP_EQUALVERIFY OP_CHECKSIG
    return bytes(output_script)


def make_p2sh_output_script(script_string: str) -> bytes:
    return make_sh_output_script(script_string, witness=False)


def make_p2pkh_output_script(pubkey: bytes) -> bytes:
    return make_pkh_output_script(pubkey, witness=False)


def make_p2wsh_output_script(script_string: str) -> bytes:
    return make_sh_output_script(script_string, witness=True)


def make_p2wpkh_output_script(pubkey: bytes) -> bytes:
    return make_pkh_output_script(pubkey, witness=True)


@overload
def _make_output(
        value: bytes,
        output_script: bytes,
        version: bytes) -> decred.DecredTxOut:
    ...  # pragma: nocover


@overload  # noqa: F811
def _make_output(
        value: bytes,
        output_script: bytes) -> tx.TxOut:
    ...  # pragma: nocover


def _make_output(  # noqa: F811
        value,
        output_script,
        version=None):
    '''Instantiates a TxOut from value and output script'''
    if 'decred' in riemann.get_current_network_name():
        return decred.DecredTxOut(
            value=value,
            version=cast(int, version),
            output_script=output_script)
    return tx.TxOut(value=value, output_script=output_script)


def make_sh_output(
        value: int,
        output_script: str,
        witness: bool = False) -> tx.TxOut:
    '''Instantiates'''
    return _make_output(
        value=utils.i2le_padded(value, 8),
        output_script=make_sh_output_script(output_script, witness))


def make_p2sh_output(value: int, output_script: str) -> tx.TxOut:
    return make_sh_output(value, output_script, witness=False)


def make_p2wsh_output(value: int, output_script: str) -> tx.TxOut:
    return make_sh_output(value, output_script, witness=True)


def make_pkh_output(
        value: int,
        pubkey: bytes,
        witness: bool = False) -> tx.TxOut:
    return _make_output(
        value=utils.i2le_padded(value, 8),
        output_script=make_pkh_output_script(pubkey, witness))


def make_p2pkh_output(value: int, pubkey: bytes) -> tx.TxOut:
    return make_pkh_output(value, pubkey, witness=False)


def make_p2wpkh_output(value: int, pubkey: bytes) -> tx.TxOut:
    return make_pkh_output(value, pubkey, witness=True)


def make_op_return_output(data: bytes) -> tx.TxOut:
    '''Generates OP_RETURN output for data less than 78 bytes.
    If data is 76 or 77 bytes, OP_PUSHDATA1 is included:
    <OP_RETURN><OP_PUSHDATA1><data len><data>
    If data is less than 76 bytes, OP_PUSHDATA1 is not included:
    <OP_RETURN><data len><data>
    80 bytes is the default setting for an OP_RETURN output script.
    https://github.com/bitpay/bitcore/issues/1389
    Args:
        data    (bytes):    data included in output
    Returns:
        (TxOut):            TxOut object with OP_RETURN output
    '''
    if len(data) > 77:  # 77 bytes is the limit
        raise ValueError('Data is too long. Expected <= 77 bytes')

    pk_script = bytearray()
    pk_script.extend(b'\x6a')       # OP_RETURN

    # OP_PUSHDATA1 only used if data is greater than 75 bytes
    if len(data) in [76, 77]:
        pk_script.extend(b'\x4c')  # OP_PUSHDATA1

    pk_script.extend([len(data)])  # One byte for length of data
    pk_script.extend(data)         # Data
    return _make_output(utils.i2le_padded(0, 8), pk_script)


def make_empty_witness() -> tx.InputWitness:
    return make_witness([])


def make_witness_stack_item(data: bytes) -> tx.WitnessStackItem:
    return tx.WitnessStackItem(item=data)


def make_witness(data_list: List[bytes]) -> tx.InputWitness:
    '''
    list(bytes) -> InputWitness
    '''
    return tx.InputWitness(
        stack=[make_witness_stack_item(item) for item in data_list])


def make_decred_witness(
        value: bytes,
        height: bytes,
        index: bytes,
        stack_script: bytes,
        redeem_script: bytes) -> decred.DecredInputWitness:
    return decred.DecredInputWitness(
        value=value,
        height=height,
        index=index,
        stack_script=stack_script,
        redeem_script=redeem_script)


@overload
def make_outpoint(
        tx_id_le: bytes, index: int, tree: int) -> decred.DecredOutpoint:
    ...  # pragma: nocover


@overload  # noqa: F811
def make_outpoint(tx_id_le: bytes, index: int) -> tx.Outpoint:
    ...  # pragma: nocover


def make_outpoint(tx_id_le, index, tree=None):  # noqa: F811
    '''
    byte-like, int, int -> Outpoint
    '''
    if 'decred' in riemann.get_current_network_name():
        tree_bytes = b'\x00' if tree is None else utils.i2le_padded(tree, 1)
        return decred.DecredOutpoint(tx_id=tx_id_le,
                                     index=utils.i2le_padded(index, 4),
                                     tree=tree_bytes)
    return tx.Outpoint(tx_id=tx_id_le,
                       index=utils.i2le_padded(index, 4))


def make_script_sig(stack_script: str, redeem_script: str) -> bytes:
    '''
    str, str -> bytearray
    '''
    script_sig = '{} {}'.format(
        stack_script,
        serialization.hex_serialize(redeem_script))
    return serialization.serialize(script_sig)


@overload
def make_legacy_input(
        outpoint: decred.DecredOutpoint,
        stack_script: bytes,
        redeem_script: bytes,
        sequence: int) -> decred.DecredTxIn:
    ...  # pragma: nocover


@overload  # noqa: F811
def make_legacy_input(
        outpoint: tx.Outpoint,
        stack_script: bytes,
        redeem_script: bytes,
        sequence: int) -> tx.TxIn:
    ...  # pragma: nocover


def make_legacy_input(  # noqa: F811
        outpoint,
        stack_script,
        redeem_script,
        sequence):
    '''Make a legacy input'''
    if 'decred' in riemann.get_current_network_name():
        return decred.DecredTxIn(
            outpoint=outpoint,
            sequence=utils.i2le_padded(sequence, 4))
    return tx.TxIn(outpoint=outpoint,
                   stack_script=stack_script,
                   redeem_script=redeem_script,
                   sequence=utils.i2le_padded(sequence, 4))


@overload
def make_witness_input(
        outpoint: decred.DecredOutpoint,
        sequence: int) -> decred.DecredTxIn:
    ...  # pragma: nocover


@overload  # noqa: F811
def make_witness_input(
        outpoint: tx.Outpoint,
        sequence: int) -> tx.TxIn:
    ...  # pragma: nocover


def make_witness_input(outpoint, sequence):  # noqa: F811
    '''Make a witness input'''
    if 'decred' in riemann.get_current_network_name():
        return decred.DecredTxIn(
            outpoint=outpoint,
            sequence=utils.i2le_padded(sequence, 4))
    return tx.TxIn(outpoint=outpoint,
                   stack_script=b'',
                   redeem_script=b'',
                   sequence=utils.i2le_padded(sequence, 4))


def make_decred_input(
        outpoint: decred.DecredOutpoint,
        sequence: int) -> decred.DecredTxIn:
    return decred.DecredTxIn(
        outpoint=outpoint,
        sequence=utils.i2le_padded(sequence, 4))


@overload
def make_tx(
        version: int,
        tx_ins: List[decred.DecredTxIn],
        tx_outs: List[decred.DecredTxOut],
        lock_time: int,
        expiry: int,
        tx_witnesses: List[decred.DecredInputWitness]) -> decred.DecredTx:
    ...  # pragma: nocover


@overload  # noqa: F811
def make_tx(
        version: int,
        tx_ins: List[tx.TxIn],
        tx_outs: List[tx.TxOut],
        lock_time: int,
        tx_joinsplits: List[zcash_shared.SproutJoinsplit],
        joinsplit_pubkey: Optional[bytes],
        joinsplit_sig: Optional[bytes],
        binding_sig: Optional[bytes]) -> sprout.SproutTx:
    ...  # pragma: nocover


@overload  # noqa: F811
def make_tx(
        tx_ins: List[tx.TxIn],
        tx_outs: List[tx.TxOut],
        lock_time: int,
        expiry: int,
        tx_joinsplits: List[zcash_shared.SproutJoinsplit],
        joinsplit_pubkey: Optional[bytes],
        joinsplit_sig: Optional[bytes],
        binding_sig: Optional[bytes]) -> overwinter.OverwinterTx:
    ...  # pragma: nocover


@overload  # noqa: F811
def make_tx(
        tx_ins: List[tx.TxIn],
        tx_outs: List[tx.TxOut],
        lock_time: int,
        expiry: int,
        value_balance: int,
        tx_shielded_spends: List[sapling.SaplingShieldedSpend],
        tx_shielded_outputs: List[sapling.SaplingShieldedOutput],
        tx_joinsplits: List[sapling.SaplingJoinsplit],
        joinsplit_pubkey: Optional[bytes],
        joinsplit_sig: Optional[bytes],
        binding_sig: Optional[bytes]) -> sapling.SaplingTx:
    ...  # pragma: nocover


@overload  # noqa: F811
def make_tx(
        version: int,
        tx_ins: List[tx.TxIn],
        tx_outs: List[tx.TxOut],
        lock_time: int,
        tx_witnesses: Optional[List[tx.InputWitness]] = None) -> tx.Tx:
    ...  # pragma: nocover


def make_tx(  # noqa: F811
        version,
        tx_ins,
        tx_outs,
        lock_time,
        expiry=None,
        value_balance=0,
        tx_shielded_spends=None,
        tx_shielded_outputs=None,
        tx_witnesses=None,
        tx_joinsplits=None,
        joinsplit_pubkey=None,
        joinsplit_sig=None,
        binding_sig=None):
    '''
    int, list(TxIn), list(TxOut), int, list(InputWitness) -> Tx
    '''
    n = riemann.get_current_network_name()
    if 'decred' in n:
        return decred.DecredTx(
            version=utils.i2le_padded(version, 4),
            tx_ins=tx_ins,
            tx_outs=tx_outs,
            lock_time=utils.i2le_padded(lock_time, 4),
            expiry=utils.i2le_padded(expiry, 4),
            tx_witnesses=[tx_witnesses])
    if 'sprout' in n and tx_joinsplits is not None:
        return sprout.SproutTx(
            version=version,
            tx_ins=tx_ins,
            tx_outs=tx_outs,
            lock_time=utils.i2le_padded(lock_time, 4),
            tx_joinsplits=tx_joinsplits if tx_joinsplits is not None else [],
            joinsplit_pubkey=joinsplit_pubkey,
            joinsplit_sig=joinsplit_sig)
    if 'overwinter' in n:
        return overwinter.OverwinterTx(
            tx_ins=tx_ins,
            tx_outs=tx_outs,
            lock_time=utils.i2le_padded(lock_time, 4),
            expiry_height=utils.i2le_padded(expiry, 4),
            tx_joinsplits=tx_joinsplits if tx_joinsplits is not None else [],
            joinsplit_pubkey=joinsplit_pubkey,
            joinsplit_sig=joinsplit_sig)
    if 'sapling' in n:
        return sapling.SaplingTx(
            tx_ins=tx_ins,
            tx_outs=tx_outs,
            lock_time=utils.i2le_padded(lock_time, 4),
            expiry_height=utils.i2le_padded(expiry, 4),
            value_balance=utils.i2le_padded(value_balance, 8),
            tx_shielded_spends=tx_shielded_spends,
            tx_shielded_outputs=tx_shielded_outputs,
            tx_joinsplits=tx_joinsplits,
            joinsplit_pubkey=joinsplit_pubkey,
            joinsplit_sig=joinsplit_sig,
            binding_sig=binding_sig)
    flag = riemann.network.SEGWIT_TX_FLAG \
        if tx_witnesses is not None else None
    return tx.Tx(version=utils.i2le_padded(version, 4),
                 flag=flag,
                 tx_ins=tx_ins,
                 tx_outs=tx_outs,
                 tx_witnesses=tx_witnesses,
                 lock_time=utils.i2le_padded(lock_time, 4))


def length_prepend(byte_string: bytes) -> bytes:
    '''Adds a VarInt length marker to a bytestring'''
    length = tx.VarInt(len(byte_string))
    return length.to_bytes() + byte_string
