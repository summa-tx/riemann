import math
import riemann
from riemann.script import serialization
from riemann import utils

SIGHASH_ALL = 0x01
SIGHASH_NONE = 0x02
SIGHASH_SINGLE = 0x03
SIGHASH_FORKID = 0x40
SIGHASH_ANYONECANPAY = 0x80


class ByteData():
    '''
    Wrapper class for byte-like data.
    Iterable
    Can be made immutable.
    self._bytes is a bytearray object when mutable.
    self._bytes is a byte object when immutable.
    Should be mostly transparent to the user.
    Can be treated like bytes or a bytearray in most cases.
    '''
    __immutable = False

    def __init__(self):
        self._bytes = bytearray()
        self._current = 0

    def __iter__(self):
        return iter(self._bytes)

    def __iadd__(self, other):
        '''
        ByteData, byte-like -> ByteData
        Define += operator.
        Extend self's bytes with other's bytes.
        '''
        if isinstance(other, bytes) or isinstance(other, bytearray):
            self._bytes.extend(other)
        elif isinstance(other, ByteData):
            self._bytes.extend(other._bytes)
        else:
            raise TypeError('unsupported operand type(s) for +=: '
                            '{} and {}'.format(type(self).__name__,
                                               type(other).__name__))
        return self

    def __ne__(self, other):
        '''
        ByteData, byte-like -> bool
        Define != operator.
        Compares self._bytes to other.
        '''
        if isinstance(other, bytes) or isinstance(other, bytearray):
            return self._bytes != other
        elif isinstance(other, ByteData):
            return self._bytes != other._bytes
        else:
            raise TypeError('Equality not supported for ByteData and {}.'
                            .format(type(other)))

    def __eq__(self, other):
        '''
        ByteData, byte-like -> bool
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
            substring = substring.to_bytes()
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
            raise ValueError('Expected byte-like object. '
                             'Got: {}'.format(type(data)))

        if length is None:
            return

        if len(data) != length:
            raise ValueError('Expected byte-like object with length {}. '
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

        # This pads out to the next 2/4/8 bytes.
        while len(self) > 1 and math.log(len(self) - 1, 2) % 1 != 0:
            self += bytes([0x00])

        self.number = number

        self._make_immutable()

    def copy(self):
        return VarInt(self.number)

    @classmethod
    def from_bytes(VarInt, byte_string):
        '''
        byte-like -> VarInt
        accepts arbitrary length input, gets a VarInt off the front
        '''
        num = byte_string
        if num[0] <= 0xfc:
            num = num[0:1]
            non_compact = False
        elif num[0] == 0xfd:
            num = num[1:3]
            non_compact = (num[1] == 0)
        elif num[0] == 0xfe:
            num = num[1:5]
            non_compact = (num[-2:] == b'\x00\x00')
        elif num[0] == 0xff:
            num = num[1:9]
            non_compact = (num[-4:] == b'\x00\x00\x00\x00')
        if len(num) not in [1, 2, 4, 8]:
            raise ValueError('Malformed VarInt. Got: {}'
                             .format(byte_string.hex()))

        ret = VarInt(utils.le2i(num))

        if non_compact:
            raise ValueError('VarInt must be compact. Got: {}'
                             .format(byte_string.hex()))

        return ret


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

    def copy(self, tx_id=None, index=None):
        return Outpoint(
            tx_id=tx_id if tx_id is not None else self.tx_id,
            index=index if index is not None else self.index)

    @classmethod
    def from_bytes(Outpoint, byte_string):
        '''
        bytes -> Outpoint
        '''
        return Outpoint(
            tx_id=byte_string[:32],
            index=byte_string[32:36])


class TxIn(ByteData):
    '''
    Outpoint, byte-like, byte-like, byte-like -> TxIn
    stack_script and redeem_script should already be serialized
    NB: sequence must be little-endian
    '''

    def __init__(self, outpoint, stack_script, redeem_script, sequence):
        super().__init__()

        self.validate_bytes(outpoint, 36)
        self.validate_bytes(stack_script, None)
        self.validate_bytes(redeem_script, None)
        self.validate_bytes(sequence, 4)

        if len(stack_script) + len(redeem_script) > 1650:
            raise ValueError('Input script_sig is too long. '
                             'Expected <= 1650 bytes. Got {} bytes.'
                             .format(len(stack_script) + len(redeem_script)))

        self += outpoint
        self += VarInt(len(stack_script) + len(redeem_script))
        self += stack_script
        self += redeem_script
        self += sequence

        self.outpoint = outpoint
        self.script_len = len(stack_script + redeem_script)
        self.stack_script = stack_script
        self.redeem_script = redeem_script
        self.script_sig = self.stack_script + self.redeem_script
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

    def is_p2sh(self):
        return self.redeem_script is not b''

    @classmethod
    def _parse_script_sig(TxIn, script_sig):
        '''
        byte_string -> (byte_string, byte_string)
        '''
        # Is there a better way to do this?
        stack_script = script_sig
        redeem_script = b''
        try:
            # If the last entry deserializes, it's a p2sh input
            # There is a vanishingly small edge case where the pubkey
            #   forms a deserializable script.
            deserialized = serialization.deserialize(script_sig)
            items = deserialized.split()
            serialization.hex_deserialize(items[-1])
            stack_script = serialization.serialize(' '.join(items[:-1]))
            redeem_script = serialization.serialize(items[-1])
        except (IndexError, ValueError):
            pass

        return stack_script, redeem_script

    @classmethod
    def from_bytes(TxIn, byte_string):
        '''
        byte_string -> TxIn
        parses a TxIn from a byte-like object
        '''
        outpoint = Outpoint.from_bytes(byte_string[:36])

        script_sig_len = VarInt.from_bytes(byte_string[36:45])
        script_start = 36 + len(script_sig_len)
        script_end = script_start + script_sig_len.number
        script_sig = byte_string[script_start:script_end]

        sequence = byte_string[script_end:script_end + 4]
        if script_sig == b'':
            stack_script = b''
            redeem_script = b''
        else:
            stack_script, redeem_script = TxIn._parse_script_sig(script_sig)

        return TxIn(
            outpoint=outpoint,
            stack_script=stack_script,
            redeem_script=redeem_script,
            sequence=sequence)


class TxOut(ByteData):
    '''
    NB: value must be little-endian
    '''

    def __init__(self, value, output_script):
        super().__init__()

        self.validate_bytes(value, 8)
        self.validate_bytes(output_script, None)

        if (output_script != b''
                and utils.le2i(value) <= 546
                and output_script[0] != 0x6a):
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

    @classmethod
    def from_bytes(TxOut, byte_string):
        n = VarInt.from_bytes(byte_string[8:])
        script_start = 8 + len(n)
        script_end = script_start + n.number
        if n.number < 0xfc:
            return TxOut(
                value=byte_string[:8],
                output_script=byte_string[script_start:script_end])
        else:
            raise NotImplementedError(
                'No support for abnormally long pk_scripts.')


class WitnessStackItem(ByteData):

    def __init__(self, item):
        super().__init__()

        self.validate_bytes(item, None)
        if len(item) > 520:
            raise ValueError(
                'Item is too large. Expected <=520 bytes. '
                'Got: {} bytes'.format(len(item)))
        self += VarInt(len(item))
        self += item

        self.item_len = len(item)
        self.item = item

        self._make_immutable()

    @classmethod
    def from_bytes(WitnessStackItem, byte_string):
        n = VarInt.from_bytes(byte_string)
        item_start = len(n)
        item_end = item_start + n.number
        return WitnessStackItem(byte_string[item_start:item_end])


class InputWitness(ByteData):

    def __init__(self, stack):
        '''
        list(WitnessStackItem) -> InputWitness
        '''
        super().__init__()
        for item in stack:
            if not isinstance(item, WitnessStackItem):
                raise ValueError(
                    'Invalid witness stack item. '
                    'Expected WitnessStackItem. Got {}'
                    .format(item))

        self += VarInt(len(stack))
        for item in stack:
            self += item

        self.stack_len = len(stack)
        self.stack = [item for item in stack]

        self._make_immutable()

    @classmethod
    def from_bytes(InputWitness, byte_string):
        stack_items = VarInt.from_bytes(byte_string)
        item_start = len(stack_items)
        items = []
        while len(items) < stack_items.number:
            item = WitnessStackItem.from_bytes(byte_string[item_start:])
            item_start += len(item)
            items.append(item)
        return InputWitness(items)

    def copy(self, stack=None):
        return InputWitness(
            stack=stack if stack is not None else self.stack)


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
            if flag != riemann.network.SEGWIT_TX_FLAG:
                raise ValueError(
                    'Invald segwit flag. '
                    'Expected None or {}. Got: {}'
                    .format(riemann.network.SEGWIT_TX_FLAG, flag))
            if tx_witnesses is None or len(tx_witnesses) is 0:
                raise ValueError('Got segwit flag but no witnesses.')

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
                        'Invalid InputWitness. '
                        'Expected instance of InputWitness. Got {}'
                        .format(type(witness)))

        if max(len(tx_ins), len(tx_outs)) > 255:
            raise ValueError('Too many inputs or outputs. Stop that.')

        if min(len(tx_ins), len(tx_outs)) == 0:
            raise ValueError('Too few inputs or outputs. Stop that.')

        for tx_in in tx_ins:
            if not isinstance(tx_in, TxIn):
                raise ValueError(
                    'Invalid TxIn. '
                    'Expected instance of TxIn. Got {}'
                    .format(type(tx_in).__name__))

        for tx_out in tx_outs:
            if not isinstance(tx_out, TxOut):
                raise ValueError(
                    'Invalid TxOut. '
                    'Expected instance of TxOut. Got {}'
                    .format(type(tx_out).__name__))

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
        self.tx_ins = tuple(tx_in for tx_in in tx_ins)
        self.tx_outs_len = len(tx_outs)
        self.tx_outs = tuple(tx_out for tx_out in tx_outs)
        self.tx_witnesses_len = self.tx_ins_len
        self.tx_witnesses = \
            tuple(wit for wit in tx_witnesses) if tx_witnesses is not None \
            else None
        self.lock_time = lock_time

        if len(self) > 100000:
            raise ValueError(
                'Tx is too large. '
                'Expect less than 100kB. Got: {} bytes'.format(len(self)))

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

        self._make_immutable()

    @classmethod
    def from_bytes(Tx, byte_string):
        version = byte_string[0:4]
        if byte_string[4:6] == riemann.network.SEGWIT_TX_FLAG:
            tx_ins_num_loc = 6
            flag = riemann.network.SEGWIT_TX_FLAG
        else:
            tx_ins_num_loc = 4
            flag = None
        tx_ins = []
        tx_ins_num = VarInt.from_bytes(byte_string[tx_ins_num_loc:])

        current = tx_ins_num_loc + len(tx_ins_num)
        for _ in range(tx_ins_num.number):
            tx_in = TxIn.from_bytes(byte_string[current:])
            current += len(tx_in)
            tx_ins.append(tx_in)

        tx_outs = []
        tx_outs_num = VarInt.from_bytes(byte_string[current:])

        current += len(tx_outs_num)
        for _ in range(tx_outs_num.number):
            tx_out = TxOut.from_bytes(byte_string[current:])
            current += len(tx_out)
            tx_outs.append(tx_out)

        if not flag:
            tx_witnesses = None
        else:
            tx_witnesses = []
            tx_witnesses_num = tx_ins_num
            for _ in range(tx_witnesses_num.number):
                tx_witness = InputWitness.from_bytes(byte_string[current:])
                current += len(tx_witness)
                tx_witnesses.append(tx_witness)

        lock_time = byte_string[current:]
        return Tx(
            version=version,
            flag=flag,
            tx_ins=tx_ins,
            tx_outs=tx_outs,
            tx_witnesses=tx_witnesses,
            lock_time=lock_time)

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

    def is_witness(self):
        return self.flag is not None

    def calculate_fee(self, input_values):
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

    def _sighash_prep(self, index, script):
        '''
        Tx, int, byte-like -> Tx
        Sighashes suck
        Performs the sighash setup described here:
        https://en.bitcoin.it/wiki/OP_CHECKSIG#How_it_works
        https://bitcoin.stackexchange.com/questions/3374/how-to-redeem-a-basic-tx
        We save on complexity by refusing to support OP_CODESEPARATOR
        '''
        sub_script = self._get_script_code(index=index)
        if sub_script == b'':
            sub_script = script
        # 0 out scripts in tx_ins
        copy_tx_ins = [tx_in.copy(stack_script=b'', redeem_script=b'')
                       for tx_in in self.tx_ins]

        # NB: The script for the current transaction input in txCopy is set to
        #     subScript (lead in by its length as a var-integer encoded!)
        copy_tx_ins[index] = \
            copy_tx_ins[index].copy(stack_script=b'', redeem_script=sub_script)

        return self.copy(tx_ins=copy_tx_ins)

    def sighash_all(self, index, script=None,
                    prevout_value=None, anyone_can_pay=False):
        '''
        Tx, int, byte-like, byte-like, bool -> bytearray
        Sighashes suck
        Generates the hash to be signed with SIGHASH_ALL
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Hashtype_SIGHASH_ALL_.28default.29
        '''

        if riemann.network.FORKID is not None:
            return self._sighash_forkid(index=index,
                                        script=script,
                                        prevout_value=prevout_value,
                                        sighash_type=SIGHASH_ALL,
                                        anyone_can_pay=anyone_can_pay)

        copy_tx = self._sighash_prep(index=index, script=script)
        if anyone_can_pay:
            return self._sighash_anyone_can_pay(
                index=index, copy_tx=copy_tx, sighash_type=SIGHASH_ALL)

        return self._sighash_final_hashing(copy_tx, SIGHASH_ALL)

    def sighash_single(self, index, script=None,
                       prevout_value=None, anyone_can_pay=False):
        '''
        Tx, int, byte-like, byte-like, bool -> bytearray
        Sighashes suck
        Generates the hash to be signed with SIGHASH_SINGLE
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Procedure_for_Hashtype_SIGHASH_SINGLE
        https://bitcoin.stackexchange.com/questions/3890/for-sighash-single-do-the-outputs-other-than-at-the-input-index-have-8-bytes-or
        https://github.com/petertodd/python-bitcoinlib/blob/051ec4e28c1f6404fd46713c2810d4ebbed38de4/bitcoin/core/script.py#L913-L965
        '''

        if index >= len(self.tx_outs):
            raise NotImplementedError(
                'I refuse to implement the SIGHASH_SINGLE bug.')

        if riemann.network.FORKID is not None:
            return self._sighash_forkid(index=index,
                                        script=script,
                                        prevout_value=prevout_value,
                                        sighash_type=SIGHASH_SINGLE,
                                        anyone_can_pay=anyone_can_pay)

        copy_tx = self._sighash_prep(index=index, script=script)

        # Remove outputs after the one we're signing
        # Other tx_outs are set to -1 value and null scripts
        copy_tx_outs = copy_tx.tx_outs[:index + 1]
        copy_tx_outs = [TxOut(value=b'\xff' * 8, output_script=b'')
                        for _ in copy_tx.tx_ins]  # Null them all
        copy_tx_outs[index] = copy_tx.tx_outs[index]  # Fix the current one

        # Other tx_ins sequence numbers are set to 0
        copy_tx_ins = [tx_in.copy(sequence=b'\x00\x00\x00\x00')
                       for tx_in in copy_tx.tx_ins]  # Set all to 0
        copy_tx_ins[index] = copy_tx.tx_ins[index]  # Fix the current one

        copy_tx = copy_tx.copy(
            tx_ins=copy_tx_ins,
            tx_outs=copy_tx_outs)

        if anyone_can_pay:  # Forward onwards
            return self._sighash_anyone_can_pay(index, copy_tx, SIGHASH_SINGLE)

        return self._sighash_final_hashing(copy_tx, SIGHASH_SINGLE)

    def _sighash_anyone_can_pay(self, index, copy_tx, sighash_type):
        '''
        int, byte-like, Tx, int -> bytes
        Applies SIGHASH_ANYONECANPAY procedure.
        Should be called by another SIGHASH procedure.
        Not on its own.
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Procedure_for_Hashtype_SIGHASH_ANYONECANPAY
        '''

        # The txCopy input vector is resized to a length of one.
        copy_tx_ins = [copy_tx.tx_ins[index]]
        copy_tx = copy_tx.copy(tx_ins=copy_tx_ins)

        return self._sighash_final_hashing(
            copy_tx, sighash_type | SIGHASH_ANYONECANPAY)

    def _sighash_final_hashing(self, copy_tx, sighash_type):
        '''
        Tx, int -> bytes
        Returns the hash that should be signed
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Procedure_for_Hashtype_SIGHASH_ANYONECANPAY
        '''
        sighash = ByteData()
        sighash += copy_tx.to_bytes()
        sighash += utils.i2le_padded(sighash_type, 4)
        return utils.hash256(sighash.to_bytes())

    def _hash_prevouts(self, anyone_can_pay):
        if anyone_can_pay:
            # If the ANYONECANPAY flag is set,
            # hashPrevouts is a uint256 of 0x0000......0000.
            hash_prevouts = b'\x00' * 32
        else:
            # hashPrevouts is the double SHA256 of all outpoints;
            outpoints = ByteData()
            for tx_in in self.tx_ins:
                outpoints += tx_in.outpoint
            hash_prevouts = utils.hash256(outpoints.to_bytes())
        return hash_prevouts

    def _hash_sequence(self, sighash_type, anyone_can_pay):
        if anyone_can_pay or sighash_type == SIGHASH_SINGLE:
            # If any of ANYONECANPAY, SINGLE sighash type is set,
            # hashSequence is a uint256 of 0x0000......0000.
            return b'\x00' * 32
        else:
            # hashSequence is the double SHA256 of nSequence of all inputs;
            sequences = ByteData()
            for tx_in in self.tx_ins:
                sequences += tx_in.sequence
            return utils.hash256(sequences.to_bytes())

    def _get_script_code(self, index):
        if len(self.tx_ins[index].redeem_script) != 0:
            script = ByteData()
            # redeemScript in case of P2SH
            script += self.tx_ins[index].redeem_script
            return script.to_bytes()
        return b''

    def _adjusted_script_code(self, index, script):
        script_code = ByteData()
        tx_in_redeem_script = self._get_script_code(index=index)
        if tx_in_redeem_script == b'':
            script_code += VarInt(len(script))
            script_code += script
            return script_code
        script_code += VarInt(len(tx_in_redeem_script))
        script_code += tx_in_redeem_script
        return script_code

    def _hash_outputs(self, index, sighash_type):
        if sighash_type == SIGHASH_ALL:
            # If the sighash type is ALL,
            # hashOutputs is the double SHA256 of all output amounts
            # paired up with their scriptPubKey;
            outputs = ByteData()
            for tx_out in self.tx_outs:
                outputs += tx_out.to_bytes()
            return utils.hash256(outputs.to_bytes())
        elif sighash_type == SIGHASH_SINGLE and index < len(self.tx_outs):
            # f sighash type is SINGLE
            # and the input index is smaller than the number of outputs,
            # hashOutputs is the double SHA256 of the output at the same index
            return utils.hash256(self.tx_outs[index].to_bytes())
        else:
            # Otherwise, hashOutputs is a uint256 of 0x0000......0000
            raise NotImplementedError(
                'I refuse to implement the SIGHASH_SINGLE bug.')

    def _adjusted_sighash_type(self, sighash_type, anyone_can_pay):
        # The sighash type is altered to include a 24-bit fork id
        # ss << ((GetForkID() << 8) | nHashType)
        forkid = riemann.network.FORKID << 8
        sighash = forkid | sighash_type | SIGHASH_FORKID
        if anyone_can_pay:
            sighash = sighash | SIGHASH_ANYONECANPAY
        return utils.i2le_padded(sighash, 4)

    def _sighash_forkid(self, index, script, prevout_value,
                        sighash_type, anyone_can_pay=False):
        '''
        Tx, int, byte-like, byte-like, int, bool -> bytes
        https://github.com/bitcoincashorg/spec/blob/master/replay-protected-sighash.md
        '''
        self.validate_bytes(prevout_value, 8)

        data = ByteData()

        # 1. nVersion of the transaction (4-byte little endian)
        data += self.version

        # 2. hashPrevouts (32-byte hash)
        data += self._hash_prevouts(anyone_can_pay=anyone_can_pay)

        # 3. hashSequence (32-byte hash)
        data += self._hash_sequence(sighash_type=sighash_type,
                                    anyone_can_pay=anyone_can_pay)

        # 4. outpoint (32-byte hash + 4-byte little endian)
        data += self.tx_ins[index].outpoint

        # 5. scriptCode of the input (serialized as scripts inside CTxOuts)
        data += self._adjusted_script_code(
            index=index,
            script=script)

        # 6. value of the output spent by this input (8-byte little endian)
        data += prevout_value

        # 7. nSequence of the input (4-byte little endian)
        data += self.tx_ins[index].sequence

        # 8. hashOutputs (32-byte hash)
        data += self._hash_outputs(index=index, sighash_type=sighash_type)

        # 9. nLocktime of the transaction (4-byte little endian)
        data += self.lock_time

        # 10. sighash type of the signature (4-byte little endian)
        data += self._adjusted_sighash_type(sighash_type=sighash_type,
                                            anyone_can_pay=anyone_can_pay)

        return utils.hash256(data.to_bytes())


class DecredByteData(ByteData):

    def __init__(self):
        if 'decred' not in riemann.get_current_network_name():
            raise ValueError('Decred classes not supported by network {}. '
                             'How did you get here?'
                             .format(riemann.get_current_network_name()))
        super().__init__()


class DecredOutpoint(DecredByteData):

    def __init__(self, tx_id, index, tree):
        super().__init__()

        self.validate_bytes(tx_id, 32)
        self.validate_bytes(index, 4)
        self.validate_bytes(tree, 1)

        self += tx_id
        self += index
        self += tree

        self.tx_id = tx_id
        self.index = index
        self.tree = tree

        self._make_immutable()

    def copy(self, tx_id=None, index=None, tree=None):
        return DecredOutpoint(
            tx_id=tx_id if tx_id is not None else self.tx_id,
            index=index if index is not None else self.index,
            tree=tree if tree is not None else self.tree)

    @classmethod
    def from_bytes(DecredOutpoint, byte_string):
        return DecredOutpoint(
            tx_id=byte_string[:32],
            index=byte_string[32:36],
            tree=byte_string[36:37])


class DecredTxIn(DecredByteData):

    def __init__(self, outpoint, sequence):
        super().__init__()

        self.validate_bytes(outpoint, 37)
        self.validate_bytes(sequence, 4)

        self += outpoint
        self += sequence

        self.outpoint = outpoint
        self.sequence = sequence

        self._make_immutable()

    def copy(self, outpoint=None, sequence=None):
        return DecredTxIn(
            outpoint=outpoint if outpoint is not None else self.outpoint,
            sequence=sequence if sequence is not None else self.sequence)

    @classmethod
    def from_bytes(DecredTxIn, byte_string):
        return DecredTxIn(
            outpoint=DecredOutpoint.from_bytes(byte_string[:37]),
            sequence=byte_string[37:41])


class DecredTxOut(ByteData):

    def __init__(self, value, version, output_script):
        super().__init__()

        self.validate_bytes(value, 8)
        self.validate_bytes(version, 2)
        self.validate_bytes(output_script, None)

        self += value
        self += version
        self += VarInt(len(output_script))
        self += output_script

        self.value = value
        self.version = version
        self.output_script_len = len(output_script)
        self.output_script = output_script

        self._make_immutable()

    def copy(self, value=None, version=None, output_script=None):
        return DecredTxOut(
            value=value if value is not None else self.value,
            version=version if version is not None else self.version,
            output_script=(output_script if output_script is not None
                           else self.output_script))

    @classmethod
    def from_bytes(DecredTxOut, byte_string):
        n = VarInt.from_bytes(byte_string[10:])
        script_start = 10 + len(n)
        script_end = script_start + n.number
        if n.number < 0xfc:
            return DecredTxOut(
                value=byte_string[:8],
                version=byte_string[8:10],
                output_script=byte_string[script_start:script_end])
        else:
            raise NotImplementedError(
                'No support for abnormally long pk_scripts.')


class DecredInputWitness(DecredByteData):

    def __init__(self, value, height, index, stack_script, redeem_script):
        super().__init__()

        self.validate_bytes(value, 8)
        self.validate_bytes(height, 4)
        self.validate_bytes(index, 4)
        self.validate_bytes(stack_script, None)
        self.validate_bytes(redeem_script, None)

        self += value
        self += height
        self += index
        self += VarInt(len(stack_script) + len(redeem_script))
        self += stack_script
        self += redeem_script

        self.value = value
        self.height = height
        self.index = index
        self.script_len = len(stack_script + redeem_script)
        self.stack_script = stack_script
        self.redeem_script = redeem_script
        self.script_sig = self.stack_script + self.redeem_script

        self._make_immutable()

    def copy(self, value=None, height=None, index=None,
             stack_script=None, redeem_script=None):
        return DecredInputWitness(
            value=value if value is not None else self.value,
            height=height if height is not None else self.height,
            index=index if index is not None else self.index,
            stack_script=(stack_script if stack_script is not None
                          else self.stack_script),
            redeem_script=(redeem_script if redeem_script is not None
                           else self.redeem_script))

    @classmethod
    def from_bytes(DecredInputWitness, byte_string):
        raise NotImplementedError('TODO')


class DecredTx(DecredByteData):

    def __init__(self, version, tx_ins, tx_outs,
                 lock_time, expiry, tx_witnesses):
        super().__init__()

        self.validate_bytes(version, 4)
        self.validate_bytes(lock_time, 4)
        self.validate_bytes(expiry, 4)

        if max(len(tx_ins), len(tx_outs)) > 255:
            raise ValueError('Too many inputs or outputs. Stop that.')

        if min(len(tx_ins), len(tx_outs)) == 0:
            raise ValueError('Too few inputs or outputs. Stop that.')

        # if len(tx_witnesses) != len(tx_ins):
        #     raise ValueError(
        #         'Witness and TxIn lists must be same length. '
        #         'Got {} inputs and {} witnesses.'
        #         .format(len(tx_ins), len(tx_witnesses)))

        for tx_in in tx_ins:
            if not isinstance(tx_in, DecredTxIn):
                raise ValueError(
                    'Invalid TxIn. '
                    'Expected instance of DecredTxIn. Got {}'
                    .format(type(tx_in).__name__))

        for tx_out in tx_outs:
            if not isinstance(tx_out, DecredTxOut):
                raise ValueError(
                    'Invalid TxOut. '
                    'Expected instance of DecredTxOut. Got {}'
                    .format(type(tx_out).__name__))

        for tx_witness in tx_witnesses:
            if not isinstance(tx_witness, DecredInputWitness):
                raise ValueError(
                    'Invalid TxWitness. '
                    'Expected instance of DecredInputWitness. Got {}'
                    .format(type(tx_witness).__name__))

        self += version
        self += VarInt(len(tx_ins))
        for tx_in in tx_ins:
            self += tx_in
        self += VarInt(len(tx_outs))
        for tx_out in tx_outs:
            self += tx_out
        self += lock_time
        self += expiry
        self += VarInt(len(tx_witnesses))
        for tx_witness in tx_witnesses:
            self += tx_witness

        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.lock_time = lock_time
        self.expiry = expiry
        self.tx_witnesses = tx_witnesses

        if len(self) > 100000:
            raise ValueError(
                'Tx is too large. '
                'Expect less than 100kB. Got: {} bytes'.format(len(self)))

        # TODO: check this
        self.tx_id_le = self.prefix_hash()
        self.tx_id = utils.change_endianness(self.tx_id_le)

        # Ignoring this, as it's only used for in-block merkle trees
        # self.tx_id_full_le = utils.blake256(self.tx_id_le
        #                                     + self.witness_hash())
        # self.tx_id_full = utils.change_endianness(self.tx_id_full_le)

        self._make_immutable()

    @classmethod
    def from_bytes(DecredTx, byte_string):
        raise NotImplementedError('TODO')

    def prefix_hash(self):
        try:
            return self.tx_id_le  # Prevent redundant hashing
        except AttributeError:
            return utils.blake256(self.prefix())

    def witness_hash(self):
        return utils.blake256(self.witness())

    def witness_signing_hash(self):
        return utils.blake256(self.witness_signing())

    def prefix(self):
        data = ByteData()
        data += self.version[:2]
        data += b'\x01\x00'  # Serialization type 1 (prefix only)
        data += VarInt(len(self.tx_ins))
        for tx_in in self.tx_ins:
            data += tx_in
        data += VarInt(len(self.tx_outs))
        for tx_out in self.tx_outs:
            data += tx_out
        data += self.lock_time
        data += self.expiry
        return data.to_bytes()

    def witness(self):
        data = ByteData()
        data += self.version[:2]
        data += b'\x02\x00'  # Serialization type 2 (witness only)
        data += VarInt(len(self.tx_witnesses))
        for tx_witness in self.tx_witnesses:
            data += tx_witness
        return data.to_bytes()

    def witness_signing(self):
        data = ByteData()
        data += self.version[:2]
        data += b'\x03\x00'  # Serialization type 3 (witness signing)
        data += VarInt(len(self.tx_witnesses))
        for tx_witness in self.tx_witnesses:
            data += VarInt(tx_witness.script_len)
            data += tx_witness.script_sig
        return data.to_bytes()

    def calculate_fee(self):
        return \
            sum([utils.le2i(w.value) for w in self.tx_witnesses]) \
            - sum([utils.le2i(o.value) for o in self.tx_outs])

    def copy(self, version=None, tx_ins=None, tx_outs=None,
             lock_time=None, expiry=None, tx_witnesses=None):
        return DecredTx(
            version=version if version is not None else self.version,
            tx_ins=tx_ins if tx_ins is not None else self.tx_ins,
            tx_outs=tx_outs if tx_outs is not None else self.tx_outs,
            lock_time=(lock_time if lock_time is not None
                       else self.lock_time),
            expiry=expiry if expiry is not None else self.expiry,
            tx_witnesses=(tx_witnesses if tx_witnesses is not None
                          else self.tx_witnesses))

    def _get_script_code(self, index):
        if len(self.tx_witnesses[index].redeem_script) != 0:
            script = ByteData()
            # redeemScript in case of P2SH
            script += self.tx_witnesses[index].redeem_script
            return script.to_bytes()
        return b''

    def sighash_none(self):
        raise NotImplementedError('SIGHASH_NONE is a bad idea.')

    def _sighash_prep(self, index, script=None):
        sub_script = self._get_script_code(index)
        if sub_script == b'':
            sub_script = script
        copy_tx_witnesses = [w.copy(stack_script=b'', redeem_script=b'')
                             for w in self.tx_witnesses]
        copy_tx_witnesses[index] = \
            copy_tx_witnesses[index].copy(stack_script=sub_script,
                                          redeem_script=b'')

        return self.copy(tx_witnesses=copy_tx_witnesses)

    def sighash_single(self, index, script=None,
                       anyone_can_pay=False):
        '''
        https://github.com/decred/dcrd/blob/master/txscript/script.go
        '''
        copy_tx = self._sighash_prep(
            index=index,
            script=script)

        try:
            copy_tx_outs = copy_tx.tx_outs[:index + 1]
            copy_tx_outs = [TxOut(value=b'\xff' * 8, output_script=b'')
                            for _ in copy_tx.tx_ins]
            copy_tx_outs[index] = copy_tx.tx_outs[index]
        except IndexError:
            raise NotImplementedError(
                'I refuse to implement the SIGHASH_SINGLE bug.')

        copy_tx_ins = [tx_in.copy(sequence=b'\x00\x00\x00\x00')
                       for tx_in in copy_tx.tx_ins]
        copy_tx_ins[index] = copy_tx.tx_ins[index]
        copy_tx = copy_tx.copy(tx_ins=copy_tx_ins, tx_outs=copy_tx_outs)

        if anyone_can_pay:
            return self._sighash_anyone_can_pay(
                index=index,
                copy_tx=copy_tx,
                sighash_type=SIGHASH_SINGLE)

        return self._sighash_final_hashing(
            index=index,
            copy_tx=copy_tx,
            sighash_type=SIGHASH_SINGLE)

    def sighash_all(self, index, script=None, anyone_can_pay=False):
        '''
        https://gist.github.com/davecgh/b00ec6e11f73620c3deddf160353961c
        https://github.com/decred/dcrd/blob/master/txscript/script.go
        '''
        copy_tx = self._sighash_prep(index, script)

        if anyone_can_pay:
            return self._sighash_anyone_can_pay(
                index=index,
                copy_tx=copy_tx,
                sighash_type=SIGHASH_ALL)

        return self._sighash_final_hashing(
            index=index,
            copy_tx=copy_tx,
            sighash_type=SIGHASH_ALL)

    def _sighash_anyone_can_pay(self, index, copy_tx, sighash_type):
        copy_tx_witnesses = [w.copy(stack_script=b'', redeem_script=b'')
                             for w in copy_tx.tx_witnesses]
        copy_tx_witnesses[index] = copy_tx.tx_witnesses[index]
        copy_tx = copy_tx.copy(tx_witnesses=copy_tx_witnesses)

        return self._sighash_final_hashing(
            index=index,
            copy_tx=copy_tx,
            sighash_type=sighash_type | SIGHASH_ANYONECANPAY)

    def _sighash_final_hashing(self, index, copy_tx, sighash_type):
        sighash = ByteData()
        sighash += utils.i2le_padded(sighash_type, 4)
        sighash += copy_tx.prefix_hash()
        sighash += copy_tx.witness_signing_hash()
        return utils.blake256(sighash.to_bytes())


class ZcashByteData(ByteData):
    def __init__(self):
        if 'zcash' not in riemann.get_current_network_name():
            raise ValueError('Zcash classes not supported by network {}. '
                             'How did you get here?'
                             .format(riemann.get_current_network_name()))
        super().__init__()


class SproutZkproof(ZcashByteData):

    def __init__(self, pi_sub_a, pi_prime_sub_a, pi_sub_b, pi_prime_sub_b,
                 pi_sub_c, pi_prime_sub_c, pi_sub_k, pi_sub_h):
        super().__init__()

        self.validate_bytes(pi_sub_a, 33)
        self.validate_bytes(pi_prime_sub_a, 33)
        self.validate_bytes(pi_sub_b, 65)
        self.validate_bytes(pi_prime_sub_b, 33)
        self.validate_bytes(pi_sub_c, 33)
        self.validate_bytes(pi_prime_sub_c, 33)
        self.validate_bytes(pi_sub_k, 33)
        self.validate_bytes(pi_sub_h, 33)

        self += pi_sub_a
        self += pi_prime_sub_a
        self += pi_sub_b
        self += pi_prime_sub_b
        self += pi_sub_c
        self += pi_prime_sub_c
        self += pi_sub_k
        self += pi_sub_h

        self.pi_sub_a = pi_sub_a
        self.pi_prime_sub_a = pi_prime_sub_a
        self.pi_sub_b = pi_sub_b
        self.pi_prime_sub_b = pi_prime_sub_b
        self.pi_sub_c = pi_sub_c
        self.pi_prime_sub_c = pi_prime_sub_c
        self.pi_sub_k = pi_sub_k
        self.pi_sub_h = pi_sub_h

        self._make_immutable()

    @classmethod
    def from_bytes(SproutZkproof, byte_string):
        return SproutZkproof(
            pi_sub_a=byte_string[0:33],
            pi_prime_sub_a=byte_string[33:66],
            pi_sub_b=byte_string[66:131],
            pi_prime_sub_b=byte_string[131:164],
            pi_sub_c=byte_string[164:197],
            pi_prime_sub_c=byte_string[197:230],
            pi_sub_k=byte_string[230:263],
            pi_sub_h=byte_string[263:296])


class SproutJoinsplit(ZcashByteData):

    def __init__(self, vpub_old, vpub_new, anchor, nullifiers, commitments,
                 ephemeral_key, random_seed, vmacs, zkproof, encoded_notes):
        super().__init__()

        if not isinstance(zkproof, SproutZkproof):
            raise ValueError(
                'Invalid zkproof. '
                'Expected instance of SproutZkproof. Got {}'
                .format(type(zkproof).__name__))
        if (utils.le2i(vpub_old) != 0 and utils.le2i(vpub_new) != 0):
            raise ValueError('vpub_old or vpub_new must be zero')

        self.validate_bytes(vpub_old, 8)
        self.validate_bytes(vpub_new, 8)
        self.validate_bytes(anchor, 32)
        self.validate_bytes(nullifiers, 64)
        self.validate_bytes(commitments, 64)
        self.validate_bytes(ephemeral_key, 32)
        self.validate_bytes(random_seed, 32)
        self.validate_bytes(vmacs, 64)
        self.validate_bytes(encoded_notes, 1202)

        self += vpub_old
        self += vpub_new
        self += anchor
        self += nullifiers
        self += commitments
        self += ephemeral_key
        self += random_seed
        self += vmacs
        self += zkproof
        self += encoded_notes

        self.vpub_old = vpub_old
        self.vpub_new = vpub_new
        self.anchor = anchor
        self.nullifiers = nullifiers
        self.commitments = commitments
        self.ephemeral_key = ephemeral_key
        self.random_seed = random_seed
        self.vmacs = vmacs
        self.zkproof = zkproof
        self.encoded_notes = encoded_notes

        self._make_immutable()

    @classmethod
    def from_bytes(SproutJoinsplit, byte_string):
        return SproutJoinsplit(
            vpub_old=byte_string[0:8],
            vpub_new=byte_string[8:16],
            anchor=byte_string[16:48],
            nullifiers=byte_string[48:112],
            commitments=byte_string[112:176],
            ephemeral_key=byte_string[176:208],
            random_seed=byte_string[208:240],
            vmacs=byte_string[240:304],
            zkproof=SproutZkproof.from_bytes(byte_string[304:600]),
            encoded_notes=byte_string[600:1802])


class SproutTx(ZcashByteData):

    def __init__(self, version, tx_ins, tx_outs, lock_time,
                 tx_joinsplits, joinsplit_pubkey, joinsplit_sig):

        super().__init__()

        if 'sprout' not in riemann.get_current_network_name():
            raise ValueError(
                'SproutTx not supported by network {}.'
                .format(riemann.get_current_network_name()))

        self.validate_bytes(version, 4)
        self.validate_bytes(lock_time, 4)

        if max(len(tx_ins), len(tx_outs)) > 255:
            raise ValueError('Too many inputs or outputs. Stop that.')

        for tx_in in tx_ins:
            if not isinstance(tx_in, TxIn):
                raise ValueError(
                    'Invalid TxIn. '
                    'Expected instance of TxOut. Got {}'
                    .format(type(tx_in).__name__))

        for tx_out in tx_outs:
            if not isinstance(tx_out, TxOut):
                raise ValueError(
                    'Invalid TxOut. '
                    'Expected instance of TxOut. Got {}'
                    .format(type(tx_out).__name__))

        if utils.le2i(version) == 1:
            if tx_joinsplits is not None and len(tx_joinsplits) != 0:
                raise ValueError('Joinsplits not allowed in version 1 txns.')
            if tx_ins is None or len(tx_ins) == 0:
                raise ValueError('Version 1 txns must have at least 1 input.')

        if utils.le2i(version) == 2:
            if len(tx_joinsplits) > 5:
                raise ValueError('Too many joinsplits. Stop that.')
            for tx_joinsplit in tx_joinsplits:
                if not isinstance(tx_joinsplit, SproutJoinsplit):
                    raise ValueError(
                        'Invalid Joinsplit. '
                        'Expected instance of SproutJoinsplit. Got {}'
                        .format(type(tx_joinsplit).__name__))
            self.validate_bytes(joinsplit_pubkey, 32)
            if joinsplit_sig is not None and joinsplit_sig != b'':
                self.validate_bytes(joinsplit_sig, 64)

        if utils.le2i(version) not in [1, 2]:
            raise ValueError('Version must be 1 or 2. '
                             'Got: {}'.format(utils.le2i(version)))

        self += version
        self += VarInt(len(tx_ins))
        for tx_in in tx_ins:
            self += tx_in
        self += VarInt(len(tx_outs))
        for tx_out in tx_outs:
            self += tx_out
        self += lock_time

        if version == utils.i2le_padded(2, 4):
            self += VarInt(len(tx_joinsplits))
            for tx_joinsplit in tx_joinsplits:
                self += tx_joinsplit
            self += joinsplit_pubkey
            self += joinsplit_sig

        self.version = version
        self.tx_ins_len = len(tx_ins)
        self.tx_ins = tuple(tx_in for tx_in in tx_ins)
        self.tx_outs_len = len(tx_outs)
        self.tx_outs = tuple(tx_out for tx_out in tx_outs)
        self.tx_joinsplits_len = len(tx_joinsplits)
        self.tx_joinsplits = tuple(js for js in tx_joinsplits)
        self.lock_time = lock_time

        if version == utils.i2le_padded(2, 4):
            self.joinsplit_pubkey = joinsplit_pubkey
            self.joinsplit_sig = joinsplit_sig
            # Zcash spec 5.4.1.4 Hsig hash function
            self.hsigs = [self._hsig(i) for i in range(self.tx_joinsplits_len)]

            self.primary_inputs = [self._primary_input(i)
                                   for i in range(self.tx_joinsplits_len)]
        else:
            self.joinsplit_pubkey = None
            self.joinsplit_sig = None
            self.hsigs = None
            self.primary_inputs = None

        self.tx_id_le = utils.hash256(self.to_bytes()).hex()
        self.tx_id = utils.hash256(self.to_bytes())[::-1].hex()

        self._make_immutable()

        if len(self) > 100000:
            raise ValueError(  # pragma: no cover
                'Tx is too large. '
                'Expect less than 100kB. Got: {} bytes'.format(len(self)))

    def _hsig(self, index):
        return utils.blake2b(
            data=self._hsig_input(index),
            digest_size=32,
            person=b'ZcashComputehSig')

    def _hsig_input(self, index):
        '''
        inputs for the hsig hash
        '''
        hsig_input = ZcashByteData()
        hsig_input += self.tx_joinsplits[index].random_seed
        hsig_input += self.tx_joinsplits[index].nullifiers
        hsig_input += self.joinsplit_pubkey
        return hsig_input.to_bytes()

    def _primary_input(self, index):
        '''
        Primary input for the zkproof
        '''
        primary_input = ZcashByteData()
        primary_input += self.tx_joinsplits[index].anchor
        primary_input += self.tx_joinsplits[index].nullifiers
        primary_input += self.tx_joinsplits[index].commitments
        primary_input += self.tx_joinsplits[index].vpub_old
        primary_input += self.tx_joinsplits[index].vpub_new
        primary_input += self.hsigs[index]
        primary_input += self.tx_joinsplits[index].vmacs
        return primary_input.to_bytes()

    @classmethod
    def from_bytes(SproutTx, byte_string):
        '''
        byte-like -> SproutTx
        '''
        version = byte_string[0:4]
        tx_ins = []
        tx_ins_num = VarInt.from_bytes(byte_string[4:])

        current = 4 + len(tx_ins_num)
        for _ in range(tx_ins_num.number):
            tx_in = TxIn.from_bytes(byte_string[current:])
            current += len(tx_in)
            tx_ins.append(tx_in)

        tx_outs = []
        tx_outs_num = VarInt.from_bytes(byte_string[current:])

        current += len(tx_outs_num)
        for _ in range(tx_outs_num.number):
            tx_out = TxOut.from_bytes(byte_string[current:])
            current += len(tx_out)
            tx_outs.append(tx_out)

        lock_time = byte_string[current:current + 4]
        current += 4

        tx_joinsplits = None
        joinsplit_pubkey = None
        joinsplit_sig = None
        if utils.le2i(version) == 2:  # If we expect joinsplits
            tx_joinsplits = []
            tx_joinsplits_num = VarInt.from_bytes(byte_string[current:])
            current += len(tx_joinsplits_num)

            for _ in range(tx_joinsplits_num.number):
                joinsplit = SproutJoinsplit.from_bytes(byte_string[current:])
                current += len(joinsplit)
                tx_joinsplits.append(joinsplit)
            joinsplit_pubkey = byte_string[current:current + 32]
            current += 32
            joinsplit_sig = byte_string[current:current + 64]

        return SproutTx(
            version=version,
            tx_ins=tx_ins,
            tx_outs=tx_outs,
            lock_time=lock_time,
            tx_joinsplits=tx_joinsplits,
            joinsplit_pubkey=joinsplit_pubkey,
            joinsplit_sig=joinsplit_sig)

    def calculate_fee(self, input_values):
        '''
        Tx, list(int) -> int
        '''
        total_in = sum(input_values)
        total_out = sum([utils.le2i(tx_out.value) for tx_out in self.tx_outs])
        for js in self.tx_joinsplits:
            total_in += utils.le2i(js.vpub_new)
            total_out += utils.le2i(js.vpub_old)
        return total_in - total_out

    def copy(self, version=None, tx_ins=None, tx_outs=None, lock_time=None,
             tx_joinsplits=None, joinsplit_pubkey=None, joinsplit_sig=None):
        '''
        SproutTx, ... -> Tx

        Makes a copy. Allows over-writing specific pieces.
        '''
        return SproutTx(
            version=version if version is not None else self.version,
            tx_ins=tx_ins if tx_ins is not None else self.tx_ins,
            tx_outs=tx_outs if tx_outs is not None else self.tx_outs,
            lock_time=(lock_time if lock_time is not None
                       else self.lock_time),
            tx_joinsplits=(tx_joinsplits if tx_joinsplits is not None
                           else self.tx_joinsplits),
            joinsplit_pubkey=(joinsplit_pubkey if joinsplit_pubkey is not None
                              else self.joinsplit_pubkey),
            joinsplit_sig=(joinsplit_sig if joinsplit_sig is not None
                           else self.joinsplit_sig))

    def _get_script_code(self, index):
        '''
        SproutTx, int -> bytes
        '''
        if len(self.tx_ins) > 0 and len(self.tx_ins[index].redeem_script) > 0:
            script = ByteData()
            # redeemScript in case of P2SH
            script += self.tx_ins[index].redeem_script
            return script.to_bytes()
        return b''

    def _sighash_prep(self, index, script):
        '''
        SproutTx, int, byte-like -> SproutTx
        Sighashes suck
        Performs the sighash setup described here:
        https://en.bitcoin.it/wiki/OP_CHECKSIG#How_it_works
        https://bitcoin.stackexchange.com/questions/3374/how-to-redeem-a-basic-tx
        We save on complexity by refusing to support OP_CODESEPARATOR
        '''
        sub_script = self._get_script_code(index=index)
        if sub_script == b'':
            sub_script = script

        if len(self.tx_ins) == 0:
            return self.copy(joinsplit_sig=b'')
        # 0 out scripts in tx_ins
        copy_tx_ins = [tx_in.copy(stack_script=b'', redeem_script=b'')
                       for tx_in in self.tx_ins]

        # NB: The script for the current transaction input in txCopy is set to
        #     subScript (lead in by its length as a var-integer encoded!)
        copy_tx_ins[index] = \
            copy_tx_ins[index].copy(stack_script=b'', redeem_script=sub_script)

        return self.copy(tx_ins=copy_tx_ins, joinsplit_sig=b'')

    def sighash_all(self, index=0, script=None,
                    prevout_value=None, anyone_can_pay=False):
        '''
        SproutTx, int, byte-like, byte-like, bool -> bytearray
        Sighashes suck
        Generates the hash to be signed with SIGHASH_ALL
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Hashtype_SIGHASH_ALL_.28default.29
        '''

        if riemann.network.FORKID is not None:
            return self._sighash_forkid(index=index,
                                        script=script,
                                        prevout_value=prevout_value,
                                        sighash_type=SIGHASH_ALL,
                                        anyone_can_pay=anyone_can_pay)

        copy_tx = self._sighash_prep(index=index, script=script)
        if anyone_can_pay:
            return self._sighash_anyone_can_pay(
                index=index, copy_tx=copy_tx, sighash_type=SIGHASH_ALL)

        return self._sighash_final_hashing(copy_tx, SIGHASH_ALL)

    def sighash_single(self, index=0, script=None,
                       prevout_value=None, anyone_can_pay=False):
        '''
        SproutTx, int, byte-like, byte-like, bool -> bytearray
        Sighashes suck
        Generates the hash to be signed with SIGHASH_SINGLE
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Procedure_for_Hashtype_SIGHASH_SINGLE
        https://bitcoin.stackexchange.com/questions/3890/for-sighash-single-do-the-outputs-other-than-at-the-input-index-have-8-bytes-or
        https://github.com/petertodd/python-bitcoinlib/blob/051ec4e28c1f6404fd46713c2810d4ebbed38de4/bitcoin/core/script.py#L913-L965
        '''

        if self.tx_joinsplits is not None:
            raise ValueError('Sighash single not permitted with joinsplits.')

        if index >= len(self.tx_outs):
            raise NotImplementedError(
                'I refuse to implement the SIGHASH_SINGLE bug.')

        if riemann.network.FORKID is not None:
            return self._sighash_forkid(index=index,
                                        script=script,
                                        prevout_value=prevout_value,
                                        sighash_type=SIGHASH_SINGLE,
                                        anyone_can_pay=anyone_can_pay)

        copy_tx = self._sighash_prep(index=index, script=script)

        # Remove outputs after the one we're signing
        # Other tx_outs are set to -1 value and null scripts
        copy_tx_outs = copy_tx.tx_outs[:index + 1]
        copy_tx_outs = [TxOut(value=b'\xff' * 8, output_script=b'')
                        for _ in copy_tx.tx_ins]  # Null them all
        copy_tx_outs[index] = copy_tx.tx_outs[index]  # Fix the current one

        # Other tx_ins sequence numbers are set to 0
        copy_tx_ins = [tx_in.copy(sequence=b'\x00\x00\x00\x00')
                       for tx_in in copy_tx.tx_ins]  # Set all to 0
        copy_tx_ins[index] = copy_tx.tx_ins[index]  # Fix the current one

        copy_tx = copy_tx.copy(
            tx_ins=copy_tx_ins,
            tx_outs=copy_tx_outs)

        if anyone_can_pay:  # Forward onwards
            return self._sighash_anyone_can_pay(index, copy_tx, SIGHASH_SINGLE)

        return self._sighash_final_hashing(copy_tx, SIGHASH_SINGLE)

    def _sighash_anyone_can_pay(self, index, copy_tx, sighash_type):
        '''
        int, SproutTx, int -> bytes
        Applies SIGHASH_ANYONECANPAY procedure.
        Should be called by another SIGHASH procedure.
        Not on its own.
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Procedure_for_Hashtype_SIGHASH_ANYONECANPAY
        '''

        if self.tx_joinsplits is not None:
            raise ValueError(
                'Sighash anyonecanpay not permitted with joinsplits.')

        # The txCopy input vector is resized to a length of one.
        copy_tx_ins = [copy_tx.tx_ins[index]]
        copy_tx = copy_tx.copy(tx_ins=copy_tx_ins)

        return self._sighash_final_hashing(
            copy_tx, sighash_type | SIGHASH_ANYONECANPAY)

    def _sighash_final_hashing(self, copy_tx, sighash_type):
        '''
        SproutTx, int -> bytes
        Returns the hash that should be signed
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Procedure_for_Hashtype_SIGHASH_ANYONECANPAY
        '''
        sighash = ByteData()
        sighash += copy_tx.to_bytes()
        sighash += utils.i2le_padded(sighash_type, 4)
        return utils.hash256(sighash.to_bytes())


class OverwinterTx(ZcashByteData):

    def __init__(self, tx_ins, tx_outs, lock_time, expiry_height,
                 tx_joinsplits, joinsplit_pubkey, joinsplit_sig):
        super().__init__()

        if 'overwinter' not in riemann.get_current_network_name():
            raise ValueError(
                'OverwinterTx not supported by network {}.'
                .format(riemann.get_current_network_name()))

        self.validate_bytes(lock_time, 4)
        self.validate_bytes(expiry_height, 4)

        if utils.le2i(expiry_height) > 499999999:
            raise ValueError('Expiry time too high.'
                             'Expected <= 499999999. Got {}'
                             .format(utils.le2i(expiry_height)))

        if max(len(tx_ins), len(tx_outs)) > 255:
            raise ValueError('Too many inputs or outputs. Stop that.')

        for tx_in in tx_ins:
            if not isinstance(tx_in, TxIn):
                raise ValueError(
                    'Invalid TxIn. '
                    'Expected instance of TxOut. Got {}'
                    .format(type(tx_in).__name__))

        for tx_out in tx_outs:
            if not isinstance(tx_out, TxOut):
                raise ValueError(
                    'Invalid TxOut. '
                    'Expected instance of TxOut. Got {}'
                    .format(type(tx_out).__name__))

        if len(tx_joinsplits) > 5:
            raise ValueError('Too many joinsplits. Stop that.')

        for tx_joinsplit in tx_joinsplits:
            if not isinstance(tx_joinsplit, SproutJoinsplit):
                raise ValueError(
                    'Invalid Joinsplit. '
                    'Expected instance of SproutJoinsplit. Got {}'
                    .format(type(tx_joinsplit).__name__))
        if len(tx_joinsplits) != 0:
            self.validate_bytes(joinsplit_pubkey, 32)
            self.validate_bytes(joinsplit_sig, 64)

        if len(tx_joinsplits) == 0 and len(tx_ins) == 0:
            raise ValueError('Transaction must have tx_ins or joinsplits.')

        self += b'\x03\x00\x00\x80'  # Version 3 + fOverwintered
        self += b'\x70\x82\xc4\x03'        # Overwinter Group ID
        self += VarInt(len(tx_ins))
        for tx_in in tx_ins:
            self += tx_in
        self += VarInt(len(tx_outs))
        for tx_out in tx_outs:
            self += tx_out
        self += lock_time
        self += expiry_height

        if len(tx_joinsplits) != 0:
            self += VarInt(len(tx_joinsplits))
            for tx_joinsplit in tx_joinsplits:
                self += tx_joinsplit
            self += joinsplit_pubkey
            self += joinsplit_sig

        self.header = b'\x03\x00\x00\x80'
        self.group_id = b'\x70\x82\xc4\x03'
        self.version = b'\x03\x00'
        self.tx_ins_len = len(tx_ins)
        self.tx_ins = tuple(tx_in for tx_in in tx_ins)
        self.tx_outs_len = len(tx_outs)
        self.tx_outs = tuple(tx_out for tx_out in tx_outs)
        self.tx_joinsplits_len = len(tx_joinsplits)
        self.lock_time = lock_time
        self.expiry_height = expiry_height

        if len(tx_joinsplits) != 0:
            self.tx_joinsplits = tuple(js for js in tx_joinsplits)
            self.joinsplit_pubkey = joinsplit_pubkey
            self.joinsplit_sig = joinsplit_sig
            # Zcash spec 5.4.1.4 Hsig hash function
            self.hsigs = (tuple(self._hsig(i)
                          for i in range(self.tx_joinsplits_len)))
            self.primary_inputs = (tuple(self._primary_input(i)
                                   for i in range(self.tx_joinsplits_len)))
        else:
            self.tx_joinsplits = tuple()
            self.joinsplit_pubkey = None
            self.joinsplit_sig = None
            self.hsigs = tuple()
            self.primary_inputs = tuple()

        self.tx_id_le = 1
        self.tx_id = 1

        self._make_immutable()

        if len(self) > 100000:
            raise ValueError(  # pragma: no cover
                'Tx is too large. '
                'Expect less than 100kB. Got: {} bytes'.format(len(self)))

    def calculate_fee(self, input_values):
        '''
        Tx, list(int) -> int
        '''
        total_in = sum(input_values)
        total_out = sum([utils.le2i(tx_out.value) for tx_out in self.tx_outs])
        for js in self.tx_joinsplits:
            total_in += utils.le2i(js.vpub_new)
            total_out += utils.le2i(js.vpub_old)
        return total_in - total_out

    def copy(self, tx_ins=None, tx_outs=None, lock_time=None,
             expiry_height=None, tx_joinsplits=None, joinsplit_pubkey=None,
             joinsplit_sig=None):
        '''
        OverwinterTx, ... -> OverwinterTx

        Makes a copy. Allows over-writing specific pieces.
        '''
        return OverwinterTx(
            tx_ins=tx_ins if tx_ins is not None else self.tx_ins,
            tx_outs=tx_outs if tx_outs is not None else self.tx_outs,
            lock_time=(lock_time if lock_time is not None
                       else self.lock_time),
            expiry_height=(expiry_height if expiry_height is not None
                           else self.expiry_height),
            tx_joinsplits=(tx_joinsplits if tx_joinsplits is not None
                           else self.tx_joinsplits),
            joinsplit_pubkey=(joinsplit_pubkey if joinsplit_pubkey is not None
                              else self.joinsplit_pubkey),
            joinsplit_sig=(joinsplit_sig if joinsplit_sig is not None
                           else self.joinsplit_sig))

    def _hsig(self, index):
        return utils.blake2b(
            data=self._hsig_input(index),
            digest_size=32,
            person=b'ZcashComputehSig')

    def _hsig_input(self, index):
        '''
        inputs for the hsig hash
        '''
        hsig_input = ZcashByteData()
        hsig_input += self.tx_joinsplits[index].random_seed
        hsig_input += self.tx_joinsplits[index].nullifiers
        hsig_input += self.joinsplit_pubkey
        return hsig_input.to_bytes()

    def _primary_input(self, index):
        '''
        Primary input for the zkproof
        '''
        primary_input = ZcashByteData()
        primary_input += self.tx_joinsplits[index].anchor
        primary_input += self.tx_joinsplits[index].nullifiers
        primary_input += self.tx_joinsplits[index].commitments
        primary_input += self.tx_joinsplits[index].vpub_old
        primary_input += self.tx_joinsplits[index].vpub_new
        primary_input += self.hsigs[index]
        primary_input += self.tx_joinsplits[index].vmacs
        return primary_input.to_bytes()

    @classmethod
    def from_bytes(OverwinterTx, byte_string):
        '''
        byte-like -> OverwinterTx
        '''
        header = byte_string[0:4]
        group_id = byte_string[4:8]

        if header != b'\x03\x00\x00\x80' or group_id != b'\x70\x82\xc4\x03':
            raise ValueError(
                'Bad header or group ID. Expected {} and {}. Got: {} and {}'
                .format(b'\x03\x00\x00\x80'.hex(),
                        b'\x70\x82\xc4\x03'.hex(),
                        header.hex(),
                        group_id.hex()))

        tx_ins = []
        tx_ins_num = VarInt.from_bytes(byte_string[8:])

        current = 8 + len(tx_ins_num)
        for _ in range(tx_ins_num.number):
            tx_in = TxIn.from_bytes(byte_string[current:])
            current += len(tx_in)
            tx_ins.append(tx_in)

        tx_outs = []
        tx_outs_num = VarInt.from_bytes(byte_string[current:])

        current += len(tx_outs_num)
        for _ in range(tx_outs_num.number):
            tx_out = TxOut.from_bytes(byte_string[current:])
            current += len(tx_out)
            tx_outs.append(tx_out)

        lock_time = byte_string[current:current + 4]
        current += 4
        expiry_height = byte_string[current:current + 4]
        current += 4

        if current == len(byte_string):
            # No joinsplits
            tx_joinsplits = tuple()
            joinsplit_pubkey = None
            joinsplit_sig = None
        else:
            tx_joinsplits = []
            tx_joinsplits_num = VarInt.from_bytes(byte_string[current:])
            current += len(tx_outs_num)
            for _ in range(tx_joinsplits_num.number):
                tx_joinsplit = SproutJoinsplit.from_bytes(
                    byte_string[current:])
                current += len(tx_joinsplit)
                tx_joinsplits.append(tx_joinsplit)

            joinsplit_pubkey = byte_string[current:current + 32]
            current += 32
            joinsplit_sig = byte_string[current:current + 64]

        return OverwinterTx(
            tx_ins=tx_ins,
            tx_outs=tx_outs,
            lock_time=lock_time,
            expiry_height=expiry_height,
            tx_joinsplits=tx_joinsplits,
            joinsplit_pubkey=joinsplit_pubkey,
            joinsplit_sig=joinsplit_sig)

    def is_witness(self):
        return False

    def sighash_all(self, anyone_can_pay=False, **kwargs):
        return self.sighash(sighash_type=SIGHASH_ALL, **kwargs)

    def sighash_single(self, anyone_can_pay=False, **kwargs):

        return self.sighash(sighash_type=SIGHASH_SINGLE, **kwargs)

    def sighash(self, sighash_type, index=0, joinsplit=False, script_code=None,
                anyone_can_pay=False, prevout_value=None):
        '''
        https://github.com/zcash/zips/blob/master/zip-0143.rst
        '''
        data = ByteData()

        data += self.header
        data += self.group_id

        data += self._hash_prevouts(anyone_can_pay)
        data += self._hash_sequence(sighash_type, anyone_can_pay)
        data += self._hash_outputs(sighash_type, index)
        data += self._hash_joinsplits()

        data += self.lock_time
        data += self.expiry_height
        if anyone_can_pay:
            sighash_type = sighash_type | SIGHASH_ANYONECANPAY
        data += utils.i2le_padded(sighash_type, 4)

        if not joinsplit:
            data += self.tx_ins[index].outpoint
            data += script_code
            data += prevout_value
            data += self.tx_ins[index].sequence

        print(data.hex())

        return utils.blake2b(
            data=data.to_bytes(),
            digest_size=32,
            person=b'ZcashSigHash' + bytes.fromhex('191ba85b'))  # Branch ID

    def _hash_prevouts(self, anyone_can_pay):
        if anyone_can_pay:
            return b'\x00' * 32

        data = ByteData()
        for tx_in in self.tx_ins:
            data += tx_in.outpoint
        return utils.blake2b(
            data=data.to_bytes(),
            digest_size=32,
            person=b'ZcashPrevoutHash')

    def _hash_sequence(self, sighash_type, anyone_can_pay):
        if anyone_can_pay or sighash_type == SIGHASH_SINGLE:
            return b'\x00' * 32

        data = ByteData()
        for tx_in in self.tx_ins:
            data += tx_in.sequence

        return utils.blake2b(
            data=data.to_bytes(),
            digest_size=32,
            person=b'ZcashSequencHash')

    def _hash_outputs(self, sighash_type, index):
        if sighash_type not in [SIGHASH_ALL, SIGHASH_SINGLE]:
            return b'\x00' * 32

        data = ByteData()

        if sighash_type == SIGHASH_ALL:
            for tx_out in self.tx_outs:
                data += tx_out

        if sighash_type == SIGHASH_SINGLE:
            if index > len(self.tx_outs):
                raise NotImplementedError(
                    'I refuse to implement the SIGHASH_SINGLE bug.')
            data += self.tx_outs[index]

        return utils.blake2b(
            data=data.to_bytes(),
            digest_size=32,
            person=b'ZcashOutputsHash')

    def _hash_joinsplits(self):
        if len(self.tx_joinsplits) == 0:
            return b'\x00' * 32

        data = ByteData()

        for joinsplit in self.tx_joinsplits:
            data += joinsplit

        data += self.joinsplit_pubkey

        return utils.blake2b(
            data=data.to_bytes(),
            digest_size=32,
            person=b'ZcashJSplitsHash')
