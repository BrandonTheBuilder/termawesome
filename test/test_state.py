import unittest 
from nose import with_setup

from model.State import State

class TestState(unittest.TestCase):
    def Setup(self):
        print "Setting shit up to test"


    @with_setup(Setup)
    def testTempPressure(self):
        P = 200000 #Pa
        T = 600 #K
        fluid = 'Water'
        testState = State(fluid)
        testState.define(T=T, P=P)
        # I am testing against the value returned the first time
        # just to make sure it is still working, I do not know
        # how else to test this. 
        val = testState.properties['h'] - 3126608
        self.assertAlmostEquals(True, val < 10)


    def testTempEntropy(self):
        T = 600 #K
        s = 7994 #J/kg
        fluid = 'Water'
        testState = State(fluid)
        testState.define(T=T, S=s)
        val = testState.properties['h'] - 3126608
        self.assertAlmostEquals(True, val < 100)



    def testPressureEnthalpy(self):
        P = 200000 #Pa
        h = 3126608.7815658785 #J/kg
        fluid = 'Water'
        testState = State(fluid)
        testState.define(P=P, H=h)
        val = testState.properties['s'] - 7994
        self.assertAlmostEquals(True, val < 10)
        
