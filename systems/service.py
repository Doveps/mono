class UpstartInfo(object):
    def __init__(self, wanted, state, pid):
        self.wanted = wanted
        self.state = state
        self.pid = pid

class Service(object):
    def __init__(self, name):
        self.name = name
        self.upstart = None

    def add_upstart(self, wanted, state, pid):
        self.upstart = UpstartInfo(wanted, state, pid)
