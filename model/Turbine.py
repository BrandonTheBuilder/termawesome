import copy

class Turbine(object):
    """
    A process is how a fluid moves between states, processes require certain 
    assumptions to constrain the state change. In the first iteration I plan on 
    only implenting isentropic, isobaric, and isenthalpic processes. In later 
    iterations I will extend it to polytropic and real processes.
    """
    def __init__(self, inlet, outlet, **kwargs):
        """
        kwargs: Assumptions which define the process. The assunptions for a 
        process tell us which property remains constant, or defines how it changes
        through the process, which allows us to define a new state.
        We need:
        rQ, rate of heat transfer positive for produced negative for added
        rW, rate of work done positive for produced negative for added
        rWs, rate of work for isentropic process
        e, isentropic efficiency of Turbine
        """
        self._one = inlet
        self._two = outlet
        # Creating an undefined isentropic state as a copy of the undefined outlet.
        self._twos = copy.deepcopy(outlet)


    def isentropic(self, eta):
        """
        Solves the isentropic process across the inputs and outputs.
        """
        if self._one.defined and not self._two.defined:
            s = self._one.properties['s']
            if self._twos.define(s=s):
                self.defined = True
            else:
                self.defined = False
        # elif self._two.defined and not self._one.defined:
        #     s = self._two.properties['s']
        #     self._ones.define(s=s)
        #     self.defined = True
        elif self._one.defined and self._two.defined:
            self.defined = True
        else:
            self.defined = False
        if self.defined:
            ws = self._one.properties['h']-self._twos.properties['h']
            self.w = eta*ws
            h_two = self._one.properties['h']-self.w
            self._two.define(h=h_two)

    def exergyBalance(self, t0, p0):
        if not self.defined:
            print 'Cannot perform exergy balance on undefined component'
            return False
        yf_one = self._one.exergy_f(t0, p0)
        y_one = self._one.exergy(t0, p0)
        yf_two = self._two.exergy_f(t0, p0)
        y_two = self._two.exergy(t0, p0)
        self.ef = self.w/(yf_one-yf_two)
        self.dy = y_two-y_one
        self.entropyProduced = self._two.properties['s'] - self._one.properties['s']
        self.exergyDestroyed = t0*self.entropyProduced
        self.exergyDV = p0*(self._two.properties['v']-self._one.properties['v'])
        self.exergyDQ = self.dy+self.w+self.entropyProduced-self.exergyDV

    def exergyBalanceY(self, t0, p0, y):
        if not self.defined:
            print 'Cannot perform exergy balance on undefined component'
            return False
        yf_one = self._one.exergy_f(t0, p0)*(1-y)
        y_one = self._one.exergy(t0, p0)*(1-y)
        yf_two = self._two.exergy_f(t0, p0)*(1-y)
        y_two = self._two.exergy(t0, p0)*(1-y)
        self.ef = self.w/(yf_one-yf_two)*(1-y)
        self.dy = y_two-y_one
        self.entropyProduced = self._two.properties['s'] - self._one.properties['s']
        self.exergyDestroyed = t0*self.entropyProduced
        self.exergyDV = p0*(self._two.properties['v']-self._one.properties['v'])
        self.exergyDQ = self.dy+self.w+self.entropyProduced-self.exergyDV
        
