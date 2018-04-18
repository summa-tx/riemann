import hashlib


def i2le(number):
    '''
    int -> bytearray
    '''
    if number == 0:
        return b'\x00'
    return number.to_bytes((number.bit_length() + 7) // 8, 'little')


def i2le_padded(number, length):
    '''
    int, int -> bytearray
    '''
    return number.to_bytes(length, 'little')


def le2i(b, signed=False):
    '''
    byte-like, bool -> int
    '''
    return int.from_bytes(b, 'little', signed=signed)


def be2i(b, signed=False):
    '''
    byte-like, bool -> int
    '''
    return int.from_bytes(b, 'big', signed=signed)


def change_endianness(b):
    '''
    iter -> iter
    '''
    return b[::-1]


def rmd160(msg_bytes):
    '''
    byte-like -> bytes
    '''
    h = hashlib.new('ripemd160')
    h.update(msg_bytes)
    return h.digest()


def sha256(msg_bytes):
    '''
    byte-like -> bytes
    '''
    return hashlib.sha256(msg_bytes).digest()


def hash160(msg_bytes):
    '''
    byte-like -> bytes
    '''
    h = hashlib.new('ripemd160')
    h.update(sha256(msg_bytes))
    return h.digest()


def hash256(msg_bytes):
    '''
    byte-like -> bytes
    '''
    return hashlib.sha256(hashlib.sha256(msg_bytes).digest()).digest()
