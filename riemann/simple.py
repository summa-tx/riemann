import riemann
from .script import examples
from .script import serialization as script_ser
from .tx import tx_builder as tb
from .encoding import addr


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
    script_array = redeem_script.split()
    loc = script_array.find('OP_CHECKSEQUENCEVERIFY')
    if loc == -1:
        return 1  # Enable lock_time, disable RBF
    return 2


def guess_sequence(redeem_script):
    '''
    str -> int
    If OP_CSV is used, guess an appropriate sequence
    Otherwise, disable RBF, but leave lock_time on.
    Fails if there's not a constant before OP_CSV
    '''
    script_array = redeem_script.split()
    loc = script_array.find('OP_CHECKSEQUENCEVERIFY')
    if loc == -1:
        return 0xFFFFFFFE  # Enable lock_time, disable RBF
    return int(script_array[loc - 1], 16)


def guess_locktime(redeem_script):
    '''
    str -> int
    If OP_CLTV is used, guess an appropriate lock_time
    Otherwise return 0 (no lock time)
    Fails if there's not a constant before OP_CLTV
    '''
    script_array = redeem_script.split()
    loc = script_array.find('OP_CHECKLOCKTIMEVERIFY')
    if loc == -1:
        return 0  # Enable lock_time, disable RBF
    return int(script_array[loc - 1], 16)


def output(value, address):
    '''
    int, str -> TxOut
    accepts base58 or bech32
    '''
    script = addr.parse(address)
    return tb.make_output(value, script)


def p2pkh_input(outpoint, sig, pubkey, sequence=0xFFFFFFFE):
    '''
    OutPoint, hex_string, hex_string, int -> TxIn
    '''
    script_sig = examples.p2pkh_script_sig.format(sig, pubkey)
    return tb.make_legacy_input(outpoint, script_sig, None, sequence)


def p2pkh_input_and_witness(outpoint, sig, pubkey, sequence=0xFFFFFFFE):
    '''
    OutPoint, hex_string, hex_string, int -> (TxIn, InputWitness)
    '''
    script_sig = examples.p2pkh_script_sig.format(sig, pubkey)
    return tb.make_legacy_input_and_empty_witness(
        outpoint, script_sig, None, sequence)


def p2sh_input(outpoint, stack_script, redeem_script, sequence=None):
    '''
    OutPoint, str, str, int -> TxIn
    '''
    if sequence is None:
        sequence = guess_sequence(redeem_script)

    return tb.make_legacy_input(outpoint, stack_script,
                                redeem_script, sequence)


def p2sh_input_and_witness(outpoint, stack_script,
                           redeem_script, sequence=None):
    '''
    OutPoint, str, str, int -> (TxIn, InputWitness)
    '''
    if sequence is None:
        sequence = guess_sequence(redeem_script)

    return tb.make_legacy_input_and_empty_witness(
        outpoint, stack_script, redeem_script, sequence)


def p2wpkh_input_and_witness(outpoint, sig, pubkey, sequence=0xFFFFFFFE):
    '''
    Outpoint, hex_string, hex_string, int -> (TxIn, InputWitness)
    '''
    return tb.make_witness_input_and_witness(outpoint, sequence, [sig, pubkey])


def p2wsh_input_and_witness(outpoint, stack, witness_script, sequence=None):
    '''
    Outpoint, str, str, int -> (TxIn, InputWitness)
    '''
    if sequence is None:
        sequence = guess_sequence(witness_script)

    stack = [item for item in stack]
    stack.append(script_ser.serialize(witness_script))

    return tb.make_witness_input_and_witness(outpoint, sequence, stack)


def legacy_tx(tx_ins, tx_outs):
    '''
    list(TxIn), list(TxOut) -> Tx
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
    '''
    # Parse legacy scripts AND witness scripts for OP_CLTV
    deser = [script_ser.deserialize(txin.script) for txin in tx_ins
             if txin is not None]
    deser += [script_ser.deserialize(wit[::-1]) for wit in tx_witnesses]
    version = max([guess_version(d) for d in deser])
    lock_time = max([guess_locktime(d) for d in deser])

    return tb.make_tx(version=version,
                      tx_ins=tx_ins,
                      tx_outs=tx_outs,
                      lock_time=lock_time,
                      tx_witnesses=tx_witnesses)
