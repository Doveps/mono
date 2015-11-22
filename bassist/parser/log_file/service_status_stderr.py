# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
from . import common
from . import service_status_common
from ...systems import service

class ServiceStatusStderrLog(service_status_common.ServiceStatusCommonLog):
    #  [ ? ]  console-setup
    states = ['?']
