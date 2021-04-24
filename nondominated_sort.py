
#%%

'''
An Efficient Approach to Nondominated Sorting for Evolutionary Multiobjective Optimization
'''

import Calculate_KKM_RC as CKR
from initialization import initialize_population
import networkx as nx


def is_dominating_mini(A,B):
    '''
    A dominates B in minimization problem means all objective values of A are
    less than B
    '''
    return A.RC<B.RC and A.KKM < B.KKM


def sortingPop(graph,population,decending = False):
    '''
    sort the population by ascending order
    '''
    # for individual in population:
    #     KKM, RC = CKR.Cal_KKM_RC(graph,individual)
    #     individual.KKM = KKM
    #     individual.RC = RC
    #sorting the population in ascending order
    sortedPop = sorted(population,key = lambda individual: (individual.KKM, individual.RC))
    return sortedPop

def ENS_BS(individual,F):
    pass

def contains_dominating_solution(F_k,solution):
    '''
    check if F_k contains dominating solution compared to the current solution
    '''
    #using reversed order to check because the most dominating solution on KKM 
    #direction has the highest possibility of dominating on RC direction 
    for x in reversed(F_k):
        if is_dominating_mini(x,solution):
            return True
    return False

def ENS_SS(individual,F):
    '''
    Sequential sort
    '''
    x = len(F)
    k = 0
    appended = False
    for F_k in F:
        if not contains_dominating_solution(F_k,individual):
            F_k.append(individual)
            return F
    F.append([individual])
    return F


def produce_fronts(graph,population):
    '''
    Produces the fronts, the fronts are ascending ordered, which means the F[0] contains 
    the most dominating non-dominated individuals among others
    '''
    F = [[]]
    sortedPop = sortingPop(graph,population)
    for individual in sortedPop:
        individual = ENS_SS(individual,F)
    return F



# # %% Test the function

# import matplotlib.pyplot as plt

# G = nx.Graph()
# G.add_edges_from([(6,7),(6,1),(6,12),(7,12),(7,1),(1,12),(12,11),(12,2),(2,11),(9,2),(9,10),(9,3),(2,10),(10,3),(3,4),(3,8),(3,5),(4,5),(4,8),(5,8)])
# pop = initialize_population(G,50,2)

# F = produce_fronts(G,pop)
# print(len(F))
# KKM = []
# RC = []
# color = []
# for i,k in enumerate(F):
#     for j,m in enumerate(k):
#         KKM.append(m.KKM)
#         RC.append(m.RC)
#         color.append(i)

# plt.scatter(RC,KKM,c=color,marker='+')
# plt.xlabel = 'RC'
# plt.ylabel = 'KKM'
# plt.title = 'Objective Space'
# plt.show()

# %%
