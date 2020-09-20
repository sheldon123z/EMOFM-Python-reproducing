import numpy as np
import math
import random



def distance_KKM_RC(A,B):
    return math.sqrt((A.KKM - B.KKM)**2 + (A.RC-B.RC)**2)



def non_contributing_set(P,PR):
    contributing_set = set()
    all_set = set(P)
    # match =[]
    for r in PR:
        mini = math.inf
        z = None
        for p in P:
            d = distance_KKM_RC(p,r)
            if d < mini:
                mini = d
                z = p
        contributing_set.add(z)
        # match.append((r,z))
    non_contributing_set = all_set - contributing_set

    return non_contributing_set


def IGD_NS(P, PR):
    non_contributing = non_contributing_set(P,PR)
    sum1 = 0
    for x in PR:
        mini = math.inf
        for y in P:
            d = distance_KKM_RC(x,y)
            if d < mini:
                mini = d
        sum1 += mini

    sum2 = 0
    for y in non_contributing:
        mini = math.inf
        for x in PR:
            d = distance_KKM_RC(x,y)
            if d < mini:
                mini = d
        sum2 += mini

    return sum1+sum2     
    
        

def fitness(chromesome,population,adapted_R):

    p_set = set(population)
    new_pop = p_set.remove(chromesome)

    return IGD_NS(new_pop,adapted_R)



def MatingSelection_KKM_RC(population,adapted_R):

    
    mini_KKM = math.inf
    for chromesome in population:
        if chromesome.KKM < mini_KKM:
            mini_KKM = chromesome.KKM

    mini_RC = math.inf
    for chromesome in population:
        if chromesome.RC < mini_RC:
            mini_RC = chromesome.RC
    
    for chromesome in population:
        chromesome.KKM = chromesome.KKM - mini_KKM
        chromesome.RC = chromesome.RC - mini_RC
        chromesome.fitness = fitness(chromesome,population,adapted_R)

    P_prime = []
    for i in range(len(population)):
        p = random.choice(population)
        q = random.choice(population)
        if p.fitness > q.fitness:
            P_prime.append(p)
        else:
            P_prime.append(q)
    return P_prime
