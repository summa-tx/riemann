import riemann
from riemann import utils
from riemann.tx import shared

from typing import List, Optional


class DecredByteData(shared.ByteData):

    def __init__(self):
        if 'decred' not in riemann.get_current_network_name():
            raise ValueError('Decred classes not supported by network {}. '
                             'How did you get here?'
                             .format(riemann.get_current_network_name()))
        super().__init__()


class DecredOutpoint(DecredByteData):

    tx_id: bytes
    index: bytes
    tree: bytes

    def __init__(self, tx_id: bytes, index: bytes, tree: bytes):
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

    def copy(self,
             tx_id: Optional[bytes] = None,
             index: Optional[bytes] = None,
             tree: Optional[bytes] = None):
        return DecredOutpoint(
            tx_id=tx_id if tx_id is not None else self.tx_id,
            index=index if index is not None else self.index,
            tree=tree if tree is not None else self.tree)

    @classmethod
    def from_bytes(DecredOutpoint, byte_string: bytes) -> 'DecredOutpoint':
        return DecredOutpoint(
            tx_id=byte_string[:32],
            index=byte_string[32:36],
            tree=byte_string[36:37])


class DecredTxIn(DecredByteData):

    outpoint: DecredOutpoint
    sequence: bytes

    def __init__(self, outpoint: DecredOutpoint, sequence: bytes):
        super().__init__()

        self.validate_bytes(outpoint, 37)
        self.validate_bytes(sequence, 4)

        self += outpoint
        self += sequence

        self.outpoint = outpoint
        self.sequence = sequence

        self._make_immutable()

    def copy(self,
             outpoint: Optional[DecredOutpoint] = None,
             sequence: Optional[bytes] = None) -> 'DecredTxIn':
        return DecredTxIn(
            outpoint=outpoint if outpoint is not None else self.outpoint,
            sequence=sequence if sequence is not None else self.sequence)

    @classmethod
    def from_bytes(DecredTxIn, byte_string: bytes) -> 'DecredTxIn':
        return DecredTxIn(
            outpoint=DecredOutpoint.from_bytes(byte_string[:37]),
            sequence=byte_string[37:41])


class DecredTxOut(DecredByteData):

    value: bytes
    version: bytes
    output_script: bytes

    def __init__(self, value: bytes, version: bytes, output_script: bytes):
        super().__init__()

        self.validate_bytes(value, 8)
        self.validate_bytes(version, 2)
        self.validate_bytes(output_script, None)

        self += value
        self += version
        self += shared.VarInt(len(output_script))
        self += output_script

        self.value = value
        self.version = version
        self.output_script_len = len(output_script)
        self.output_script = output_script

        self._make_immutable()

    def copy(self,
             value: Optional[bytes] = None,
             version: Optional[bytes] = None,
             output_script: Optional[bytes] = None) -> 'DecredTxOut':
        return DecredTxOut(
            value=value if value is not None else self.value,
            version=version if version is not None else self.version,
            output_script=(output_script if output_script is not None
                           else self.output_script))

    @classmethod
    def from_bytes(DecredTxOut, byte_string: bytes) -> 'DecredTxOut':
        n = shared.VarInt.from_bytes(byte_string[10:])
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

    value: bytes
    height: bytes
    index: bytes
    stack_script: bytes
    redeem_script: bytes

    def __init__(self,
                 value: bytes,
                 height: bytes,
                 index: bytes,
                 stack_script: bytes,
                 redeem_script: bytes):
        super().__init__()

        self.validate_bytes(value, 8)
        self.validate_bytes(height, 4)
        self.validate_bytes(index, 4)
        self.validate_bytes(stack_script, None)
        self.validate_bytes(redeem_script, None)

        self += value
        self += height
        self += index
        self += shared.VarInt(len(stack_script) + len(redeem_script))
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

    def copy(self,
             value: Optional[bytes] = None,
             height: Optional[bytes] = None,
             index: Optional[bytes] = None,
             stack_script: Optional[bytes] = None,
             redeem_script: Optional[bytes] = None) -> 'DecredInputWitness':
        return DecredInputWitness(
            value=value if value is not None else self.value,
            height=height if height is not None else self.height,
            index=index if index is not None else self.index,
            stack_script=(stack_script if stack_script is not None
                          else self.stack_script),
            redeem_script=(redeem_script if redeem_script is not None
                           else self.redeem_script))

    @classmethod
    def from_bytes(DecredInputWitness,
                   byte_string: bytes) -> 'DecredInputWitness':
        raise NotImplementedError('TODO')


class DecredTx(DecredByteData):

    def __init__(self,
                 version: bytes,
                 tx_ins: List[DecredTxIn],
                 tx_outs: List[DecredTxOut],
                 lock_time: bytes,
                 expiry: bytes,
                 tx_witnesses: List[DecredInputWitness]):
        super().__init__()

        self.validate_bytes(version, 4)
        self.validate_bytes(lock_time, 4)
        self.validate_bytes(expiry, 4)

        if min(len(tx_ins), len(tx_outs)) == 0:
            raise ValueError('Too few inputs or outputs. Stop that.')

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
        self += shared.VarInt(len(tx_ins))
        for tx_in in tx_ins:
            self += tx_in
        self += shared.VarInt(len(tx_outs))
        for tx_out in tx_outs:
            self += tx_out
        self += lock_time
        self += expiry
        self += shared.VarInt(len(tx_witnesses))
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

        # Ignoring this for now, as it's only used for in-block merkle trees
        # self.tx_id_full_le = utils.blake256(self.tx_id_le
        #                                     + self.witness_hash())
        # self.tx_id_full = utils.change_endianness(self.tx_id_full_le)

        self._make_immutable()

    @classmethod
    def from_bytes(DecredTx, byte_string: bytes) -> 'DecredTx':
        raise NotImplementedError('TODO')

    def prefix_hash(self) -> bytes:
        try:
            return self.tx_id_le  # Prevent redundant hashing
        except AttributeError:
            return utils.blake256(self.prefix())

    def witness_hash(self) -> bytes:
        return utils.blake256(self.witness())

    def witness_signing_hash(self) -> bytes:
        return utils.blake256(self.witness_signing())

    def prefix(self) -> bytes:
        data = DecredByteData()
        data += self.version[:2]
        data += b'\x01\x00'  # Serialization type 1 (prefix only)
        data += shared.VarInt(len(self.tx_ins))
        for tx_in in self.tx_ins:
            data += tx_in
        data += shared.VarInt(len(self.tx_outs))
        for tx_out in self.tx_outs:
            data += tx_out
        data += self.lock_time
        data += self.expiry
        return data.to_bytes()

    def witness(self) -> bytes:
        data = DecredByteData()
        data += self.version[:2]
        data += b'\x02\x00'  # Serialization type 2 (witness only)
        data += shared.VarInt(len(self.tx_witnesses))
        for tx_witness in self.tx_witnesses:
            data += tx_witness
        return data.to_bytes()

    def witness_signing(self) -> bytes:
        data = DecredByteData()
        data += self.version[:2]
        data += b'\x03\x00'  # Serialization type 3 (witness signing)
        data += shared.VarInt(len(self.tx_witnesses))
        for tx_witness in self.tx_witnesses:
            data += shared.VarInt(tx_witness.script_len)
            data += tx_witness.script_sig
        return data.to_bytes()

    def calculate_fee(self) -> int:
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

    def sighash_none(self) -> bytes:
        raise NotImplementedError('SIGHASH_NONE is a bad idea.')

    def _sighash_prep(self,
                      index: int,
                      script: Optional[bytes] = None) -> 'DecredTx':
        copy_tx_witnesses = [w.copy(stack_script=b'', redeem_script=b'')
                             for w in self.tx_witnesses]
        copy_tx_witnesses[index] = \
            copy_tx_witnesses[index].copy(stack_script=script,
                                          redeem_script=b'')

        return self.copy(tx_witnesses=copy_tx_witnesses)

    def sighash_single(self,
                       index: int,
                       script: Optional[bytes] = None,
                       anyone_can_pay: bool = False) -> bytes:
        '''
        https://github.com/decred/dcrd/blob/master/txscript/script.go
        '''
        copy_tx = self._sighash_prep(
            index=index,
            script=script)

        try:
            copy_tx_outs = copy_tx.tx_outs[:index + 1]
            copy_tx_outs = [DecredTxOut(
                            value=b'\xff' * 8,
                            version=b'\x00\x00',
                            output_script=b'')
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
                sighash_type=shared.SIGHASH_SINGLE)

        return self._sighash_final_hashing(
            index=index,
            copy_tx=copy_tx,
            sighash_type=shared.SIGHASH_SINGLE)

    def sighash_all(self,
                    index: int,
                    script: Optional[bytes] = None,
                    anyone_can_pay: bool = False) -> bytes:
        '''
        https://gist.github.com/davecgh/b00ec6e11f73620c3deddf160353961c
        https://github.com/decred/dcrd/blob/master/txscript/script.go
        '''
        copy_tx = self._sighash_prep(index, script)

        if anyone_can_pay:
            return self._sighash_anyone_can_pay(
                index=index,
                copy_tx=copy_tx,
                sighash_type=shared.SIGHASH_ALL)

        return self._sighash_final_hashing(
            index=index,
            copy_tx=copy_tx,
            sighash_type=shared.SIGHASH_ALL)

    def _sighash_anyone_can_pay(self,
                                index: int,
                                copy_tx: 'DecredTx',
                                sighash_type: int) -> bytes:
        copy_tx_witnesses = [
            w.copy(stack_script=b'', redeem_script=b'')
            for w in copy_tx.tx_witnesses]
        copy_tx_witnesses[index] = copy_tx.tx_witnesses[index]
        copy_tx = copy_tx.copy(tx_witnesses=copy_tx_witnesses)

        return self._sighash_final_hashing(
            index=index,
            copy_tx=copy_tx,
            sighash_type=sighash_type | shared.SIGHASH_ANYONECANPAY)

    def _sighash_final_hashing(
            self,
            index: int,
            copy_tx: 'DecredTx',
            sighash_type: int) -> bytes:
        sighash = DecredByteData()
        sighash += utils.i2le_padded(sighash_type, 4)
        sighash += copy_tx.prefix_hash()
        sighash += copy_tx.witness_signing_hash()
        return utils.blake256(sighash.to_bytes())
