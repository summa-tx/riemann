import riemann
from riemann import utils
from riemann.tx import shared
from riemann.tx.tx import TxIn, TxOut
from riemann.tx import zcash_shared as z

from typing import cast, Optional, Sequence, Tuple


class SaplingZkproof(z.ZcashByteData):

    pi_sub_a: bytes
    pi_sub_b: bytes
    pi_sub_c: bytes

    def __init__(self, pi_sub_a: bytes, pi_sub_b: bytes, pi_sub_c: bytes):
        super().__init__()

        self.validate_bytes(pi_sub_a, 48)
        self.validate_bytes(pi_sub_b, 96)
        self.validate_bytes(pi_sub_c, 48)

        self += pi_sub_a
        self += pi_sub_b
        self += pi_sub_c

        self.pi_sub_a = pi_sub_a
        self.pi_sub_b = pi_sub_b
        self.pi_sub_c = pi_sub_c

        self._make_immutable()

    @classmethod
    def from_bytes(SaplingZkproof, byte_string: bytes) -> 'SaplingZkproof':
        return SaplingZkproof(
            pi_sub_a=byte_string[0:48],
            pi_sub_b=byte_string[48:144],
            pi_sub_c=byte_string[144:192])


class SaplingShieldedSpend(z.ZcashByteData):

    cv: bytes
    anchor: bytes
    nullifier: bytes
    rk: bytes
    zkproof: SaplingZkproof
    spend_auth_sig: bytes

    def __init__(self,
                 cv: bytes,
                 anchor: bytes,
                 nullifier: bytes,
                 rk: bytes,
                 zkproof: SaplingZkproof,
                 spend_auth_sig: bytes):
        super().__init__()

        self.validate_bytes(cv, 32)
        self.validate_bytes(anchor, 32)
        self.validate_bytes(nullifier, 32)
        self.validate_bytes(rk, 32)
        self.validate_bytes(spend_auth_sig, 64)
        if not isinstance(zkproof, SaplingZkproof):
            raise ValueError(
                'Invalid zkproof. '
                'Expected instance of SaplingZkproof. Got {}'
                .format(type(zkproof).__name__))

        self += cv
        self += anchor
        self += nullifier
        self += rk
        self += zkproof
        self += spend_auth_sig

        self.cv = cv
        self.anchor = anchor
        self.nullifier = nullifier
        self.rk = rk
        self.zkproof = zkproof
        self.spend_auth_sig = spend_auth_sig

        self._make_immutable()

    @classmethod
    def from_bytes(SaplingShieldedSpend,
                   byte_string: bytes) -> 'SaplingShieldedSpend':
        return SaplingShieldedSpend(
            cv=byte_string[0:32],
            anchor=byte_string[32:64],
            nullifier=byte_string[64:96],
            rk=byte_string[96:128],
            zkproof=SaplingZkproof.from_bytes(byte_string[128:320]),
            spend_auth_sig=byte_string[320:384])


class SaplingShieldedOutput(z.ZcashByteData):

    cv: bytes
    cmu: bytes
    ephemeral_key: bytes
    enc_ciphertext: bytes
    out_ciphertext: bytes
    zkproof: SaplingZkproof

    def __init__(self,
                 cv: bytes,
                 cmu: bytes,
                 ephemeral_key: bytes,
                 enc_ciphertext: bytes,
                 out_ciphertext: bytes,
                 zkproof: SaplingZkproof):
        super().__init__()

        self.validate_bytes(cv, 32)
        self.validate_bytes(cmu, 32)
        self.validate_bytes(ephemeral_key, 32)
        self.validate_bytes(enc_ciphertext, 580)
        self.validate_bytes(out_ciphertext, 80)
        if not isinstance(zkproof, SaplingZkproof):
            raise ValueError(
                'Invalid zkproof. '
                'Expected instance of SaplingZkproof. Got {}'
                .format(type(zkproof).__name__))

        self += cv
        self += cmu
        self += ephemeral_key
        self += enc_ciphertext
        self += out_ciphertext
        self += zkproof

        self.cv = cv
        self.cmu = cmu
        self.ephemeral_key = ephemeral_key
        self.enc_ciphertext = enc_ciphertext
        self.out_ciphertext = out_ciphertext
        self.zkproof = zkproof

        self._make_immutable()

    @classmethod
    def from_bytes(
            SaplingShieldedOutput,
            byte_string: bytes) -> 'SaplingShieldedOutput':
        return SaplingShieldedOutput(
            cv=byte_string[0:32],
            cmu=byte_string[32:64],
            ephemeral_key=byte_string[64:96],
            enc_ciphertext=byte_string[96:676],
            out_ciphertext=byte_string[676:756],
            zkproof=SaplingZkproof.from_bytes(byte_string[756:948]))


class SaplingJoinsplit(z.ZcashByteData):

    vpub_old: bytes
    vpub_new: bytes
    anchor: bytes
    nullifiers: bytes
    commitments: bytes
    ephemeral_key: bytes
    random_seed: bytes
    vmacs: bytes
    zkproof: SaplingZkproof
    encoded_notes: bytes

    def __init__(self,
                 vpub_old: bytes,
                 vpub_new: bytes,
                 anchor: bytes,
                 nullifiers: bytes,
                 commitments: bytes,
                 ephemeral_key: bytes,
                 random_seed: bytes,
                 vmacs: bytes,
                 zkproof: SaplingZkproof,
                 encoded_notes: bytes):
        super().__init__()

        if not isinstance(zkproof, SaplingZkproof):
            raise ValueError(
                'Invalid zkproof. '
                'Expected instance of SaplingZkproof. Got {}'
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
    def from_bytes(SaplingJoinsplit, byte_string: bytes) -> 'SaplingJoinsplit':
        return SaplingJoinsplit(
            vpub_old=byte_string[0:8],
            vpub_new=byte_string[8:16],
            anchor=byte_string[16:48],
            nullifiers=byte_string[48:112],
            commitments=byte_string[112:176],
            ephemeral_key=byte_string[176:208],
            random_seed=byte_string[208:240],
            vmacs=byte_string[240:304],
            zkproof=SaplingZkproof.from_bytes(byte_string[304:496]),
            encoded_notes=byte_string[496:1698])


class SaplingTx(z.ZcashByteData):

    tx_ins: Tuple[TxIn, ...]
    tx_outs: Tuple[TxOut, ...]
    lock_time: bytes
    expiry_height: bytes
    value_balance: bytes
    tx_shielded_spends: Tuple[SaplingShieldedSpend, ...]
    tx_shielded_outputs: Tuple[SaplingShieldedOutput, ...]
    tx_joinsplits: Tuple[SaplingJoinsplit, ...]
    joinsplit_pubkey: Optional[bytes]
    joinsplit_sig: Optional[bytes]
    binding_sig: Optional[bytes]
    hsigs: Tuple[bytes, ...]
    primary_inputs: Tuple[bytes, ...]
    tx_id_le: bytes
    tx_id: bytes

    def __init__(self,
                 tx_ins: Sequence[TxIn],
                 tx_outs: Sequence[TxOut],
                 lock_time: bytes,
                 expiry_height: bytes,
                 value_balance: bytes,
                 tx_shielded_spends: Sequence[SaplingShieldedSpend],
                 tx_shielded_outputs: Sequence[SaplingShieldedOutput],
                 tx_joinsplits: Sequence[SaplingJoinsplit],
                 joinsplit_pubkey: Optional[bytes],
                 joinsplit_sig: Optional[bytes],
                 binding_sig: Optional[bytes]):
        super().__init__()

        if 'sapling' not in riemann.get_current_network_name():
            raise ValueError(
                'SaplingTx not supported by network {}.'
                .format(riemann.get_current_network_name()))

        self.validate_bytes(lock_time, 4)
        self.validate_bytes(expiry_height, 4)
        self.validate_bytes(value_balance, 8)

        if utils.le2i(expiry_height) > 499999999:
            raise ValueError('Expiry time too high.'
                             'Expected <= 499999999. Got {}'
                             .format(utils.le2i(expiry_height)))

        if (len(tx_shielded_spends) + len(tx_shielded_outputs) == 0
                and value_balance != b'\x00' * 8):
            raise ValueError('If no shielded inputs or outputs, value balance '
                             'must be 8 0-bytes. Got {}'
                             .format(value_balance.hex()))
        elif binding_sig is not None:
            self.validate_bytes(binding_sig, 64)

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

        for shielded_spend in tx_shielded_spends:
            if not isinstance(shielded_spend, SaplingShieldedSpend):
                raise ValueError(
                    'Invalid shielded spend. '
                    'Expected instance of SaplingShieldedSpend. Got {}'
                    .format(type(shielded_spend).__name__))

        for shielded_output in tx_shielded_outputs:
            if not isinstance(shielded_output, SaplingShieldedOutput):
                raise ValueError(
                    'Invalid shielded output. '
                    'Expected instance of SaplingShieldedOutput. Got {}'
                    .format(type(shielded_output).__name__))

        for tx_joinsplit in tx_joinsplits:
            if not isinstance(tx_joinsplit, SaplingJoinsplit):
                raise ValueError(
                    'Invalid Joinsplit. '
                    'Expected instance of SaplingJoinsplit. Got {}'
                    .format(type(tx_joinsplit).__name__))

        if len(tx_joinsplits) != 0:
            self.validate_bytes(joinsplit_pubkey, 32)
            self.validate_bytes(joinsplit_sig, 64)

        if len(tx_joinsplits) + len(tx_ins) + len(tx_shielded_spends) == 0:
            raise ValueError('Transaction must have some input value.')

        self += b'\x04\x00\x00\x80'  # Sapling is always v4 with overwintered
        self += b'\x85\x20\x2f\x89'  # Sapling version group id
        self += shared.VarInt(len(tx_ins))
        for tx_in in tx_ins:
            self += tx_in
        self += shared.VarInt(len(tx_outs))
        for tx_out in tx_outs:
            self += tx_out
        self += lock_time
        self += expiry_height
        self += value_balance

        self += shared.VarInt(len(tx_shielded_spends))
        if len(tx_shielded_spends) != 0:
            for shielded_spend in tx_shielded_spends:
                self += shielded_spend

        self += shared.VarInt(len(tx_shielded_outputs))
        if len(tx_shielded_outputs) != 0:
            for shielded_output in tx_shielded_outputs:
                self += shielded_output

        self += shared.VarInt(len(tx_joinsplits))
        if len(tx_joinsplits) != 0:
            for tx_joinsplit in tx_joinsplits:
                self += tx_joinsplit
            self += cast(bytes, joinsplit_pubkey)
            self += cast(bytes, joinsplit_sig)

        if len(tx_shielded_outputs) + len(tx_shielded_spends) != 0:
            self += cast(bytes, binding_sig)
            self.binding_sig = binding_sig
        else:
            self.binding_sig = None

        self.header = b'\x04\x00\x00\x80'  # Sapling is always v4
        self.group_id = b'\x85\x20\x2f\x89'  # Sapling version group id
        self.tx_ins = tuple(tx_in for tx_in in tx_ins)
        self.tx_outs = tuple(tx_out for tx_out in tx_outs)
        self.lock_time = lock_time
        self.expiry_height = expiry_height
        self.value_balance = value_balance

        if len(tx_shielded_spends) != 0:
            self.tx_shielded_spends = tuple(ss for ss in tx_shielded_spends)
        else:
            self.tx_shielded_spends = tuple()

        if len(tx_shielded_outputs) != 0:
            self.tx_shielded_outputs = tuple(so for so in tx_shielded_outputs)
        else:
            self.tx_shielded_outputs = tuple()

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

        self.tx_id_le = utils.hash256(self.to_bytes())
        self.tx_id = self.tx_id_le[::-1]

        self._make_immutable()

        if len(self) > 100000:
            raise ValueError(  # pragma: no cover
                'Tx is too large. '
                'Expect less than 100kB. Got: {} bytes'.format(len(self)))

    def calculate_fee(self, input_values: Sequence[int]) -> int:
        '''
        SaplingTx, list(int) -> int
        '''
        total_in = sum(input_values)
        total_out = sum([utils.le2i(tx_out.value) for tx_out in self.tx_outs])
        shileded_net = utils.le2i(self.value_balance, signed=True)
        for js in self.tx_joinsplits:
            total_in += utils.le2i(js.vpub_new)
            total_out += utils.le2i(js.vpub_old)
        return total_in - total_out + shileded_net

    def copy(self,
             tx_ins: Optional[Sequence[TxIn]] = None,
             tx_outs: Optional[Sequence[TxOut]] = None,
             lock_time: Optional[bytes] = None,
             expiry_height: Optional[bytes] = None,
             value_balance: Optional[bytes] = None,
             tx_shielded_spends:
             Optional[Sequence[SaplingShieldedSpend]] = None,
             tx_shielded_outputs:
             Optional[Sequence[SaplingShieldedOutput]] = None,
             tx_joinsplits: Optional[Sequence[SaplingJoinsplit]] = None,
             joinsplit_pubkey: Optional[bytes] = None,
             joinsplit_sig: Optional[bytes] = None,
             binding_sig: Optional[bytes] = None):
        '''
        SaplingTx, ... -> SaplingTx

        Makes a copy. Allows over-writing specific pieces.
        '''
        return SaplingTx(
            tx_ins=tx_ins if tx_ins is not None else self.tx_ins,
            tx_outs=tx_outs if tx_outs is not None else self.tx_outs,
            lock_time=(lock_time if lock_time is not None
                       else self.lock_time),
            expiry_height=(expiry_height if expiry_height is not None
                           else self.expiry_height),
            value_balance=(value_balance if value_balance is not None
                           else self.value_balance),
            tx_shielded_spends=(
                tx_shielded_spends if tx_shielded_spends is not None
                else self.tx_shielded_spends),
            tx_shielded_outputs=(
                tx_shielded_outputs if tx_shielded_outputs is not None
                else self.tx_shielded_outputs),
            tx_joinsplits=(tx_joinsplits if tx_joinsplits is not None
                           else self.tx_joinsplits),
            joinsplit_pubkey=(joinsplit_pubkey if joinsplit_pubkey is not None
                              else self.joinsplit_pubkey),
            joinsplit_sig=(joinsplit_sig if joinsplit_sig is not None
                           else self.joinsplit_sig),
            binding_sig=(binding_sig if binding_sig is not None
                         else self.binding_sig))

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
    def from_bytes(SaplingTx, byte_string: bytes) -> 'SaplingTx':
        '''
        byte-like -> SaplingTx
        '''
        header = byte_string[0:4]
        group_id = byte_string[4:8]

        if header != b'\x04\x00\x00\x80' or group_id != b'\x85\x20\x2f\x89':
            raise ValueError(
                'Bad header or group ID. Expected {} and {}. Got: {} and {}'
                .format(b'\x04\x00\x00\x80'.hex(),
                        b'\x85\x20\x2f\x89'.hex(),
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
        value_balance = byte_string[current:current + 8]
        current += 8

        tx_shielded_spends = []
        shielded_spends_num = shared.VarInt.from_bytes(byte_string[current:])

        current += len(shielded_spends_num)
        for _ in range(shielded_spends_num.number):
            ss = SaplingShieldedSpend.from_bytes(byte_string[current:])
            current += len(ss)
            tx_shielded_spends.append(ss)

        tx_shielded_outputs = []
        shielded_outputs_num = shared.VarInt.from_bytes(byte_string[current:])

        current += len(shielded_outputs_num)
        for _ in range(shielded_outputs_num.number):
            so = SaplingShieldedOutput.from_bytes(byte_string[current:])
            current += len(so)
            tx_shielded_outputs.append(so)

        tx_joinsplits = []
        tx_joinsplits_num = shared.VarInt.from_bytes(byte_string[current:])
        current += len(tx_outs_num)
        for _ in range(tx_joinsplits_num.number):
            tx_joinsplit = SaplingJoinsplit.from_bytes(
                byte_string[current:])
            current += len(tx_joinsplit)
            tx_joinsplits.append(tx_joinsplit)

        joinsplit_pubkey: Optional[bytes]
        joinsplit_sig: Optional[bytes]
        if len(tx_joinsplits) > 0:
            joinsplit_pubkey = byte_string[current:current + 32]
            current += 32
            joinsplit_sig = byte_string[current:current + 64]
            current += 64
        else:
            joinsplit_pubkey = None
            joinsplit_sig = None

        binding_sig: Optional[bytes]
        if len(tx_shielded_spends) + len(tx_shielded_outputs) > 0:
            binding_sig = byte_string[current:current + 64]
            current += 64
        else:
            binding_sig = None

        return SaplingTx(
            tx_ins=tx_ins,
            tx_outs=tx_outs,
            lock_time=lock_time,
            expiry_height=expiry_height,
            value_balance=value_balance,
            tx_shielded_spends=tx_shielded_spends,
            tx_shielded_outputs=tx_shielded_outputs,
            tx_joinsplits=tx_joinsplits,
            joinsplit_pubkey=joinsplit_pubkey,
            joinsplit_sig=joinsplit_sig,
            binding_sig=binding_sig)

    def is_witness(self) -> bool:
        return False

    def sighash_all(self, anyone_can_pay: bool = False, **kwargs) -> bytes:
        return self.sighash(sighash_type=shared.SIGHASH_ALL, **kwargs)

    def sighash_single(self, anyone_can_pay: bool = False, **kwargs) -> bytes:
        return self.sighash(sighash_type=shared.SIGHASH_SINGLE, **kwargs)

    def sighash(self,
                sighash_type: int,
                prevout_value: bytes,
                index: int = 0,
                joinsplit: bool = False,
                script_code: Optional[bytes] = None,
                anyone_can_pay: bool = False) -> bytes:
        '''
        ZIP243
        https://github.com/zcash/zips/blob/master/zip-0243.rst
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
        data += self._hash_shielded_spends()
        data += self._hash_shielded_outputs()

        data += self.lock_time
        data += self.expiry_height
        data += self.value_balance

        if anyone_can_pay:
            sighash_type = sighash_type | shared.SIGHASH_ANYONECANPAY
        data += utils.i2le_padded(sighash_type, 4)

        if not joinsplit:
            data += self.tx_ins[index].outpoint
            data += cast(bytes, script_code)
            data += prevout_value
            data += self.tx_ins[index].sequence

        return utils.blake2b(
            data=data.to_bytes(),
            digest_size=32,
            person=b'ZcashSigHash' + bytes.fromhex('bb09b876'))  # Branch ID

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

    def _hash_shielded_spends(self) -> bytes:
        if len(self.tx_shielded_spends) == 0:
            return b'\x00' * 32

        data = z.ZcashByteData()

        for ss in self.tx_shielded_spends:
            data += ss[:320]  # Strip off spend_auth_sig

        return utils.blake2b(
            data=data.to_bytes(),
            digest_size=32,
            person=b'ZcashSSpendsHash')

    def _hash_shielded_outputs(self) -> bytes:
        if len(self.tx_shielded_outputs) == 0:
            return b'\x00' * 32

        data = z.ZcashByteData()

        for so in self.tx_shielded_outputs:
            data += so

        return utils.blake2b(
            data=data.to_bytes(),
            digest_size=32,
            person=b'ZcashSOutputHash')
