#!/usr/bin/env python3
# This script parses output from the Doveps scanner. For documentation,
# see README.md
import argparse

import bassist

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
        '-s', '--scanner-directory',
        required=True,
        help='The path to the directory containing scanner results')
args = arg_parser.parse_args()

parsed = bassist.parser.directory.Directory(args.scanner_directory)
print("parsed:")
for host in parsed.hosts:
    print('host: %s'%host.path)
    print('using parsers:')
    for parser in host.parsers:
        print('%s: %s'%(parser.__class__, parser.path))
