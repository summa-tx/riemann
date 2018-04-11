import binascii
import hashlib


def i2le(number):
    b = '%x' % number
    if len(b) & 1:
        b = '0' + b
    b = binascii.unhexlify(b)[::-1]
    return b


def change_endianness(b):
    return b[::-1]


def rmd160(msg_bytes):
    h = hashlib.new('ripemd160')
    h.update(msg_bytes)
    return h.digest()


def sha256(msg_bytes):
    return hashlib.sha256(msg_bytes).digest()


def hash160(msg_bytes):
    h = hashlib.new('ripemd160')
    h.update(sha256(msg_bytes))
    return h.digest()


def hash256(msg_bytes):
    return hashlib.sha256(hashlib.sha256(msg_bytes).digest()).digest()
