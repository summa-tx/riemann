import riemann
from riemann import utils

from typing import Any, Optional, Union
Byteslike = Union[bytes, bytearray, 'ByteData']

SIGHASH_ALL = 0x01
SIGHASH_NONE = 0x02
SIGHASH_SINGLE = 0x03
SIGHASH_FORKID = 0x40
SIGHASH_ANYONECANPAY = 0x80


class ByteData():
    '''
    Wrapper class for byte-like data
    Iterable and subscriptable (by iterating and subscribing to wrapped data)
    Can be made immutable
    self._bytes is a bytearray object when mutable
    self._bytes is a byte object when immutable
    Should be mostly transparent to the user
    Can be treated like bytes or a bytearray in most cases
    '''
    __immutable = False

    def __init__(self):
        self._bytes = bytearray()

    def __iter__(self):
        return iter(self._bytes)

    def __getitem__(self, val):
        return self._bytes[val]

    def __iadd__(self, other: Byteslike):
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

    def __setattr__(self, key: str, value):
        if self.__immutable:
            raise TypeError("%r cannot be written to." % self)
        object.__setattr__(self, key, value)

    def __repr__(self):
        '''
        ByteData -> str
        '''
        return '{}: {}'.format(type(self).__name__, self._bytes)

    def to_bytes(self) -> bytes:
        '''
        ByteData -> bytes
        '''
        return bytes(self._bytes)

    def hex(self) -> str:
        '''
        ByteData -> hex_string
        '''
        return self._bytes.hex()

    def _make_immutable(self):
        '''
        Prevents any future changes to the object
        '''
        self._bytes = bytes(self._bytes)
        self.__immutable = True

    def find(self, substring: Byteslike) -> int:
        '''
        byte-like -> int
        Finds the index of substring
        '''
        if isinstance(substring, ByteData):
            substring = substring.to_bytes()
        return self._bytes.find(substring)

    @staticmethod
    def validate_bytes(data: Any, length: Optional[int] = 4):
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

        # allow any length
        if length is None:
            return

        if len(data) != length:
            raise ValueError('Expected byte-like object with length {}. '
                             'Got {} with length {}.'
                             .format(length, type(data), len(data)))

    @classmethod
    def from_hex(C, hex_string: str):
        return C.from_bytes(bytes.fromhex(hex_string))

    @classmethod
    def from_bytes(ByteData, byte_string: bytes) -> 'ByteData':
        ret = ByteData()
        ret += byte_string
        return ret


class VarInt(ByteData):
    '''
    NB: number must be integer
    '''
    def __init__(self, number: int, length: Optional[int] = None):
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
        elif number <= 0xffff or length == 3:
            self += bytes([0xfd])
            length = 3
        elif number <= 0xffffffff or length == 5:
            self += bytes([0xfe])
            length = 5
        elif number <= 0xffffffffffffffff or length == 9:
            self += bytes([0xff])
            length = 9
        self += utils.i2le(number)

        if length is not None:
            while len(self) < length:
                self += b'\x00'

        self.number = number

        self._make_immutable()

    def copy(self) -> 'VarInt':
        return VarInt(self.number)

    @classmethod
    def from_bytes(VarInt, byte_string: bytes) -> 'VarInt':
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
            non_compact = (num[-1:] == b'\x00')
        elif num[0] == 0xfe:
            num = num[1:5]
            non_compact = (num[-2:] == b'\x00\x00')
        elif num[0] == 0xff:
            num = num[1:9]
            non_compact = (num[-4:] == b'\x00\x00\x00\x00')
        if len(num) not in [1, 2, 4, 8]:
            raise ValueError('Malformed VarInt. Got: {}'
                             .format(byte_string.hex()))

        if (non_compact
            and ('overwinter' in riemann.get_current_network_name()
                 or 'sapling' in riemann.get_current_network_name())):
            raise ValueError('VarInt must be compact. Got: {}'
                             .format(byte_string.hex()))

        ret = VarInt(
            utils.le2i(num),
            length=len(num) + 1 if non_compact else 0)

        return ret
