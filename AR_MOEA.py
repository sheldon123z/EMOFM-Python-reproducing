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


    def one_way_crossover(self, pi,pj):
        n = len(pi[0])
        #get the node from the chromesome, the index is the node since the value 
        #represents its role as central node or non-central node
        #select a random seed in pi
        seed = random.choice(list(range(len(pi[0]))))
        #get seed's label
        community_num = graph.nodes[seed]['community']
        #get all nodes labels
        community_labels = dict(graph.nodes(data='community'))
        #get same seed label nodes list, the value is the index+1 in chromesome
        same_label_nodes = [key for (key,value) in community_labels.items() if value == community_num]
        for i in same_label_nodes:
            
        


        print(same_label_nodes)


#%%
    def Moea(self):

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
                    
                



#%%
import random
import networkx as nx
import membership
import initialization
import copy


def one_way_crossover(pi,pj):
    n = len(pi[0])
    #get the node from the chromesome, the index is the node since the value 
    #represents its role as central node or non-central node
    seed = random.choice(list(range(len(pi[0]))))
    # print(seed)
    community_num = pi[2].nodes[seed+1]['community']
    print('community_num',community_num)

    pi_community_labels = dict(pi[2].nodes(data='community'))
    # print(community_labels)
    #get the same label nodes list
    same_label_nodes = [key for (key,value) in pi_community_labels.items() if value == community_num]
    print('same label nodes in pi:',same_label_nodes)

    pj_community_labels = dict(pj[2].nodes(data='community'))
    # print(community_labels)
    #get the same label nodes list
    same_label_nodes = [key for (key,value) in pj_community_labels.items() if value == community_num]
    print('same label nodes in pj:',same_label_nodes)

    child = copy.copy(pj)
    for node in same_label_nodes:
        child[2].nodes[node]['community'] = community_num

    # print('parent a：{}\n\n parent b ：{}\n\n child：{}'.format(pi[2].nodes.data(),pj[2].nodes.data(),\
    # child[2].nodes.data()))

    return child

# graph = nx.Graph()
# graph.add_edges_from([(6,7),(6,1),(6,12),(7,12),(7,1),(1,12),(12,11),(12,2),(2,11),(9,2),(9,10),(9,3),(2,10),(10,3),(3,4),(3,8),(3,5),(4,5),(4,8),(5,8)])
# CN = [6,8,10]
# NC = [1,2,3,4,5,7,9,11,12]
# out = membership.membership_matrix(graph,CN,NC)
# print()
# print(out)

G = nx.Graph()
G2 = nx.read_edgelist('birthdeath.t01.edges',nodetype=int)

G.add_edges_from([(6,7),(6,1),(6,12),(7,12),(7,1),(1,12),(12,11),(12,2),(2,11),(9,2),(9,10),(9,3),(2,10),(10,3),(3,4),(3,8),(3,5),(4,5),(4,8),(5,8)])
pop = initialization.initialization(G2,4,2)
pi = pop[0]
pj = pop[1]
community_labels = one_way_crossover(random.choice(pop),random.choice(pop))
# %%
