#!/usr/bin/env python
from model.State import State
from model.Turbine import Turbine
from model.Condensor import Condensor
from model.Reheater import Reheater
from model.Pump import Pump


# Reheater
class CFWH(object):
    """
    This is a very specific use of the base state and component functions
    that I need for a project in my Thermo class. Once I am done with the project
    I plan on introducing a much more generica way of developing a cycle
    """
    def __init__(self, t0, p0, p_1, t_1, p_2, eta_t, eta_p, p_cond):
        self.one = State('Water', P=p_1, T=t_1)
        self.one.define()
        self.two = State('Water', P=p_2)
        self.turb_one = Turbine(self.one, self.two)
        self.turb_one.isentropic(eta_t)
        self.turb_one.exergyBalance(p0, t0)

        self.three = State('Water', P=p_cond)
        self.turb_two = Turbine(self.two, self.three)
        self.turb_two.isentropic(eta_t)
        self.four = State('Water', P=p_cond, Q=0)
        self.four.define()

        self.five = State('Water', P=p_2)
        self.pump_one = Pump(self.four, self.five)
        self.pump_one.isentropic(eta_p)
        self.six = State('Water', P=p_1, Q=0)
        self.six.define()

        self.seven = State('Water', P=p_2, Q=0)
        self.seven.define()
        self.eight = State('Water', P=p_cond, h=self.seven.properties['h'])
        self.eight.define()
     
        
        y = ((self.six.properties['h']-self.five.properties['h'])
                /(self.two.properties['h']-self.seven.properties['h']))


        self.turb_two.w = self.turb_two.w * (1-y)
        self.turb_two.exergyBalanceY(t0, p0, y)
        self.pump_one.w = self.pump_one.w * (1-y)
        self.pump_one.exergyBalanceY(t0, p0, y)

        self.superHeater = Reheater(self.seven, self.one)
        self.eta = (sum([self.turb_one.w, self.turb_two.w, self.pump_one.w])/
                    sum([self.superHeater.q]))

def cfwh():
    
    p_1 = 100*10**5 # Pa
    p_6 = p_1
    p_5 = p_1
    t_1 = 620 # K
    p_cond = 10*10**3 # Pa
    p_3 = p_cond
    p_4 = p_cond
    p_8 = p_cond
    p_2 = 10*10**4 # Pa
    p_7 = p_2
    eta_t = 0.9
    eta_p = 0.95
    t_3 = 600 # K
    t0 = 300 # K
    p0 = 100*10**3 # Pa
    return CFWH(t0, p0, p_1, t_1, p_2, eta_t, eta_p, p_cond)

if __name__ == '__main__':
    cycle = cfwh()
    import IPython; IPython.embed()
