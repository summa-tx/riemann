import riemann
from . import tx
from .. import utils
from ..script import serialization


def make_sh_script_pubkey(script_bytes, witness=False):
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

    return output_script


def make_sh_output_script(script_string, witness=False):
    '''
    str -> bytearray
    '''
    if witness and not riemann.network.SEGWIT:
        raise ValueError(
            'Network {} does not support witness scripts.'
            .format(riemann.get_current_network_name()))

    script_bytes = serialization.serialize(script_string)
    return make_sh_script_pubkey(script_bytes=script_bytes, witness=witness)


def make_pkh_output_script(pubkey, witness=False):
    '''
    bytearray -> bytearray
    '''
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
    return output_script


def make_p2sh_output_script(script_string):
    return make_sh_output_script(script_string, witness=False)


def make_p2pkh_output_script(pubkey):
    return make_pkh_output_script(pubkey, witness=False)


def make_p2wsh_output_script(script_string):
    return make_sh_output_script(script_string, witness=True)


def make_p2wpkh_output_script(pubkey):
    return make_pkh_output_script(pubkey, witness=True)


def _make_output(value, output_script, version=None):
    '''
    byte-like, byte-like -> TxOut
    '''
    if 'decred' in riemann.get_current_network_name():
        return tx.DecredTxOut(
            value=value,
            version=version,
            output_script=output_script)
    return tx.TxOut(value=value, output_script=output_script)


def make_sh_output(value, output_script, witness=False):
    '''
    int, str -> TxOut
    '''
    return _make_output(
        value=utils.i2le_padded(value, 8),
        output_script=make_sh_output_script(output_script, witness))


def make_p2sh_output(value, output_script):
    return make_sh_output(value, output_script, witness=False)


def make_p2wsh_output(value, output_script):
    return make_sh_output(value, output_script, witness=True)


def make_pkh_output(value, pubkey, witness=False):
    '''
    int, bytearray -> TxOut
    '''
    return _make_output(
        value=utils.i2le_padded(value, 8),
        output_script=make_pkh_output_script(pubkey, witness))


def make_p2pkh_output(value, pubkey):
    return make_pkh_output(value, pubkey, witness=False)


def make_p2wpkh_output(value, pubkey):
    return make_pkh_output(value, pubkey, witness=True)


def make_op_return_output(data):
    '''
    byte-like -> TxOut
    https://github.com/bitpay/bitcore/issues/1389
    '''
    if len(data) > 77:  # 77 bytes is the limit
        raise ValueError('Data is too long. Expected <= 77 bytes')
    pk_script = bytearray()
    pk_script.extend(b'\x6a')  # OP_RETURN
    pk_script.extend(b'\x4c')  # OP_PUSHDATA1
    pk_script.extend([len(data)])  # One byte for length of data
    pk_script.extend(data)  # Data
    return _make_output(utils.i2le_padded(0, 8), pk_script)


def make_empty_witness():
    return make_witness([])


def make_witness_stack_item(data):
    '''
    bytearray -> WitnessStackItem
    '''
    return tx.WitnessStackItem(item=data)


def make_witness(data_list):
    '''
    list(bytearray) -> InputWitness
    '''
    return tx.InputWitness(
        stack=[make_witness_stack_item(item) for item in data_list])


def make_decred_witness(value, height, index, stack_script, redeem_script):
    return tx.DecredInputWitness(
        value=value,
        height=height,
        index=index,
        stack_script=stack_script,
        redeem_script=redeem_script)


def make_outpoint(tx_id_le, index, tree=None):
    '''
    byte-like, int, int -> Outpoint
    '''
    if 'decred' in riemann.get_current_network_name():
        return tx.DecredOutpoint(tx_id=tx_id_le,
                                 index=utils.i2le_padded(index, 4),
                                 tree=utils.i2le_padded(tree, 1))
    return tx.Outpoint(tx_id=tx_id_le,
                       index=utils.i2le_padded(index, 4))


def make_script_sig(stack_script, redeem_script):
    '''
    str, str -> bytearray
    '''
    stack_script += ' {}'.format(
        serialization.hex_serialize(redeem_script))
    return serialization.serialize(stack_script)


def make_legacy_input(outpoint, stack_script, redeem_script, sequence):
    '''
    Outpoint, byte-like, byte-like, int -> TxIn
    '''
    if 'decred' in riemann.get_current_network_name():
        return tx.DecredTxIn(
            outpoint=outpoint,
            sequence=utils.i2le_padded(sequence, 4))
    return tx.TxIn(outpoint=outpoint,
                   stack_script=stack_script,
                   redeem_script=redeem_script,
                   sequence=utils.i2le_padded(sequence, 4))


def make_legacy_input_and_empty_witness(outpoint, stack_script,
                                        redeem_script, sequence):
    '''
    Outpoint, byte-like, byte-like, int -> (TxIn, InputWitness)
    '''
    return (make_legacy_input(outpoint=outpoint,
                              stack_script=stack_script,
                              redeem_script=redeem_script,
                              sequence=sequence),
            make_empty_witness())


def make_witness_input(outpoint, sequence):
    '''
    Outpoint, int -> TxIn
    '''
    if 'decred' in riemann.get_current_network_name():
        return tx.DecredTxIn(
            outpoint=outpoint,
            sequence=utils.i2le_padded(sequence, 4))
    return tx.TxIn(outpoint=outpoint,
                   stack_script=b'',
                   redeem_script=b'',
                   sequence=utils.i2le_padded(sequence, 4))


def make_decred_input(outpoint, sequence):
    return tx.DecredTxIn(
        outpoint=outpoint,
        sequence=utils.i2le_padded(sequence, 4))


def make_witness_input_and_witness(outpoint, sequence,
                                   stack=None, **kwargs):
    '''
    Outpoint, int, list(bytearray) -> (Input, InputWitness)
    '''
    if 'decred' in riemann.get_current_network_name():
        return(make_witness_input(outpoint, sequence),
               make_decred_witness(value=kwargs['value'],
                                   height=kwargs['height'],
                                   index=kwargs['index'],
                                   stack_script=kwargs['stack_script'],
                                   redeem_script=kwargs['redeem_script']))
    return (make_witness_input(outpoint, sequence),
            make_witness(stack))


def make_tx(version, tx_ins, tx_outs, lock_time,
            expiry=None, tx_witnesses=None,
            tx_joinsplits=None, joinsplit_pubkey=None, joinsplit_sig=None):
    '''
    int, list(TxIn), list(TxOut), int, list(InputWitness) -> Tx
    '''
    n = riemann.get_current_network_name()
    if 'decred' in n:
        return tx.DecredTx(
            version=utils.i2le_padded(version, 4),
            tx_ins=tx_ins,
            tx_outs=tx_outs,
            lock_time=utils.i2le_padded(lock_time, 4),
            expiry=utils.i2le_padded(expiry, 4),
            tx_witnesses=[tx_witnesses])
    if 'sprout' in n and tx_joinsplits is not None:
        return tx.SproutTx(
            version=version,
            tx_ins=tx_ins,
            tx_outs=tx_outs,
            lock_time=utils.i2le_padded(lock_time, 4),
            tx_joinsplits=tx_joinsplits if tx_joinsplits is not None else [],
            joinsplit_pubkey=joinsplit_pubkey,
            joinsplit_sig=joinsplit_sig)
    if 'overwinter' in n:
        return tx.OverwinterTx(
            tx_ins=tx_ins,
            tx_outs=tx_outs,
            lock_time=utils.i2le_padded(lock_time, 4),
            expiry_height=utils.i2le_padded(expiry, 4),
            tx_joinsplits=tx_joinsplits if tx_joinsplits is not None else [],
            joinsplit_pubkey=joinsplit_pubkey,
            joinsplit_sig=joinsplit_sig)
    flag = riemann.network.SEGWIT_TX_FLAG \
        if tx_witnesses is not None else None
    return tx.Tx(version=utils.i2le_padded(version, 4),
                 flag=flag,
                 tx_ins=tx_ins,
                 tx_outs=tx_outs,
                 tx_witnesses=tx_witnesses,
                 lock_time=utils.i2le_padded(lock_time, 4))


def length_prepend(byte_string):
    '''
    bytes -> bytes
    '''
    length = tx.VarInt(len(byte_string))
    return length.to_bytes() + byte_string
