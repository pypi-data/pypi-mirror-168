import base64
import hashlib
import os.path
from pathlib import Path
import time
from Cryptodome import Random
from Cryptodome.Cipher import AES

key = [0x10, 0x01, 0x15, 0x1B, 0xA1, 0x11, 0x57, 0x72, 0x6C, 0x21, 0x56, 0x57, 0x62, 0x16, 0x05, 0x3D,
       0xFF, 0xFE, 0x11, 0x1B, 0x21, 0x31, 0x57, 0x72, 0x6B, 0x21, 0xA6, 0xA7, 0x6E, 0xE6, 0xE5, 0x3F]

unpad = lambda s: s[:-ord(s[len(s) - 1:])]

BASE_DIR = Path(__file__).resolve().parent.parent
_SC_PATH = os.path.join(BASE_DIR, 'sc')


class Configuration:
    def __init__(self):
        self.key = bytes(key)
        self.sc = None
        self.sc_loader()

    def de_secure(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))

    def sc_loader(self):
        self.sc = str(
            self.de_secure(b'mjjRs+gDShI8P5JGeYPxO0+osuwnlJF4VrnaxkCTlTnoQdZxzuLdkwukxG2ik5krbtZ7fSvgLtrdbrqgEBzAWQ=='),
            'utf-8')
