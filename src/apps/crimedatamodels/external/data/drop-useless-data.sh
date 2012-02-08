#!/bin/sh

# Crime data comes in csv with some junk lines at the beginning and end
# It also has some irregularities with whitespace between fields.
# This strips those lines and whitespace and writes to a new file prefixed
# with 'stripped-'
#
# Usage:
#   ./drop-useless-data.sh crime-data-2008.csv
# will create stripped-crime-data-2008.csv
#
# You should verify that no useful lines were dropped after running this script

head -n-8 <$1 | tail -n+4 | sed 's/,\s\+/,/g' >stripped-$1
