import numpy as np
import random
class chromesome():

    def __init__(self,N):
        self.b = [0]*N
        self.r = [random.random() for i in range(N)]
        self.cover = list(range(1,N+1))
        self.membership_metrix=None
        self.KKM = 0
        self.RC = 0
        self.fitness = None
        self.Qov = None

    def Q_equal(self,other):
        if not isinstance(other, chromesome):
            return NotImplemented
        return self.KKM == other.KKM and self.RC==other.RC

    def __eq__(self, other): 

        if not isinstance(other, chromesome):
            return NotImplemented
        return self.KKM == other.KKM and self.RC==other.RC
        
    def __cmp__(self,other):

        if not isinstance(other, chromesome):
            return NotImplemented

        if self.KKM < other.KKM and self.RC < other.RC:
            return -1
        elif self.KKM > other.KKM and self.RC > other.RC:
            return 1
        else:
            return 0

    
    def __hash__(self):
        return hash((self.KKM, self.RC))
