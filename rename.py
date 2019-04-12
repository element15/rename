#!/usr/local/bin/python3

VERSION='0.1.0'
LICENSE = """\
rename.py
Written by Christian Moomaw

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""
help_description = """\
Rename the files described according to Python regex patterns`search_pattern`
and `replace_pattern`.
"""
help_epilogue = """\

MORE DETAILS

For details on the permitted regex grammar for the <search_pattern> argument,
refer to the Python 3 `re` documentation (link below). For details on how to
format <replace_pattern> refer to #re.sub on the aforementioned doc page.

https://docs.python.org/3/library/re.html

The `--date` option likewise requires the existing date format to be specified.
Date formats consist of three parts (day, month, and year) which may be in any
order:

Year formats:
    y    two or four-digit year (04 or 2004)
    yy   two-digit year only (04)
    yyyy four-digit year only (2004)
Month formats:
    m    numeric month which may or may not be left-padded (4 or 04)
    mm   numeric month which is left-padded (04)
    mmm  case insensitive alphabetic month (apr or april)
Day formats:
    d    day which may or may not be left-padded (1 or 01)
    dd   day date which is left-padded (01)

Examples:
"dmy"      ==> 1/4/04 or 01/04/04 or 1/4/2004 etc...
"mmmdyy"   ==> April 1 04 or APR 01, 04 etc...
"mmddyyyy" ==> 04/01/2004, 04.01.2004, 04012004, etc...
"""

from os import rename
from warnings import warn
import argparse
import re

# Two digit years which are strictly less than this value will be interpreted
# as being a part of the 2000s. All other years will be considered part of the
# 1900s. This value may be overriden by the user using a command argument
DEFAULT_CENTURY_ROLLOVER = 50

def parse_args():
	# Parse the command arguments in sys.argv

	parser = argparse.ArgumentParser(description=help_description,
		epilog=help_epilogue,
		formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('files', metavar='file', type=str, nargs='+',
		help='file to be renamed')
	parser.add_argument('-n', '--dry-run', action='store_true',
		help="perform a dry run; don't actually rename anything")
	parser.add_argument('-v', '--version', action='version',
		version=('%(prog)s ' + VERSION), help='print the version and exit')
	parser.add_argument('-c', '--century', metavar='<century_prefix>', type=str,
		nargs=1, help='specify the number to prepend to two-digit years')

	# Make -p and -d mutually exclusive
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-p', '--pattern', nargs=2, type=str,
		metavar=('<search_pattern>', '<replace_pattern>'),
		help=('rename all matching files from <search_pattern> to'
			'<replace_pattern>'))
	group.add_argument('-d', '--date', nargs=1, type=str, metavar='<format>',
		help=('reformat any dates found in filenames to conform to ISO 8601 '
			'(yyyy-mm-dd)'))


	args = parser.parse_args()
	return args


def date_pattern(mode):
	# Given a string describing an existing date format, generate a regex
	# pattern to extract a date matching said format from a string.

	# A valid mode is composed of one each from the month, day, and year
	# categories below. The examples given to the right are 1 April 2004.
	# The boolean value in each tuple indicates whether dilineating characters
	# (such as comma, hyphen, or space) should be required after the given
	# value. This is to avoid ambiguities associated with variable-length
	# pattern groups.
	mode_key = {
		# NOTE: The presence of a three-digit year in a filename results in
		# undefined behavior.
		'y': 	(r'(?P<y>\d{2,4})', True),  # 04, 2004 (and 004; see note above)
		'yy': 	(r'(?P<y>\d{2})',   False), # 04
		'yyyy': (r'(?P<y>\d{4})',   False), # 2004
		'm': 	(r'(?P<m>\d{1,2})', True),  # 4, 04
		'mm': 	(r'(?P<m>\d{2})',   False), # 04
		'mmm': 	(r'(?P<m>\w+)',     False), # Apr, April, aprile
		'd': 	(r'(?P<d>\d{1,2})', True),  # 1, 01
		'dd': 	(r'(?P<d>\d{2})',   False), # 01
	}

	# Parse the mode spec by separating it into it's three components
	mode_pattern = re.compile(r'(?P<a>(?P<x>[mdy])(?P=x)*)\W?'
		r'(?P<b>(?P<y>[mdy])(?P=y)*)\W?(?P<c>(?P<z>[mdy])(?P=z)*)')
	mode_match = mode_pattern.match(mode)

	# Ensure that the specified mode contains exactly one each of day, month,
	# and year. (For example, 'ddmmdd' is not a valid mode.)
	mode_parts = (mode_match.group('a')[:1], mode_match.group('b')[:1],
		mode_match.group('c')[:1])
	mode_parts = set(mode_parts) # Remove duplicates
	if len(mode_parts) != 3:
		raise ValueError('Invalid date pattern: ' + mode)

	# Build the date regex pattern from the appropriate `mode_key` entries
	mode_values = [mode_key[mode_match.group(i)] for i in ('a', 'b', 'c')]
	date_pattern = re.compile(r'(?P<prefix>.*?)' +
		mode_values[0][0] + r',?[.\- ]' + (r'' if mode_values[0][1] else r'?') +
		mode_values[1][0] + r',?[.\- ]' + (r'' if mode_values[1][1] else r'?') +
		mode_values[2][0] + r'(?P<suffix>.*)'
	)
	return date_pattern

def reformat_date(str, pattern, rollover=DEFAULT_CENTURY_ROLLOVER,
	century_prefix=None):
	# Given arbitrary string `str` and regex pattern `pattern` generated by
	# `date_pattern()`, find and reformat a date in `str` to be of the form
	# 'yyyy-mm-dd' (see ISO 8601). The `rollover` value determines how
	# two-digit years are converted to four-digit years

	month_key = { # Alphabetic months must be all lowercase
		'01': ('01', '1', 'jan', 'january', 'gen', 'gennaio'),
		'02': ('02', '2', 'feb', 'february', 'febbraio'),
		'03': ('03', '3', 'mar', 'march', 'marzo'),
		'04': ('04', '4', 'apr', 'april', 'aprile'),
		'05': ('05', '5', 'may', 'mag', 'maggio'),
		'06': ('06', '6', 'jun', 'june', 'giu', 'giunio'),
		'07': ('07', '7', 'jul', 'july', 'lug', 'luglio'),
		'08': ('08', '8', 'aug', 'august', 'ago', 'agosto'),
		'09': ('09', '9', 'sep', 'sept', 'september', 'set', 'sett',
			'settembre'),
		'10': ('10', 'oct', 'october', 'ott', 'ottobre'),
		'11': ('11', 'nov', 'november', 'novembre'),
		'12': ('12', 'dec', 'december', 'dic', 'dicembre')
	}

	m = pattern.match(str)
	if not m:
		warn('No date match found in string: ' + str)
		return str
	year = m.group('y')
	month = m.group('m')
	day = m.group('d')

	# Prepend '19' or '20' to the year if necessary
	if len(year) == 2:
		if century_prefix:
			century = century_prefix
		else:
			century = '20' if int(year) < rollover else '19'
		year = century + year
	# Normalize the month according to `month_key`
	month = month.lower()
	found_month_match = False
	for key in month_key:
		if month in month_key[key]:
			month = key
			found_month_match = True
			break
	if not found_month_match:
		raise ValueError('Unable to normalize month string: ' + month)
	# Left-pad the day with a zero if necessary
	if len(day) == 1:
		day = '0' + day

	# Generate new string with normalized date
	reformatted_str = (m.group('prefix') + year + '-' + month + '-' + day +
		m.group('suffix'))
	return reformatted_str

def remove_collisions(rename_pairs):
	# Given a list of length-two tuples, ensure that the second value in each
	# tuple is unique by adding a suffix number (i.e. '_1', '_2'. ...) where
	# necessary, and return the resulting collsion-free `rename_pairs`

	# First, find all the collisions. The following dict will be formatted as
	# follows:
	# {
	#     index1: [collision1_1, collision1_2, ...]
	#     index2: [collision2_1, collision2_2, ...]
	#     ...
	# }
	collisions = {}
	known_colliders = set() # This list is to avoid double-listing indices
	for i in range(0, len(rename_pairs) - 1):
		for j in range(i + 1, len(rename_pairs)):
			if (rename_pairs[i][1] == rename_pairs[j][1] and
				j not in known_colliders):
				known_colliders.add(i)
				known_colliders.add(j)
				if i in collisions:
					collisions[i].append(j)
				else:
					collisions[i] = [j]

	# Now, remove those collisions. If the string ends with what appears to be
	# a file extension, place the number before the extension.
	p = re.compile(r'(?P<a>.*?)(?P<b>\.[^.]+)?$')
	for i in collisions:
		for j in range(0, len(collisions[i])):
			k = collisions[i][j] # Index in rename_pairs
			p2 = r'\g<a>_' + str(j + 2) + r'\g<b>'
			rename_pairs[k][1] = re.sub(p, p2, rename_pairs[k][1], 1)

	# Sanity check
	resultants = [i[1] for i in rename_pairs]
	if len(resultants) != len(set(resultants)):
		raise ValueError('Collision removal algorithm failure')

	return rename_pairs

def main():
	args = parse_args()
	if args.pattern:
		p = re.compile(args.pattern[0])
		rename_pairs = [[f, re.sub(p, args.pattern[1], f, 1)]
			for f in args.files]
	else: # args.date
		p = date_pattern(args.date[0])
		rename_pairs = [[f, reformat_date(f, p,
			century_prefix=(args.century if not args.century else
				args.century[0]))] for f in args.files]

	# Remove trivial renames and collisions
	rename_pairs = [i for i in rename_pairs if i[0] != i[1]]
	rename_pairs = remove_collisions(rename_pairs)

	for i in rename_pairs: # Show preview of rename operations
		print(i[0] + ' ==> ' + i[1])

	if not args.dry_run:
		response = input('Continue with rename? [y/N] ').lower()
		affermative = ('y', 'yes')
		if response in affermative:
			for i in rename_pairs:
				rename(i[0], i[1])

main()
