from salsa20 import generate_salsa20_stream
from binascii import unhexlify, hexlify


class TestSalsa:

    # Test vectors taken from https://tools.ietf.org/html/draft-agl-tls-chacha20poly1305-04#section-7

    def test_one(self):
        key = unhexlify("0000000000000000000000000000000000000000000000000000000000000000")
        nonce = unhexlify("0000000000000000")
        expected = "76b8e0ada0f13d90405d6ae55386bd28bdd219b8a08ded1aa836efcc8b770dc7da41597c5157488d7724e03fb8d84a376a43b8f41518a11cc387b669b2ee6586"
        assert str(hexlify(next(generate_salsa20_stream(key, nonce))), encoding='utf-8') == expected

    def test_two(self):
        key = unhexlify("0000000000000000000000000000000000000000000000000000000000000001")
        nonce = unhexlify("0000000000000000")
        expected = "4540f05a9f1fb296d7736e7b208e3c96eb4fe1834688d2604f450952ed432d41bbe2a0b6ea7566d2a5d1e7e20d42af2c53d792b1c43fea817e9ad275ae546963"
        assert str(hexlify(next(generate_salsa20_stream(key, nonce))), encoding='utf-8') == expected

    # Why this exepected result has 60 bytes? Seems strange
    def test_three(self):
        key = unhexlify("0000000000000000000000000000000000000000000000000000000000000000")
        nonce = unhexlify("0000000000000001")
        expected = "de9cba7bf3d69ef5e786dc63973f653a0b49e015adbff7134fcb7df137821031e85a050278a7084527214f73efc7fa5b5277062eb7a0433e445f41e3"
        assert str(hexlify(next(generate_salsa20_stream(key, nonce))), encoding='utf-8').startswith(expected)

    def test_four(self):
        key = unhexlify("0000000000000000000000000000000000000000000000000000000000000000")
        nonce = unhexlify("0100000000000000")
        expected = "ef3fdfd6c61578fbf5cf35bd3dd33b8009631634d21e42ac33960bd138e50d32111e4caf237ee53ca8ad6426194a88545ddc497a0b466e7d6bbdb0041b2f586b"
        assert str(hexlify(next(generate_salsa20_stream(key, nonce))), encoding='utf-8') == expected
