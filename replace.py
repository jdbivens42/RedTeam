#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--all', action="store_true", help="Read the entire contents of STDIN before performing replacement.")
parser.add_argument('-d', '--delete', action="append", help="Delete this string sequence. Note: all deletions are done before PAIRS are processed. Use OLD '' for granular control over order") 
parser.add_argument('-v', '--verbosity', default=0, action="count", help="Print replacement information to STDERR")
parser.add_argument('PAIR',  help="A pair is in the form: OLD NEW . Replace all occurences of OLD with NEW", action="append", nargs="*")

args = parser.parse_args()
for pair_list in args.PAIR:
    if args.verbosity > 1:
        print(pair_list, file=sys.stderr)
    assert len(pair_list) % 2 == 0 , "OLD and NEW must come in pairs."


def replace_all(s, pairs):
    for old, new in pairs:
        if args.verbosity > 0:
            print("Replacing {} with {}".format(old, new), file=sys.stderr)
        s = s.replace(old, new)
        if args.verbosity > 1:
            print("Update: {}".format(s), file=sys.stderr)
    return s
if args.delete:
    pairs = [(d, '') for d in args.delete]
else:
    pairs = []
# Check whether the first delete command comes before the start
# of the OLD / NEW pairs

for pair_list in args.PAIR:
    for pair in zip(pair_list[::2], pair_list[1::2]):
        pairs.append(pair)

if args.verbosity > 1:
    print("Pairs: {}".format(pairs), file=sys.stderr)

if args.all:
    data = sys.stdin.read()
    print(replace_all(data, pairs), end="")
else:
    for line in sys.stdin:
        print(replace_all(line, pairs), end="")
