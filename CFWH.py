#!/usr/bin/env python
from model.State import State
from model.Turbine import Turbine
from model.Condensor import Condensor
from model.Reheater import Reheater
from model.Pump import Pump
from model.CFeedWater import CFeedWater

import util.plotting as plot


# Reheater
class CFWH(object):
    """
    This is a very specific use of the base state and component functions
    that I need for a project in my Thermo class. Once I am done with the project
    I plan on introducing a much more generica way of developing a cycle
    """
    def __init__(self, t0, p0, p_1, t_1, p_2, eta_t, eta_p, p_cond, TL, TH):
        self.one = State('Water', P=p_1, T=t_1)
        self.one.define()
        self.two = State('Water', P=p_2)
        self.turb_one = Turbine(self.one, self.two)
        self.turb_one.isentropic(eta_t)
        self.turb_one.exergyBalance(t0, p0)

        self.three = State('Water', P=p_cond)
        self.turb_two = Turbine(self.two, self.three)
        self.turb_two.isentropic(eta_t)
        self.four = State('Water', P=p_cond, Q=0)
        self.four.define()

        self.five = State('Water', P=p_1)
        self.pump_one = Pump(self.four, self.five)
        self.pump_one.isentropic(eta_p)
        self.six = State('Water', P=p_1, T=400)
        self.six.define()

        self.seven = State('Water', P=p_2, Q=0)
        self.seven.define()
        self.eight = State('Water', P=p_cond, h=self.seven.properties['h'])
        self.eight.define()
     
        
        y = ((self.six.properties['h']-self.five.properties['h'])
                /(self.two.properties['h']-self.seven.properties['h']))
        self.y = y
        self.turb_two.exergyBalanceY(t0, p0, y)
        self.pump_one.exergyBalanceY(t0, p0, y)
        self.superHeater = Reheater(self.six, self.one)
        self.eta = (sum([self.turb_one.w, self.turb_two.w, self.pump_one.w])/
                    sum([self.superHeater.q]))
        self.E = self.eta*(1/(1-float(TL)/float(TH)))
        self.cfwh = CFeedWater([self.two, self.five], [y, 1], [self.seven, self.six],
                    [y, (1-y)], t0, p0)

def cfwh(p_2):
    TL = 300
    TH = 650
    p_1 = 100*10**5 # Pa
    p_6 = p_1
    p_5 = p_1
    t_1 = 620 # K
    p_cond = 10*10**3 # Pa
    p_3 = p_cond
    p_4 = p_cond
    p_8 = p_cond
    p_7 = p_2
    eta_t = 0.9
    eta_p = 0.95
    t_3 = 600 # K
    t0 = 300 # K
    p0 = 100*10**3 # Pa
    return CFWH(t0, p0, p_1, t_1, p_2, eta_t, eta_p, p_cond, TL, TH)


if __name__ == '__main__':
    pLow = 10*10**3
    pHigh = 100*10**5
    results = []
    int_p = []
    for x in range(pLow+1, pHigh-1, 10000):
        int_p.append(x/1000)
        results.append(cfwh(x))

    thermal = [res.eta for res in results]
    exergetic = [res.E for res in results]

    idx = thermal.index(max(thermal))
    print 'Max Thermal Efficiency of {} with an Intermediate pressure of {} kPa'.format(
            max(thermal), int_p[thermal.index(max(thermal))])
    print 'Max Exergetic Efficiency of {} with an Intermediate pressure of {} kPa'.format(
            max(exergetic), int_p[exergetic.index(max(exergetic))])
    print 'Turbine one: {}'.format(results[idx].turb_one.ef)
    print 'Turbine two: {}'.format(results[idx].turb_two.ef)
    print 'Pump: {}'.format(results[idx].pump_one.ef)
    print 'Y {}'.format(results[idx].y)
    print 'CFWH: {}'.format(results[idx].cfwh.ef)

    plot.plotData('Thermal Efficiencies of a CFWH Cycle', 'Intermediate Pressure (kPa)',
                    'Thermal Efficiency', [int_p, thermal])
    plot.plotData('Exergetic Efficiencies of a CFWH Cycle', 'Intermediate Pressure (kPa)',
                    'Exergetic Efficiency', [int_p, exergetic])
    plot.plotComponent('CFWH Turbine One', [res.turb_one for res in results], int_p)
    plot.plotComponent('CFWH Turbine Two', [res.turb_two for res in results], int_p)
    plot.plotComponent('CFWH Pump', [res.pump_one for res in results], int_p)
    plot.plotComponent('CFWH Feed Water', [res.cfwh for res in results], int_p)