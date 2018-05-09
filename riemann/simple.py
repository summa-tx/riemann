import riemann
from . import utils
from .script import examples
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
    if 'zcash' in riemann.get_current_network_name():
        return 1
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
        script=b'',
        version=b'\x00' * 2)


def outpoint(tx_id, index, tree=None):
    '''
    hex_str, int, int -> Outpoint
    '''
    tx_id_le = bytes.fromhex(tx_id)[::-1]  # accepts block explorer txid string
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


def unsigned_input(outpoint, redeem_script=b'', sequence=0xFFFFFFFE):
    '''
    Outpoint, byte-like, int -> TxIn
    '''
    if redeem_script != b'':
        sequence = guess_sequence(redeem_script)
        redeem_script = script_ser.serialize(redeem_script)
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
        sequence=b'\x00' * 4)


def p2pkh_input(outpoint, sig, pubkey, sequence=0xFFFFFFFE):
    '''
    OutPoint, hex_string, hex_string, int -> TxIn
    Create a signed legacy TxIn from a p2pkh prevout
    '''
    script_sig = examples.p2pkh_script_sig.format(sig, pubkey)
    return tb.make_legacy_input(outpoint, script_sig, None, sequence)


def p2pkh_input_and_witness(outpoint, sig, pubkey, sequence=0xFFFFFFFE):
    '''
    OutPoint, hex_string, hex_string, int -> (TxIn, InputWitness)
    Create a signed legacy TxIn from a p2pkh prevout
    Create an empty InputWitness for it
    Useful for transactions spending some witness and some legacy prevouts
    '''
    script_sig = examples.p2pkh_script_sig.format(sig, pubkey)
    return tb.make_legacy_input_and_empty_witness(
        outpoint, script_sig, None, sequence)


def p2sh_input(outpoint, stack_script, redeem_script, sequence=None):
    '''
    OutPoint, str, str, int -> TxIn
    Create a signed legacy TxIn from a p2pkh prevout
    '''
    if sequence is None:
        sequence = guess_sequence(redeem_script)

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
    return tb.make_witness_input_and_witness(outpoint, sequence, [sig, pubkey])


def p2wsh_input_and_witness(outpoint, stack, witness_script, sequence=None):
    '''
    Outpoint, str, str, int -> (TxIn, InputWitness)
    Create a signed witness TxIn and InputWitness from a p2wsh prevout
    '''
    if sequence is None:
        sequence = guess_sequence(witness_script)

    stack = [item for item in stack]
    stack.append(script_ser.serialize(witness_script))

    return tb.make_witness_input_and_witness(outpoint, sequence, stack)


def empty_input_witness():
    return tb.make_witness([])


def unsigned_tx(tx_ins, tx_outs, **kwargs):
    '''
    list(TxIn), list(TxOut) -> Tx
    Create an unsigned transaction
    Use this to generate sighashes for unsigned TxIns
    Gotcha: it requires you to know the timelock and version
            it will _not_ guess them
            becuase it may not have acess to all scripts
    Hint: set version to 2 if using sequence number relative time locks
    '''
    return tb.make_tx(
        version=kwargs['version'] if 'version' in kwargs else 1,
        tx_ins=tx_ins,
        tx_outs=tx_outs,
        lock_time=kwargs['lock_time'] if 'lock_time' in kwargs else 0)


def legacy_tx(tx_ins, tx_outs):
    '''
    list(TxIn), list(TxOut) -> Tx
    Construct a fully-signed legacy transaction
    '''

    # Look at each input to guess lock_time and version
    deser = [script_ser.deserialize(txin.script) for txin in tx_ins]
    version = max([guess_version(d) for d in deser])
    lock_time = max([guess_locktime(d) for d in deser])

    return tb.make_tx(version=version,
                      tx_ins=tx_ins,
                      tx_outs=tx_outs,
                      lock_time=lock_time,
                      tx_witnesses=None)


def witness_tx(tx_ins, tx_outs, tx_witnesses):
    '''
    list(TxIn), list(TxOut), list(InputWitness) -> Tx
    Construct a fully-signed witness transaction
    '''
    # Parse legacy scripts AND witness scripts for OP_CLTV
    deser = [script_ser.deserialize(tx_in.redeem_script) for tx_in in tx_ins
             if tx_in is not None]
    deser += [script_ser.deserialize(wit[::-1]) for wit in tx_witnesses]
    version = max([guess_version(d) for d in deser])
    lock_time = max([guess_locktime(d) for d in deser])

    return tb.make_tx(
        version=version,
        tx_ins=tx_ins,
        tx_outs=tx_outs,
        lock_time=lock_time,
        tx_witnesses=tx_witnesses)
