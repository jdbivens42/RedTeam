#!/usr/bin/env python3
import fileinput
import base64
import shlex

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--program", 
    help='command that can execute the final payload from STDIN. Ex: python, /bin/bash')
parser.add_argument("-w", "--wrap", 
    help='if set, treat the input as a python program and wrap it in a decoding stub',
                    action="store_true")
parser.add_argument("file", nargs="*", 
                    help='file to read, if empty, stdin is used')
args = parser.parse_args()

prog = args.program
if not prog:
    prog = "python"

lines = list(fileinput.input(args.file))
s = "".join(lines)
payload = base64.b64encode(s.encode()).decode()

if args.wrap:
    imports="base64 as b"
    decoder="b.b64decode"

    command = 'import {};exec({}("{}"))'.format(imports, decoder, payload)
    print("echo {} | {}".format(shlex.quote(command), prog))
else:
    decoder="""python -c 'import fileinput as i,base64 as b,sys;o=sys.stdout;o.write(b.b64decode("".join(list(i.input()))));'"""
    print("echo {} | {} | {}".format(payload, decoder, prog))
