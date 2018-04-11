import binascii
import math


def lx(number):
    b = '%x' % number
    if len(b) & 1:
        b = '0' + b
    b = binascii.unhexlify(b)[::-1]
    return b


class Serializable(bytearray):
    @classmethod
    def from_hex_string(Class, h):
        return Class(binascii.unhexlify(h))


class VarInt(Serializable):
    def __init__(self, number):
        if number < 0x0:
            raise ValueError('VarInt cannot be less than 0. '
                             'Got: {}'.format(number))
        if number > 0xffffffffffffffff:
            raise ValueError('VarInt cannot be greater than 2 ** 64. '
                             'Got: 2 ** {}'
                             .format(int(math.log(number, 2))))
        if number <= 0xfc:
            pass  # No prefix
        elif number <= 0xffff:
            self += bytes([0xfd])
        elif number <= 0xffffffff:
            self += bytes([0xfe])
        elif number <= 0xffffffffffffffff:
            self += bytes([0xff])
        self += lx(number)
        while len(self) > 1 and math.log(len(self) - 1, 2) % 1 != 0:
            self += bytes([0x00])


class Outpoint(Serializable):

    def __init__(self, tx_id, index):

        if not isinstance(tx_id, bytearray) or len(tx_id) != 32:
            raise ValueError(
                'Invalid tx_id. '
                'Expected 32 bytes. Got: {}'
                .format(tx_id))

        if not isinstance(index, bytearray) or len(index) != 4:
            raise ValueError(
                'Invalid index. '
                'Expected 4 bytes. Got: {}'
                .format(index))

        self += tx_id
        self += index


class TxIn(Serializable):

    def __init__(self, outpoint, script, sequence):

        if not isinstance(outpoint, Outpoint):
            raise ValueError(
                'Invalid Outpoint. '
                'Expected Outpoint instance. Got: {}'
                .format(type(outpoint)))

        if not isinstance(script, bytearray):
            raise ValueError(
                'Invalid Script. '
                'Expected many bytes. Got: {}'
                .format(script))

        if not isinstance(sequence, bytearray):
            raise ValueError(
                'Invalid sequence. '
                'Expected 4 bytes. Got: {}'
                .format(sequence))

        self += outpoint
        self += VarInt([len(script)])
        self += script
        self += sequence


class TxOut(Serializable):

    def __init__(self, value, pk_script):

        if not isinstance(value, bytearray) or len(value) != 8:
            raise ValueError(
                'Invalid value. '
                'Expected 8 bytes. Got: {}'
                .format(value))

        if not isinstance(pk_script, bytearray):
            raise ValueError(
                'Invalid pk_script. '
                'Expected 8 bytes. Got: {}'
                .format(pk_script))

        self += value
        self += bytes([len(pk_script)])
        self += pk_script


class TxWitness(Serializable):

    def __init__(self, stack):
        for item in stack:
            if not isinstance(item, bytearray):
                raise ValueError(
                    'Invalid witness stack item. '
                    'Expected bytes. Got {}'
                    .format(item))
        self += bytes([len(stack)])
        self += stack


class Tx(Serializable):

    def __init__(self, version, flag, tx_ins,
                 tx_outs, tx_witnesses, lock_time):
        if not isinstance(version, bytearray) or len(version) != 4:
            raise ValueError(
                'Invalid version. '
                'Expected 4 bytes. Got: {}'
                .format(version))

        if flag is not None:
            if flag is not b'\x00\x01':
                raise ValueError(
                    'Invald segwit flag. '
                    'Expected None or {}. Got: {}'
                    .format(b'\x00\x01', flag))
            if tx_witnesses is None:
                raise ValueError('Got segwit flag but no witnesses')

        if flag is None and tx_witnesses is not None:
            raise ValueError('Got witnesses but no segwit flag.')

        if max(len(tx_ins), len(tx_outs), len(tx_witnesses)) > 255:
            raise ValueError('Too many inputs or outputs. Stop that.')

        for tx_in in tx_ins:
            if not isinstance(tx_in, TxIn):
                raise ValueError(
                    'Invalid TxIn.'
                    'Expected instance of TxIn. Got {}'
                    .format(type(tx_in)))

        for tx_out in tx_outs:
            if not isinstance(tx_out, TxOut):
                raise ValueError(
                    'Invalid TxOut.'
                    'Expected instance of TxOut. Got {}'
                    .format(type(tx_out)))

        for witness in tx_witnesses:
            if not isinstance(witness, TxWitness):
                raise ValueError(
                    'Invalid TxWitness.'
                    'Expected instance of TxWitness. Got {}'
                    .format(type(witness)))

        if not isinstance(lock_time, bytearray):
            raise ValueError(
                'Invalid lock_time. '
                'Expected 4 bytes. Got: {}'
                .format(lock_time))

        self += version
        if flag is not None:
            self += flag
        self += VarInt([len(tx_ins)])
        for tx_in in tx_ins:
            self += tx_in
        self += VarInt([len(tx_outs)])
        for tx_out in tx_outs:
            self += tx_out
        for witness in tx_witnesses:
            self += witness
        self += lock_time

        if len(self) > 100000:
            raise ValueError(
                'Tx is too large.'
                'Expect less than 100kB. Got: {} bytes'.format(len(self)))
