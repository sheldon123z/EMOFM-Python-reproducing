
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


def AR_MOEA(P, Gen, stage, G, R, A):
    Pop = copy.deepcopy(P)
    R_prime = R
    if stage == 1:
        for i in Pop:
            i.KKM, i.RC = CKR.Cal_KKM_RC(G, i)
    if stage == 2:
        pass
    for g in range(Gen):
        P_prime = MS.MatingSelection(P, R_prime)
        O = []
        i = len(P_prime)
        print('P_prime length', i)
        while i > 0:
            pi = random.choice(P_prime)
            P_prime.remove(pi)
            pj = random.choice(P_prime)
            P_prime.remove(pj)
            i -= 2
            # crossover the b vector and produce two childs
            child_i, child_j = UC.uniform_crossover(pi, pj, kkm_rc=True)
            # set up the membership matrix on the childs
            child_i = membership.membership_matrix(G, child_i, f=2)
            child_j = membership.membership_matrix(G, child_j, f=2)
            # child_i.KKM, child_i.RC = CKR.Cal_KKM_RC(G,child_i)
            O.append(child_i)
            O.append(child_j)
        AUO = list(set(A).union(set(O)))
        A, R_prime = RD.ref_adapt(AUO, R, Pop)
        combined_pop = list(set(Pop).union(set(O)))
        Pop = ES.environmental_selection(G, combined_pop, R_prime, N)
    return Pop


G = nx.Graph()
G.add_edges_from([(6, 7), (6, 1), (6, 12), (7, 12), (7, 1), (1, 12), (12, 11), (12, 2), (2, 11),
                  (9, 2), (9, 10), (9, 3), (2, 10), (10, 3), (3, 4), (3, 8), (3, 5), (4, 5), (4, 8), (5, 8)])
Gen = 5
N_pop = 20
N = len(G.nodes())
P = Init.initialize_population(G, N_pop, f=2)

KKM = [P[i].RC for i in range(len(P))]
RC = [P[i].KKM for i in range(len(P))]



R = [individual.chromesome(N) for i in range(3)]

R[0].KKM = 10
R[0].RC = 0

R[1].KKM = 5
R[1].RC = 8

R[2].KKM = 0
R[2].RC = 16

result = AR_MOEA(P, Gen, 1, G, R, P)
KKM2 = [P[i].RC for i in range(len(result))]
RC2 = [P[i].KKM for i in range(len(result))]

plt.scatter(KKM,RC,marker='*',alpha=0.3)
plt.scatter(KKM2, RC2, marker='^', alpha=1)
plt.show()
print(len(result))
print(result)


# %%
