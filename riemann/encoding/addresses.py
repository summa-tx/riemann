import riemann
from .. import utils
from ..script import serialization as script_ser


def make_sh_address(script_string, witness=False):
    '''
    str, bool -> str
    '''
    addr_bytes = bytearray()
    script_bytes = script_ser.serialize(script_string)
    if witness:
        script_hash = utils.sha256(script_bytes)
        addr_bytes.extend(riemann.network.P2WSH_PREFIX)
        addr_bytes.extend(script_hash)
        return riemann.network.SEGWIT_ENCODER.encode(addr_bytes)
    else:
        script_hash = utils.hash160(script_bytes)
        addr_bytes.extend(riemann.network.P2SH_PREFIX)
        addr_bytes.extend(script_hash)
        return riemann.network.LEGACY_ENCODER.encode(addr_bytes)


def make_p2wsh_address(script_string):
    return make_sh_address(script_string, witness=True)


def make_p2sh_address(script_string):
    return make_sh_address(script_string, witness=False)


def make_pkh_address(pubkey, witness=False):
    '''
    bytes, bool -> str
    '''
    addr_bytes = bytearray()
    pubkey_hash = utils.hash160(pubkey)
    if witness:
        addr_bytes.extend(riemann.network.P2WPKH_PREFIX)
        addr_bytes.extend(pubkey_hash)
        return riemann.network.SEGWIT_ENCODER.encode(addr_bytes)
    else:
        addr_bytes.extend(riemann.network.P2PKH_PREFIX)
        addr_bytes.extend(pubkey_hash)
        return riemann.network.LEGACY_ENCODER.encode(addr_bytes)


def make_p2wpkh_address(pubkey):
    return make_pkh_address(pubkey, witness=True)


def make_p2pkh_address(pubkey):
    return make_pkh_address(pubkey, witness=False)


def parse(address):
    try:
        return bytearray(riemann.network.LEGACY_ENCODER.decode(address))
    except ValueError:
        try:
            return bytearray(riemann.network.SEGWIT_ENCODER.decode(address))
        except Exception:
            raise ValueError(
                'Unsupported address format. Got: {}'.format(address))


def to_output_script(address):
    '''
    There's probably a better way to do this
    '''
    parsed = parse(address)

    if parsed.find(riemann.network.P2WPKH_PREFIX) == 0:
        return parsed

    elif parsed.find(riemann.network.P2WSH_PREFIX) == 0:
        return parsed

    elif parsed.find(riemann.network.P2PKH_PREFIX) == 0:
        prefix = b'\x76\xa9\x14'
        parsed_hash = parsed[len(riemann.network.P2PKH_PREFIX):]
        suffix = b'\x88\xac'

    elif parsed.find(riemann.network.P2SH_PREFIX) == 0:
        prefix = b'\xa9'
        parsed_hash = parsed[len(riemann.network.P2SH_PREFIX):]
        suffix = b'\x87'

    else:
        raise ValueError('Cannot parse output script from address.')

    output_script = prefix + parsed_hash + suffix
    return output_script


def parse_hash(address):
    '''
    There's probably a better way to do this.
    '''

    raw = parse(address)

    if address.find(riemann.network.BECH32_HRP) == 0:
        if raw.find(riemann.network.P2WSH_PREFIX) == 0:
            return raw[len(riemann.network.P2WSH_PREFIX):]
        if raw.find(riemann.network.P2WPKH_PREFIX) == 0:
            return raw[len(riemann.network.P2WPKH_PREFIX):]
    else:
        if raw.find(riemann.network.P2SH_PREFIX) == 0:
            return raw[len(riemann.network.P2SH_PREFIX):]
        if raw.find(riemann.network.P2PKH_PREFIX) == 0:
            return raw[len(riemann.network.P2PKH_PREFIX):]
