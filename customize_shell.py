#!/usr/bin/env python3

import netifaces as ni

import subprocess
import sys
import os

import argparse

path_to_replacer = './replace.py'
path_to_replacer = os.path.realpath(os.path.expanduser(path_to_replacer))

parser = argparse.ArgumentParser()

parser.add_argument("-a","--LHOST", help="The ip Address of the listening host.")
parser.add_argument("-p","--LPORT", default="443", help="The listening port.")
parser.add_argument("-s","--SHELL", default='/bin/bash', help="The shell to use for the connection.")

parser.add_argument("--no-prompt", action="store_true", help="Do no prompt - assume default LHOST")
parser.add_argument("-w", "--wrap", default="{{{}}}", 
    help="Wrap each parameter in this python format string. Default is {{{}}}, meaning that strings {LHOST}, {LPORT}, etc. are replaced.")
parser.add_argument('-v', '--verbosity', default=0, action="count", help="Print replacement information to STDERR")

parser.add_argument("file", nargs="+", help='files to customize.')

args = parser.parse_args()

ip_map = [(i, ni.ifaddresses(i)[ni.AF_INET][0]['addr']) for i in ni.interfaces() ]
r = range(len(ip_map))

# Get our IP address. Prompt the user if necessary
def validate_choice(choice, upper_limit):
    try:
        choice = int(choice)
        if choice >=0 and choice <= upper_limit:
            return choice
    except Exception as e:
        print(e)
    return None

choice = None
default = 1
if not args.no_prompt and not args.LHOST:
    while choice is None:
        for i in r:
            print("{: <4}{: <6}({})".format(str(i)+" :", ip_map[i][0], ip_map[i][1]))
        choice = input("\nPlease Select an IP to listen on [{}]:".format(default))
        if not choice:
            choice = str(default)
        choice = validate_choice(choice, len(r))
        args.LHOST = ip_map[choice][1]
else:
    args.LHOST = ip_map[default][1]

pairs = []
for var in ["LHOST", "LPORT", "SHELL"]:
    pairs.append(args.wrap.format(var))
    pairs.append(getattr(args, var))

if args.verbosity:
    pairs.insert(0, "-"+"v"*args.verbosity)
for filename in args.file:
    with open (args.file[0], 'rb') as f:
        subprocess.run([path_to_replacer] + pairs, stdin=f, stdout=sys.stdout, stderr=sys.stderr)
