#!/usr/bin/env python
"""Transform the original Zip Code Database SQL to strip out long state name"""
import re

values_pattern = re.compile(r"""\(
    '(?P<zip>[^']+)'[^']*
    '(?P<abbr>[^']+)'[^']*
    '(?P<lat>[^']+)'[^']*
    '(?P<lng>[^']+)'[^']*
    '(?P<city>[^']*)'[^\)]*""", re.VERBOSE)
values_replace_pattern = r"('\g<zip>', '\g<city>', '\g<abbr>', '\g<lat>', '\g<lng>'"

with open('zip_codes.sql') as f:
    for line in f:
        print re.sub(values_pattern, values_replace_pattern, line),
