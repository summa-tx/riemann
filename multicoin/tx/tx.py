import multicoin
import math
from .. import utils


SIGHASH_ALL = 0x01
SIGHASH_NONE = 0x02
SIGHASH_SINGLE = 0x3
SIGHASH_ANYONECANPAY = 0x80


class ByteData():
    '''
    Wrapper class for byte-like data.
    Iterable
    Can be made immutable.
    self._bytes is a bytearray object when mutable.
    self._bytes is a byte object when immutable.
    '''
    __immutable = False

    def __init__(self):
        self._bytes = bytearray()
        self._current = 0

    def __iter__(self):
        return self._bytes

    def __next__(self):
        if self._current > len(self._bytes):
            raise StopIteration
        self._current += 1
        return self._bytes[self._current - 1]

    def __iadd__(self, other):
        '''
        ByteData, bytes-like -> ByteData
        Define += operator.
        Extend self's bytes with other's bytes.
        '''
        if isinstance(other, bytes) or isinstance(other, bytearray):
            self._bytes.extend(other)
        elif isinstance(other, ByteData):
            self._bytes.extend(other._bytes)
        else:
            raise TypeError('unsupported operand type(s) for +=: '
                            '{} and {}'.format(type(self), type(other)))
        return self

    def __ne__(self, other):
        '''
        ByteData, bytes-like -> bool
        Define != operator.
        Compares self._bytes to other.
        '''
        if isinstance(other, bytes) or isinstance(other, bytearray):
            return self._bytes != other
        elif isinstance(other, ByteData):
            return self._bytes != other._bytes

    def __eq__(self, other):
        '''
        ByteData, bytes-like -> bool
        Define == operator.
        '''
        return not self != other

    def __len__(self):
        '''
        ByteData -> int
        '''
        return len(self._bytes)

    def __setattr__(self, key, value):
        if self.__immutable:
            raise TypeError("%r cannot be written to." % self)
        object.__setattr__(self, key, value)

    def __repr__(self):
        '''
        ByteData -> str
        '''
        return '{}: {}'.format(type(self).__name__, self._bytes)

    def to_bytes(self):
        '''
        ByteData -> bytes
        '''
        return bytes(self._bytes)

    def hex(self):
        '''
        ByteData -> hex_string
        '''
        return self._bytes.hex()

    def _make_immutable(self):
        '''
        Prevents any future changes to the object
        self._bytes = bytes(self._bytes)
        '''
        self.__immutable = True

    def find(self, substring):
        '''
        byte-like -> int
        Finds the index of substring
        '''
        if isinstance(substring, ByteData):
            substring = ByteData.to_bytes
        return self._bytes.find(substring)

    @staticmethod
    def validate_bytes(data, length=4):
        '''
        Raises ValueError if data is not bytes.
        Raises ValueError if len(data) is not length.
        Length may be None for unknown lengths (e.g. scripts).
        length=None will allow 0 length data.
        '''
        if (not isinstance(data, ByteData)
                and not isinstance(data, bytes)
                and not isinstance(data, bytearray)):
            raise ValueError('Expected bytes-like object. '
                             'Got: {}'.format(type(data)))

        if length is None:
            return

        if len(data) != length:
            raise ValueError('Expected bytes-like object with length {}. '
                             'Got {} with length {}.'
                             .format(length, type(data), len(data)))


class VarInt(ByteData):
    '''
    NB: number must be integer
    '''
    def __init__(self, number):
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

        self._make_immutable()

    def copy(self):
        return VarInt(self.number)


class Outpoint(ByteData):
    '''
    NB: Args must be little-endian
    '''

    def __init__(self, tx_id, index):
        super().__init__()

        self.validate_bytes(tx_id, 32)
        self.validate_bytes(index, 4)

        self += tx_id
        self += index

        self.tx_id = tx_id
        self.index = index

        self._make_immutable()

    def copy(self):
        raise NotImplementedError('Copying outpoints not currently supported.'
                                  'Please make a new instance.')


class TxIn(ByteData):
    '''
    Outpoint, bytes-like, bytes-like, bytes-like -> TxIn
    stack_script and redeem_script should already be serialized
    NB: sequence must be little-endian
    '''

    def __init__(self, outpoint, stack_script, redeem_script,
                 sequence):
        super().__init__()

        self.validate_bytes(outpoint, 36)
        self.validate_bytes(stack_script, None)
        self.validate_bytes(redeem_script, None)

        if len(stack_script) + len(redeem_script) > 1650:
            raise ValueError('Input script_sig is too long. '
                             'Expected <= 1650 bytes. Got {} bytes.'
                             .format(len(stack_script) + len(redeem_script)))

        self.validate_bytes(sequence, 4)

        self += outpoint
        self += VarInt(len(stack_script) + len(redeem_script))
        self += stack_script
        self += redeem_script
        self += sequence

        self.outpoint = outpoint
        self.script_len = len(stack_script + redeem_script)
        self.stack_script = stack_script
        self.redeem_script = redeem_script
        self.sequence = sequence

        self._make_immutable()

    def copy(self, outpoint=None, stack_script=None,
             redeem_script=None, sequence=None):
        '''
        TxIn -> TxIn
        '''
        return TxIn(
            outpoint=outpoint if outpoint is not None else self.outpoint,
            stack_script=(stack_script if stack_script is not None
                          else self.stack_script),
            redeem_script=(redeem_script if redeem_script is not None
                           else self.redeem_script),
            sequence=sequence if sequence is not None else self.sequence)


class TxOut(ByteData):
    '''
    NB: value must be little-endian
    '''

    def __init__(self, value, output_script):
        super().__init__()

        self.validate_bytes(value, 8)
        self.validate_bytes(output_script, None)

        if utils.le2i(value) <= 546:
            raise ValueError('Transaction value below dust limit. '
                             'Expected more than 546 sat. Got: {} sat.'
                             .format(utils.le2i(value)))

        self += value
        self += VarInt(len(output_script))
        self += output_script

        self.value = value
        self.output_script_len = len(output_script)
        self.output_script = output_script

        self._make_immutable()

    def copy(self, value=None, output_script=None):
        return TxOut(
            value=value if value is not None else self.value,
            output_script=(output_script if output_script is not None
                           else self.output_script))


class WitnessStackItem(ByteData):

    def __init__(self, item):
        super().__init__()

        self.validate_bytes(item, None)

        self += VarInt(len(item))
        self += item

        self.item_len = len(item)
        self.item = item

        self._make_immutable()


class InputWitness(ByteData):

    def __init__(self, stack):
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

        self._make_immutable()


class Tx(ByteData):
    '''
    byte-like, byte-like, list(TxIn),
    list(TxOut), list(InputWitness), byte-like -> Tx
    NB: version, lock_time must be little-endian
    '''

    def __init__(self, version, flag, tx_ins,
                 tx_outs, tx_witnesses, lock_time):

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
            self.tx_id_le = utils.hash256(self._bytes)
            self.tx_id = utils.change_endianness(self.tx_id_le)
            self.wtx_id = None
            self.wtx_le = None

        self._make_immutable()

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
        return len(self._bytes)

    def calc_fee(self, input_values):
        '''
        Tx, list(int) -> int
        Inputs don't know their value without the whole chain.
        '''
        return \
            sum(input_values) \
            - sum([utils.le2i(o.value) for o in self.tx_outs])

    def sighash_none(self):
        raise NotImplementedError('SIGHASH_NONE is a bad idea.')

    def copy(self, version=None, flag=None, tx_ins=None,
             tx_outs=None, tx_witnesses=None, lock_time=None):
        '''
        Tx, byte-like, byte-like, list(TxIn),
        list(TxOut), list(InputWitness), byte-like -> Tx

        Makes a copy. Allows over-writing specific pieces.
        '''
        return Tx(version=version if version is not None else self.version,
                  flag=flag if flag is not None else self.flag,
                  tx_ins=tx_ins if tx_ins is not None else self.tx_ins,
                  tx_outs=tx_outs if tx_outs is not None else self.tx_outs,
                  tx_witnesses=(tx_witnesses if tx_witnesses is not None
                                else self.tx_witnesses),
                  lock_time=(lock_time if lock_time is not None
                             else self.lock_time))

    def with_new_inputs(self, new_tx_ins):
        '''
        Tx, list(TxIn) -> Tx
        '''
        return self.copy(tx_ins=[i for i in self.tx_ins] + new_tx_ins)

    def with_new_outputs(self, new_tx_outs):
        '''
        Tx, list(TxOut) -> Tx
        '''
        return self.copy(tx_outs=[o for o in self.tx_outs] + new_tx_outs)

    def with_new_inputs_and_witnesses(self, new_tx_ins, new_witnesses):
        '''
        Tx, list(TxIn), list(InputWitness) -> Tx

        NB: must have a one-to-one correspondance
        '''
        return self.copy(
            tx_is=[i for i in self.tx_ins] + new_tx_ins,
            tx_witnesses=[w for w in self.tx_witnesses] + new_witnesses)

    def _sighash_prep(self, current, prevout_pk_script):
        '''
        Tx, byte-like -> Tx
        Sighashes suck
        Performs the sighash setup described here:
        https://en.bitcoin.it/wiki/OP_CHECKSIG#How_it_works
        https://bitcoin.stackexchange.com/questions/3374/how-to-redeem-a-basic-tx
        We save on complexity by refusing to support OP_CODESEPARATOR
        '''
        sub_script = prevout_pk_script  # Follow wiki naming convention
        # NB: The scripts for all transaction inputs in txCopy are set
        #     to empty scripts (exactly 1 byte 0x00)
        copy_tx_ins = [tx_in.copy(stack_script=None, redeem_script=None)
                       for tx_in in self.tx_ins]

        # NB: The script for the current transaction input in txCopy is set to
        #     subScript (lead in by its length as a var-integer encoded!)
        copy_tx_ins[current] = \
            copy_tx_ins[current].copy(redeem_script=sub_script)

        return self.copy(tx_ins=copy_tx_ins)

    def sighash_single(self, current, prevout_pk_script, anyone_can_pay=False):
        '''
        Tx, int, byte-like, bool -> bytearray
        Sighashes suck
        Generates the hash to be signed with SIGHASH_SINGLE
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Procedure_for_Hashtype_SIGHASH_SINGLE
        https://bitcoin.stackexchange.com/questions/3890/for-sighash-single-do-the-outputs-other-than-at-the-input-index-have-8-bytes-or
        '''
        copy_tx = self._sighash_prep(current, prevout_pk_script)
        # NB: The output of txCopy is resized
        #     to the size of the current input index+1.
        copy_tx_outs = copy_tx.tx_outs[:current + 1]

        # NB: All other txCopy outputs
        #     aside from the output that is the same as the current input index
        #     are set to a blank script and a value of (long) -1.
        copy_tx_outs = [TxOut(value=b'\xff' * 8, output_script=None)
                        for _ in copy_tx.tx_ins]  # Null them all
        copy_tx_outs[current] = copy_tx.tx_outs[current]  # Fix the current one

        # NB: All other txCopy inputs aside from the current input
        #     are set to have an nSequence index of zero.
        copy_tx_ins = [tx_in.copy(sequence=b'\x00\x00\x00\x00')
                       for tx_in in copy_tx.tx_ins]  # Set all to 0
        copy_tx_ins[current] = copy_tx.tx_ins[current]  # Fix the current one

        copy_tx = copy_tx.copy(tx_ins=copy_tx_ins, tx_outs=copy_tx_outs)

        if anyone_can_pay:  # Forward onwards
            return Tx._sighash_anyone_can_pay(prevout_pk_script,
                                              copy_tx, SIGHASH_SINGLE)

        return Tx._sighash_final_hashing(copy_tx, SIGHASH_SINGLE)

    def sighash_all(self, current, prevout_pk_script, anyone_can_pay=False):
        '''
        Tx, int, byte-like, bool -> bytearray
        Sighashes suck
        Generates the hash to be signed with SIGHASH_ALL
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Hashtype_SIGHASH_ALL_.28default.29
        '''

        copy_tx = self._sighash_prep(current, prevout_pk_script)
        if anyone_can_pay:
            return Tx._sighash_anyone_can_pay(prevout_pk_script,
                                              copy_tx, SIGHASH_ALL)

        return Tx._sighash_final_hashing(copy_tx, SIGHASH_ALL)

    @staticmethod
    def _sighash_anyone_can_pay(prevout_pk_script, copy_tx, sighash_type):
        '''
        byte-like, Tx, int -> bytes
        Applies SIGHASH_ANYONECANPAY procedure.
        Should be called by another SIGHASH procedure.
        Not on its own.
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Procedure_for_Hashtype_SIGHASH_ANYONECANPAY
        '''
        # The txCopy input vector is resized to a length of one.
        copy_tx_ins = [prevout_pk_script]
        copy_tx = copy_tx.copy(tx_ins=copy_tx_ins)

        return Tx._sighash_final_hashing(copy_tx,
                                         sighash_type & SIGHASH_ANYONECANPAY)

    @staticmethod
    def _sighash_final_hashing(copy_tx, sighash_type):
        '''
        Tx, int -> bytes
        Returns the hash that should be signed
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Procedure_for_Hashtype_SIGHASH_ANYONECANPAY
        '''
        data = bytearray()
        data.extend(copy_tx._bytes)
        data.extend(utils.i2le_padded(sighash_type, 4))
        return utils.hash256(data)
