import os
from bassist.parser import host as parser_host
import logging
import logging.config
from app import record

def parse(scanner_directory):
    logger = logging.getLogger(__name__)
    logger.debug('importing parsers')
    parsed_host = parser_host.Host(scanner_directory)
    logger.debug('finished importing parsers')

    for parser in parsed_host.parsers:
        logger.debug('parser log: %s', parser.log)
        logger.debug('parsing: %s', parser.path)
        parser.parse()
