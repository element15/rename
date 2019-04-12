# rename.py

Version 0.1.0  
Written by Christian Moomaw

## USAGE

	usage: rename.py [-h] [-n] [-v] [-c century_prefix]
	                 (-p <search_pattern> <replace_pattern> | -d <format>)
	                 file [file ...]

	Rename the files described according to Python regex patterns`search_pattern`
	and `replace_pattern`.

	positional arguments:
	  file                  file to be renamed

	optional arguments:
	  -h, --help            show this help message and exit
	  -n, --dry-run         perform a dry run; don't actually rename anything
	  -v, --version         print the version and exit
	  -c <century_prefix>, --century <century_prefix>
	                        specify the number to prepend to two-digit years
	  -p <search_pattern> <replace_pattern>, --pattern <search_pattern> <replace_pattern>
	                        rename all matching files from <search_pattern>
	                        to<replace_pattern>
	  -d <format>, --date <format>
	                        reformat any dates found in filenames to conform to
	                        ISO 8601 (yyyy-mm-dd)

## MORE DETAILS

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
