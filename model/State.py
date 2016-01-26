from CoolProp import CoolProp as CP

class State(object):
    """
        The state of a fluid is defined with two unique intensive properties
        this class keeps track of the state of the fluid and solves for all other 
        intensive properties. 
    """
    def __init__(self, fluid, **kwargs):
        """
        fluid: The type of fluid this is.
        flowRate: The mass flow rate of the stream, kg/s
        kwargs: intensive properties to define the state.
        The Properties that we are interested in are:
        h, specific Enthalpy
        u, specific Internal Energy
        v, specific Volume
        s, specific Entropy
        m, specific mass flow rate 
        """
        self.fluid = fluid
        self.flowRate = None
        self.h = None
        self.u = None
        self.s = None
        self.v = None
        if kwargs is not None:
            self.__dict__.update(kwargs)
        


    def undefined(self, **kwargs):
        """
        Undefined state
        """
        self.__dict__.update(kwargs)

    def defined(self, **kwargs):
        """
        Define the fluid state based off of the inputed properties
        """
        #Make a list of defined properties
        inputProp = []
        for key in kwargs.keys():
            inputProp.extend([key, kwargs[key]])
        inputProp.append(self.fluid)
        self.h = CP.PropsSI('H', *inputProp)
        self.s = CP.PropsSI('S',*inputProp)
        self.u = CP.PropsSI('U', *inputProp)
        self.v = 1/CP.PropsSI('D', *inputProp)
        

    def __add__(self, other):
        pass


    def isDefined(self):
        pass
    