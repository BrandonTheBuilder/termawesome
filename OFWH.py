#!/usr/bin/env python
from model.State import State
from model.Turbine import Turbine
from model.Condensor import Condensor
from model.Reheater import Reheater
from model.Pump import Pump

class OFWH(object):
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
        self.four = State('Water', P=p_cond)
        self.condensor = Condensor(p_cond, self.three, self.four)

        self.five = State('Water', P=p_2)
        self.pump_one = Pump(self.four, self.five)
        self.pump_one.isentropic(eta_p)
        self.six = State('Water', P=p_2, Q=0)
        if self.six.define():        
            y = ((self.six.properties['h']-self.five.properties['h'])
                /(self.two.properties['h']-self.five.properties['h']))
        else:
            print 'Failed to define state 6'

        self.seven = State('Water', P=p_1)
        self.pump_two = Pump(self.six, self.seven)
        self.pump_two.isentropic(eta_p)
        self.pump_two.exergyBalance(t0, p0)

        self.turb_two.w = self.turb_two.w * (1-y)
        self.turb_two.exergyBalanceY(t0, p0, y)
        self.pump_one.w = self.pump_one.w * (1-y)
        self.pump_one.exergyBalanceY(t0, p0, y)

        self.superHeater = Reheater(self.seven, self.one)
        self.eta = (sum([self.turb_one.w, self.turb_two.w, self.pump_one.w, self.pump_two.w])/
                    sum([self.superHeater.q]))


def ofwh():
    p_1 = 100*10**5 # Pa
    t_1 = 620 # K
    p_2 = 10*10**4 # Pa
    p_cond = 10*10**3 # Pa
    eta_t = 0.9
    eta_p = 0.95
    t0 = 300 # K
    p0 = 100*10**3 # P
    return OFWH(t0, p0, p_1, t_1, p_2, eta_t, eta_p, p_cond)

if __name__ == '__main__':
    cycle = ofwh()
    import IPython; IPython.embed()