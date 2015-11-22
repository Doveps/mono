# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
from . import common
from . import service_status_common
from ...systems import service

class ServiceStatusStdoutLog(service_status_common.ServiceStatusCommonLog):
    #  [ + ]  apparmor
    #  [ - ]  dbus
    states = ['+', '-']
