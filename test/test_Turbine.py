import unittest

from model.Turbine import Turbine
from model.State import State

class TestProcess(unittest.TestCase):
    
    def testMixingChamber(self):
        stream_in = State('Water', flowRate = 2)
        stream_in.defined(P=970000, T=800)
        rQ = 0;
        P2 = 15000 #Pa
        stream_out = State('Water')
        stream_out.undefined(P=P2)
