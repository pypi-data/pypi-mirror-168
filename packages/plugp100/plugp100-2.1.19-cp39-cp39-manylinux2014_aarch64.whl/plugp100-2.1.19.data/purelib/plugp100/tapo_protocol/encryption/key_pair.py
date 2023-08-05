from Crypto.PublicKey import RSA

from plugp100.tapo_protocol.encryption import helpers


class KeyPair(object):

    @staticmethod
    def create_key_pair() -> 'KeyPair':
        key = RSA.generate(1024)
        private_key = key.export_key(pkcs=8, format="DER")
        public_key = key.publickey().export_key(pkcs=8, format="DER")

        private_key = helpers.mime_encoder(private_key)
        public_key = helpers.mime_encoder(public_key)

        return KeyPair(
            private_key=private_key,
            public_key=public_key
        )

    def __init__(self, private_key: str, public_key: str):
        self.private_key = private_key
        self.public_key = public_key

    def get_private_key(self):
        return self.private_key

    def get_public_key(self):
        return self.public_key
