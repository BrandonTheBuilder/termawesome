#!/usr/bin/env python
from model.State import State
# Reheater
class ReheatedRankine(object):
    def __init__(self):
        self._one = State('Water', Q=1, P=10*10**6)
        self._one.define()
        


    
if __name__ == '__main__':
    cycle = ReheatedRankine()