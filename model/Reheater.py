# No need to wory about exergy.

class Reheater(object):
    def __init__(self, inlet, outlet):
        self.q = outlet.properties['h']-inlet.properties['h']