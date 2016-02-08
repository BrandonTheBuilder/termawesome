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
        self._twos = outlet


    def isentropic(self, eta):
        """
        Solves the isentropic process across the inputs and outputs.
        """
        if self._one.defined and not self._two.defined:
            s = self._one.properties['s']
            self._twos.define(s=s)
            self.defined = True
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
            h_two = self._one.properties['h']-eta*ws
            import IPython; IPython.embed()
            self._two.define(H=h_two)