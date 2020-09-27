import numpy as np
import math
import random
import copy
import membership


def distance_between_solution_reference(A,B,kkm_rc = True):
    '''
    Euclidean distance between two points in the objective space
    '''
    if kkm_rc:
        return math.sqrt((A.KKM - B.KKM)**2 + (A.RC-B.RC)**2)
    else:
        return math.sqrt((A.Qov - B.Qov)**2 + (A.Numoverlapping-B.Numoverlapping)**2)

def non_contributing_set(P,PR,kkm_rc=True):
    '''
    Get non-contributing set form the population
    the non-contributing set refers to those points which doesn't have a closest reference point
    '''
    contributing_set = []
    all_set = P
    remove =[]

    # select from each of the reference point, each reference point must have a closest-
    # distance-point from the population, put them into a set, and the left points are 
    # non-contributing points

    for r in PR:
        mini = math.inf
        z = None
        for p in P:
            d = distance_between_solution_reference(p,r,kkm_rc)
            if d < mini:
                mini = d
                z = p
        contributing_set.append(z)
        # match.append((r,z))
    for n in all_set:
        if n in contributing_set:
            remove.append(n)

    for r in remove:
        all_set.remove(r)

    return all_set

def contributing_set(P,PR,kkm_rc=True):
    '''
    Get contributing set form the population
    the contributing set refers to those points who have a closest reference point
    '''
    contributing_set = []
    for r in PR:
        mini = math.inf
        z = None
        for p in P:
            d = distance_between_solution_reference(p,r,kkm_rc)
            if d < mini:
                mini = d
                z = p
        contributing_set.append(z)

    return contributing_set



def IGD_NS(P, PR,kkm_rc = True):
    '''
    Get the IGD_NS metric value from the population and the reference set
    P: population 
    PR: reference value
    '''
    non_contributing = []
    if kkm_rc:
        non_contributing = non_contributing_set(P,PR)
    else:
        non_contributing = non_contributing_set(P,PR,False)
    sum1 = 0
    for x in PR:
        mini = math.inf
        for y in P:
            d = distance_between_solution_reference(x,y)
            if d < mini:
                mini = d
        sum1 += mini

    sum2 = 0
    for y in non_contributing:
        mini = math.inf
        for x in PR:
            d = distance_between_solution_reference(x,y)
            if d < mini:
                mini = d
        sum2 += mini

    return sum1+sum2     
    
        

def fitness(chromesome,P,adapted_R,kkm_rc=True):
    '''
    Find the fitness value of the given chromesome
    P: population 
    adapted_R: adapted reference set
    '''
    p_set = set(P)
    p_set.remove(chromesome)

    return IGD_NS(p_set,adapted_R,kkm_rc)



def MatingSelection(graph,P,adapted_R,kkm_rc = True):
    '''
    Perform mating selection on population and adapted reference
    If the objectives are KKM and RC, then put true flag on kkm_rc
    '''
    population = copy.deepcopy(P)
    P_prime = []
    # Normolize KKM and RC using the minimum KKM and RC value in the population 
    if kkm_rc:
        min_KKM = min([p.KKM for p in population])
        min_RC = min([p.RC for p in population])
        for chromesome in population:
            chromesome.fitness = 0

        for chromesome in population:
            chromesome.KKM = chromesome.KKM - min_KKM
            chromesome.RC = chromesome.RC - min_RC
            chromesome.fitness = fitness(chromesome,population,adapted_R,kkm_rc)

   
        for i in range(len(population)):
            p = random.choice(population)
            q = random.choice(population)
            if p.fitness > q.fitness:
                p.KKM += min_KKM
                p.RC += min_RC
                P_prime.append(p)
            else:
                q.KKM += min_KKM
                q.RC += min_RC
                P_prime.append(q)
    else:
        min_Qov = min([p.Qov for p in population])
        min_Numoverlapping = min([p.Numoverlapping for p in population])
        for chromesome in population:
            chromesome.fitness = 0

        for chromesome in population:
            chromesome.Qov = chromesome.Qov - min_Qov
            chromesome.Numoverlapping = chromesome.Numoverlapping - min_Numoverlapping
            chromesome.fitness = fitness(chromesome,population,adapted_R)

        for i in range(len(population)):
            p = random.choice(population)
            q = random.choice(population)
            if p.fitness > q.fitness:
                p.Qov += min_Qov
                p.Numoverlapping += min_Numoverlapping
                P_prime.append(p)
            else:
                q.Qov += min_Qov
                q.Numoverlapping += min_Numoverlapping
                P_prime.append(q)

    return P_prime
