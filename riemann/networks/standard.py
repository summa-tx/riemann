from riemann import tx
from riemann import utils as rutils
from riemann.encoding import addresses as addr
from riemann.script import serialization as ser
from riemann.script import opcodes

MAX_STANDARD_TX_WEIGHT = 400000
MIN_STANDARD_TX_NONWITNESS_SIZE = 82


def check_is_standard_tx(t: tx.Tx) -> bool:
    '''
    Analog of Bitcoin's IsStandardTx
    Args:
        t (tx.Tx): the transaction
    Returns:
        (bool): True for standard, false for non-standard
    '''
    # 'version'
    if t.version[0] not in [1, 2]:
        return False

    # 'tx-size'
    if len(t.no_witness()) * 3 + len(t) > MAX_STANDARD_TX_WEIGHT:
        return False

    for tx_in in t.tx_ins:
        try:
            # 'scriptsig-size'
            # 'scriptsig-not-pushonly'
            if (len(tx_in.script_sig) > 1650
                    or not is_push_only(tx_in.script_sig)):
                return False
        except Exception:
            return False

    # 'scriptpubkey'
    # 'dust'
    # 'multi-op-return'
    if not check_is_standard(t):
        return False

    return True


def is_push_only(script_sig: bytes) -> bool:
    '''
    Determines whether a script is push-only
    Does this by parsing, and inspecting non-data elements
    Args:
        script_sig (bytes): the scriptSig
    Returns:
        (bool): True if Push Only, otherwise False
    '''
    script = ser.deserialize(script_sig)
    non_data_opcodes = [t for t in script if t[0:3] == 'OP_']
    for token in non_data_opcodes:
        integer_opcode = opcodes.CODE_TO_INT[token]
        if (integer_opcode in [79, 80]
                or integer_opcode >= 97):
            return False
    return True


def check_is_standard(t: tx.Tx) -> bool:
    '''
    Analog of Bitcoin's IsStandard
    Args:
        t (tx.Tx): the transaction to check
    Returns:
        (bool): True for standard, false for non-standard
    '''
    for o in t.tx_outs:
        # 'scriptpubkey'
        if not is_standard_output_type(o):
            return False

        # 'dust'
        if (rutils.le2i(o.value) < 550
                and o.output_script[:2] != b'\x00\x14'):
            return False

    # 'multi-op-return'
    if len([is_op_return(o) for o in t.tx_outs]) > 1:
        return False

    return True


def is_op_return(o: tx.TxOut) -> bool:
    '''
    Checks whether a txout is standard TX_NULL_DATA op_return output
    Args:
        o (tx.TxOut): the output
    Returns:
        (bool): True if standard opreturn, otherwise false
    '''
    script: str = ser.deserialize(o.output_script)
    split_script = script.split()

    # TX_NULL_DATA, up to 83 bytes (80 for safety)
    if (rutils.le2i(o.value) == 0
            and split_script[0] == 'OP_RETURN'
            and len(script) < 80):
        return True
    return False


def is_standard_output_type(o: tx.TxOut) -> bool:
    '''
    Checks standardness of an output based on its value and output script
    Args:
        o (tx.TxOut): the output the check
    Returns:
        (bool): True if standard, False otherwise
    '''
    # TX_SCRIPTHASH
    # TX_WITNESS_V0_KEYHASH
    # TX_WITNESS_V0_SCRIPTHASH
    # TX_PUBKEYHASH
    try:
        addr.from_output_script(o.output_script)
        return True
    except ValueError:
        pass

    script: str = ser.deserialize(o.output_script)
    split_script = script.split()

    # TX_PUBKEY
    if (split_script[-1] == 'OP_CHECKSIG'
            and len(split_script) == 2
            and len(bytes.fromhex(split_script[1])) in [33, 65]):
        return True

    # TX_MULTISIG, up to x-of-3
    if (split_script[-1] == 'OP_CHECKMULTISIG'
            and split_script[-2] in ['OP_1', 'OP_2', 'OP_3']):

        num_pubkeys = int(split_script[-2][-1])
        num_sigs = int(split_script[0][-1])

        if (num_sigs > num_pubkeys  # 3-of-2, or 16-of-3, or something
                or len(split_script) != num_pubkeys + 3):  # some junk script
            return False
        for pubkey in split_script[1:-2]:
            if len(bytes.fromhex(pubkey)) not in [33, 65]:
                return False
        return True

    # TX_NONSTANDARD/TX_WITNESS_UNKNOWN
    return False


def check_tx_size_small(t: tx.Tx) -> bool:
    '''
    Args:
        t (tx.Tx): the transaction
    Returns:
        (bool): True for standard, False for non-standard
    '''
    return len(t.no_witness()) >= MIN_STANDARD_TX_NONWITNESS_SIZE


def check_final(
        t: tx.Tx,
        best_height: int = 0,
        best_timestamp: int = 0) -> bool:
    '''
    Checks absolute locktime of a transaction.
    Pass in the best height and timestamp
    Args:
        t               (tx.Tx): the transaction
        best_height     (int): best known Bitcoin height
        best_timestamp  (int): best known Bitcoin timestamp
    '''
    lock = rutils.le2i(t.lock_time)
    if lock >= 500_000_000:  # timelocked
        return lock <= best_timestamp
    else:  # height-locked
        return lock <= best_height


def check_bip68_final():
    ...


def check_nonstandard_inputs():
    ...


def check_witness_nonstandard():
    ...


def check_too_many_sigops():
    ...


def check_non_mandatory_script():
    ...
