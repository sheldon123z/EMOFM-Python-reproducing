#该部分算法为文章第一部分算法的实现

# %%
import networkx as nx
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

'''
population : 种群数量
generation： 世代次数
stage：阶段代号
graph：networkx graph类型
reference：文章中的参变量R
'''
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
        print('Generation NO.{}, Population size: {}'.format(g,len(P)))
        P_prime = MS.MatingSelection(graph,P, R_prime)
        # print('after mating p_prime',len(P_prime))
        O = Variation(graph, P_prime, N)
        # print('after variation P_prime length', len(P_prime))
        # AUO = list(set(A).union(set(O)))
        AUO = copy.deepcopy(A)
        for o in O:
            AUO.append(o)

        A, R_prime = RD.ref_adapt(AUO, R, P)
        # print('refadapted is ', len(P))
        # PUO = list(set(P).union(set(O)))
        PUO = copy.deepcopy(P)
        for o in O:
            PUO.append(o)

        # print('combined population is {}'.format(len(PUO)))
        P = ES.environmental_selection(graph, PUO, R_prime, N_pop)
        # print('environmental selected population is {}'.format(len(P)))
    for i in P:
        membership.factor_individual(graph,i, f=2)  
    return P

def decode_cover_to_dic(cover):

    partition = dict()
    for n in range(len(cover)):
        partition[n+1] = cover[n]-1
    return partition

if __name__ == "__main__":
    from draw_community import community_layout
    import matplotlib.pyplot as plt



    G = nx.Graph()
    G.add_edges_from([(6, 7), (6, 1), (6, 12), (7, 12), (7, 1), (1, 12), (12, 11), (12, 2), (2, 11),
                      (9, 2), (9, 10), (9, 3), (2, 10), (10, 3), (3, 4), (3, 8), (3, 5), (4, 5), (4, 8), (5, 8)])

    Gen = 20
    N_pop = 30
    N = len(G.nodes())
    P = Init.initialize_population(G, N_pop, f=2)

    KKM = [P[i].RC for i in range(len(P))]
    RC = [P[i].KKM for i in range(len(P))]

    #initialize initial reference points
    R = [individual.chromesome(N) for i in range(10)]

    #setup reference points
    for i in range(10):
        R[i].KKM = (10 - i)
        R[i].RC = i
    
    #RUNNING the algorithm 
    result = AR_MOEA(P, Gen, 1, G, R)
    
    #--- drawing the graph----#
    KKM_ref = [R[i].RC for i in range(len(R))]
    RC_ref = [R[i].KKM for i in range(len(R))]
    plt.scatter(KKM_ref, RC_ref, marker='+', alpha=0.5)

    
    KKM_result = [result[i].RC for i in range(len(result))]
    RC_result = [result[i].KKM for i in range(len(result))]

    plt.scatter(KKM, RC, marker='*', alpha=0.5)
    plt.scatter(KKM_result, RC_result, marker='^', alpha=1)
    plt.xlabel("RC")
    plt.ylabel("KKM")
    plt.show()

    for i,p in enumerate(result):
        partition = decode_cover_to_dic(p.cover)
        pos = community_layout(G,partition)
        nx.draw_networkx(G,pos,node_color = list(partition.values()),node_size=300,with_labels=True)
        plt.title('chromesome No.{}'.format(i))
        plt.show()
    print(len(result))



