from model.State import State

class Condensor(object):
    def __init__(self, fluid, P, inlet):
        #Define the exit state of the condensor at pressure with a quality of 0
        self._inlet = inlet
        self._exit = State(fluid, P=P, Q=0)
