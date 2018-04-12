# import tx
import multicoin
from . import utils
from .script import parsing


def make_p2sh_output_script(script_string):
    output_script = bytearray()

    script_bytes = parsing.serialize_from_string(script_string)
    script_hash = utils.hash160(script_bytes)

    output_script.extend(multicoin.network.P2SH_PREFIX)
    output_script.extend(script_hash)

    return output_script
