from .. import utils

if str != bytes:
    # Python 3.x
    def ord(c):
        return c

    def chr(n):
        return bytes((n,))

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)
b58chars = __b58chars


def b58encode(v):
    """ encode v, which is a string of bytes, to base58.
    """
    long_value = 0
    for (i, c) in enumerate(v[::-1]):
        if isinstance(c, str):
            c = ord(c)
        long_value += (256**i) * c

    result = ''
    while long_value >= __b58base:
        div, mod = divmod(long_value, __b58base)
        result = __b58chars[mod] + result
        long_value = div
    result = __b58chars[long_value] + result

    # Bitcoin does a little leading-zero-compression:
    # leading 0-bytes in the input become leading-1s
    nPad = 0
    for c in v:
        if c == 0:
            nPad += 1
        else:
            break

    return (__b58chars[0]*nPad) + result


def b58decode(v, length=None):
    """ decode v into a string of len bytes
    """
    long_value = 0
    for i, c in enumerate(v[::-1]):
        pos = __b58chars.find(c)
        assert pos != -1
        long_value += pos * (__b58base**i)

    result = bytes()
    while long_value >= 256:
        div, mod = divmod(long_value, 256)
        result = chr(mod) + result
        long_value = div
    result = chr(long_value) + result

    nPad = 0
    for c in v:
        if c == __b58chars[0]:
            nPad += 1
            continue
        break

    result = bytes(nPad) + result
    if length is not None and len(result) != length:
        return None

    return result


def checksum(v):
    """Return 32-bit checksum based on SHA256"""
    return utils.hash256(v)[0:4]


def b58encode_chk(v):
    """b58encode a string, with 32-bit checksum"""
    return b58encode(v + checksum(v))


def b58decode_chk(v):
    """decode a base58 string, check and remove checksum"""
    result = b58decode(v)
    if result is None:
        return None
    if result[-4:] == checksum(result[:-4]):
        return result[:-4]
    else:
        return None


def get_bcaddress_version(strAddress):
    """
    Returns None if strAddress is invalid.
    Otherwise returns integer version of address.
    """
    addr = b58decode_chk(strAddress)
    if addr is None or len(addr) != 21:
        return None
    version = addr[0]
    return ord(version)


BASE58_ALPHABET = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
BASE58_BASE = len(BASE58_ALPHABET)
BASE58_LOOKUP = dict((c, i) for i, c in enumerate(BASE58_ALPHABET))


class EncodingError(ValueError):
    pass


def encode(s):
    """Convert binary to base58 using BASE58_ALPHABET."""
    v, prefix = to_long(256, lambda x: x, iter(s))
    s = from_long(v, prefix, BASE58_BASE, lambda v: BASE58_ALPHABET[v])
    return s.decode("utf8")


def decode(s):
    """Convert base58 to binary using BASE58_ALPHABET."""
    v, prefix = to_long(
        BASE58_BASE, lambda c: BASE58_LOOKUP[c], s.encode("utf8"))
    return from_long(v, prefix, 256, lambda x: x)


def encode_with_checksum(data):
    """
    A "hashed_base58" structure is a base58 integer (which looks like a string)
    with four bytes of hash data at the end.
    This function turns data into its hashed_base58 equivalent.
    """
    return encode(data + utils.hash256(data)[:4])


def decode_with_checksum(s):
    """
    If the passed string is hashed_base58, return the binary data.
    Otherwise raises an EncodingError.
    """
    data = decode(s)
    data, the_hash = data[:-4], data[-4:]
    if utils.hash256(data)[:4] == the_hash:
        return data
    raise EncodingError("hashed base58 has bad checksum %s" % s)


def hash_checksum(base58):
    """Return True if and only if base58 is valid hashed_base58."""
    try:
        decode_with_checksum(base58)
    except EncodingError:
        return False
    return True


def from_long(v, prefix, base, charset):
    """The inverse of to_long. Convert an integer to an arbitrary base.
    v: the integer value to convert
    prefix: the number of prefixed 0s to include
    base: the new base
    charset: an array indicating a printable character to use for each value.
    """
    ba = bytearray()
    while v > 0:
        try:
            v, mod = divmod(v, base)
            ba.append(charset(mod))
        except Exception:
            raise EncodingError(
                "can't convert to character corresponding to %d" % mod)
    ba.extend([charset(0)] * prefix)
    ba.reverse()
    return bytes(ba)


def to_long(base, lookup_f, s):
    """
    Convert an array to a (possibly bignum) integer, along with a prefix value
    of how many prefixed zeros there are.
    base:
        the source base
    lookup_f:
        a function to convert an element of s to a value between 0 and base-1.
    s:
        the value to convert
    """
    prefix = 0
    v = 0
    for c in s:
        v *= base
        try:
            v += lookup_f(c)
        except Exception:
            raise EncodingError("bad character %s in string %s" % (c, s))
        if v == 0:
            prefix += 1
    return v, prefix


"""
The MIT License (MIT)

Copyright (c) 2013 by Richard Kiss

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
