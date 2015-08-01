import logging

from . import packages
from . import processes

module_logger = logging.getLogger(__name__)

def get_class(system_name):
    '''Example: accept 'packages', convert to packages.Packages.'''
    module_name = globals()[system_name]
    class_name = system_name.capitalize()
    ClassPointer = getattr(module_name, class_name)
    return ClassPointer
