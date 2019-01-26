#!/usr/bin/env python3
#https://github.com/KyleBanks/XOREncryption/blob/master/Python/XOREncryption.py
#https://github.com/python/cpython/blob/3.7/Lib/fileinput.py
import sys

def xor(data, key):
    key = [ord(k) for k in key]
    char_codes = []
    
    for i in range(len(data)):
        char_codes.append(data[i] ^ key[i % len(key)])

    return bytearray(char_codes)

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("USAGE:  cat file | ./xor.py ENCRYPTION_KEY")
        sys.exit(1)
    else:
        data = sys.stdin.buffer.read()
        output = xor(data, sys.argv[1])

        #hex_str = ''.join([r'\x{}'.format(hex(o)) for o in output])
        hex_str = ''.join('{:02x}'.format(o) for o in output)
        print(hex_str)
