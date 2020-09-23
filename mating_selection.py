import numpy as np
import math
import random
import copy


def distance_KKM_RC(A,B):
    '''
    Euclidean distance between two points in the objective space
    '''
    return math.sqrt((A.KKM - B.KKM)**2 + (A.RC-B.RC)**2)

def non_contributing_set(P,PR):
    '''
    Get non-contributing set form the population
    the non-contributing set refers to those points which doesn't have a closest reference point
    '''
    contributing_set = set()
    all_set = set(P)

    # select from each of the reference point, each reference point must have a closest-
    # distance-point from the population, put them into a set, and the left points are 
    # non-contributing points

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
    '''
    Get contributing set form the population
    the contributing set refers to those points who have a closest reference point
    '''
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
    '''
    Get the IGD_NS metric value from the population and the reference set
    P: population 
    PR: reference value
    '''
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
    
        

def fitness(chromesome,P,adapted_R):
    '''
    Find the fitness value of the given chromesome
    P: population 
    adapted_R: adapted reference set
    '''
    p_set = set(P)
    p_set.remove(chromesome)

    return IGD_NS(p_set,adapted_R)



def MatingSelection(P,adapted_R,kkm_rc = True):
    '''
    Perform mating selection on population and adapted reference
    If the objectives are KKM and RC, then put true flag on kkm_rc
    '''
    population = copy.deepcopy(P)

    # Normolize KKM and RC using the minimum KKM and RC value in the population 
    if kkm_rc:
        mini_KKM = math.inf
        mini_RC = math.inf
        for chromesome in population:
            if chromesome.KKM < mini_KKM:
                mini_KKM = chromesome.KKM
            if chromesome.RC < mini_RC:
                mini_RC = chromesome.RC

        for chromesome in population:
            chromesome.KKM = round(chromesome.KKM - mini_KKM,2)
            chromesome.RC = round(chromesome.RC - mini_RC,2)
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
