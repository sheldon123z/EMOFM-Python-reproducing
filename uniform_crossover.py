
# %% Uniform crossover
import random
import networkx as nx
import membership 
import copy
import itertools
import calculate_KKM_RC as CKR
from initialization import initialize_population
from itertools import combinations


def uniform_crossover(pi,pj,kkm_rc=False,Qov =False):
    
    
    child1 = copy.deepcopy(pi)
    child2 = copy.deepcopy(pj)
    if kkm_rc:
        for i in range(len(pi.b)):
            rand_number = random.uniform(0,1)
            if rand_number > 0.5:
                #cross b vector
                child1.b[i] = pj.b[i]
                child1.cover[i] = pj.cover[i]
                # child1 = membership.membership_matrix(G,child1,2)

                child2.b[i] = pi.b[i]
                child2.cover[i]= pi.cover[i]
                # child2 = membership.membership_matrix(G,child2,2)
            
    return child1,child2

# #Test Enzemy_g163 graph
# G = nx.Graph()
# G.add_edges_from([(6,7),(6,1),(6,12),(7,12),(7,1),(1,12),(12,11),(12,2),(2,11),(9,2),(9,10),(9,3),(2,10),(10,3),(3,4),(3,8),(3,5),(4,5),(4,8),(5,8)])

# #Test birthdeath graph generated 
# G2 = nx.read_edgelist('birthdeath.t01.edges',nodetype=int)

# A path graph
# G3 = nx.path_graph(30)
# mapping = dict(zip(G3, range(1, 31)))
# G3 = nx.relabel_nodes(G3, mapping)

# #Test karate club graph
# G4 = nx.karate_club_graph()
# mapping = dict(zip(G4, range(1, 34)))
# G4 = nx.relabel_nodes(G4, mapping)


# pop = initialize_population(G,4,2)
# parent1 = random.choice(pop)
# parent2 = random.choice(pop)
# child1, child2 = uniform_crossover(G,parent1,parent2)
# KKM, RC = CKR.Cal_KKM_RC(G,child1)
# -------------------------------print testing information-----------------------
# print('parent number：{}\n\nb vector is: {}\n\nr vector is {}\n\nnode communities: {}\n\n membership matrix is:\n{}\n\n\n'
# .format(1,parent1.b,parent1.r,parent1.cover,parent1.membership_metrix))
# print('parent number：{}\n\nb vector is: {}\n\nr vector is {}\n\nnode communities: {}\n\n membership matrix is:\n{}\n\n\n'
# .format(2,parent2.b,parent2.r,parent2.cover,parent2.membership_metrix))

# print('child number：{}\n\nb vector is: {}\n\nr vector is {}\n\nnode communities: {}\n\n membership matrix is:\n{}\n\n\n'
# .format(1,child1.b,child1.r,child1.cover,child1.membership_metrix))
# print('child number：{}\n\nb vector is: {}\n\nr vector is {}\n\nnode communities: {}\n\n membership matrix is:\n{}\n\n\n'
# .format(2,child2[0],child2[1],child2[2],child2[3]))


#%% Mating selection




