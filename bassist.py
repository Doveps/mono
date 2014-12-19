#!/usr/bin/env python
# This script parses output from the Doveps scanner. For documentation,
# see README.md
import argparse
import logging
import logging.config
import os

import parser.directory
import flavor.directory

logging.config.fileConfig('log.conf')
if os.path.isfile('log_override.py'):
    from log_override import LOG_OVERRIDES
    logging.config.dictConfig(LOG_OVERRIDES)

logger = logging.getLogger('bassist')

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
        '-f', '--flavor-directory',
        required=True,
        help='The path to the directory containing bassist flavors')
arg_parser.add_argument(
        '-l', '--parse-logs',
        nargs='*', metavar='LOG',
        help='Only parse the given logs, for example "debs_stdout"')
arg_parser.add_argument(
        '-n', '--flavor-name',
        help='Generates a flavor from scanner results using the given name')
arg_parser.add_argument(
        '-s', '--scanner-directory',
        required=True,
        help='The path to the directory containing scanner results')
args = arg_parser.parse_args()

logger.debug('reading flavors')
flavors = flavor.directory.Directory(args.flavor_directory).db
flavor = None
if args.flavor_name:
    flavor = flavors.get_obj_from_name(args.flavor_name)
logger.debug('retrieved flavor %s', flavor)

logger.debug('importing parsers')
parsed = parser.directory.Directory(args.scanner_directory)
logger.debug('finished importing parsers')

for host in parsed.hosts:
    logger.info('host: %s', host.path)
    for parser in host.parsers:

        logger.debug('parser log: %s', parser.log)
        if args.parse_logs:
            if not parser.log in args.parse_logs:
                logger.info(
                        'skipping parse of %s since you requested only %s',
                        parser.path, args.parse_logs)
                continue

        logger.info('parsing: %s', parser.path)
        parser.parse()
        if flavor:
            parser.record(flavor)

flavors.close()
