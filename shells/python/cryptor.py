#!/usr/bin/env python3
import string
import random

def rand_pass(size=32, use_digits=True):
    digits = ""
    if use_digits:
        digits = string.digits
    return ''.join(random.choices(string.ascii_letters + digits, k=size))


#############################################################################################################

# https://github.com/zeromq/pyzmq/blob/master/zmq/utils/z85.py
import sys
import struct

PY3 = sys.version_info[0] >= 3
# Z85CHARS is the base 85 symbol table
Z85CHARS = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"
# Z85MAP maps integers in [0,84] to the appropriate character in Z85CHARS
Z85MAP = dict([(c, idx) for idx, c in enumerate(Z85CHARS)])

_85s = [ 85**i for i in range(5) ][::-1]

def encode(rawbytes):
    """encode raw bytes into Z85"""
    # Accepts only byte arrays bounded to 4 bytes
    if len(rawbytes) % 4:
        raise ValueError("length must be multiple of 4, not %i" % len(rawbytes))
    
    nvalues = len(rawbytes) / 4
    
    values = struct.unpack('>%dI' % nvalues, rawbytes)
    encoded = []
    for v in values:
        for offset in _85s:
            encoded.append(Z85CHARS[(v // offset) % 85])
    
    # In Python 3, encoded is a list of integers (obviously?!)
    if PY3:
        return bytes(encoded)
    else:
        return b''.join(encoded)

def decode(z85bytes):
    """decode Z85 bytes to raw bytes, accepts ASCII string"""
    if PY3 and isinstance(z85bytes, str):
        try:
            z85bytes = z85bytes.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError('string argument should contain only ASCII characters')

    if len(z85bytes) % 5:
        raise ValueError("Z85 length must be multiple of 5, not %i" % len(z85bytes))
    
    nvalues = len(z85bytes) / 5
    values = []
    for i in range(0, len(z85bytes), 5):
        value = 0
        for j, offset in enumerate(_85s):
            value += Z85MAP[z85bytes[i+j]] * offset
        values.append(value)
    return struct.pack('>%dI' % nvalues, *values)

#############################################################################################################

from Crypto.Cipher import AES
from Crypto import Random

class AESCryptor:
    # https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
    def __init__(self, key):
        self.key = key
        self.BS = 16
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * bytes([self.BS - len(s) % self.BS])
        self.unpad = lambda s: s[:-ord(s[len(s)-1:])]

    def encrypt(self, msg):
        msg = self.pad(msg)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(msg)

    def decrypt(self, enc):
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt( enc[16:] ))

# Minimal decryption stub
decryptor = """
import struct
from Crypto.Cipher import AES
from Crypto import Random

e = {encoded}

m = {char_map}
n = len(e) / 5
v = []
for i in range(0, len(e), 5):
    x = 0
    for j, offset in enumerate([ 85**i for i in range(5) ][::-1]):
        x += m[e[i+j]] * offset
    v.append(x)
d = struct.pack('>%dI' % n, *v)

u = lambda s: s[:-ord(s[len(s)-1:])]
iv = d[:16]
c = AES.new({key}, AES.MODE_CBC, iv)
d = u(c.decrypt(d[16:]))

exec(d.decode())

"""

#############################################################################################################

script = sys.stdin.buffer.readlines()
imports = [line.strip(b' \t') for line in script if line.strip(b' \t').startswith(b'import')]

script = b''.join(script)


key = rand_pass()
cryptor = AESCryptor(key)
encrypted = cryptor.encrypt(script)

encoded = encode(encrypted)


# Don't conceal the imports; pyinstaller neads to see them
decryptor = ''.join(imports) + decryptor.format(encoded=encoded, char_map=repr(Z85MAP), key=repr(key))
print(decryptor)

