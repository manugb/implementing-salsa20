#!/usr/bin/env python
from common import string_to_n_bytes, create_args_parser
from salsa20 import XSalsa20_xor


if __name__ == "__main__":
    parser = create_args_parser()
    args = parser.parse_args()

    iv = string_to_n_bytes(args.iv, 24)
    key = string_to_n_bytes(args.key, 32)
    header_bytes = 50

    with open(args.file, "rb") as picture:
        picture.seek(header_bytes)
        picture_content = picture.read()
        cipher = XSalsa20_xor(picture_content, iv, key)
        with open(args.file + ".encr", "wb") as encrypted:
            picture.seek(0)
            encrypted.write(picture.read(header_bytes))
            encrypted.write(cipher)
