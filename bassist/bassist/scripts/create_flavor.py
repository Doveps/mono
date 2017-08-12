# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
from . import common

class Run(common.Script):
    description = 'Create a new flavor'
    flavor_arg_description = 'Record as the given flavor name'

    def __init__(self):
        self.set_logging()
        self.set_arg_parser()
        self.args = self.arg_parser.parse_args()

        self.read_flavors()
        self.compared_flavor = None

        self.record()
        self.finish()

    def record(self):
        self.parse()
        for parser in self.parsed_host.parsers:
            parser.record(self.requested_flavor)
