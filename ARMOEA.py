# %%import networkx as nx
import networkx as nx
import matplotlib.pyplot as plt
import individual
import initialization as Init
import numpy as np
import random
import calculate_KKM_RC as CKR
import mating_selection as MS
import uniform_crossover as UC
import environmental_selection as ES
import refpoint_adaption as RD
import membership
import copy

def Variation(G,P_prime, N):
    O = []
    
    while len(P_prime) > 0:
        pi = random.choice(P_prime)
        P_prime.remove(pi)
        if (len(P_prime) != 0):
            pj = random.choice(P_prime)
            P_prime.remove(pj)
        else:
            pj = pi
        # crossover the b vector and produce two children
        child_i, child_j = UC.uniform_crossover(pi, pj, kkm_rc=True)
        # set up the membership matrix on the child
        child_i = membership.factor_individual(G, child_i, f=2)
        child_j = membership.factor_individual(G, child_j, f=2)
        # child_i.KKM, child_i.RC = CKR.Cal_KKM_RC(G,child_i)
        O.append(child_i)
        O.append(child_j)
    return O

def AR_MOEA(population, generation, stage, graph, reference):

    P = copy.deepcopy(population)
    A = copy.deepcopy(population)
    R = copy.deepcopy(reference)
    R_prime = copy.deepcopy(R)

    N_pop = len(P)
    if stage == 1:
        for i in P:
            membership.factor_individual(graph,i, f=2)
    if stage == 2:
        pass
    for g in range(generation):
        P_prime = MS.MatingSelection(graph,P, R_prime)
        print('after mating p_prime',len(P_prime))
        O = Variation(graph, P_prime, N)
        print('after variation P_prime length', len(P_prime))
        # AUO = list(set(A).union(set(O)))
        AUO = copy.deepcopy(A)
        for o in O:
            AUO.append(o)

        A, R_prime = RD.ref_adapt(AUO, R, P)
        print('refadapted is ', len(P))
        # PUO = list(set(P).union(set(O)))
        PUO = copy.deepcopy(P)
        for o in O:
            PUO.append(o)

        print('combined population is {}'.format(len(PUO)))
        P = ES.environmental_selection(graph, PUO, R_prime, N_pop)
        print('environmental selected population is {}'.format(len(P)))
    for i in P:
        membership.factor_individual(graph,i, f=2)  
    return P


if __name__ == "__main__":

    G = nx.Graph()
    # G.add_edges_from([(6, 7), (6, 1), (6, 12), (7, 12), (7, 1), (1, 12), (12, 11), (12, 2), (2, 11),
    #                   (9, 2), (9, 10), (9, 3), (2, 10), (10, 3), (3, 4), (3, 8), (3, 5), (4, 5), (4, 8), (5, 8)])
    G.add_edges_from([(6,7),(6,1),(6,12),(7,12),(7,1),(1,12),(12,11),(12,2),(2,11),
                    (9,2),(9,10),(9,3),(2,10),(10,3),(3,4),(3,8),(3,5),(4,5),(4,8),(5,8)])
    Gen = 5
    N_pop = 60
    N = len(G.nodes())
    P = Init.initialize_population(G, N_pop, f=2)

    KKM = [P[i].RC for i in range(len(P))]
    RC = [P[i].KKM for i in range(len(P))]

    R = [individual.chromesome(N) for i in range(10)]

    # R[0].KKM = 10
    # R[0].RC = 0

    # R[1].KKM = 5
    # R[1].RC = 5

    # R[2].KKM = 0
    # R[2].RC = 10
    # R[2].KKM = 3
    # R[2].RC = 7

    for i in range(10):
        R[i].KKM = (10 - i)
        R[i].RC = i

    KKM3 = [R[i].RC for i in range(len(R))]
    RC3 = [R[i].KKM for i in range(len(R))]
    plt.scatter(KKM3, RC3, marker='+', alpha=0.5)

    result = AR_MOEA(P, Gen, 1, G, R)
    KKM2 = [result[i].RC for i in range(len(result))]
    RC2 = [result[i].KKM for i in range(len(result))]

    plt.scatter(KKM, RC, marker='*', alpha=0.3)
    plt.scatter(KKM2, RC2, marker='^', alpha=1)

    plt.show()
    print(len(result))
    # for i in result:
    # print('b vector {}, r vector {},cover: {}'.format(i.b,i.r,i.cover))
    # print('{} KKM {}, RC{}',i,i.KKM, i.RC)
    # print(result)

# %%
