import riemann
from . import utils
from .script import serialization as script_ser
from .tx import tx_builder as tb
from .encoding import addresses as addr


def guess_version(redeem_script):
    '''
    str -> int
    Bitcoin uses tx version 2 for nSequence signaling.
    Zcash uses tx version 2 for joinsplits.

    We want to signal nSequence if we're using OP_CSV.
    Unless we're in zcash.
    '''
    n = riemann.get_current_network_name()
    if 'sprout' in n:
        return 1
    if 'overwinter' in n:
        return 3
    if 'sapling' in n:
        return 4
    try:
        script_array = redeem_script.split()
        script_array.index('OP_CHECKSEQUENCEVERIFY')
        return 2
    except ValueError:
        return 1  # Enable lock_time, disable RBF


def guess_sequence(redeem_script):
    '''
    str -> int
    If OP_CSV is used, guess an appropriate sequence
    Otherwise, disable RBF, but leave lock_time on.
    Fails if there's not a constant before OP_CSV
    '''
    try:
        script_array = redeem_script.split()
        loc = script_array.index('OP_CHECKSEQUENCEVERIFY')
        return int(script_array[loc - 1], 16)
    except ValueError:
        return 0xFFFFFFFE  # Enable lock_time, disable RBF


def guess_locktime(redeem_script):
    '''
    str -> int
    If OP_CLTV is used, guess an appropriate lock_time
    Otherwise return 0 (no lock time)
    Fails if there's not a constant before OP_CLTV
    '''
    try:
        script_array = redeem_script.split()
        loc = script_array.index('OP_CHECKLOCKTIMEVERIFY')
        return int(script_array[loc - 1], 16)
    except ValueError:
        return 0  # Enable lock_time, disable RBF


def output(value, address):
    '''
    int, str -> TxOut
    accepts base58 or bech32 addresses
    '''
    script = addr.to_output_script(address)
    value = utils.i2le_padded(value, 8)
    return tb._make_output(value, script)


def empty_output():
    '''
    -> Output
    Empty TxOut for partial txns or sighash_single signing
    The value is -1, which is standard for null TxOuts
    '''
    return tb._make_output(
        value=b'\xff' * 8,
        output_script=b'',
        version=b'\x00' * 2)


def outpoint(tx_id, index, tree=None):
    '''
    hex_str, int, int -> Outpoint
    accepts block explorer txid string
    '''
    tx_id_le = bytes.fromhex(tx_id)[::-1]
    return tb.make_outpoint(tx_id_le, index, tree)


def empty_outpoint():
    '''
    -> Outpoint
    Empty Outpoint for partial txns or sighash_single signing
    '''
    return tb.make_outpoint(
        tx_id_le=b'\x00' * 32,
        index=0,
        tree=b'\x00')


def unsigned_input(outpoint, redeem_script=None, sequence=None):
    '''
    Outpoint, byte-like, int -> TxIn
    '''
    if redeem_script is not None and sequence is None:
        sequence = guess_sequence(redeem_script)
    if sequence is None:
        sequence = 0xFFFFFFFE
    return tb.make_legacy_input(
        outpoint=outpoint,
        stack_script=b'',
        redeem_script=b'',
        sequence=sequence)


def empty_input():
    '''
    -> TxIn
    Empty TxIn for partial txns or sighash_single signing
    '''
    return tb.make_witness_input(
        outpoint=empty_outpoint(),
        sequence=0)


def p2pkh_input(outpoint, sig, pubkey, sequence=0xFFFFFFFE):
    '''
    OutPoint, hex_string, hex_string, int -> TxIn
    Create a signed legacy TxIn from a p2pkh prevout
    '''
    stack_script = '{sig} {pk}'.format(sig=sig, pk=pubkey)
    stack_script = script_ser.serialize(stack_script)
    return tb.make_legacy_input(outpoint, stack_script, b'', sequence)


def p2pkh_input_and_witness(outpoint, sig, pubkey, sequence=0xFFFFFFFE):
    '''
    OutPoint, hex_string, hex_string, int -> (TxIn, InputWitness)
    Create a signed legacy TxIn from a p2pkh prevout
    Create an empty InputWitness for it
    Useful for transactions spending some witness and some legacy prevouts
    '''
    stack_script = '{sig} {pk}'.format(sig=sig, pk=pubkey)
    return tb.make_legacy_input_and_empty_witness(
        outpoint=outpoint,
        stack_script=script_ser.serialize(stack_script),
        redeem_script=b'',
        sequence=sequence)


def p2sh_input(outpoint, stack_script, redeem_script, sequence=None):
    '''
    OutPoint, str, str, int -> TxIn
    Create a signed legacy TxIn from a p2pkh prevout
    '''
    if sequence is None:
        sequence = guess_sequence(redeem_script)

    stack_script = script_ser.serialize(stack_script)
    redeem_script = script_ser.hex_serialize(redeem_script)
    redeem_script = script_ser.serialize(redeem_script)

    return tb.make_legacy_input(
        outpoint=outpoint,
        stack_script=stack_script,
        redeem_script=redeem_script,
        sequence=sequence)


def p2sh_input_and_witness(outpoint, stack_script,
                           redeem_script, sequence=None):
    '''
    OutPoint, str, str, int -> (TxIn, InputWitness)
    Create a signed legacy TxIn from a p2pkh prevout
    Create an empty InputWitness for it
    Useful for transactions spending some witness and some legacy prevouts
    '''
    if sequence is None:
        sequence = guess_sequence(redeem_script)

    stack_script = script_ser.serialize(stack_script)
    redeem_script = script_ser.hex_serialize(redeem_script)
    redeem_script = script_ser.serialize(redeem_script)

    return tb.make_legacy_input_and_empty_witness(
        outpoint=outpoint,
        stack_script=stack_script,
        redeem_script=redeem_script,
        sequence=sequence)


def p2wpkh_input_and_witness(outpoint, sig, pubkey, sequence=0xFFFFFFFE):
    '''
    Outpoint, hex_string, hex_string, int -> (TxIn, InputWitness)
    Create a signed witness TxIn and InputWitness from a p2wpkh prevout
    '''
    return tb.make_witness_input_and_witness(
        outpoint=outpoint,
        sequence=sequence,
        stack=[bytes.fromhex(sig), bytes.fromhex(pubkey)])


def p2wsh_input_and_witness(outpoint, stack, witness_script, sequence=None):
    '''
    Outpoint, str, str, int -> (TxIn, InputWitness)
    Create a signed witness TxIn and InputWitness from a p2wsh prevout
    '''
    if sequence is None:
        sequence = guess_sequence(witness_script)
    stack = list(map(
        lambda x: b'' if x == 'NONE' else bytes.fromhex(x), stack.split()))
    stack.append(script_ser.serialize(witness_script))
    return tb.make_witness_input_and_witness(outpoint, sequence, stack)


def empty_input_witness():
    return tb.make_witness([])


def unsigned_legacy_tx(tx_ins, tx_outs, **kwargs):
    '''Create an unsigned transaction
    Use this to generate sighashes for unsigned TxIns
    Gotcha: it requires you to know the timelock and version
            it will _not_ guess them
            becuase it may not have acess to all scripts
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
        version=kwargs['version'] if 'version' in kwargs else 1,
        tx_ins=tx_ins,
        tx_outs=tx_outs,
        lock_time=kwargs['lock_time'] if 'lock_time' in kwargs else 0,
        expiry=kwargs['expiry'] if 'expiry' in kwargs else 0,
        tx_joinsplits=(kwargs['tx_joinsplits']
                       if 'tx_joinsplits' in kwargs else None),
        joinsplit_pubkey=(kwargs['joinsplit_pubkey']
                          if 'joinsplit_pubkey' in kwargs
                          else None),
        joinsplit_sig=(kwargs['joinsplit_sig']
                       if 'joinsplit_sig' in kwargs else None))


def unsigned_witness_tx(tx_ins, tx_outs, **kwargs):
    '''Create an unsigned segwit transaction
    Create an unsigned segwit transaction
    Use this to generate sighashes for unsigned TxIns
    Gotcha: it requires you to know the timelock and version
            it will _not_ guess them
            becuase it may not have acess to all scripts
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
        version=kwargs['version'] if 'version' in kwargs else 1,
        tx_ins=tx_ins,
        tx_outs=tx_outs,
        lock_time=kwargs['lock_time'] if 'lock_time' in kwargs else 0,
        tx_witnesses=[tb.make_empty_witness() for _ in tx_ins])


def legacy_tx(tx_ins, tx_outs, **kwargs):
    '''
    Construct a fully-signed legacy transaction
    Args:
        tx_ins      list(TxIn instances): list of transaction inputs
        tx_outs     list(TxOut instances): list of transaction outputs

        **kwargs:
        version     (int): transaction version number
        locktime    (hex): transaction locktime
        expiry              (int): overwinter expiry time
        tx_joinsplits       (list): list of joinsplits transactions
        joinsplit_pubkey    (bytes): joinsplit public key
        joinsplit_sig       (bytes): joinsplit signature

    Returns:
        (Tx instance): signed transaction with empty witness
    '''

    # Look at each input to guess lock_time and version
    deser = [script_ser.deserialize(tx_in.redeem_script)
             for tx_in in tx_ins if tx_in.redeem_script is not None]
    version = max([guess_version(d) for d in deser])
    lock_time = max([guess_locktime(d) for d in deser])

    return tb.make_tx(
        version=version,
        tx_ins=tx_ins,
        tx_outs=tx_outs,
        lock_time=lock_time,
        tx_witnesses=None,
        expiry=kwargs['expiry'] if 'expiry' in kwargs else 0,
        tx_joinsplits=(kwargs['tx_joinsplits']
                       if 'tx_joinsplits' in kwargs else None),
        joinsplit_pubkey=(kwargs['joinsplit_pubkey']
                          if 'joinsplit_pubkey' in kwargs else None),
        joinsplit_sig=(kwargs['joinsplit_sig']
                       if 'joinsplit_sig' in kwargs else None))


def witness_tx(tx_ins, tx_outs, tx_witnesses):
    '''
    list(TxIn), list(TxOut), list(InputWitness) -> Tx
    Construct a fully-signed witness transaction
    '''
    # Parse legacy scripts AND witness scripts for OP_CLTV
    deser = [script_ser.deserialize(tx_in.redeem_script) for tx_in in tx_ins
             if tx_in is not None]
    for w in tx_witnesses:
        try:
            deser.append(script_ser.deserialize(w.stack[-1].item))
        except (NotImplementedError, ValueError):
            pass
    version = max([guess_version(d) for d in deser])
    lock_time = max([guess_locktime(d) for d in deser])

    return tb.make_tx(
        version=version,
        tx_ins=tx_ins,
        tx_outs=tx_outs,
        lock_time=lock_time,
        tx_witnesses=tx_witnesses)
