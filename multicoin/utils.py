import binascii


def i2lx(number):
    b = '%x' % number
    if len(b) & 1:
        b = '0' + b
    b = binascii.unhexlify(b)[::-1]
    return b
