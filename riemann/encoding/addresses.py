import riemann
from riemann import utils
from riemann.script import serialization as script_ser


def _hash_to_sh_address(
        script_hash: bytes,
        witness: bool = False,
        cashaddr: bool = True) -> str:
    '''
    Turns a script hash into a SH address. Prefers Cashaddrs to legacy
    addresses whenever supported.

    Args:
        script_hash: The 20 or 32 byte hash of the script
        witness:      Pass True to generate a witness address if supported.
                      Default False.
        cashaddr:     Pass False to prefer legacy to cashaddr. Default True
    Returns:
        The encoded address
    '''
    addr_bytes = bytearray()
    if riemann.network.CASHADDR_P2SH is not None and cashaddr:
        addr_bytes.extend(riemann.network.CASHADDR_P2SH)
        addr_bytes.extend(script_hash)
        return riemann.network.CASHADDR_ENCODER.encode(addr_bytes)
    if witness:
        addr_bytes.extend(riemann.network.P2WSH_PREFIX)
        addr_bytes.extend(script_hash)
        return riemann.network.SEGWIT_ENCODER.encode(addr_bytes)
    else:
        addr_bytes.extend(riemann.network.P2SH_PREFIX)
        addr_bytes.extend(script_hash)
        return riemann.network.LEGACY_ENCODER.encode(addr_bytes)


def _ser_script_to_sh_address(
        script_bytes: bytes,
        witness: bool = False,
        cashaddr: bool = True) -> str:
    '''
    Turns a serialized script into a SH address. Prefers Cashaddrs to legacy
    addresses whenever supported.

    Args:
        script_bytes: The serialized script, as a bytestring
        witness:      Pass True to generate a witness address if supported.
                      Default False.
        cashaddr:     Pass False to prefer legacy to cashaddr. Default True

    Returns:
        The encoded address
    '''
    if witness:
        script_hash = utils.sha256(script_bytes)
    else:
        script_hash = utils.hash160(script_bytes)
    return _hash_to_sh_address(
        script_hash=script_hash,
        witness=witness,
        cashaddr=cashaddr)


def make_sh_address(
        script_string: str,
        witness: bool = False,
        cashaddr: bool = True) -> str:
    '''
    Turns a human-readable script into an address. Prefers Cashaddrs to legacy
    addresses whenever supported.

    Args:
        script_string: The human-readable script
        witness:       Pass True to generate a witness address if supported.
                       Default False.
        cashaddr:      Pass False to prefer legacy to cashaddr. Default True

    Returns:
        The encoded address
    '''
    script_bytes = script_ser.serialize(script_string)

    return _ser_script_to_sh_address(
        script_bytes=script_bytes,
        witness=witness,
        cashaddr=cashaddr)


def make_p2wsh_address(script_string: str) -> str:
    '''
    Turns a human-readable script into a p2wsh address

    Args:
        script_string: The human-readable script
    Returns:
        The encoded address
    '''
    return make_sh_address(script_string=script_string,
                           witness=True)


def make_p2sh_address(script_string: str) -> str:
    '''
    Turns a human-readable script into a p2sh address, cashaddr if possible

    Args:
        script_string: The human-readable script
    Returns:
        The encoded address
    '''
    return make_sh_address(script_string=script_string,
                           witness=False)


def make_legacy_p2sh_address(script_string: str) -> str:
    '''
    Turns a human-readable script into a non-cashaddr p2sh address

    Args:
        script_string: The human-readable script
    Returns:
        The encoded address
    '''
    return make_sh_address(script_string=script_string,
                           witness=False,
                           cashaddr=False)


def _make_pkh_address(
        pubkey_hash: bytes,
        witness: bool = False,
        cashaddr: bool = True) -> str:
    '''
    Turns a 20-byte public key has into an address

    Args:
        pubkey_hash: The 20 or 32 byte hash of the public key
        witness:      Pass True to generate a witness address if supported.
                      Default False.
        cashaddr:     Pass False to prefer legacy to cashaddr. Default True
    Returns:
        The encoded address
    '''
    addr_bytes = bytearray()
    if riemann.network.CASHADDR_P2PKH is not None and cashaddr:
        addr_bytes.extend(riemann.network.CASHADDR_P2PKH)
        addr_bytes.extend(pubkey_hash)
        return riemann.network.CASHADDR_ENCODER.encode(addr_bytes)
    if witness:
        addr_bytes.extend(riemann.network.P2WPKH_PREFIX)
        addr_bytes.extend(pubkey_hash)
        return riemann.network.SEGWIT_ENCODER.encode(addr_bytes)
    else:
        addr_bytes.extend(riemann.network.P2PKH_PREFIX)
        addr_bytes.extend(pubkey_hash)
        return riemann.network.LEGACY_ENCODER.encode(addr_bytes)


def make_pkh_address(
        pubkey: bytes,
        witness: bool = False,
        cashaddr: bool = True) -> str:
    '''
    Turns a pubkey into an address. Prefers Cashaddrs to legacy addresses
    whenever supported.

    Args:
        pubkey:       The 33 or 65 byte public key
        witness:      Pass True to generate a witness address if supported.
                      Default False.
        cashaddr:     Pass False to prefer legacy to cashaddr. Default True
    Returns:
        The encoded address
    '''
    pubkey_hash = utils.hash160(pubkey)
    return _make_pkh_address(pubkey_hash=pubkey_hash,
                             witness=witness,
                             cashaddr=cashaddr)


def make_p2wpkh_address(pubkey: bytes) -> str:
    '''
    Turns a pubkey into a p2wpkh address

    Args:
        pubkey:       The 33 or 65 byte public key
    Returns:
        The encoded address
    '''
    return make_pkh_address(pubkey=pubkey, witness=True)


def make_p2pkh_address(pubkey: bytes) -> str:
    '''
    Turns a pubkey into a p2pkh address, cashaddr if available

    Args:
        pubkey:       The 33 or 65 byte public key
    Returns:
        The encoded address
    '''
    return make_pkh_address(pubkey=pubkey, witness=False)


def make_legacy_p2pkh_address(pubkey: bytes) -> str:
    '''
    Turns a pubkey into a legacy p2pkh address

    Args:
        pubkey:       The 33 or 65 byte public key
    Returns:
        The encoded address
    '''
    return make_pkh_address(pubkey=pubkey, witness=False, cashaddr=False)


def parse(address: str) -> bytes:
    '''
    Decode an address to the underlying raw bytes

    Args:
        address: The address to parse
    Returns:
        The raw bytestring encoded by the address
    '''
    try:
        return bytearray(riemann.network.LEGACY_ENCODER.decode(address))
    except ValueError:
        pass

    try:
        return bytearray(riemann.network.SEGWIT_ENCODER.decode(address))
    except Exception:
        pass

    try:
        return bytearray(riemann.network.CASHADDR_ENCODER.decode(address))
    except Exception:
        pass

    raise ValueError(
        'Unsupported address format. Got: {}'.format(address))


def to_output_script(address: str) -> bytes:
    '''
    Convert an address into its associated output script.

    Args:
        address: The address to parse
    Returns:
        The output script that corresponds to the address, suitable for
        inclusion in a TxOut
    '''
    parsed = parse(address)
    parsed_hash = b''

    try:
        if (parsed.find(riemann.network.P2WPKH_PREFIX) == 0
                and len(parsed) == 22):
            return parsed
    except TypeError:
        pass

    try:
        if (parsed.find(riemann.network.P2WSH_PREFIX) == 0
                and len(parsed) == 34):
            return parsed
    except TypeError:
        pass

    try:
        if (parsed.find(riemann.network.CASHADDR_P2SH) == 0
                and len(parsed) == len(riemann.network.CASHADDR_P2SH) + 20):
            prefix = b'\xa9\x14'  # OP_HASH160 PUSH14
            parsed_hash = parsed[len(riemann.network.P2SH_PREFIX):]
            suffix = b'\x87'  # OP_EQUAL
    except TypeError:
        pass

    try:
        if (parsed.find(riemann.network.CASHADDR_P2PKH) == 0
                and len(parsed) == len(riemann.network.CASHADDR_P2PKH) + 20):
            prefix = b'\x76\xa9\x14'  # OP_DUP OP_HASH160 PUSH14
            parsed_hash = parsed[len(riemann.network.P2PKH_PREFIX):]
            suffix = b'\x88\xac'  # OP_EQUALVERIFY OP_CHECKSIG
    except TypeError:
        pass

    if (parsed.find(riemann.network.P2PKH_PREFIX) == 0
            and len(parsed) == len(riemann.network.P2PKH_PREFIX) + 20):
        prefix = b'\x76\xa9\x14'  # OP_DUP OP_HASH160 PUSH14
        parsed_hash = parsed[len(riemann.network.P2PKH_PREFIX):]
        suffix = b'\x88\xac'  # OP_EQUALVERIFY OP_CHECKSIG

    if (parsed.find(riemann.network.P2SH_PREFIX) == 0
            and len(parsed) == len(riemann.network.P2SH_PREFIX) + 20):
        prefix = b'\xa9\x14'  # OP_HASH160 PUSH14
        parsed_hash = parsed[len(riemann.network.P2SH_PREFIX):]
        suffix = b'\x87'  # OP_EQUAL

    if parsed_hash == b'':
        raise ValueError('Cannot parse output script from address.')

    output_script = prefix + parsed_hash + suffix
    return output_script


def from_output_script(output_script: bytes, cashaddr: bool = True) -> str:
    '''
    Convert an output script (the on-chain format) to an address

    Args:
        output_script: The output script to encode as an address
        cashaddr: Pass False to prefer legacy to cashaddr. Default True.
    '''
    try:
        if (len(output_script) == len(riemann.network.P2WSH_PREFIX) + 32
                and output_script.find(riemann.network.P2WSH_PREFIX) == 0):
            # Script hash is the last 32 bytes
            return _hash_to_sh_address(
                output_script[-32:], witness=True, cashaddr=cashaddr)
    except TypeError:
        pass
    try:
        if (len(output_script) == len(riemann.network.P2WPKH_PREFIX) + 20
                and output_script.find(riemann.network.P2WPKH_PREFIX) == 0):
            # PKH is the last 20 bytes
            return _make_pkh_address(
                output_script[-20:], witness=True, cashaddr=cashaddr)
    except TypeError:
        pass

    if len(output_script) == 25 and output_script.find(b'\x76\xa9\x14') == 0:
        return _make_pkh_address(
            output_script[3:23], witness=False, cashaddr=cashaddr)

    elif len(output_script) == 23 and output_script.find(b'\xa9\x14') == 0:
        return _hash_to_sh_address(
            output_script[2:22], witness=False, cashaddr=cashaddr)

    raise ValueError('Cannot parse address from script.')


def parse_hash(address: str) -> bytes:
    '''
    Extract the pubkey or script hash encoded in an address

    Args:
        address: The address to parse
    Returns:
        The 20 or 32 byte hash represented by the address
    '''
    raw = parse(address)

    # Cash addresses
    try:
        if address.find(riemann.network.CASHADDR_PREFIX) == 0:
            if raw.find(riemann.network.CASHADDR_P2SH) == 0:
                return raw[len(riemann.network.CASHADDR_P2SH):]
            if raw.find(riemann.network.CASHADDR_P2PKH) == 0:
                return raw[len(riemann.network.CASHADDR_P2PKH):]
    except TypeError:
        pass

    # Segwit addresses
    try:
        if address.find(riemann.network.BECH32_HRP) == 0:
            if raw.find(riemann.network.P2WSH_PREFIX) == 0:
                return raw[len(riemann.network.P2WSH_PREFIX):]
            if raw.find(riemann.network.P2WPKH_PREFIX) == 0:
                return raw[len(riemann.network.P2WPKH_PREFIX):]
    except TypeError:
        pass

    # Legacy Addresses
    if raw.find(riemann.network.P2SH_PREFIX) == 0:
        return raw[len(riemann.network.P2SH_PREFIX):]
    if raw.find(riemann.network.P2PKH_PREFIX) == 0:
        return raw[len(riemann.network.P2PKH_PREFIX):]

    raise ValueError('Could not parse hash, unknown error')
