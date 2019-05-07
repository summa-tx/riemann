from riemann import tx
from riemann import utils
from riemann.tx import decred
from riemann.tx import tx_builder as tb
from riemann.encoding import addresses as addr

from typing import overload


def output(value: int, address: str) -> tx.TxOut:
    '''
    int, str -> TxOut
    accepts base58 or bech32 addresses
    '''
    script = addr.to_output_script(address)
    value_bytes = utils.i2le_padded(value, 8)
    return tb._make_output(value_bytes, script)


@overload
def outpoint(tx_id: str, index: int, tree: int) -> decred.DecredOutpoint:
    ...


@overload  # noqa: F811
def outpoint(tx_id: str, index: int) -> tx.Outpoint:
    ...


def outpoint(tx_id, index, tree=None):  # noqa: F811
    '''
    hex_str, int, int -> Outpoint
    accepts block explorer txid string
    '''
    tx_id_le = bytes.fromhex(tx_id)[::-1]
    return tb.make_outpoint(tx_id_le, index, tree)


@overload
def unsigned_input(
        outpoint: tx.Outpoint,
        sequence: int) -> tx.TxIn:
    ...


@overload   # noqa: F811
def unsigned_input(
        outpoint: decred.DecredOutpoint,
        sequence: int) -> decred.DecredTxIn:
    ...


def unsigned_input(outpoint, sequence=0xFFFFFFFE):   # noqa: F811
    '''
    Outpoint, byte-like, int -> TxIn
    '''
    return tb.make_legacy_input(
        outpoint=outpoint,
        stack_script=b'',
        redeem_script=b'',
        sequence=sequence)


def unsigned_legacy_tx(tx_ins, tx_outs, **kwargs):
    '''Create an unsigned transaction
    Use this to generate sighashes for unsigned TxIns
    Hint: set version to 2 if using sequence number relative time locks

    Args:
        tx_ins      list(TxIn instances): list of transaction inputs
        tx_outs     list(TxOut instances): list of transaction outputs

        **kwargs:
        version     (int): transaction version number
        locktime            (hex): transaction locktime
        expiry              (int): overwinter expiry time
        tx_joinsplits       (list): list of joinsplits transactions
        joinsplit_pubkey    (bytes): joinsplit public key
        joinsplit_sig       (bytes): joinsplit signature

    Returns:
        (Tx instance): unsigned transaction
    '''
    return tb.make_tx(
        version=kwargs['version'] if 'version' in kwargs else 2,
        tx_ins=tx_ins,
        tx_outs=tx_outs,
        lock_time=kwargs['lock_time'] if 'lock_time' in kwargs else 0,
        expiry=kwargs['expiry'] if 'expiry' in kwargs else 0,
        tx_joinsplits=(kwargs['tx_joinsplits']
                       if 'tx_joinsplits' in kwargs else []),
        joinsplit_pubkey=(kwargs['joinsplit_pubkey']
                          if 'joinsplit_pubkey' in kwargs
                          else []),
        joinsplit_sig=(kwargs['joinsplit_sig']
                       if 'joinsplit_sig' in kwargs else []))


def unsigned_witness_tx(tx_ins, tx_outs, **kwargs):
    '''Create an unsigned segwit transaction
    Create an unsigned segwit transaction
    Use this to generate sighashes for unsigned TxIns
    Hint: set version to 2 if using sequence number relative time locks

    Args:
        tx_ins      list(TxIn instances): list of transaction inputs
        tx_outs     list(TxOut instances): list of transaction outputs

        **kwargs:
        version     (int): transaction version number
        locktime    (hex): transaction locktime

    Returns:
        (Tx instance): unsigned transaction with empty witness
    '''
    return tb.make_tx(
        version=kwargs['version'] if 'version' in kwargs else 2,
        tx_ins=tx_ins,
        tx_outs=tx_outs,
        lock_time=kwargs['lock_time'] if 'lock_time' in kwargs else 0,
        tx_witnesses=[tb.make_empty_witness() for _ in tx_ins])
