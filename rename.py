#!/usr/local/bin/python3

help_string = """\
rename.py
Version 2019-04-06a
Written by Christian Moomaw

USAGE

    rename.py [-n] <search_pattern> <replace_pattern> <file_1> [file_2] ...

    -n  (Also, `--dry-run`) Perform a dry run; print the rename operations
        which would have been performed, but don't actually rename
        anything

DESCRIPTION

Rename the files described according to Python regex patterns
`search_pattern` and `replace_pattern`. Replacement grammar comes from the
Python 3 `re.sub()` function.

LICENSE

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

from os import rename
from sys import argv
import re

def get_params():
	# Parses the arguments in sys.argv. Returns a `dict` with the following
	# fields:
	# {
	# 	"dry_run": boolean indicating whether to execute a dry run
	#   "search_pattern": regex input pattern
	# 	"replace_pattern": regex pattern used to rename each file
	# 	"file_list": list containing all specified file strings
	# }
	#
	# NOTE: This function does not validate any command syntax.

	out = {}
	arg_shift = 0 # If `-n` is present, all other args will be shifted by 1

	if len(argv) < 4: # Filename, search_pattern, replace_pattern, file_1
		return out

	if argv[1].lower() in ('-n', '--dry-run'):
		if len(argv) < 5: # Need one more argument
			return out
		out['dry_run'] = True
		arg_shift = 1
	else:
		out['dry_run'] = False

	out['search_pattern'] = argv[1 + arg_shift]
	out['replace_pattern'] = argv[2 + arg_shift]
	out['file_list'] = argv[(3 + arg_shift):]

	return out

def main():
	params = get_params()
	if not params:
		print(help_string)
		return

	# Generate rename pairs
	p = re.compile(params['search_pattern'])
	rename_pairs = [(f, re.sub(p, params['replace_pattern'], f)) \
			for f in params['file_list']] # List of (before, after) tuples
	# Remove trivial renames
	rename_pairs = [i for i in rename_pairs if i[0] != i[1]]

	if params['dry_run']:
		for i in rename_pairs:
			print(i[0] + ' ==> ' + i[1])
	else:
		for i in rename_pairs:
			print(i[0] + ' ==> ' + i[1])
			rename(i[0], i[1])



main()
