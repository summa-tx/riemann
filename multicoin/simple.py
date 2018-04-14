import multicoin
# from .script import serialization as script_ser
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


def build_output(value, address):
    script = addr.parse(address)
    return tb.make_output(value, script)
