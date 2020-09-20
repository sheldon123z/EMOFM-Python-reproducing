import networkx as nx
import numpy as np
import random

class AR_MOEA():

    def __init__(self, graph, population,gen,stage_num):
        self.graph = graph
        self.population = population
        self.gen = gen
        self.stage_num = stage_num


    def MatingSelection(self,P):
        pass

    def EnvSelection(self):
        pass
    
    def Cal_KKM(self):
        pass
    
    def Cal_RC(self):
        pass
    
    def Cal_ExtendedQ(self):
        pass

    def Evaluation(self,chrosome):
        if stage_num == 1:
            kkm = self.Cal_KKM(chrosome)
            rc = self.Cal_RC(self.population)
        # elif stage_num == 2:
        #     Q = self.Cal_ExtendedQ(self)
        
        return kkm, rc


#%%
    def Moea_s1(self):

        for i in population:
            self.Evaluation(self,i)

        for g in range(len(gen)):
            P_prime = self.MatingSelection(self,self.population)
            O = []
            while P_prime:
                p_i = random.choice(P_prime)
                p_j = random.choice(P_prime)
                P_prime.remove(p_i)
                P_prime.remove(p_j)
                if stage_num == 1:
                    #TODO finish the s1 moea


    #TODO finish the s2 moea
    def Moea_s2(self):
        pass         
                



