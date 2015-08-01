from .. import common as primitive
from . import apt

class Packages(primitive.Common):
    def __init__(self, facts):
        super(Packages, self).__init__(facts)

        # dynamically load package manager object
        module_name = globals()[self.facts['pkg_mgr']]
        class_name = self.facts['pkg_mgr'].capitalize()
        self.manager_class = getattr(module_name, class_name)

    def update_directives(self, name, handlers):
        # example: name is 'apache2'
        # on ubuntu, pkg_mgr is apt, so self.manager_class is apt.Apt
        # thus: directive = apt.Apt('apache2')
        directive = self.manager_class(name)
        handlers['tasks'].add(directive)
        self.logger.debug('handlers is now %s',handlers)

