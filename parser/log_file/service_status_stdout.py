from . import common
from . import service_status_common
from systems import service

class ServiceStatusStdoutLog(service_status_common.ServiceStatusCommonLog):
    #  [ + ]  apparmor
    #  [ - ]  dbus
    states = ['+', '-']
