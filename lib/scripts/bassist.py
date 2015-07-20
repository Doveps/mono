# This object is intended to run from script bassist.py
import logging
import logging.config
import argparse

import savant.comparisons
import savant.db
import savant.managers

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
            self.compare()
            self.finish()

    def set_logging(self):
        logging.config.fileConfig('log.conf', disable_existing_loggers=False)
        self.logger = logging.getLogger(__name__)

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
        required_args.add_argument(
                '-c', '--config-directory',
                help='The path to write the configuration management code.')

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

    def compare(self):
        if not self.parse_all:
            return

        if self.args.record:
            return

        flavor_comparison = diff_flavor.Flavor(self.requested_flavor, self.compared_flavor)

        if not flavor_comparison.different():
            print('Flavors are identical.')
            return

        db = savant.db.DB(self.args.inference_db)
        exported = flavor_comparison.export()
        savant_comparison = savant.comparisons.Comparison(db, diffs=exported)

        print('The flavor comparison generated ID %s'%savant_comparison.id)

        if not savant_comparison.all_assigned():
            print('One or more diffs from this comparison remain to be assigned to sets. Look for the id in Savant Web.')
            return

        print('All diffs from this comparison have been assigned to sets.')

        if not self.args.config_directory:
            print('To generate configuration management code, specify a directory (-c/--config-directory).')
            return

        manager = savant.managers.Manager(
                db, savant_comparison.get_set_ids(), self.requested_flavor)
        manager.write(self.args.config_directory)

    def finish(self):
        self.flavors.close()
