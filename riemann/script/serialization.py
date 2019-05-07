import riemann
from riemann import utils
from riemann.script.opcodes import CODE_TO_INT, INT_TO_CODE


def serialize(script_string: str) -> bytes:
    '''serialize a human-readable script to bytes'''
    string_tokens = script_string.split()
    serialized_script = bytearray()

    for token in string_tokens:
        if token == 'OP_CODESEPARATOR' or token == 'OP_PUSHDATA4':
            raise NotImplementedError('{} is a bad idea.'.format(token))

        if token in riemann.network.CODE_TO_INT_OVERWRITE:
            serialized_script.extend(
                [riemann.network.CODE_TO_INT_OVERWRITE[token]])

        elif token in CODE_TO_INT:
            serialized_script.extend([CODE_TO_INT[token]])

        else:
            token_bytes = bytes.fromhex(token)

            if len(token_bytes) <= 75:
                op = 'OP_PUSH_{}'.format(len(token_bytes))
                serialized_script.extend([CODE_TO_INT[op]])
                serialized_script.extend(token_bytes)

            elif len(token_bytes) > 75 and len(token_bytes) <= 255:
                op = 'OP_PUSHDATA1'
                serialized_script.extend([CODE_TO_INT[op]])
                serialized_script.extend(utils.i2le(len(token_bytes)))
                serialized_script.extend(token_bytes)

            elif len(token_bytes) > 255 and len(token_bytes) <= 1000:
                op = 'OP_PUSHDATA2'
                serialized_script.extend([CODE_TO_INT[op]])
                serialized_script.extend(
                    utils.i2le_padded(len(token_bytes), 2))
                serialized_script.extend(token_bytes)

            else:
                raise NotImplementedError(
                    'Hex string too long to serialize.')

    return serialized_script


def hex_serialize(script_string: str) -> str:
    '''serialize a human-readable script to hex'''
    return serialize(script_string).hex()


def deserialize(serialized_script: bytes) -> str:
    '''deserialize a script from bytes to human-readable'''
    deserialized = []
    i = 0
    while i < len(serialized_script):
        current_byte = serialized_script[i]
        if current_byte == 0xab:
            raise NotImplementedError('OP_CODESEPARATOR is a bad idea.')
        if current_byte <= 75 and current_byte != 0:

            deserialized.append(
                serialized_script[i + 1: i + 1 + current_byte].hex())

            i += 1 + current_byte
            if i > len(serialized_script):
                raise IndexError(
                    'Push {} caused out of bounds exception.'
                    .format(current_byte))

        elif current_byte == 76:
            # next hex blob length
            blob_len = serialized_script[i + 1]

            deserialized.append(
                serialized_script[i + 2: i + 2 + blob_len].hex())

            i += 2 + blob_len

        elif current_byte == 77:
            # next hex blob length
            blob_len = utils.le2i(serialized_script[i + 1: i + 3])

            deserialized.append(
                serialized_script[i + 3: i + 3 + blob_len].hex())

            i += 3 + blob_len

        elif current_byte == 78:
            raise NotImplementedError('OP_PUSHDATA4 is a bad idea.')

        else:
            if current_byte in riemann.network.INT_TO_CODE_OVERWRITE:
                deserialized.append(
                    riemann.network.INT_TO_CODE_OVERWRITE[current_byte])
            elif current_byte in INT_TO_CODE:
                deserialized.append(INT_TO_CODE[current_byte])
            else:
                raise ValueError(
                    'Unsupported opcode. '
                    'Got 0x%x' % serialized_script[i])
            i += 1

    return ' '.join(deserialized)


def hex_deserialize(script_hex: str) -> str:
    '''deserialize a script from hex to human-readable'''
    return deserialize(bytes.fromhex(script_hex))
