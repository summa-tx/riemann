# import tx
import multicoin
from . import utils
from .script import parsing


def make_sh_output_script(script_string, witness=False):
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
    output_script = bytearray()

    if type(pubkey) is not bytearray and type(pubkey) is not bytes:
        raise ValueError('Unknown pubkey format. '
                         'Expected bytes. Got: {}'.format(type(pubkey)))

    pubkey_hash = utils.hash160(pubkey)

    prefix = \
        multicoin.network.P2PKH_PREFIX if not witness \
        else multicoin.network.P2WPKH_PREFIX

    output_script.apppend(prefix)
    output_script.append(pubkey_hash)

    return output_script


def make_p2sh_output_script(script_string):
    return make_sh_output_script(script_string, witness=False)


def make_p2pkh_output_script(pubkey):
    return make_pkh_output_script(pubkey, witness=False)


def make_p2wsh_output_script(script_string):
        return make_sh_output_script(script_string, witness=True)


def make_p2wpkh_output_script(pubkey):
    return make_pkh_output_script(pubkey, witness=True)
