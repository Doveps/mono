# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import argparse

from . import common
from ..parser import host as parser_host
from .. import interview

class RunException(Exception):
    pass

class Run(common.Script):
    description = 'Create automation by inferring OS contents'

    def __init__(self):
        self.set_logging()
        self.set_args()

        self.run_parsers()
        self.compare()
        self.finish()

    def parse_saver(self, obj):
        '''Pass this method to the parser. It will be invoked there, allowing
        our interview object to import the parser data.'''
        self.interview.reply(obj)

    def parse(self):
        self.logger.debug('importing parsers')
        self.parsed_host = parser_host.Host(self.args.scanner_directory)
        self.logger.debug('finished importing parsers')

        for parser in self.parsed_host.parsers:

            self.logger.debug('parser log: %s', parser.log)

            self.logger.debug('parsing: %s', parser.path)
            parser.parse(self.parse_saver)

    def run_parsers(self):
        self.interview = interview.start(self.args.scan_id)

        if self.interview.should_run():
            self.logger.info('parsing')
            self.parse()
        else:
            self.logger.info('re-using existing parse results')

        #for parser in self.parsed_host.parsers:
        #    parser.record()

    def set_args(self):
        self.arg_parser = argparse.ArgumentParser( description=self.description )

        self.required_args = self.arg_parser.add_argument_group('required arguments')
        self.required_args.add_argument(
                '-s', '--scanner-directory',
                required=True,
                help='The path to the directory containing scanner results')
        self.required_args.add_argument(
                '-c', '--config-directory',
                required=True,
                help='The path to write the configuration management \
                        code')

        self.arg_parser.add_argument(
                '-t', '--config-tool',
                default='ansible',
                help='The configuration management tool to use. The \
                        default is Ansible. Currently no other tools \
                        are supported.')
        self.arg_parser.add_argument(
                '-i', '--scan-id',
                help='If you want to re-use your parse results, give any arbitrary \
                        ID here. This can be useful for testing.')

        self.args = self.arg_parser.parse_args()

    def compare(self):
        self.logger.warn('not implemented yet: compare')
