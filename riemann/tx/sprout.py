import riemann
from riemann import utils
from riemann.tx import shared
from riemann.tx.tx import TxIn, TxOut
from riemann.tx import zcash_shared as z

from typing import cast, Optional, Sequence, Tuple


class SproutTx(z.ZcashByteData):

    tx_ins: Tuple[TxIn, ...]
    tx_outs: Tuple[TxOut, ...]
    lock_time: bytes
    tx_joinsplits: Tuple[z.SproutJoinsplit, ...]
    joinsplit_pubkey: Optional[bytes]
    joinsplit_sig: Optional[bytes]
    version: bytes
    hsigs: Tuple[bytes, ...]
    primary_inputs: Tuple[bytes, ...]
    tx_id_le: bytes
    tx_id: bytes

    def __init__(self,
                 version: bytes,
                 tx_ins: Sequence[TxIn],
                 tx_outs: Sequence[TxOut],
                 lock_time: bytes,
                 tx_joinsplits: Sequence[z.SproutJoinsplit],
                 joinsplit_pubkey: Optional[bytes],
                 joinsplit_sig: Optional[bytes]):

        super().__init__()

        if 'sprout' not in riemann.get_current_network_name():
            raise ValueError(
                'SproutTx not supported by network {}.'
                .format(riemann.get_current_network_name()))

        self.validate_bytes(version, 4)
        self.validate_bytes(lock_time, 4)

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
                if not isinstance(tx_joinsplit, z.SproutJoinsplit):
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
        self += shared.VarInt(len(tx_ins))
        for tx_in in tx_ins:
            self += tx_in
        self += shared.VarInt(len(tx_outs))
        for tx_out in tx_outs:
            self += tx_out
        self += lock_time

        if version == utils.i2le_padded(2, 4):
            self += shared.VarInt(len(tx_joinsplits))
            for tx_joinsplit in tx_joinsplits:
                self += tx_joinsplit
            self += cast(bytes, joinsplit_pubkey)
            self += cast(bytes, joinsplit_sig)

        self.version = version
        self.tx_ins = tuple(tx_in for tx_in in tx_ins)
        self.tx_outs = tuple(tx_out for tx_out in tx_outs)
        self.tx_joinsplits = tuple(js for js in tx_joinsplits)
        self.lock_time = lock_time

        if version == utils.i2le_padded(2, 4):
            self.joinsplit_pubkey = joinsplit_pubkey
            self.joinsplit_sig = joinsplit_sig
            # Zcash spec 5.4.1.4 Hsig hash function
            self.hsigs = (tuple(self._hsig(i)
                          for i in range(len(self.tx_joinsplits))))
            self.primary_inputs = (tuple(self._primary_input(i)
                                   for i in range(len(self.tx_joinsplits))))
        else:
            self.joinsplit_pubkey = None
            self.joinsplit_sig = None
            self.hsigs = tuple()
            self.primary_inputs = tuple()

        self.tx_id_le = utils.hash256(self.to_bytes())
        self.tx_id = utils.hash256(self.to_bytes())[::-1]

        self._make_immutable()

        if len(self) > 100000:
            raise ValueError(  # pragma: no cover
                'Tx is too large. '
                'Expect less than 100kB. Got: {} bytes'.format(len(self)))

    def _hsig(self, index: int) -> bytes:
        return utils.blake2b(
            data=self._hsig_input(index),
            digest_size=32,
            person=b'ZcashComputehSig')

    def _hsig_input(self, index: int) -> bytes:
        '''
        inputs for the hsig hash
        '''
        hsig_input = z.ZcashByteData()
        hsig_input += self.tx_joinsplits[index].random_seed
        hsig_input += self.tx_joinsplits[index].nullifiers
        hsig_input += cast(bytes, self.joinsplit_pubkey)
        return hsig_input.to_bytes()

    def _primary_input(self, index: int) -> bytes:
        '''
        Primary input for the zkproof
        '''
        primary_input = z.ZcashByteData()
        primary_input += self.tx_joinsplits[index].anchor
        primary_input += self.tx_joinsplits[index].nullifiers
        primary_input += self.tx_joinsplits[index].commitments
        primary_input += self.tx_joinsplits[index].vpub_old
        primary_input += self.tx_joinsplits[index].vpub_new
        primary_input += self.hsigs[index]
        primary_input += self.tx_joinsplits[index].vmacs
        return primary_input.to_bytes()

    @classmethod
    def from_bytes(SproutTx, byte_string: bytes) -> 'SproutTx':
        '''
        byte-like -> SproutTx
        '''
        version = byte_string[0:4]
        tx_ins = []
        tx_ins_num = shared.VarInt.from_bytes(byte_string[4:])

        current = 4 + len(tx_ins_num)
        for _ in range(tx_ins_num.number):
            tx_in = TxIn.from_bytes(byte_string[current:])
            current += len(tx_in)
            tx_ins.append(tx_in)

        tx_outs = []
        tx_outs_num = shared.VarInt.from_bytes(byte_string[current:])

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
            tx_joinsplits_num = shared.VarInt.from_bytes(byte_string[current:])
            current += len(tx_joinsplits_num)

            for _ in range(tx_joinsplits_num.number):
                joinsplit = z.SproutJoinsplit.from_bytes(byte_string[current:])
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

    def calculate_fee(self, input_values: Sequence[int]) -> int:
        '''
        Tx, list(int) -> int
        '''
        total_in = sum(input_values)
        total_out = sum([utils.le2i(tx_out.value) for tx_out in self.tx_outs])
        for js in self.tx_joinsplits:
            total_in += utils.le2i(js.vpub_new)
            total_out += utils.le2i(js.vpub_old)
        return total_in - total_out

    def copy(self,
             version: Optional[bytes] = None,
             tx_ins: Optional[Sequence[TxIn]] = None,
             tx_outs: Optional[Sequence[TxOut]] = None,
             lock_time: Optional[bytes] = None,
             tx_joinsplits: Optional[Sequence[z.SproutJoinsplit]] = None,
             joinsplit_pubkey: Optional[bytes] = None,
             joinsplit_sig: Optional[bytes] = None) -> 'SproutTx':
        '''
        SproutTx, ... -> SproutTx

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

    def _sighash_prep(self, index: int, script: bytes) -> 'SproutTx':
        '''
        SproutTx, int, byte-like -> SproutTx
        Sighashes suck
        Performs the sighash setup described here:
        https://en.bitcoin.it/wiki/OP_CHECKSIG#How_it_works
        https://bitcoin.stackexchange.com/questions/3374/how-to-redeem-a-basic-tx
        We save on complexity by refusing to support OP_CODESEPARATOR
        '''

        if len(self.tx_ins) == 0:
            return self.copy(joinsplit_sig=b'')
        # 0 out scripts in tx_ins
        copy_tx_ins = [tx_in.copy(stack_script=b'', redeem_script=b'')
                       for tx_in in self.tx_ins]

        # NB: The script for the current transaction input in txCopy is set to
        #     subScript (lead in by its length as a var-integer encoded!)
        to_strip = shared.VarInt.from_bytes(script)
        copy_tx_ins[index] = \
            copy_tx_ins[index].copy(redeem_script=script[len(to_strip):])

        return self.copy(tx_ins=copy_tx_ins, joinsplit_sig=b'')

    def sighash_all(self,
                    index: int,
                    script: bytes,
                    anyone_can_pay: bool = False):
        '''
        SproutTx, int, byte-like, byte-like, bool -> bytearray
        Sighashes suck
        Generates the hash to be signed with SIGHASH_ALL
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Hashtype_SIGHASH_ALL_.28default.29
        '''

        copy_tx = self._sighash_prep(index=index, script=script)
        if anyone_can_pay:
            return self._sighash_anyone_can_pay(
                index=index, copy_tx=copy_tx, sighash_type=shared.SIGHASH_ALL)

        return self._sighash_final_hashing(copy_tx, shared.SIGHASH_ALL)

    def sighash_single(self,
                       index: int,
                       script: bytes,
                       anyone_can_pay: bool = False):
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
            return self._sighash_anyone_can_pay(
                index, copy_tx, shared.SIGHASH_SINGLE)

        return self._sighash_final_hashing(copy_tx, shared.SIGHASH_SINGLE)

    def _sighash_anyone_can_pay(
            self,
            index: int,
            copy_tx: 'SproutTx',
            sighash_type: int) -> bytes:
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
            copy_tx, sighash_type | shared.SIGHASH_ANYONECANPAY)

    def _sighash_final_hashing(
            self,
            copy_tx: 'SproutTx',
            sighash_type: int) -> bytes:
        '''
        SproutTx, int -> bytes
        Returns the hash that should be signed
        https://en.bitcoin.it/wiki/OP_CHECKSIG#Procedure_for_Hashtype_SIGHASH_ANYONECANPAY
        '''
        sighash = z.ZcashByteData()
        sighash += copy_tx.to_bytes()
        sighash += utils.i2le_padded(sighash_type, 4)
        return utils.hash256(sighash.to_bytes())
