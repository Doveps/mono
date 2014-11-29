#!/usr/bin/env python
# This script parses output from the Doveps scanner. For documentation,
# see README.md
import argparse
import logging

import parser.directory
import flavor.directory

# define a Handler which writes to a log file
fh = logging.FileHandler('bassist.log')
fh.setLevel(logging.DEBUG)
fh_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
fh.setFormatter(fh_formatter)

# define a Handler which writes INFO messages or higher to the sys.stderr
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch_formatter = logging.Formatter('%(levelname)-8s %(message)s')
ch.setFormatter(ch_formatter)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(fh)
root_logger.addHandler(ch)

logger = logging.getLogger('bassist')

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
        '-f', '--flavor-directory',
        required=True,
        help='The path to the directory containing bassist flavors')
arg_parser.add_argument(
        '-s', '--scanner-directory',
        required=True,
        help='The path to the directory containing scanner results')
arg_parser.add_argument(
        '-n', '--flavor-name',
        help='Generates a flavor from scanner results using the given name')
args = arg_parser.parse_args()

logger.debug('reading flavors')
flavors = flavor.directory.Directory(args.flavor_directory).db
flavor = None
if args.flavor_name:
    flavor = flavors.get_obj_from_name(args.flavor_name)
logger.debug('retrieved flavor %s', flavor)

#fh.setLevel(logging.WARNING)

logger.debug('importing parsers')
parsed = parser.directory.Directory(args.scanner_directory)
logger.debug('finished importing parsers')

#fh.setLevel(logging.DEBUG)

for host in parsed.hosts:
    logger.info('host: %s', host.path)
    for parser in host.parsers:
        logger.info('parsing: %s', parser.path)
        parser.parse()
        if flavor:
            parser.record(flavor)

flavors.close()
