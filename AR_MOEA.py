import networkx as nx
import numpy as np
import random

class AR_MOEA():

    def __init__(self, graph, population,gen,stage_num):
        self.graph = graph
        self.population = population
        self.gen = gen
        self.stage_num = stage_num


    def MatingSelection(self,P):
        pass

    def EnvSelection(self):
        pass
    
    def Cal_KKM(self):
        pass
    
    def Cal_RC(self):
        pass
    
    def Cal_ExtendedQ(self):
        pass

    def Evaluation(self,chrosome):
        if stage_num == 1:
            kkm = self.Cal_KKM(chrosome)
            rc = self.Cal_RC(self.population)
        # elif stage_num == 2:
        #     Q = self.Cal_ExtendedQ(self)
        
        return kkm, rc


#%%
    def Moea_s1(self):

        for i in population:
            self.Evaluation(self,i)

        for g in range(len(gen)):
            P_prime = self.MatingSelection(self,self.population)
            O = []
            while P_prime:
                p_i = random.choice(P_prime)
                p_j = random.choice(P_prime)
                P_prime.remove(p_i)
                P_prime.remove(p_j)
                if stage_num == 1:
                    #TODO finish the s1 moea


    #TODO finish the s2 moea
    def Moea_s2(self):
        pass         
                






# %% Uniform crossover
import random
import networkx as nx
import membership
import copy
import itertools
from initialization import membership_matrix,initialize_population
from itertools import combinations


#get the nodes in the input community_labels vector, but the label information is lost
def get_communities_list(community_labels):
    # community_labels =[12, 2, 4, 4, 5, 12, 7, 4, 9, 9, 2, 12]
    # output [[0, 5, 11], [1, 10], [2, 3, 7], [4], [6], [8, 9]]
    appeared = set()
    communities = []
    for i in community_labels:
        if i not in appeared:
            temp = []
            appeared.add(i)
            for j,k in enumerate(community_labels):
                if k == i:
                    temp.append(j)
            communities.append(temp)
    return communities

def Cal_KKM(graph,chromesome):

    community_labels = chromesome[2]
    k = len(set(community_labels))
    n = len(community_labels)

    communities = get_communities_list(community_labels)

    print('communities division is:',communities)  
    print()

    adjacent_matrix = nx.convert_matrix.to_numpy_array(graph)

    print('adjacency matrix of the graph is:',adjacent_matrix)

    L = 0.0
    # since the adjacent matrix is synmmetric so it can be done like this
    for i in communities:
        node_combs = combinations(i,2)
        inside_sum = 0.0
        for j in node_combs:
            inside_sum += adjacent_matrix[j[0]][j[1]]
        L += inside_sum/len(i)

    # or like this
    # for i in communities:
    #     temp = 0
    #     for k in i:
    #         for w in i:
    #             temp += adjacent_matrix[k][w]
    #     L += temp /len(i) 
    # print('L is: ',L)     
    KKM = 2*float((n-k)) - L

    RC = 0.0
    nodes = list(range(1,n+1))
    for i in communities:
        temp = 0
        omega = communities.copy()
        omega.remove(i)
        diff = list(itertools.chain.from_iterable(omega))
        for k in i:
            for w in diff:
                temp += adjacent_matrix[k][w]
        RC += temp /len(i)   

   

    print('KKM {} RC {}'.format(KKM,RC))

    return KKM,RC


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

pop = initialize_population(G4,4,2)
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

KKM, RC = Cal_KKM(G4,child1)

#%% Mating selection









    






# %%
