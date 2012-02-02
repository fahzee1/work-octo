#!/usr/bin/env python
"""
Read columnar state abbreviation information and output it in JSON.

"""

import json
from optparse import OptionParser
import re
import string

def parse_args():
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='infile',
        help='Read abbreviations from FILE', metavar='FILE')
    (options, args) = parser.parse_args()
    if options.infile is None:
        parser.error("-f FILE or --file FILE required")
    return (options, args)

def parse_states(file):
    states = dict()
    for line in file:
        if re.match(r'^#', line): # skip comments
            continue
        (state, abbr) = read_state_abbr_pair(line)
        states[state] = abbr
    return states

def read_state_abbr_pair(line):
    (state, abbr) = re.split(r'\s{2,}', line.strip())
    state = string.capwords(state)
    state = re.sub(r'\bOf\b', 'of', state)
    return (state, abbr)

def abbrs_to_json(states):
    return json.dumps(states)

def main():
    (options, args) = parse_args()
    with open(options.infile) as file:
        states = parse_states(file)
    print abbrs_to_json(states)

if '__main__' == __name__:
    main()
