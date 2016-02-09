import copy

class Pump(object):
    """
    """
    def __init__(self, inlet, outlet, **kwargs):
        """
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
            self.w = ws/eta
            h_two = self._one.properties['h']-self.w
            self._two.define(h=h_two)

    def exergyBalance(self, t0, p0):
        if not self.defined:
            print 'Cannot perform exergy balance on undefined component'
            return False
        yf_one = self._one.exergy_f(t0, p0)
        yf_two = self._two.exergy_f(t0, p0)
        self.ef = (yf_one-yf_two)/self.w
        self.dy = yf_two-yf_one
        self.entropyProduced = self._two.properties['s'] - self._one.properties['s']
        self.exergyDestroyed = t0*self.entropyProduced
        self.exergyDV = p0*(self._two.properties['v']-self._one.properties['v'])
        self.exergyDQ = self.dy+self.w+self.entropyProduced-self.exergyDV

    def exergyBalanceY(self, t0, p0, y):
        if not self.defined:
            print 'Cannot perform exergy balance on undefined component'
            return False
        yf_one = self._one.exergy_f(t0, p0)*(1-y)
        yf_two = self._two.exergy_f(t0, p0)*(1-y)
        self.ef = (yf_one-yf_two)/self.w
        self.dy = yf_two-yf_one
        self.entropyProduced = self._two.properties['s'] - self._one.properties['s']
        self.exergyDestroyed = t0*self.entropyProduced
        self.exergyDV = p0*(self._two.properties['v']-self._one.properties['v'])
        self.exergyDQ = self.dy+self.w+self.entropyProduced-self.exergyDV
        