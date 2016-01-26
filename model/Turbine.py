class Turbine(object):
    """
    A process is how a fluid moves between states, processes require certain 
    assumptions to constrain the state change. In the first iteration I plan on 
    only implenting isentropic, isobaric, and isenthalpic processes. In later 
    iterations I will extend it to polytropic and real processes.
    """
    def __init__(self, inputs, outputs, **kwargs):
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
        pass