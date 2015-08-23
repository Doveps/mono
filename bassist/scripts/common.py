# This object is intended to run from script bassist.py
import logging
import logging.config
import argparse
import ConfigParser

from ..parser import host as parser_host
from ..flavor import directory as flavor_directory

class Script(object):
    '''This module contains things that are available for use of our packages'
    scripts. This includes setting up argparse, logger, etc.'''

    def set_logging(self):
        '''If we're running from the root of the project, this stuff will work.
        If not, load logging_config.'''

        try:
            logging.config.fileConfig('log.conf', disable_existing_loggers=False)
        except ConfigParser.NoSectionError:
            # probably no log.conf file
            logging.basicConfig(
                    format='%(message)s',
                    )

        self.logger = logging.getLogger(__name__)

        try:
            from log_override import LOG_OVERRIDES
            logging.config.dictConfig(LOG_OVERRIDES)
        except:
            self.logger.debug('unable to load log_override; ignoring')

    def set_arg_parser(self):
        self.arg_parser = argparse.ArgumentParser( description=self.description )

        self.required_args = self.arg_parser.add_argument_group('required arguments')
        self.required_args.add_argument(
                '-f', '--flavor-db',
                required=True,
                help='The path to the directory containing the flavor ZODB files')
        self.required_args.add_argument(
                '-n', '--flavor-name',
                required=True,
                help=self.flavor_arg_description)
        self.required_args.add_argument(
                '-s', '--scanner-directory',
                required=True,
                help='The path to the directory containing scanner results')

    def read_flavors(self):
        self.logger.debug('reading flavors')
        self.flavors = flavor_directory.Directory(self.args.flavor_db).db
        self.requested_flavor = self.flavors.get_obj_from_name(self.args.flavor_name)
        self.logger.debug('retrieved requested flavor %s', self.requested_flavor)

    def parse(self):
        self.logger.debug('importing parsers')
        self.parsed_host = parser_host.Host(self.args.scanner_directory)
        self.logger.debug('finished importing parsers')

        for parser in self.parsed_host.parsers:

            self.logger.debug('parser log: %s', parser.log)

            self.logger.debug('parsing: %s', parser.path)
            parser.parse()

    def finish(self):
        self.flavors.close()
