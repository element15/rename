# rename.py

Version 0.3.1  
Written by Christian Moomaw

## USAGE

	usage: rename.py [-h] [-v] {pattern,p,multipattern,m,mp,multi,date,d} ...

	Rename files according to regex patterns.

	optional arguments:
	  -h, --help            show this help message and exit
	  -v, --version         print the version and exit

	sub-commands:
	  {pattern,p,multipattern,m,mp,multi,date,d}
	                        run `rename.py <command> -h` for help with a
	                        particular sub-command
	    pattern (p)         rename files based on a regex pattern
	    multipattern (m, mp, multi)
	                        rename files based on multiple regex files loaded from
	                        a JSON file
	    date (d)            reformat any dates found in filenames to conform to
	                        ISO 8601 (yyyy-mm-dd)

### `pattern` sub-command

	usage: rename.py pattern [-h] [-d]
	                         <search_pattern> <replace_pattern> file [file ...]

	positional arguments:
	  <search_pattern>   source regex pattern
	  <replace_pattern>  replace regex pattern
	  file               file to be renamed

	optional arguments:
	  -h, --help         show this help message and exit
	  -d, --dry-run      perform a dry run; don't actually rename anything

	MORE DETAILS

	For details on the permitted regex grammar for the <search_pattern> argument,
	refer to the Python 3 `re` documentation (link below). For details on how to
	format <replace_pattern> refer to #re.sub on the aforementioned doc page.

	https://docs.python.org/3/library/re.html


### `multipattern` sub-command

	usage: rename.py multipattern [-h] [-d] <pattern_file> file [file ...]

	positional arguments:
	  <pattern_file>  source JSON pattern file
	  file            file to be renamed

	optional arguments:
	  -h, --help      show this help message and exit
	  -d, --dry-run   perform a dry run; don't actually rename anything

	MORE DETAILS

	IMPORTANT: Backslash ('\') characters in the pattern file must be properly
	escaped.

	The given JSON files must be formatted as an array of arrays. The outer array
	contains the collection of pattern pairs, and each inner array represents one
	pattern pair. Additionally, multiple string replacements may be allowed for a
	given pattern pair by adding a third value to the inner array equal to 'm',
	'multi', or 'multiple', similar to specifying the `-m` flag for single pattern
	replacement. PseudoJSON and an example follow:

	[
		['search_pattern_1', 'replace_pattern_1', 'm'],
		['search_pattern_2', 'replace_pattern_2'],
		['search_pattern_3', 'replace_pattern_3', 'multi']
	]

	[
	    ['([\\d \\-]_spam_eggs\\.txt', 'spam_eggs_\\g<1>.txt'],
	    ['bakedbeans', 'spam', 'm'],
	    ['(\\d+)_', '\\g<1>-', 'm']
	]


### `date` sub-command

	usage: rename.py date [-h] [-d] [-c <prefix>] [-i <separator>]
	                      [-o <separator>] [-s]
	                      <format> file [file ...]

	positional arguments:
	  <format>              existing date format in filenames. See below for more
	                        details concerning valid input date formats.
	  file                  file to be renamed

	optional arguments:
	  -h, --help            show this help message and exit
	  -d, --dry-run         perform a dry run; don't actually rename anything
	  -c <prefix>, --century <prefix>
	                        specify the number to prepend to two-digit years
	                        (default: "['20']")
	  -i <separator>, --input-separator <separator>
	                        specify the character class of separators between
	                        input date components (default: "['[_.\\- ]']")
	  -o <separator>, --output-separator <separator>
	                        specify the separator between output date components
	                        (default: "['-']")
	  -s, --strict-commas   disallow commas following date components (i.e. April
	                        1, 2004)

	MORE DETAILS

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

## LICENSE

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
