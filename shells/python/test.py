#Script: b'print("hi")\n'
#Encrypted: b'f!(\xfa\x9a\x13\xbc\xc3:\xa1\x8b^\x1d\x81qb\xfa#;\x16\x99]\n1\xa2\xa9\xce\x0f\x1e\x01\x03Y'

import struct
from Crypto.Cipher import AES
from Crypto import Random

e = b'w*5P0NIiuKi?.Er9F5it}xF6qNoZdOQn=AG9SVvC'

m = {48: 0, 49: 1, 50: 2, 51: 3, 52: 4, 53: 5, 54: 6, 55: 7, 56: 8, 57: 9, 97: 10, 98: 11, 99: 12, 100: 13, 101: 14, 102: 15, 103: 16, 104: 17, 105: 18, 106: 19, 107: 20, 108: 21, 109: 22, 110: 23, 111: 24, 112: 25, 113: 26, 114: 27, 115: 28, 116: 29, 117: 30, 118: 31, 119: 32, 120: 33, 121: 34, 122: 35, 65: 36, 66: 37, 67: 38, 68: 39, 69: 40, 70: 41, 71: 42, 72: 43, 73: 44, 74: 45, 75: 46, 76: 47, 77: 48, 78: 49, 79: 50, 80: 51, 81: 52, 82: 53, 83: 54, 84: 55, 85: 56, 86: 57, 87: 58, 88: 59, 89: 60, 90: 61, 46: 62, 45: 63, 58: 64, 43: 65, 61: 66, 94: 67, 33: 68, 47: 69, 42: 70, 63: 71, 38: 72, 60: 73, 62: 74, 40: 75, 41: 76, 91: 77, 93: 78, 123: 79, 125: 80, 64: 81, 37: 82, 36: 83, 35: 84}
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
c = AES.new('jGwDzXciimz4V36uQYy2e48GWsWL1hMv', AES.MODE_CBC, iv)
d = u(c.decrypt(d[16:]))

exec(d.decode())

