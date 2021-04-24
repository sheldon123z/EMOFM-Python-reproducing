'''
subinitialization 算法
'''
import networkx as nx
import numpy as np
import random
from sklearn.cluster import KMeans
from membership import membership_7


def calculate_r(r_prime,Ujl):
    
    r = (r_prime - np.min(Ujl))/(np.max(Ujl) - np.min(Ujl))
    return r

def subinitialization(graph,pi,N_sub):
    SubPi= []
    NC = [i+1 for i, x in enumerate(pi.b) if x == 0]
    CN = [i+1 for i, x in enumerate(pi.b) if x == 1]

    u = np.full(shape=(len(NC),len(CN)),dtype=float,fill_value=0)
    for i in range(len(NC)):
        for j in range(len(CN)):
            u[i][j] = membership_7(graph,2,CN,NC,i, j) 

    membership = u
    S1 = []
    S2 = []
    for j in range(len(NC)):
        mean = sum(membership[j]/len(membership[j]))
        S1 = [v for v in membership[j] if v <= mean]
        S2 = [v for v in membership[j] if v >= mean]
        r_prime = pi.r[j]
        pi.r[j] = calculate_r(r_prime,u[j])
        for j in range(len(pi.r)):
            rand = random.random(0,1)
            if rand<0.5:
                pi.r[j] = random.random(0,1)
        
        SubPi.append(pi)
    return SubPi


        
            


