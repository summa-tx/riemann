import multicoin
from .script import examples
from .script import serialization as script_ser
from .tx import tx_builder as tb
from .encoding import addr


def guess_version():
    '''
    -> int
    Bitcoin uses tx type 2 for nSequence signaling.
    Zcash uses tx type 2 for joinsplits.

    We want to signal nSequence enforcement (just in case).
    Unless we're in zcash.
    '''
    if 'zcash' in multicoin.get_current_network():
        return 1
    else:
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


def simple_output(value, address):
    '''
    int, str -> TxOut
    accepts base58 or bech32
    '''
    script = addr.parse(address)
    return tb.make_output(value, script)


def simple_p2pkh_input(outpoint, sig, pubkey, sequence=0xFFFFFFFE):
    '''
    OutPoint, hex_string, hex_string, int -> TxIn
    '''
    script_sig = examples.p2pkh_script_sig.format(sig, pubkey)
    return tb.make_legacy_input(outpoint, script_sig, None, sequence)


def simple_p2pkh_input_and_witness(outpoint, sig, pubkey, sequence=0xFFFFFFFE):
    '''
    OutPoint, hex_string, hex_string, int -> (TxIn, InputWitness)
    '''
    script_sig = examples.p2pkh_script_sig.format(sig, pubkey)
    return tb.make_legacy_input_and_empty_witness(
        outpoint, script_sig, None, sequence)


def simple_p2sh_input(outpoint, stack_script, redeem_script, sequence=None):
    '''
    OutPoint, str, str, int -> TxIn
    '''
    if sequence is None:
        sequence = guess_sequence(redeem_script)

    return tb.make_legacy_input(outpoint, stack_script,
                                redeem_script, sequence)


def simple_p2sh_input_and_witness(outpoint, stack_script,
                                  redeem_script, sequence=None):
    '''
    OutPoint, str, str, int -> (TxIn, InputWitness)
    '''
    if sequence is None:
        sequence = guess_sequence(redeem_script)

    return tb.make_legacy_input_and_empty_witness(
        outpoint, stack_script, redeem_script, sequence)


def simple_p2wpkh_input_and_witness(outpoint, sig,
                                    pubkey, sequence=0xFFFFFFFE):
    '''
    Outpoint, hex_string, hex_string, int -> (TxIn, InputWitness)
    '''
    return tb.make_witness_input_and_witness(outpoint, sequence, [sig, pubkey])


def simple_p2wsh_input_and_witness(outpoint, stack,
                                   witness_script, sequence=None):
    '''
    Outpoint, str, str, int -> (TxIn, InputWitness)
    '''
    if sequence is None:
        sequence = guess_sequence(witness_script)

    stack = [item for item in stack]
    stack.append(script_ser.serialize_from_string(witness_script))

    return tb.make_witness_input_and_witness(outpoint, sequence, stack)


def simple_legacy_tx(tx_ins, tx_outs):
    version = guess_version()
    # Look at each input to guess lock_time
    lock_time = max(
        [guess_locktime(script_ser.deserialize_script(txin.script))
         for txin in tx_ins])

    return tb.make_tx(version=version,
                      tx_ins=tx_ins,
                      tx_outs=tx_outs,
                      lock_time=lock_time,
                      tx_witnesses=None,
                      make_immutable=True)


def simple_witness_tx(tx_ins, tx_outs, tx_witnesses):
    version = guess_version()

    # Parse legacy scripts AND witness scripts for OP_CLTV
    times = [guess_locktime(script_ser.deserialize_script(txin.script))
             for txin in tx_ins if txin.script is not None]
    times.extend([guess_locktime(script_ser.deserialize_script(wit[::-1]))
                  for wit in tx_witnesses])
    lock_time = max(times)

    return tb.make_tx(version=version,
                      tx_ins=tx_ins,
                      tx_outs=tx_outs,
                      lock_time=lock_time,
                      tx_witnesses=tx_witnesses,
                      make_immutable=True)
