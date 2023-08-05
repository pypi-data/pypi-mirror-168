import base64
import hashlib


def mime_encoder(to_encode: bytes):
    encoded_list = list(base64.b64encode(to_encode).decode("UTF-8"))

    count = 0
    for i in range(76, len(encoded_list), 76):
        encoded_list.insert(i + count, '\r\n')
        count += 1
    return ''.join(encoded_list)


class Helpers:

    @staticmethod
    def sha_digest_username(data: str):
        b_arr = data.encode("UTF-8")
        digest = hashlib.sha1(b_arr).digest()

        sb = ""
        for i in range(0, len(digest)):
            b = digest[i]
            hex_string = hex(b & 255).replace("0x", "")
            if len(hex_string) == 1:
                sb += "0"
                sb += hex_string
            else:
                sb += hex_string
        print(sb)
        return sb
