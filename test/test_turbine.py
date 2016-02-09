import unittest

from model.Turbine import Turbine
from model.State import State

class TestProcess(unittest.TestCase):
    
    def testMixingChamber(self):
        stream_in = State('Water', flowRate = 2)
        stream_in.define(P=970000, T=800)
        rQ = 0;
        P2 = 15000 #Pa
        stream_out = State('Water')


    # def testIsentropic(self):
    #     T1 = 560 #Celcius
    #     P1 = 12 #MPa
    #     P2 = 1 #MPa
    #     T1 = T1 + 273 #K
    #     P1 = P1 * 10**6 #Pa
    #     P2 = P2 * 10**6 #Pa
    #     state_one = State('Water', P=P1, T=T1)
    #     state_one.define()
    #     state_two = State('Water', P=P2)
    #     state_two.define()
    #     turb = Turbine(state_one, state_two)
    #     turb.isentropic()
    #     self.assertEquals(True, (turb.ws/1000-(3506.2-2823.3))<10)

    def testIsentropic(self):
        inlet = State('Water', Q = 1, P = 10*10**6)
        outlet = State('Water', P = 10*10**3)
        inlet.define()
        turb = Turbine(inlet, outlet)
        turb.isentropic(0.9)
        self.assertEquals(True, outlet.defined)
        self.assertEquals(abs(outlet.properties['h']*10**(-3)-1870)<10, True)

    
    def testExergyBalance(self):
        inlet = State('Water', Q = 1, P = 10*10**6)
        outlet = State('Water', P = 10*10**3)
        inlet.define()
        turb = Turbine(inlet, outlet)
        turb.isentropic(0.9)
        turb.exergyBalance(300, 100*10**3)
        import IPython; IPython.embed()