import multicoin
import math
from .. import utils


class ByteData():

    __immutable = False

    def __init__(self):
        self._bytearray = bytearray()
        self._current = 0

    def __iter__(self):
        return self._bytearray

    def __next__(self):
        if self._current > len(self._bytearray):
            raise StopIteration
        self._current += 1
        return self._bytearray[self._current - 1]

    def __iadd__(self, other):
        if isinstance(other, bytes) or isinstance(other, bytearray):
            self._bytearray.extend(other)
        elif isinstance(other, ByteData):
            self._bytearray.extend(other._bytearray)
        else:
            raise TypeError('unsupported operand type(s) for +=: '
                            '{} and {}'.format(type(self), type(other)))
        return self

    def __ne__(self, other):
        if isinstance(other, bytes) or isinstance(other, bytearray):
            return self._bytearray != other
        elif isinstance(other, ByteData):
            return self._bytearray != other.bytearray

    def __eq__(self, other):
        return not self != other

    def __len__(self):
        return len(self._bytearray)

    def __setattr__(self, key, value):
        if self.__immutable:
            raise TypeError("%r cannot be written to." % self)
        object.__setattr__(self, key, value)

    def __repr__(self):
        return '{}: {}'.format(type(self).__name__, self._bytearray)

    def to_bytes(self):
        return bytes(self._bytearray)

    def hex(self):
        return self._bytearray.hex()

    def make_immutable(self):
        self._bytearray = bytes(self._bytearray)
        self.__immutable = True

    def find(self, substring):
        if isinstance(substring, ByteData):
            substring = ByteData.to_bytes
        return self._bytearray.find(substring)

    @staticmethod
    def validate_bytes(data, length=4):
        if (not isinstance(data, ByteData)
                and not isinstance(data, bytes)
                and not isinstance(data, bytearray)):
            raise ValueError('Expected byte-like object. '
                             'Got: {}'.format(type(data)))

        if length is None:
            return

        if len(data) != length:
            raise ValueError('Expected bytes-like object with length {}. '
                             'Got {} with length {}.'
                             .format(length, type(data), len(data)))


class VarInt(ByteData):
    def __init__(self, number, make_immutable=True):
        super().__init__()
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
        if make_immutable:
            self.make_immutable()


class Outpoint(ByteData):

    def __init__(self, tx_id, index, make_immutable=True):
        super().__init__()

        self.validate_bytes(tx_id, 32)
        self.validate_bytes(index, 4)

        self += tx_id
        self += index

        self.tx_id = tx_id
        self.index = index

        if make_immutable:
            self.make_immutable()


class TxIn(ByteData):

    def __init__(self, outpoint, stack_script, redeem_script,
                 sequence, make_immutable=True):
        super().__init__()

        self.validate_bytes(outpoint, 36)
        self.validate_bytes(stack_script, None)
        self.validate_bytes(redeem_script, None)

        self.validate_bytes(sequence, 4)

        self += outpoint
        self += VarInt(len(stack_script + redeem_script))
        self += stack_script
        self += redeem_script
        self += sequence

        self.outpoint = outpoint
        self.script_len = len(stack_script + redeem_script)
        self.stack_script = stack_script
        self.redeem_script = redeem_script
        self.sequence = sequence

        if make_immutable:
            self.make_immutable()


class TxOut(ByteData):

    def __init__(self, value, output_script, make_immutable=True):
        super().__init__()

        self.validate_bytes(value, 8)
        self.validate_bytes(output_script, None)

        self += value
        self += VarInt(len(output_script))
        self += output_script

        self.value = value
        self.output_script_len = len(output_script)
        self.output_script = output_script

        if make_immutable:
            self.make_immutable()


class WitnessStackItem(ByteData):

    def __init__(self, item, make_immutable=True):
        super().__init__()

        self.validate_bytes(item, None)

        self += VarInt(len(item))
        self += item

        self.item_len = len(item)
        self.item = item

        if make_immutable:
            self.make_immutable()


class InputWitness(ByteData):

    def __init__(self, stack, make_immutable=True):
        super().__init__()
        for item in stack:
            if not isinstance(item, WitnessStackItem):
                raise ValueError(
                    'Invalid witness stack item. '
                    'Expected bytes. Got {}'
                    .format(item))
        self += VarInt(len(stack))
        for item in stack:
            self += item

        self.stack_len = len(stack)
        self.stack = [item for item in stack]

        if make_immutable:
            self.make_immutable()


class Tx(ByteData):

    def __init__(self, version, flag, tx_ins,
                 tx_outs, tx_witnesses, lock_time,
                 make_immutable=True):

        super().__init__()

        self.validate_bytes(version, 4)
        self.validate_bytes(lock_time, 4)

        if flag is not None:
            if flag != multicoin.network.SEGWIT_TX_FLAG:
                raise ValueError(
                    'Invald segwit flag. '
                    'Expected None or {}. Got: {}'
                    .format(multicoin.networkself.SEGWIT_TX_FLAG, flag))
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
                if not isinstance(witness, InputWitness):
                    raise ValueError(
                        'Invalid InputWitness.'
                        'Expected instance of InputWitness. Got {}'
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
            self.wtx_id_le = utils.hash256(self.to_bytes())
            self.tx_id = utils.change_endianness(self.tx_id_le)
            self.wtx_id = utils.change_endianness(self.wtx_id_le)

        else:
            self.tx_id_le = utils.hash256(self.to_bytes())
            self.tx_id = utils.change_endianness(self.tx_id_le)
            self.wtx_id = None
            self.wtx_le = None

        if make_immutable:
            self.make_immutable()

        if len(self) > 100000:
            raise ValueError(
                'Tx is too large.'
                'Expect less than 100kB. Got: {} bytes'.format(len(self)))

    def no_witness(self):
        '''
        Tx -> bytes
        '''
        tx = bytes()
        tx += self.version
        tx += VarInt(len(self.tx_ins)).to_bytes()
        for tx_in in self.tx_ins:
            tx += tx_in.to_bytes()
        tx += VarInt(len(self.tx_outs)).to_bytes()
        for tx_out in self.tx_outs:
            tx += tx_out.to_bytes()
        tx += self.lock_time
        return bytes(tx)

    @property
    def size(self):
        '''
        Tx -> int
        size in bytes
        '''
        return len(self._bytearray)

    def sighash_single(self, index, anyone_can_pay=False):
        '''
        Tx, int, bool
        Sighashes suck
        '''
        pass

    def sighash_all(self, anyone_can_pay=False):
        pass

    def sighash_none(self):
        raise NotImplementedError('SIGHASH_NONE is a bad idea.')

    def calc_fee(self, input_values):
        '''
        Tx, list(int) -> int
        Inputs don't know their value without the whole chain.
        '''
        return \
            sum(input_values) \
            - sum([utils.le2i(o.value) for o in self.tx_outs])
