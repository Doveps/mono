#!/usr/bin/env python3
# This script parses output from the Doveps scanner. For documentation,
# see README.md
import argparse
import logging

import bassist

# define a Handler which writes to a log file
fh = logging.FileHandler('bassist.log')

# define a Handler which writes INFO messages or higher to the sys.stderr
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch_formatter = logging.Formatter('%(levelname)-8s %(message)s')
ch.setFormatter(ch_formatter)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    handlers=[fh, ch])
logger = logging.getLogger('bassist')

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
        '-s', '--scanner-directory',
        required=True,
        help='The path to the directory containing scanner results')
args = arg_parser.parse_args()

logger.debug('creating a parser')
parsed = bassist.parser.directory.Directory(args.scanner_directory)
logger.debug('finished creating parser')

for host in parsed.hosts:
    logger.info('host: %s', host.path)
    for parser in host.parsers:
        logger.info('%s: %s', parser.__class__, parser.path)
