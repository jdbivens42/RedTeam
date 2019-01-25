#!/usr/bin/env python3

import netifaces as ni
import random

import subprocess
import sys
import os

import shlex
import argparse
import re
import string

def rand_pass(size=32, use_digits=True):
    digits = ""
    if use_digits:
        digits = string.digits
    return ''.join(random.choices(string.ascii_letters + digits, k=size))

path_to_replacer = os.path.join(os.path.dirname(__file__), 'replace.py')
path_to_replacer = os.path.realpath(os.path.expanduser(path_to_replacer))

parser = argparse.ArgumentParser()
supported = ["LHOST", "LPORT", "RHOST", "RPORT", "SHELL", "SHELL_ARGS", "PROTO", "EXE", "RAND_INT", "RAND_PASS"]
parser.add_argument("-a","--LHOST", help="The ip Address of the listening host.")
parser.add_argument("-p","--LPORT", default="443", help="The listening port.")
parser.add_argument("-r","--RHOST", help="The ip Address of the listening host.")
parser.add_argument("-q","--RPORT", help="The listening port.")
parser.add_argument("-s","--SHELL", default='/bin/bash', help="The shell to use for the connection.")
parser.add_argument("--SHELL_ARGS", default="-i", help="Any arguments that should be passed to the shell.")
parser.add_argument("--PROTO", help="The shell to use for the connection.")
parser.add_argument("--EXE", help="The executable that will run this program. The contents of shebang line, after the #!")
parser.add_argument("--RAND_INT", 
    help="Takes two values: START END . Produces a random integer in the range [START, END] (inclusive). The same value is used for all occurances of RAND_INT.", nargs=2)

parser.add_argument("--RAND_PASS", type=int, action="store",
    help="Produces a random password of length LEN." +
         " Passwords may contain letters and numbers. The same string is used for all occurances of the placeholder.", 
    nargs="?")
parser.add_argument("--no-prompt", action="store_true", help="Do no prompt - assume default LHOST")
parser.add_argument("--no-warnings", action="store_true", help="Disable warnings.")
parser.add_argument("-w", "--wrap", default="{{{}}}", 
    help="Wrap each parameter in this python format string. Default is {{{}}}, meaning that strings {LHOST}, {LPORT}, etc. are replaced.")
parser.add_argument('-v', '--verbosity', default=0, action="count", help="Print replacement information to STDERR")

parser.add_argument("file", nargs="+", help='files to customize.')

args = parser.parse_args()

def print_err(msg):
    print(msg, file=sys.stderr)

if args.RAND_INT:
    args.RAND_INT = [int(i) for i in args.RAND_INT]
    args.RAND_INT = random.randint(min(args.RAND_INT), max(args.RAND_INT))
    args.RAND_INT=str(args.RAND_INT)

if args.RAND_PASS is not None:
    args.RAND_PASS = rand_pass(size=args.RAND_PASS)
    print_err("RAND_PASS: {}".format(args.RAND_PASS), file=sys.stderr)

ip_map = [(i, ni.ifaddresses(i)[ni.AF_INET][0]['addr']) for i in ni.interfaces() ]
r = range(len(ip_map))

# Takes in a format string
# Returns a regular expression
#  Reluctant wildcard added inside format string
#  Grouping done around wildcard
#  Metachars escaped
#  Grouping done around entire pattern
#  Goal / Result:
#   match.group(0) is like {LHOST}, match.group(1) is like LHOST
def make_pattern(wrap):
    tmp = "---^UnIqu3_StRing^---"
    left, right = wrap.format(tmp).split(tmp)
    return "({})".format(re.escape(left) + "(.*?)" + re.escape(right))
    

def check_template(filename, pattern, supported, args):
    with open (filename, 'r') as f:
        for line in f:
            matches = re.findall(pattern, line)
            for m in matches:
                if not args.no_warnings:
                    if m[0] not in supported and " " not in m[0]:
                        print_err("Warning: {} not supported".format(m[0]), file=sys.stderr)
                        print_err("Exiting. Run with --no-warnings to suppress.".format(m), file=sys.stderr)
                        sys.exit(1)
                    elif hasattr(args, m[1]) and getattr(args, m[1]) is None:
                        print_err("Warning: {} found but has no default".format(m[0]), file=sys.stderr)
                        print_err("Exiting. Run with --no-warnings to suppress.".format(m), file=sys.stderr)
                        sys.exit(1)
                    else:
                        if args.verbosity > 0:
                            print_err("Using: {} = {}".format(m, getattr(args, m[1]))) 
                
# Get our IP address. Prompt the user if necessary
def validate_choice(choice, upper_limit):
    try:
        choice = int(choice)
        if choice >=0 and choice <= upper_limit:
            return choice
    except Exception as e:
        print_err(e)
    return None

choice = None
default = 1
if not args.no_prompt and not args.LHOST:
    while choice is None:
        for i in r:
            print_err("{: <4}{: <6}({})".format(str(i)+" :", ip_map[i][0], ip_map[i][1]))
        print_err("\nPlease Select an IP to listen on [{}]:".format(default))
        choice = input()
        if not choice:
            choice = str(default)
        choice = validate_choice(choice, len(r))
        args.LHOST = ip_map[choice][1]
elif not args.LHOST:
    args.LHOST = ip_map[default][1]

pairs = []
for var in supported:
    value = getattr(args,var)
    if value is not None:
        pairs.append(args.wrap.format(var))
        pairs.append(value)
if args.verbosity:
    pairs.insert(0, "-"+"v"*args.verbosity)

pattern = make_pattern(args.wrap)
for filename in args.file:
    check_template(filename, pattern, [args.wrap.format(s) for s in supported ], args )
    with open (filename, 'rb') as f:
        subprocess.run([path_to_replacer] + pairs, stdin=f , stdout=sys.stdout, stderr=sys.stderr)
