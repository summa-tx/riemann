import riemann
import math
from .. import utils


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


class DecredByteData(ByteData):

    def __init__(self):
        if 'decred' not in riemann.get_current_network_name():
            raise ValueError('Decred classes not supported by network {}. '
                             'How did you get here?'
                             .format(riemann.get_current_network_name()))
        super().__init__()


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
        '''
        num = byte_string
        if num[0] >= 0xfd:
            num = num[1:]
            if len(num) == 0:
                raise ValueError('Malformed VarInt. Got: {}'
                                 .format(byte_string.hex()))
        return VarInt(utils.le2i(num))


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


class WitnessStackItem(ByteData):

    def __init__(self, item):
        super().__init__()

        self.validate_bytes(item, None)

        self += VarInt(len(item))
        self += item

        self.item_len = len(item)
        self.item = item

        self._make_immutable()

    @classmethod
    def from_bytes(WitnessStackItem, byte_string):
        WitnessStackItem.validate_bytes(byte_string, None)
        return WitnessStackItem(byte_string[1:])


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
                    'Expected bytes. Got {}'
                    .format(item))

        self += VarInt(len(stack))
        for item in stack:
            self += item

        self.stack_len = len(stack)
        self.stack = [item for item in stack]

        self._make_immutable()

    @classmethod
    def from_bytes(InputWitness, byte_string):
        # TODO: This assumes <=255 bytes in each witness stack item
        WitnessStackItem.validate_bytes(byte_string, None)
        stack_len = byte_string[0]
        current = 1
        items = []
        while len(items) < stack_len:
            item_len = byte_string[current]
            prefixed_item = byte_string[current: current + 1 + item_len]
            items += [WitnessStackItem.from_bytes(prefixed_item)]
            current += item_len + 1
        return InputWitness(items)


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
        self.tx_ins = [tx_in for tx_in in tx_ins]
        self.tx_outs_len = len(tx_outs)
        self.tx_outs = [tx_out for tx_out in tx_outs]
        self.tx_witnesses_len = self.tx_ins_len
        self.tx_witnesses = \
            [wit for wit in tx_witnesses] if tx_witnesses is not None else None
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

    def _sighash_prep(self, index, prevout_pk_script):
        '''
        Tx, int, byte-like -> Tx
        Sighashes suck
        Performs the sighash setup described here:
        https://en.bitcoin.it/wiki/OP_CHECKSIG#How_it_works
        https://bitcoin.stackexchange.com/questions/3374/how-to-redeem-a-basic-tx
        We save on complexity by refusing to support OP_CODESEPARATOR
        '''
        sub_script = prevout_pk_script  # Follow wiki naming convention
        # NB: The scripts for all transaction inputs in txCopy are set
        #     to empty scripts (exactly 1 byte 0x00)
        copy_tx_ins = [tx_in.copy(stack_script=b'', redeem_script=b'')
                       for tx_in in self.tx_ins]

        # NB: The script for the current transaction input in txCopy is set to
        #     subScript (lead in by its length as a var-integer encoded!)
        copy_tx_ins[index] = \
            copy_tx_ins[index].copy(stack_script=b'', redeem_script=sub_script)

        return self.copy(tx_ins=copy_tx_ins)

    def sighash_single(self, index, prevout_pk_script, prevout_value=None,
                       anyone_can_pay=False):
        '''
        Tx, int, byte-like, byte-like, bool -> bytearray
        Sighashes suck
        Generates the hash to be signed with SIGHASH_SINGLE
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Procedure_for_Hashtype_SIGHASH_SINGLE
        https://bitcoin.stackexchange.com/questions/3890/for-sighash-single-do-the-outputs-other-than-at-the-input-index-have-8-bytes-or
        https://github.com/petertodd/python-bitcoinlib/blob/051ec4e28c1f6404fd46713c2810d4ebbed38de4/bitcoin/core/script.py#L913-L965
        '''

        if riemann.network.FORKID is not None:
            return self._sighash_forkid(index=index,
                                        prevout_pk_script=prevout_pk_script,
                                        prevout_value=prevout_value,
                                        sighash_type=SIGHASH_SINGLE,
                                        anyone_can_pay=anyone_can_pay)

        copy_tx = self._sighash_prep(index, prevout_pk_script)
        try:
            # NB: The output of txCopy is resized
            #     to the size of the current input index+1.
            copy_tx_outs = copy_tx.tx_outs[:index + 1]

            # NB: All other txCopy outputs
            #     aside from the output that is the same as the current index
            #     are set to a blank script and a value of (long) -1.
            copy_tx_outs = [TxOut(value=b'\xff' * 8, output_script=b'')
                            for _ in copy_tx.tx_ins]  # Null them all

            copy_tx_outs[index] = copy_tx.tx_outs[index]  # Fix the current one
        except IndexError:
            raise NotImplementedError(
                'I refuse to implement the SIGHASH_SINGLE bug.')

        # NB: All other txCopy inputs aside from the current input
        #     are set to have an nSequence index of zero.
        copy_tx_ins = [tx_in.copy(sequence=b'\x00\x00\x00\x00')
                       for tx_in in copy_tx.tx_ins]  # Set all to 0
        copy_tx_ins[index] = copy_tx.tx_ins[index]  # Fix the current one

        copy_tx = copy_tx.copy(tx_ins=copy_tx_ins, tx_outs=copy_tx_outs)

        if anyone_can_pay:  # Forward onwards
            return Tx._sighash_anyone_can_pay(index, copy_tx, SIGHASH_SINGLE)

        return Tx._sighash_final_hashing(copy_tx, SIGHASH_SINGLE)

    def sighash_all(self, index, prevout_pk_script, prevout_value=None,
                    anyone_can_pay=False):
        '''
        Tx, int, byte-like, byte-like, bool -> bytearray
        Sighashes suck
        Generates the hash to be signed with SIGHASH_ALL
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Hashtype_SIGHASH_ALL_.28default.29
        '''

        if riemann.network.FORKID is not None:
            return self._sighash_forkid(index=index,
                                        prevout_pk_script=prevout_pk_script,
                                        prevout_value=prevout_value,
                                        sighash_type=SIGHASH_ALL,
                                        anyone_can_pay=anyone_can_pay)

        copy_tx = self._sighash_prep(index, prevout_pk_script)
        if anyone_can_pay:
            return Tx._sighash_anyone_can_pay(index, copy_tx, SIGHASH_ALL)

        return Tx._sighash_final_hashing(copy_tx, SIGHASH_ALL)

    @staticmethod
    def _sighash_anyone_can_pay(index, copy_tx, sighash_type):
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

        return Tx._sighash_final_hashing(
            copy_tx, sighash_type | SIGHASH_ANYONECANPAY)

    @staticmethod
    def _sighash_final_hashing(copy_tx, sighash_type):
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

    def script_code(self, index, prevout_pk_script):
        script = ByteData()
        if len(self.tx_ins[index].redeem_script) != 0:
            # redeemScript in case of P2SH
            script += VarInt(len(self.tx_ins[index].redeem_script))
            script += self.tx_ins[index].redeem_script
        else:
            # scriptPubKey in the general case
            script += VarInt(len(prevout_pk_script))
            script += prevout_pk_script
        return script.to_bytes()

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

    def _sighash_forkid(self, index, prevout_pk_script, prevout_value,
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

        data += self.script_code(index=index,
                                 prevout_pk_script=prevout_pk_script)

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


class DecredTx(ByteData):

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

        if len(tx_witnesses) != len(tx_ins):
            raise ValueError(
                'Witness and TxIn lists must be same length. '
                'Got {} inputs and {} witnesses.'
                .format(len(tx_ins), len(tx_witnesses)))

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

    def sighash_none(self):
        raise NotImplementedError('SIGHASH_NONE is a bad idea.')

    def _sighash_prep(self, index, prevout_pk_script):
        sub_script = prevout_pk_script
        copy_tx_witnesses = [w.copy(stack_script=b'', redeem_script=b'')
                             for w in self.tx_witnesses]
        copy_tx_witnesses[index] = \
            copy_tx_witnesses[index].copy(stack_script=sub_script,
                                          redeem_script=b'')

        return self.copy(tx_witnesses=copy_tx_witnesses)

    def sighash_single(self, index, prevout_pk_script, anyone_can_pay=False):
        '''
        https://github.com/decred/dcrd/blob/master/txscript/script.go
        '''
        copy_tx = self._sighash_prep(index, prevout_pk_script)

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

    def sighash_all(self, index, prevout_pk_script, anyone_can_pay=False):
        '''
        https://gist.github.com/davecgh/b00ec6e11f73620c3deddf160353961c
        https://github.com/decred/dcrd/blob/master/txscript/script.go
        '''
        copy_tx = self._sighash_prep(index, prevout_pk_script)

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
        copy_tx_ins = [copy_tx.tx_ins[index]]
        copy_tx_witnesses = [copy_tx.tx_witnesses[index]]
        copy_tx = copy_tx.copy(tx_ins=copy_tx_ins,
                               tx_witnesses=copy_tx_witnesses)

        return self._sighash_final_hashing(
            index=index,
            copy_tx=copy_tx,
            sighash_type=sighash_type | SIGHASH_ANYONECANPAY)

    def _sighash_final_hashing(self, index, copy_tx, sighash_type):
        sighash = ByteData()
        sighash += utils.i2le_padded(sighash_type, 4)
        sighash += copy_tx.prefix_hash()
        sighash += copy_tx.witness_signing_hash()
        print(sighash.hex())

        return utils.blake256(sighash.to_bytes())
