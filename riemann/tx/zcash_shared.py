import riemann
from riemann import utils
from riemann.tx import shared


class ZcashByteData(shared.ByteData):
    def __init__(self):
        if 'zcash' not in riemann.get_current_network_name():
            raise ValueError('Zcash classes not supported by network {}. '
                             'How did you get here?'
                             .format(riemann.get_current_network_name()))
        super().__init__()


class SproutZkproof(ZcashByteData):

    pi_sub_a: bytes
    pi_prime_sub_a: bytes
    pi_sub_b: bytes
    pi_prime_sub_b: bytes
    pi_sub_c: bytes
    pi_prime_sub_c: bytes
    pi_sub_k: bytes
    pi_sub_h: bytes

    def __init__(self,
                 pi_sub_a: bytes,
                 pi_prime_sub_a: bytes,
                 pi_sub_b: bytes,
                 pi_prime_sub_b: bytes,
                 pi_sub_c: bytes,
                 pi_prime_sub_c: bytes,
                 pi_sub_k: bytes,
                 pi_sub_h: bytes):
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
    def from_bytes(SproutZkproof, byte_string: bytes) -> 'SproutZkproof':
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

    vpub_old: bytes
    vpub_new: bytes
    anchor: bytes
    nullifiers: bytes
    commitments: bytes
    ephemeral_key: bytes
    random_seed: bytes
    vmacs: bytes
    zkproof: SproutZkproof
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
                 zkproof: SproutZkproof,
                 encoded_notes: bytes):
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
    def from_bytes(SproutJoinsplit, byte_string: bytes) -> 'SproutJoinsplit':
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
