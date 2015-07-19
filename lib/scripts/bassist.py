# This object is intended to run from script bassist.py
import logging
import logging.config
import argparse

import savant.comparisons
import savant.db

from ..parser import host as parser_host
from ..flavor import directory as flavor_directory
from ..flavor import obj as flavor_obj
from ..diff import flavor as diff_flavor

class Bassist(object):
    def __init__(self, full_auto=True):
        if full_auto:
            self.set_logging()
            self.get_args()
            self.read_flavors()
            self.parse()
            self.finish()

    def set_logging(self):
        logging.config.fileConfig('log.conf', disable_existing_loggers=False)
        self.logger = logging.getLogger('bassist')

        try:
            from log_override import LOG_OVERRIDES
            logging.config.dictConfig(LOG_OVERRIDES)
        except:
            self.logger.debug('unable to load log_override; ignoring')

    def get_args(self):
        arg_parser = argparse.ArgumentParser(
                description='Generate either a new flavor, or compare to an \
                        existing flavor by parsing scanner results.')
        arg_parser.add_argument(
                '-l', '--parse-logs',
                nargs='*', metavar='LOG',
                help='Only parse the given logs, for example "debs_stdout"')

        required_args = arg_parser.add_argument_group('required arguments')
        required_args.add_argument(
                '-f', '--flavor-db',
                required=True,
                help='The path to the directory containing the flavor ZODB files')
        required_args.add_argument(
                '-n', '--flavor-name',
                required=True,
                help='Compare with or record to the given flavor name')
        required_args.add_argument(
                '-s', '--scanner-directory',
                required=True,
                help='The path to the directory containing scanner results')

        comparison_args = arg_parser.add_argument_group('comparison arguments')
        comparison_args.add_argument(
                '-r', '--record',
                action='store_true',
                help='When set, record to the given flavor name; otherwise \
                        compare to the given flavor name')
        comparison_args.add_argument(
                '-i', '--inference-db',
                help='The path to the directory containing the inference ZODB \
                        files; if you are not recording, this argument is \
                        REQUIRED')

        self.args = arg_parser.parse_args()

    def read_flavors(self):
        self.logger.debug('reading flavors')
        self.flavors = flavor_directory.Directory(self.args.flavor_db).db
        self.requested_flavor = self.flavors.get_obj_from_name(self.args.flavor_name)
        self.logger.debug('retrieved requested flavor %s', self.requested_flavor)

        self.compared_flavor = None
        if not self.args.record:
            self.compared_flavor = flavor_obj.Obj()

    def parse(self):
        self.logger.debug('importing parsers')
        self.parsed_host = parser_host.Host(self.args.scanner_directory)
        self.logger.debug('finished importing parsers')

        self.parse_all = not self.args.parse_logs

        for parser in self.parsed_host.parsers:

            self.logger.debug('parser log: %s', parser.log)
            if not self.parse_all:
                if not parser.log in args.parse_logs:
                    logger.info(
                            'skipping parse of %s since you requested only %s',
                            parser.path, args.parse_logs)
                    continue

            self.logger.info('parsing: %s', parser.path)
            parser.parse()
            if self.args.record:
                parser.record(self.requested_flavor)
            else:
                if self.parse_all:
                    parser.record(self.compared_flavor)
                else:
                    parser.diff(self.requested_flavor)

    def finish(self):
        if self.parse_all and not self.args.record:
            flavor_comparison = diff_flavor.Flavor(self.requested_flavor, self.compared_flavor)
            if flavor_comparison.different():
                db = savant.db.DB(self.args.inference_db)
                exported = flavor_comparison.export()
                savant_comparison = savant.comparisons.Comparison(db, diffs=exported)

                print('The flavor comparison generated ID %s'%savant_comparison.id)
                if savant_comparison.all_assigned():
                    print('All diffs from this comparison have been assigned to sets.')
                else:
                    print('One or more diffs from this comparison remain to be assigned to sets. Look for the id in Savant Web.')

            else:
                print('Flavors are identical.')

        self.flavors.close()
