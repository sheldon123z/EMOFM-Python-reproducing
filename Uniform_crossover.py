# %% Uniform crossover
import random
import networkx as nx
import membership
import copy
import itertools
from initialization import membership_matrix,initialize_population
from itertools import combinations
from Calculate_KKM_RC import Cal_KKM_RC

def uniform_crossover(G,pi,pj):
    
    
    child1 = copy.deepcopy(pi)
    child2 = copy.deepcopy(pj)

    for i in range(len(pi[0])):
        rand_number = random.uniform(0,1)
        if rand_number > 0.5:
            #cross b vector
            child1[0][i] = pj[0][i]
            child1[2][i] = pj[2][i]
            child1.pop()
            child1 = membership_matrix(G,child1,2)

            child2[0][i] = pi[0][i]
            child2[2][i]= pi[2][i]
            child2.pop()
            child2 = membership_matrix(G,child2,2)
            
    return child1,child2


# G = nx.Graph()
# G2 = nx.read_edgelist('birthdeath.t01.edges',nodetype=int)
# G.add_edges_from([(6,7),(6,1),(6,12),(7,12),(7,1),(1,12),(12,11),(12,2),(2,11),(9,2),(9,10),(9,3),(2,10),(10,3),(3,4),(3,8),(3,5),(4,5),(4,8),(5,8)])

# G3 = nx.path_graph(30)
# G3.remove_node(0)
G4 = nx.karate_club_graph()
mapping = dict(zip(G4, range(1, 34)))
G4 = nx.relabel_nodes(G4, mapping)

pop = initialize_population(G4,2,2)
parent1 = random.choice(pop)
parent2 = random.choice(pop)
child1, child2 = uniform_crossover(G4,parent1,parent2)

print('parent number：{}\n\nb vector is: {}\n\nr vector is {}\n\nnode communities: {}\n\n membership matrix is:\n{}\n\n\n'
.format(1,parent1[0],parent1[1],parent1[2],parent1[3]))
print('parent number：{}\n\nb vector is: {}\n\nr vector is {}\n\nnode communities: {}\n\n membership matrix is:\n{}\n\n\n'
.format(2,parent2[0],parent2[1],parent2[2],parent2[3]))

print('child number：{}\n\nb vector is: {}\n\nr vector is {}\n\nnode communities: {}\n\n membership matrix is:\n{}\n\n\n'
.format(1,child1[0],child1[1],child1[2],child1[3]))
# print('child number：{}\n\nb vector is: {}\n\nr vector is {}\n\nnode communities: {}\n\n membership matrix is:\n{}\n\n\n'
# .format(2,child2[0],child2[1],child2[2],child2[3]))

# print(child1)

KKM, RC = Cal_KKM_RC(G4,child1)
# %%
