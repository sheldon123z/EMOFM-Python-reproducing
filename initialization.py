#%%
import numpy as np
import networkx as nx
import random
import calculate_KKM_RC as CKR
from numpy import linalg
from scipy.linalg import expm
import membership
import copy
import individual



def get_central_nodes(graph):
    V = dict(graph.degree())
    K = []

    while V:
        #get the max degree node
        #不知道这个是随机选取的最大度节点还是选择第一个最大度节点呢？
        w = max(V,key=V.get)
        maxi_degree_nodes = [node for (node,value) in V.items() if V[w] == value ]
        #TODO 如果是随机选择 那么则会产生不同的中心节点集合，因为剪切网络的顺序是不同的
        w = random.choice(maxi_degree_nodes)
        K.append(w)
        del V[w]
        for n in nx.neighbors(graph,w):
            if n in V:
                del V[n]
    return K
    


def initialize_population(graph,N_pop,f):

    N = len(graph.nodes())
    pop = []


    ''' 
    Initialize population
    '''
    for i in range(int(N_pop)):
        pop.append(individual.chromesome(N))

    #Step 1 

    K = get_central_nodes(graph)
    print('candidate central nodes:',K)
    
    #Step 2

    #select ith chromesome from the first to the N_pop/2
    for i in range(int(N_pop/2)):
        #rand is the index of the central node
        rand_number_of_nodes = random.randint(1,len(K))
        K_copy = copy.deepcopy(K)
        #random number is the number of central node to be put into the initial chrosomes
        for j in range(rand_number_of_nodes):
            rand_node = random.choice(K_copy)
            K_copy.remove(rand_node)
            #rand_node is the index of the node, so it has to minus 1 to find the correct central node
            pop[i].b[rand_node-1] = 1

    # select ith chromesome 
    # print('num_nodes',num_nodes)
    randBinList = lambda n: [random.randint(0,1) for b in range(1,n+1)]
    for i in range(int(N_pop/2),N_pop):
        # rand_number_of_nodes = random.randint(1,N-1)
        # # print('rand_number_of_nodes:',rand_number_of_nodes)
        # #range()doesn't include the last bit, so +1 in case all the nodes are selected as central nodes
        # #put the 随机数量的中心节点到初始化群落中

        # for j in range(rand_number_of_nodes):
        #     rand_node = random.choice(range(N))
        #     # #rand is the index of Pib_node, so minus 1
        #     pop[i].b[rand_node-1] = 1
        while all(v==0 for v in pop[i].b):
            pop[i].b = randBinList(N)





    #labelling the node 
    for i,chromesome in enumerate(pop):
        #get CN and NC nodes, since the central is 
        # extracted from b vector, the node is labelled from 1, so the index +1 is the node's label
        chromesome = membership.factor_individual(graph,chromesome,f=2)
        # KKM,RC = CKR.Cal_KKM_RC(graph,chromesome)
        # chromesome.KKM = KKM
        # chromesome.RC = RC
        
        # print('chromesome number：{}\n\nb vector is: {}\n\nr vector is {}\n\nnode communities: {}\n\n membership matrix is:\n{}\n\n\n'
        # .format(i,pop[i][0],pop[i][1],pop[i][2],pop[i][3]))


    # for i,chromesome in enumerate(pop):
    #     print('the chromesome {}\'s label is {}'.format(i,chromesome[2].nodes.data()))
    return pop

# test
# G = nx.Graph()
# G.add_edges_from([(6,7),(6,1),(6,12),(7,12),(7,1),(1,12),(12,11),(12,2),(2,11),(9,2),(9,10),(9,3),(2,10),(10,3),(3,4),(3,8),(3,5),(4,5),(4,8),(5,8)])
# pop = initialize_population(G,4,2)
# print(pop)




# %%
