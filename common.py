import argparse
import hashlib


def string_to_n_bytes(string, n):
    hasher = hashlib.sha512()
    hasher.update(string.encode('utf-8'))
    return hasher.digest()[:n]


def create_args_parser():
    parser = argparse.ArgumentParser(prog='Salsa20 CLI')
    parser.add_argument('iv', help='Nonce')
    parser.add_argument('key', help='Encrypt/Decrypt key')
    parser.add_argument('file', help='Encrypt/Decrypt file')
    return parser
