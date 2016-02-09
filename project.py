#!/usr/bin/env python
from model.State import State
from model.Turbine import Turbine
from model.Condensor import Condensor
from model.Reheater import Reheater
from model.Pump import Pump
# Reheater
class ReheatedRankine(object):
    """
    This is a very specific use of the base state and component functions
    that I need for a project in my Thermo class. Once I am done with the project
    I plan on introducing a much more generica way of developing a cycle
    """
    def __init__(self, p_1, t_1, p_2, p_cond, eta_t, eta_p,t_3, t0, p0):
        self._one = State('Water', P=p_1, T=t_1)
        self._one.define()
        self._two = State('Water', P=p_2)
        self.turb_one = Turbine(self._one, self._two)
        self.turb_one.isentropic(eta_t)
        self.turb_one.exergyBalance(t0, p0)
        self._three = State('Water', P=p_2, T=t_3)
        self._three.define()
        self.reheater = Reheater(self._two, self._three)
        self._four = State('Water', P=p_cond)
        self.turb_two = Turbine(self._three, self._four)
        self.turb_two.isentropic(eta_t)
        self.turb_two.exergyBalance(t0, p0)
        self._five = State('Water')
        self.condensor = Condensor(p_cond, self._four, self._five)
        self._six = State('Water', P=p_1)
        self.pump = Pump(self._five, self._six)
        self.pump.isentropic(eta_p)
        self.pump.exergyBalance(t0, p0)
        self.superHeater = Reheater(self._six, self._one)
        self.eta = (sum([self.turb_two.w, self.turb_one.w, self.pump.w])/
                    sum([self.reheater.q, self.superHeater.q]))


    
if __name__ == '__main__':
    p_1 = 100*10**5 # Pa
    t_1 = 620 # K
    p_cond = 10*10**3 # Pa
    p_2 = 10*10**4 # Pa
    eta_t = 0.9
    eta_p = 0.95
    t_3 = 600 # K
    t0 = 300 # K
    p0 = 100*10**3 # Pa
    cycle = ReheatedRankine(p_1, t_1, p_2, p_cond, eta_t, eta_p, t_3, t0, p0)
    import IPython; IPython.embed()
