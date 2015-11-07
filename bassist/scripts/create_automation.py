import savant.comparisons
import savant.db
import savant.managers

from ..flavor import obj as flavor_obj
from ..diff import flavor as diff_flavor

from . import common

class RunException(Exception):
    pass

class Run(common.Script):
    description = 'Create automation by comparing flavors'
    flavor_arg_description = 'Compare with the given flavor name'

    def __init__(self):
        self.set_logging()
        self.set_args()

        self.read_flavors()
        self.compared_flavor = flavor_obj.Obj()

        self.run_parsers()
        self.compare()
        self.finish()

    def run_parsers(self):
        self.parse()
        for parser in self.parsed_host.parsers:
            parser.record(self.compared_flavor)

    def set_args(self):
        self.set_arg_parser()
        self.arg_parser.add_argument(
                '-t', '--config-tool',
                default='ansible',
                help='The configuration management tool to use. The \
                        default is Ansible. Currently no other tools \
                        are supported.')

        self.required_args.add_argument(
                '-i', '--inference-db',
                required=True,
                help='The path to the directory containing the inference \
                        ZODB files')
        self.required_args.add_argument(
                '-c', '--config-directory',
                help='The path to write the configuration management \
                        code')

        self.args = self.arg_parser.parse_args()

    def compare(self):
        flavor_comparison = diff_flavor.Flavor(self.requested_flavor, self.compared_flavor)

        if not flavor_comparison.different():
            print('Flavors are identical.')
            return

        db = savant.db.DB(self.args.inference_db)
        exported = flavor_comparison.export()

        try:
            savant_comparison = savant.comparisons.Comparison(db, diffs=exported)
        except AttributeError:
            raise RunException, "Failed database operation! Did you create a flavor yet?"

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
        manager.write(self.args.config_directory, self.args.config_tool)
        print(manager.get_report())
        db.close()
