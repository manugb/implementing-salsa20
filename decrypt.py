#!/usr/bin/env python
from salsa20 import XSalsa20_xor
from common import string_to_n_bytes, create_args_parser


if __name__ == "__main__":
    parser = create_args_parser()
    args = parser.parse_args()

    iv = string_to_n_bytes(args.iv, 24)
    key = string_to_n_bytes(args.key, 32)
    header_bytes = 50

    with open(args.file + ".encr", "rb") as picture:
        picture.seek(header_bytes)
        encrypted = picture.read()
        original = XSalsa20_xor(encrypted, iv, key)
        with open(args.file, "wb") as decrypted:
            picture.seek(0)
            decrypted.write(picture.read(header_bytes))
            decrypted.write(original)
