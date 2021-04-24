#这个文件是整体算法，包含第一部分和第二部分，尚未完成，测试第一部分运行AEMOEA.py

import initialization as Init
from ARMOEA import AR_MOEA
import networkx as nx
import individual
from matplotlib import pyplot as plt
from subinitialization import subinitialization





def delete_dominated_individuals(P):
    pass


def general_framework(Gen,R,N_pop,N_sub,graph,R_sub):
    

    #Stage 1
    P = Init.initialize_population(G, N_pop, f=2)

    # drawing the initial population objective space graph
    KKM = [P[i].RC for i in range(len(P))]
    RC = [P[i].KKM for i in range(len(P))]
    plt.scatter(KKM, RC, marker='g*', alpha=0.3)

    #RUNNING the algorithm 
    result = AR_MOEA(P, Gen, 1, G, R)
    
    #--- drawing the non-overlapping optimization graph on objective space----#
    KKM_ref = [R[i].RC for i in range(len(R))]
    RC_ref = [R[i].KKM for i in range(len(R))]
    plt.scatter(KKM_ref, RC_ref, marker='+', alpha=0.5)
    
    #--- drawing the result population of non-overlapping optimization graph on objective space----#
    KKM_result = [result[i].RC for i in range(len(result))]
    RC_result = [result[i].KKM for i in range(len(result))]
    plt.scatter(KKM_result, RC_result, marker='r^', alpha=1)


    plt.xlabel("RC")
    plt.ylabel("KKM")
    plt.show()

    #Stage 2
    FR = []
    for pi in range(len(result)):
        SubPi = subinitialization(pi,N_sub)
        SubPi = AR_MOEA(SubPi,Gen,2,G,R_sub)
        delete_dominated_individuals(SubPi)
        FR.append(p for p in SubPi)
    return FR
    







if __name__ == "__main__":

    G = nx.Graph()
    # G.add_edges_from([(6, 7), (6, 1), (6, 12), (7, 12), (7, 1), (1, 12), (12, 11), (12, 2), (2, 11),
    #                   (9, 2), (9, 10), (9, 3), (2, 10), (10, 3), (3, 4), (3, 8), (3, 5), (4, 5), (4, 8), (5, 8)])
    G.add_edges_from([(6,7),(6,1),(6,12),(7,12),(7,1),(1,12),(12,11),(12,2),(2,11),
                    (9,2),(9,10),(9,3),(2,10),(10,3),(3,4),(3,8),(3,5),(4,5),(4,8),(5,8)])
    Gen = 3
    N_pop = 10
    N = len(G.nodes())



    #initialize initial reference points
    R = [individual.chromesome(N) for i in range(10)]

    #setup reference points
    for i in range(10):
        R[i].KKM = (10 - i)
        R[i].RC = i
    
    N_sub = 10
    general_framework(Gen,R,N_pop,N_sub,G)