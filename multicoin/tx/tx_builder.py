# import tx
import multicoin
from . import tx
from .. import utils
from ..script import parsing


# TODO: Coerce the [expletive] out of everything

def make_sh_output_script(script_string, witness=False):
    '''
    str -> bytearray
    '''

    if witness and not multicoin.network.SEGWIT:
        raise ValueError(
            'Network {} does not support witness scripts.'
            .format(multicoin.get_current_network()))

    output_script = bytearray()

    script_bytes = parsing.serialize_from_string(script_string)
    script_hash = \
        utils.hash160(script_bytes) if not witness \
        else utils.sha256(script_bytes)

    prefix = \
        multicoin.network.P2SH_PREFIX if not witness \
        else multicoin.network.P2WSH_PREFIX

    output_script.extend(prefix)
    output_script.extend(script_hash)

    return output_script


def make_pkh_output_script(pubkey, witness=False):
    '''
    bytearray -> bytearray
    '''
    if witness and not multicoin.network.SEGWIT:
        raise ValueError(
            'Network {} does not support witness scripts.'
            .format(multicoin.get_current_network()))

    output_script = bytearray()

    if type(pubkey) is not bytearray and type(pubkey) is not bytes:
        raise ValueError('Unknown pubkey format. '
                         'Expected bytes. Got: {}'.format(type(pubkey)))

    pubkey_hash = utils.hash160(pubkey)

    prefix = \
        multicoin.network.P2PKH_PREFIX if not witness \
        else multicoin.network.P2WPKH_PREFIX

    output_script.extend(prefix)
    output_script.extend(pubkey_hash)

    return output_script


def make_p2sh_output_script(script_string):
    return make_sh_output_script(script_string, witness=False)


def make_p2pkh_output_script(pubkey):
    return make_pkh_output_script(pubkey, witness=False)


def make_p2wsh_output_script(script_string):
        return make_sh_output_script(script_string, witness=True)


def make_p2wpkh_output_script(pubkey):
    return make_pkh_output_script(pubkey, witness=True)


def make_sh_output(value, script, witness=False):
    '''
    int, str -> TxOut
    '''
    return tx.TxOut(value=utils.i2le_padded(value),
                    script=make_sh_output(script, witness))


def make_p2sh_output(value, script):
    return make_sh_output(value, script, witness=False)


def make_p2wsh_output(value, script):
    return make_sh_output(value, script, witness=True)


def make_pkh_output(value, pubkey, witness=False):
    '''
    int, bytearray -> TxOut
    '''
    return tx.TxOut(value=utils.i2le_padded(value),
                    script=make_pkh_output(pubkey, witness))


def make_p2pkh_output(value, pubkey):
    return make_pkh_output(value, pubkey, witness=False)


def make_p2wpkh_output(value, pubkey, witness=False):
    return make_pkh_output(value, pubkey, witness=True)


def make_witness_stack_item(data):
    '''
    bytearray -> WitnessStackItem
    '''
    return tx.WitnessStackItem(item=data)


def make_witness(data_list):
    '''
    list(bytearray) -> TxWitness
    '''
    return tx.TxWitness(
        stack=[make_witness_stack_item(item) for item in data_list])


def make_outpoint(tx_id_le, index):
    '''
    bytearray, int -> Outpoint
    '''
    return tx.Outpoint(tx_id=tx_id_le,
                       index=utils.i2le_padded(index, 4))


def make_script_sig(script_sig, redeem_script):
    '''
    str, str -> bytearray
    '''
    script_sig += ' {}'.format(
        parsing.hex_serialize_from_string(redeem_script))
    return parsing.serialize_from_string(script_sig)


def make_input(outpoint, script_sig, redeem_script, sequence):
    '''
    Outpoint, str, str, int -> TxIn
    '''
    return tx.TxIn(outpoint=outpoint,
                   script=make_script_sig(script_sig, redeem_script),
                   sequence=utils.i2le_padded(sequence, 4))


def make_tx(version, tx_ins, tx_outs, lock_time, tx_witnesses=None):

    '''
    int, list(TxIn), list(TxOut), int, list(TxWitness) -> Tx
    '''
    flag = multicoin.network.SEGWIT_TX_FLAG \
        if tx_witnesses is not None else None
    return tx.Tx(version=utils.i2le_padded(version, 4),
                 flag=flag,
                 tx_ins=tx_ins,
                 tx_outs=tx_outs,
                 tx_witnesses=tx_witnesses,
                 lock_time=utils.i2le_padded(lock_time, 4))
