from .opcodes import CODE_TO_INT, INT_TO_CODE
import binascii


def serialize_from_string(script_string):
    string_tokens = script_string.split()
    serialized_script = bytearray()

    for token in string_tokens:
        if token in CODE_TO_INT:  # If the string is a known opcode
            serialized_script.extend([CODE_TO_INT[token]])  # Put it in there
            continue  # Skip rest of loop

        token_bytes = binascii.unhexlify(token)

        if len(token_bytes) > 76:
            raise NotImplementedError('PUSHDATA ops not supported')

        op = 'OP_PUSH_{}'.format(len(token_bytes))
        serialized_script.extend([CODE_TO_INT[op]])
        serialized_script.extend(token_bytes)

    return serialized_script


def hex_serialize_from_string(script_string):
    return serialize_from_string(script_string).hex()


def deserialize_script(serialized_script):

    deserialized = []
    i = 0
    while i < len(serialized_script):
        current_byte = serialized_script[i]
        if current_byte <= 76 and current_byte != 0:

            deserialized.append(
                serialized_script[i+1:i+1+current_byte].hex())

            i += 1 + current_byte
            if i > len(serialized_script):
                raise IndexError(
                    'Pushdata {} caused out of bounds exception'
                    .format(current_byte))

        else:
            try:
                deserialized.append(INT_TO_CODE[current_byte])
            except KeyError:
                raise ValueError(
                    'Unsupported opcode. '
                    'Got 0x%X' % serialized_script[i])
            i += 1

    return ' '.join(deserialized)


def deserialize_script_hex(script_hex):
    return deserialize_script(binascii.unhexlify(script_hex))
