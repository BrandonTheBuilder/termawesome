#!/usr/bin/env python
from model.State import State
from model.Turbine import Turbine
from model.Condensor import Condensor
from model.Reheater import Reheater
from model.Pump import Pump

import util.plotting as plot
# Reheater
class ReheatedRankine(object):
    """
    This is a very specific use of the base state and component functions
    that I need for a project in my Thermo class. Once I am done with the project
    I plan on introducing a much more generica way of developing a cycle
    """
    def __init__(self, p_1, t_1, p_2, p_cond, eta_t, eta_p,t_3, t0, p0, TL, TH):
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
        self.E = self.eta*(1/(1-float(TL)/float(TH)))
def reheater(p_2):
    TL = 300
    TH = 650
    p_1 = 100*10**5 # Pa
    t_1 = 620 # K
    p_cond = 10*10**3 # Pa
    eta_t = 0.9
    eta_p = 0.95
    t_3 = 600 # K
    t0 = 300 # K
    p0 = 100*10**3 # Pa
    return ReheatedRankine(p_1, t_1, p_2, p_cond, eta_t, eta_p, t_3, t0, p0, TL, TH)



if __name__ == '__main__':
    pLow = 10*10**3
    pHigh = 100*10**5
    results = []
    int_p = []
    for x in range(pLow+1000, pHigh-1000, 10000):
        int_p.append(x/1000)
        results.append(reheater(x))

    thermal = [res.eta for res in results]
    exergetic = [res.E for res in results]

    idx = thermal.index(max(thermal))
    print 'Max Thermal Efficiency of {} with an Intermediate pressure of {} kPa'.format(
            max(thermal), int_p[thermal.index(max(thermal))])
    print 'Max Exergetic Efficiency of {} with an Intermediate pressure of {} kPa'.format(
            max(exergetic), int_p[exergetic.index(max(exergetic))])
    print 'Turbine one: {}'.format(results[idx].turb_one.ef)
    print 'Turbine two: {}'.format(results[idx].turb_two.ef)
    print 'Pump: {}'.format(results[idx].pump.ef)

    plot.plotData('Thermal Efficiencies of a Reheater Cycle', 'Intermediate Pressure (kPa)',
                    'Thermal Efficiency', [int_p, thermal])
    plot.plotData('Exergetic Efficiencies of a Reheater Cycle', 'Intermediate Pressure (kPa)',
                    'Exergetic Efficiency', [int_p, exergetic])
    plot.plotComponent('Reheater Turbine One', [res.turb_one for res in results], int_p)
    plot.plotComponent('Reheater Turbine Two', [res.turb_two for res in results], int_p)
    plot.plotComponent('Reheater Pump', [res.pump for res in results], int_p)


    



