# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import logging

from . import paths, packages, processes

module_logger = logging.getLogger(__name__)

def get_class(system_name):
    '''Example: accept 'packages', convert to packages.Packages.'''
    try:
        module_name = globals()[system_name]
    except KeyError, e:
        raise KeyError, 'Missing ansible primitive for system: %s'%system_name

    class_name = system_name.capitalize()
    ClassPointer = getattr(module_name, class_name)
    return ClassPointer
