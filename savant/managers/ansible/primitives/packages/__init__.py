from .. import common as primitive
from . import apt

class Packages(primitive.Common):
    def __init__(self, set_obj, facts):
        super(Packages, self).__init__(set_obj, facts)

        # dynamically load package manager object
        module_name = globals()[self.facts['pkg_mgr']]
        class_name = self.facts['pkg_mgr'].capitalize()
        self.manager_class = getattr(module_name, class_name)

    def update_directives(self, handlers):
        # first iteration: assume we should install package given in set name

        # example: set info is 'add|packages|apache2'
        # on ubuntu, pkg_mgr is apt, so self.manager_class is apt.Apt
        # thus: entry = apt.Apt('apache2')
        entry = self.manager_class(self.set.info.name)
        handlers['tasks'].add(entry)
        self.logger.debug('handlers is now %s',handlers)

