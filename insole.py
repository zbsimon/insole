#!/usr/bin/env python
from __future__ import print_function

import sys

delim = ','

vals_per_line = 9

lines = []


def pretty_print(lines, outfile=sys.stdout):
    for line in lines:
        strrepr = ""
        for val in line:
            strrepr += val + ", "
        strrepr = strrepr.strip(',')
        print(strrepr, file=outfile)


for line in sys.stdin:
    vals = line.split(',')
    vals = [val.strip() for val in vals]
    counter = 0
    line = []
    for val in vals:
        line.append(val)
        if counter % vals_per_line == 0:
            lines.append(line)
            line = []
        counter += 1

    pretty_print(lines)
