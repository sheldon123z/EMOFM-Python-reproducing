import networkx as nx
import numpy as np
import random
import calculate_KKM_RC as CKR
import Mating_selection as MS
import uniform_crossover as UC

def AR_MOEA(P,R,Gen,stage,G):
    if stage == 1:
        for i in P:
            i.KKM, i.RC = CKR.Cal_KKM_RC(G,i)
    if stage == 2:
        pass
    for g in range(Gen):
        P_prime = MS.MatingSelection_KKM_RC(P,R)
        O = []
        while P_prime:
            if stage == 1:
                pi = random.choice(P_prime)
                pj = random.choice(P_prime)
                pi = UC.uniform_crossover(G,pi,pj)


        

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
    pass


#TODO finish the s2 moea
def Moea_s2(self):
    pass         
                



