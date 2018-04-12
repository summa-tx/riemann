import math
from . import utils


class Serializable(bytearray):

    def make_immutable(self):
        return bytes(self)


class VarInt(Serializable):
    def __init__(self, number):
        if number < 0x0:
            raise ValueError('VarInt cannot be less than 0. '
                             'Got: {}'.format(number))
        if number > 0xffffffffffffffff:
            raise ValueError('VarInt cannot be greater than (2 ** 64) - 1. '
                             'Got: {}'
                             .format(number))
        if number <= 0xfc:
            pass  # No prefix
        elif number <= 0xffff:
            self += bytes([0xfd])
        elif number <= 0xffffffff:
            self += bytes([0xfe])
        elif number <= 0xffffffffffffffff:
            self += bytes([0xff])
        self += utils.i2le(number)
        while len(self) > 1 and math.log(len(self) - 1, 2) % 1 != 0:
            self += bytes([0x00])

        self.number = number


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

        self.tx_id = tx_id
        self.index = index


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
        self += VarInt(len(script))
        self += script
        self += sequence

        self.outpoint = outpoint
        self.script_len = len(script)
        self.script = script
        self.sequence = sequence


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
                'Expected bytearray. Got: {}'
                .format(type(pk_script)))

        self += value
        self += VarInt(len(pk_script))
        self += pk_script

        self.value = value
        self.pk_script_len = len(pk_script)
        self.pk_script = pk_script


class StackItem(Serializable):

    def __init__(self, item):
        if not isinstance(item, bytearray):
            raise ValueError(
                'Invalid item. '
                'Expected bytearray. Got {}'
                .format(item))

        self += VarInt(len(item))
        self += item

        self.item_len = len(item)
        self.item = item


class TxWitness(Serializable):

    def __init__(self, stack):
        for item in stack:
            if not isinstance(item, StackItem):
                raise ValueError(
                    'Invalid witness stack item. '
                    'Expected bytes. Got {}'
                    .format(item))
        self += VarInt(len(stack))
        for item in stack:
            self += item

        self.stack_len = len(stack)
        self.stack = [item for item in stack]


class Tx(Serializable):

    def __init__(self, version, flag, tx_ins,
                 tx_outs, tx_witnesses, lock_time):
        if not isinstance(version, bytearray) or len(version) != 4:
            raise ValueError(
                'Invalid version. '
                'Expected 4 bytes. Got: {}'
                .format(version))

        if flag is not None:
            if flag != b'\x00\x01':
                raise ValueError(
                    'Invald segwit flag. '
                    'Expected None or {}. Got: {}'
                    .format(b'\x00\x01', flag))
            if tx_witnesses is None:
                raise ValueError('Got segwit flag but no witnesses')

        if tx_witnesses is not None:
            if flag is None:
                raise ValueError('Got witnesses but no segwit flag.')
            if len(tx_witnesses) != len(tx_ins):
                raise ValueError(
                    'Witness and TxIn lists must be same length. '
                    'Got {} inputs and {} witnesses.'
                    .format(len(tx_ins), len(tx_witnesses)))
            for witness in tx_witnesses:
                if not isinstance(witness, TxWitness):
                    raise ValueError(
                        'Invalid TxWitness.'
                        'Expected instance of TxWitness. Got {}'
                        .format(type(witness)))

        if max(len(tx_ins), len(tx_outs)) > 255:
            raise ValueError('Too many inputs or outputs. Stop that.')

        if min(len(tx_ins), len(tx_outs)) == 0:
            raise ValueError('Too few inputs or outputs. Stop that.')

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

        if not isinstance(lock_time, bytearray):
            raise ValueError(
                'Invalid lock_time. '
                'Expected 4 bytes. Got: {}'
                .format(lock_time))

        self += version
        if flag is not None:
            self += flag
        self += VarInt(len(tx_ins))
        for tx_in in tx_ins:
            self += tx_in
        self += VarInt(len(tx_outs))
        for tx_out in tx_outs:
            self += tx_out
        if tx_witnesses is not None:
            for witness in tx_witnesses:
                self += witness
        self += lock_time

        self.version = version
        self.flag = flag
        self.tx_ins_len = len(tx_ins)
        self.tx_ins = [tx_in for tx_in in tx_ins]
        self.tx_outs_len = len(tx_outs)
        self.tx_outs = [tx_out for tx_out in tx_outs]
        self.tx_witnesses_len = self.tx_ins_len
        self.tx_witnesses = \
            [wit for wit in tx_witnesses] if tx_witnesses is not None else None
        self.lock_time = lock_time

        if flag is not None:
            self.tx_id_le = utils.hash256(self.no_witness())
            self.wtx_id_le = utils.hash256(self.make_immutable())
            self.tx_id = utils.change_endianness(self.tx_id_le)
            self.wtx_id = utils.change_endianness(self.wtx_id_le)

        else:
            self.tx_id_le = utils.hash256(self.make_immutable())
            self.tx_id = utils.change_endianness(self.tx_id_le)
            self.wtx_id = None
            self.wtx_le = None

        if len(self) > 100000:
            raise ValueError(
                'Tx is too large.'
                'Expect less than 100kB. Got: {} bytes'.format(len(self)))

    def no_witness(self):
        tx = bytes()
        tx += self.version
        tx += VarInt(len(self.tx_ins))
        for tx_in in self.tx_ins:
            tx += tx_in
        tx += VarInt(len(self.tx_outs))
        for tx_out in self.tx_outs:
            tx += tx_out
        tx += self.lock_time
        return bytes(tx)
