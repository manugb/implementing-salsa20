from struct import Struct, pack
from copy import deepcopy


little_u64 = Struct("<Q")
little16_i32 = Struct("<16i")  # 16 little-endian 32-bit signed ints.
little8_i32 = Struct("<8i")    # 04 little-endian 32-bit signed ints.
little4_i32 = Struct("<4i")    # 04 little-endian 32-bit signed ints.
little2_i32 = Struct("<2i")    # 02 little-endian 32-bit signed ints.


def generate_matrix(key, nonce, block_number):
    assert len(key) == 32 and isinstance(key, bytes), "Key should be 32 bytes"
    assert len(nonce) == 8 and isinstance(nonce, bytes), "Nonce should be 8 bytes"

    key_1, key_2, key_3, key_4, key_5, key_6, key_7, key_8 = little8_i32.unpack(key)
    block_1, block_2 = little2_i32.unpack(little_u64.pack(block_number))
    nonce_1, nonce_2 = little2_i32.unpack(nonce)

    return [
        0x61707865,        key_1,      key_2,      key_3,
        key_4,        0x3320646e,    nonce_1,    nonce_2,
        block_1,         block_2, 0x79622d32,      key_5,
        key_6,             key_7,      key_8, 0x6b206574,
    ]


def xor(a, b):
    return a ^ b


def bxor(b1, b2):  # use xor for bytes
    return little16_i32.pack(*[xor(x, y) for x, y in zip(little16_i32.unpack(b1), little16_i32.unpack(b2))])


def rot32(w, left):
    """ rot32 32-bit word left by left or right by -left
        without creating a Python long.
        Timing depends on left but not on w.
    """
    left &= 31  # which makes nLeft >= 0
    if left == 0:
        return w

    # Note: now 1 <= nLeft <= 31.
    #     RRRsLLLLLL   There are nLeft RRR's, (31-nLeft) LLLLLL's,
    # =>  sLLLLLLRRR   and one s which becomes the sign bit.
    RRR = (((w >> 1) & 0x7fffFFFF) >> (31 - left))
    sLLLLLL = -((1 << (31 - left)) & w) | (0x7fffFFFF >> left) & w
    return RRR | (sLLLLLL << left)


def add32(a, b):
    """ Add two 32-bit words discarding carry above 32nd bit,
        and without creating a Python long.
        Timing shouldn't vary.
    """
    lo = (a & 0xFFFF) + (b & 0xFFFF)
    hi = (a >> 16) + (b >> 16) + (lo >> 16)
    return (-(hi & 0x8000) | (hi & 0x7FFF)) << 16 | (lo & 0xFFFF)


def _do_salsa20_round(x):
    x[4] = xor(x[4], rot32(add32(x[0], x[12]), 7))
    x[8] = xor(x[8], rot32(add32(x[4], x[0]), 9))
    x[12] = xor(x[12], rot32(add32(x[8], x[4]), 13))
    x[0] = xor(x[0], rot32(add32(x[12], x[8]), 18))
    x[9] = xor(x[9], rot32(add32(x[5], x[1]), 7))
    x[13] = xor(x[13], rot32(add32(x[9], x[5]), 9))
    x[1] = xor(x[1], rot32(add32(x[13], x[9]), 13))
    x[5] = xor(x[5], rot32(add32(x[1], x[13]), 18))
    x[14] = xor(x[14], rot32(add32(x[10], x[6]), 7))
    x[2] = xor(x[2], rot32(add32(x[14], x[10]), 9))
    x[6] = xor(x[6], rot32(add32(x[2], x[14]), 13))
    x[10] = xor(x[10], rot32(add32(x[6], x[2]), 18))
    x[3] = xor(x[3], rot32(add32(x[15], x[11]), 7))
    x[7] = xor(x[7], rot32(add32(x[3], x[15]), 9))
    x[11] = xor(x[11], rot32(add32(x[7], x[3]), 13))
    x[15] = xor(x[15], rot32(add32(x[11], x[7]), 18))
    x[1] = xor(x[1], rot32(add32(x[0], x[3]), 7))
    x[2] = xor(x[2], rot32(add32(x[1], x[0]), 9))
    x[3] = xor(x[3], rot32(add32(x[2], x[1]), 13))
    x[0] = xor(x[0], rot32(add32(x[3], x[2]), 18))
    x[6] = xor(x[6], rot32(add32(x[5], x[4]), 7))
    x[7] = xor(x[7], rot32(add32(x[6], x[5]), 9))
    x[4] = xor(x[4], rot32(add32(x[7], x[6]), 13))
    x[5] = xor(x[5], rot32(add32(x[4], x[7]), 18))
    x[11] = xor(x[11], rot32(add32(x[10], x[9]), 7))
    x[8] = xor(x[8], rot32(add32(x[11], x[10]), 9))
    x[9] = xor(x[9], rot32(add32(x[8], x[11]), 13))
    x[10] = xor(x[10], rot32(add32(x[9], x[8]), 18))
    x[12] = xor(x[12], rot32(add32(x[15], x[14]), 7))
    x[13] = xor(x[13], rot32(add32(x[12], x[15]), 9))
    x[14] = xor(x[14], rot32(add32(x[13], x[12]), 13))
    x[15] = xor(x[15], rot32(add32(x[14], x[13]), 18))
    return x


def sum_matrix(a, b):
    return [add32(x, y) for x, y in zip(a, b)]


def word_to_bytes(words):
    return little16_i32.pack(*words)


def generate_salsa20_stream(key, nonce):
    block_number = 0
    while True:
        matrix = generate_matrix(key, nonce, block_number)
        temp = deepcopy(matrix)
        for _ in range(10):
            temp = _do_salsa20_round(temp)
        matrix = sum_matrix(temp, matrix)
        yield word_to_bytes(matrix)
        block_number += 1


def salsa_20_xor_bytes(content, key, nonce):
    assert isinstance(content, bytes), "Content should be bytes"

    buffer = b''
    chunk_size = 64  # 64 bytes
    salsa_generator = generate_salsa20_stream(key, nonce)
    total_chunks = len(content) // chunk_size

    for i in range(total_chunks):
        chunk = content[i*chunk_size:(i+1)*chunk_size]
        salsa_stream = next(salsa_generator)[0:len(chunk)]
        buffer += bxor(chunk, salsa_stream)
        print("XOReando el chunk {0} de {1}, el buffer es de: {2}".format(i, total_chunks, len(buffer)))

    return buffer
