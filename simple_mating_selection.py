import numpy as np
import math
import random
import copy


def distance_KKM_RC(A,B):
    return math.sqrt((A[1] - B[1])**2 + (A[0]-B[0])**2)



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

def contributing_set(P,PR):
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
    return contributing_set

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



def MatingSelection_KKM_RC(pop,adapted_R):

    population = copy.deepcopy(pop)
    mini_KKM = math.inf
    for chromesome in population:
        if chromesome[1] < mini_KKM:
            mini_KKM = chromesome[1]

    mini_RC = math.inf
    for chromesome in population:
        if chromesome[0] < mini_RC:
            mini_RC = chromesome[0]
    
    for chromesome in population:
        chromesome[1] = chromesome[1] - mini_KKM
        chromesome[0] = chromesome[0] - mini_RC
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


