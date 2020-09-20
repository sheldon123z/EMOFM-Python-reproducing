
#%%
import Calculate_KKM_RC as KKMRC
from initialization import initialize_population
import networkx as nx
def is_dominating_mini(A,B):
    flag = True
    for i, j in zip(A,B):
        if i > j:
            flag = False
    return flag


def contains_dominating_solution(F_k,solution):

    for x in reversed(F_k):
        if is_dominating_mini(x[4][0],solution[4][0]) and is_dominating_mini(x[4][1],solution[4][1]):
            return True
    return False


def sortingPop(graph,population,decending = False):
    for individual in population:
        KR = KKMRC.Cal_KKM_RC(graph,individual)
        individual.append([KR[0],KR[1]])
    #sorting the population in ascending order
    sortedPop = sorted(population,key = lambda individual: individual[4][0])
    return sortedPop

def ENS_BS(individual,F):
    pass

def ENS_SS(individual,F):
    
    x = len(F)
    k = 0
    appended = False
    for F_k in F:
        if not contains_dominating_solution(F_k,individual[4][0]):
            F_k.append(individual)
            return F
    F.append([individual])
    return F


def MainStep(graph,population):

    F = [[]]
    sortedPop = sortingPop(graph,population)
    for individual in sortedPop:
        individual = ENS_SS(individual,F)
    return F



G = nx.Graph()
G.add_edges_from([(6,7),(6,1),(6,12),(7,12),(7,1),(1,12),(12,11),(12,2),(2,11),(9,2),(9,10),(9,3),(2,10),(10,3),(3,4),(3,8),(3,5),(4,5),(4,8),(5,8)])
pop = initialize_population(G,4,2)

F = MainStep(G,pop)



# %%
