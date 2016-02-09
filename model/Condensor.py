from model.State import State

class Condensor(object):
    def __init__(self, P, inlet, outlet):
        #Define the exit state of the condensor at pressure with a quality of 0
        self._inlet = inlet
        self._outlet = outlet
        self._outlet.define(P=P, Q=0)
