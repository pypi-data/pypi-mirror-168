import base64

from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from . import helpers
from .key_pair import KeyPair
from plugp100.tapo_protocol.encryption.pkcs7 import PKCS7Encoder


class TpLinkCipher:

    @staticmethod
    def create_from_keypair(handshake_key: str, keypair: KeyPair) -> 'TpLinkCipher':
        decode: bytes = base64.b64decode(handshake_key.encode("UTF-8"))
        decode2: bytes = base64.b64decode(keypair.get_private_key())

        cipher = PKCS1_v1_5.new(RSA.import_key(decode2))
        do_final = cipher.decrypt(decode, None)
        if do_final is None:
            raise ValueError("Decryption failed!")

        b_arr: bytearray = bytearray()
        b_arr2: bytearray = bytearray()

        for i in range(0, 16):
            b_arr.insert(i, do_final[i])
        for i in range(0, 16):
            b_arr2.insert(i, do_final[i + 16])

        return TpLinkCipher(b_arr, b_arr2)

    def __init__(self, b_arr: bytearray, b_arr2: bytearray):
        self.iv = b_arr2
        self.key = b_arr

    def encrypt(self, data):
        data = PKCS7Encoder().encode(data)
        data: str
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(data.encode("UTF-8"))
        return helpers.mime_encoder(encrypted).replace("\r\n", "")

    def decrypt(self, data: str):
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        pad_text = aes.decrypt(base64.b64decode(data.encode("UTF-8"))).decode("UTF-8")
        return PKCS7Encoder().decode(pad_text)
