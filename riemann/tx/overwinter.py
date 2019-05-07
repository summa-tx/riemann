import riemann
from riemann import utils
from riemann.tx import shared
from riemann.tx.tx import TxIn, TxOut
from riemann.tx import zcash_shared as z

from typing import cast, Optional, Sequence, Tuple


class OverwinterTx(z.ZcashByteData):

    tx_ins: Tuple[TxIn, ...]
    tx_outs: Tuple[TxOut, ...]
    lock_time: bytes
    expiry_height: bytes
    tx_joinsplits: Tuple[z.SproutJoinsplit, ...]
    joinsplit_pubkey: Optional[bytes]
    joinsplit_sig: Optional[bytes]
    header: bytes
    group_id: bytes
    hsigs: Tuple[bytes, ...]
    primary_inputs: Tuple[bytes, ...]
    tx_id_le: bytes
    tx_id: bytes

    def __init__(self,
                 tx_ins: Sequence[TxIn],
                 tx_outs: Sequence[TxOut],
                 lock_time: bytes,
                 expiry_height: bytes,
                 tx_joinsplits: Sequence[z.SproutJoinsplit],
                 joinsplit_pubkey: Optional[bytes],
                 joinsplit_sig: Optional[bytes]):
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

        if len(tx_joinsplits) > 5:
            raise ValueError('Too many joinsplits. Stop that.')

        for tx_joinsplit in tx_joinsplits:
            if not isinstance(tx_joinsplit, z.SproutJoinsplit):
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
        self += b'\x70\x82\xc4\x03'  # Overwinter Group ID
        self += shared.VarInt(len(tx_ins))
        for tx_in in tx_ins:
            self += tx_in
        self += shared.VarInt(len(tx_outs))
        for tx_out in tx_outs:
            self += tx_out
        self += lock_time
        self += expiry_height

        self += shared.VarInt(len(tx_joinsplits))
        if len(tx_joinsplits) != 0:
            for tx_joinsplit in tx_joinsplits:
                self += tx_joinsplit
            self += cast(bytes, joinsplit_pubkey)
            self += cast(bytes, joinsplit_sig)

        self.header = b'\x03\x00\x00\x80'
        self.group_id = b'\x70\x82\xc4\x03'
        self.version = b'\x03\x00'
        self.tx_ins = tuple(tx_in for tx_in in tx_ins)
        self.tx_outs = tuple(tx_out for tx_out in tx_outs)
        self.lock_time = lock_time
        self.expiry_height = expiry_height

        if len(tx_joinsplits) != 0:
            self.tx_joinsplits = tuple(js for js in tx_joinsplits)
            self.joinsplit_pubkey = joinsplit_pubkey
            self.joinsplit_sig = joinsplit_sig
            # Zcash spec 5.4.1.4 Hsig hash function
            self.hsigs = (tuple(self._hsig(i)
                          for i in range(len(self.tx_joinsplits))))
            self.primary_inputs = (tuple(self._primary_input(i)
                                   for i in range(len(self.tx_joinsplits))))
        else:
            self.tx_joinsplits = tuple()
            self.joinsplit_pubkey = None
            self.joinsplit_sig = None
            self.hsigs = tuple()
            self.primary_inputs = tuple()

        self.tx_id_le = self.tx_id_le = utils.hash256(self.to_bytes())
        self.tx_id = self.tx_id_le[::-1]

        self._make_immutable()

        if len(self) > 100000:
            raise ValueError(  # pragma: no cover
                'Tx is too large. '
                'Expect less than 100kB. Got: {} bytes'.format(len(self)))

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
             tx_ins: Optional[Sequence[TxIn]] = None,
             tx_outs: Optional[Sequence[TxOut]] = None,
             lock_time: Optional[bytes] = None,
             expiry_height: Optional[bytes] = None,
             tx_joinsplits: Optional[Sequence[z.SproutJoinsplit]] = None,
             joinsplit_pubkey: Optional[bytes] = None,
             joinsplit_sig: Optional[bytes] = None) -> 'OverwinterTx':
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
    def from_bytes(OverwinterTx, byte_string: bytes) -> 'OverwinterTx':
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
        tx_ins_num = shared.VarInt.from_bytes(byte_string[8:])

        current = 8 + len(tx_ins_num)
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
        expiry_height = byte_string[current:current + 4]
        current += 4

        tx_joinsplits: Sequence[z.SproutJoinsplit]
        if current == len(byte_string):
            # No joinsplits
            tx_joinsplits = tuple()
            joinsplit_pubkey = None
            joinsplit_sig = None
        else:
            tx_joinsplits = []
            tx_joinsplits_num = shared.VarInt.from_bytes(byte_string[current:])
            current += len(tx_outs_num)
            for _ in range(tx_joinsplits_num.number):
                tx_joinsplit = z.SproutJoinsplit.from_bytes(
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

    def is_witness(self) -> bool:
        return False

    def sighash_all(self, anyone_can_pay: bool = False, **kwargs) -> bytes:
        return self.sighash(sighash_type=shared.SIGHASH_ALL, **kwargs)

    def sighash_single(self, anyone_can_pay: bool = False, **kwargs) -> bytes:
        return self.sighash(sighash_type=shared.SIGHASH_SINGLE, **kwargs)

    def sighash(self,
                sighash_type: int,
                prevout_value: bytes,
                script_code: bytes,
                index: int = 0,
                joinsplit: bool = False,
                anyone_can_pay: bool = False) -> bytes:
        '''
        ZIP143
        https://github.com/zcash/zips/blob/master/zip-0143.rst
        '''

        if joinsplit and anyone_can_pay:
            raise ValueError('ANYONECANPAY can\'t be used with joinsplits')

        data = z.ZcashByteData()

        data += self.header
        data += self.group_id

        data += self._hash_prevouts(anyone_can_pay)
        data += self._hash_sequence(sighash_type, anyone_can_pay)
        data += self._hash_outputs(sighash_type, index)
        data += self._hash_joinsplits()

        data += self.lock_time
        data += self.expiry_height
        if anyone_can_pay:
            sighash_type = sighash_type | shared.SIGHASH_ANYONECANPAY
        data += utils.i2le_padded(sighash_type, 4)

        if not joinsplit:
            data += self.tx_ins[index].outpoint
            data += script_code
            data += prevout_value
            data += self.tx_ins[index].sequence

        return utils.blake2b(
            data=data.to_bytes(),
            digest_size=32,
            person=b'ZcashSigHash' + bytes.fromhex('191ba85b'))  # Branch ID

    def _hash_prevouts(self, anyone_can_pay: bool) -> bytes:
        if anyone_can_pay:
            return b'\x00' * 32

        data = z.ZcashByteData()
        for tx_in in self.tx_ins:
            data += tx_in.outpoint

        return utils.blake2b(
            data=data.to_bytes(),
            digest_size=32,
            person=b'ZcashPrevoutHash')

    def _hash_sequence(self, sighash_type: int, anyone_can_pay: bool) -> bytes:
        if anyone_can_pay or sighash_type == shared.SIGHASH_SINGLE:
            return b'\x00' * 32

        data = z.ZcashByteData()
        for tx_in in self.tx_ins:
            data += tx_in.sequence

        return utils.blake2b(
            data=data.to_bytes(),
            digest_size=32,
            person=b'ZcashSequencHash')

    def _hash_outputs(self, sighash_type: int, index: int) -> bytes:
        if sighash_type not in [shared.SIGHASH_ALL, shared.SIGHASH_SINGLE]:
            return b'\x00' * 32

        data = z.ZcashByteData()

        if sighash_type == shared.SIGHASH_ALL:
            for tx_out in self.tx_outs:
                data += tx_out

        if sighash_type == shared.SIGHASH_SINGLE:
            if index > len(self.tx_outs):
                raise NotImplementedError(
                    'I refuse to implement the SIGHASH_SINGLE bug.')
            data += self.tx_outs[index]

        return utils.blake2b(
            data=data.to_bytes(),
            digest_size=32,
            person=b'ZcashOutputsHash')

    def _hash_joinsplits(self) -> bytes:
        if len(self.tx_joinsplits) == 0:
            return b'\x00' * 32

        data = z.ZcashByteData()

        for joinsplit in self.tx_joinsplits:
            data += joinsplit

        data += cast(bytes, self.joinsplit_pubkey)

        return utils.blake2b(
            data=data.to_bytes(),
            digest_size=32,
            person=b'ZcashJSplitsHash')
