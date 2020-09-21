#%%
import numpy as np
import networkx as nx
import random
from numpy import linalg
from scipy.linalg import expm
import membership
import copy
import individual



# def get_NC(chromesome):
#     NC = [i+1 for i, x in enumerate(chromesome.b) if x == 0]
#     return NC

# def get_CN(chromesome):
#     CN = [i+1 for i, x in enumerate(chromesome.b) if x == 1]
#     return CN

# def membership_7(G,f,CN,NC,i,j):
#     u_ij = 1/(sum(nx.resistance_distance(G,NC[i],CN[j])**(2/(f-1))/nx.resistance_distance(G,NC[i],CN[l]) for l in range(len(CN))))
#     # u = 1/(sum(DK_distance(G,NC[i],CN[j])**2/DK_distance(G,NC[i],CN[l]) for l in range(len(CN))))
#     return u_ij


# def membership_matrix(graph,chromesome,f):

#     CN = get_CN(chromesome)
#     NC = get_NC(chromesome)
#     #initialize membership matrix with filled 0s
#     u = np.full(shape=(len(NC),len(CN)),dtype=float,fill_value=0)
#     #calculate each NC node membership
#     for i in range(0,len(NC),1):
#         for j in range(0,len(CN),1):
#             u[i][j] = membership_7(graph,2,CN,NC,i, j) 
#     # print(u)
#     binary_membership_matrix = np.zeros_like(u,dtype=int)
#     #set the max number of the row as 1
#     binary_membership_matrix[np.arange(len(u)),u.argmax(1)]=1
    
#     for i in range(len(binary_membership_matrix)):
#         for j in range(len(binary_membership_matrix[0])):
#             chromesome.cover[CN[j]-1] = CN[j]
#             if binary_membership_matrix[i][j] == 1:
#                 chromesome.cover[NC[i]-1] = CN[j]
                
#     chromesome.membership_metrix = binary_membership_matrix
#     return chromesome


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
    


def initialize_population(graph,pop_size,f):

    N = len(graph.nodes())
    pop = []
    N_nodes = list(range(1,N+1))
    # print('N_nodes',N_nodes)


    #initialize 0 two-vector population, each tuple contains two vectors, each tuple represents a chromesome
    #the first index 0 of the tuple represent b vector
    # the index 1 of the tupe represent r vector
    # the index 2 of the tupe represent a graph object which has a nodes labelling with the community number in the 
    # node attribute
    for i in range(int(pop_size)):
        pop.append(individual.chromesome(N))

    #Step 1 

    K = get_central_nodes(graph)
    print('candidate central nodes:',K)
    
    #Step 2

    #select ith chromesome from the first to the pop_size/2
    for i in range(int(pop_size)):
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
    for i in range(int(pop_size/2+1),pop_size):
        rand_number_of_nodes = random.randint(1,N)
        # print('rand_number_of_nodes:',rand_number_of_nodes)
        #range()doesn't include the last bit, so +1 in case all the nodes are selected as central nodes
        #put the 随机数量的中心节点到初始化群落中
        temp_N = copy.deeocopy(N_nodes)
        for j in range(rand_number_of_nodes):
            rand_node = random.choice(temp_N)
            # print('rand_node:',rand_node)
            temp_N.remove(rand_node)
            #rand is the index of Pib_node, so minus 1
            pop[i].b[rand_node-1] = 1

    #labelling the node 
    for i,chromesome in enumerate(pop):
        #get CN and NC nodes, since the central is 
        # extracted from b vector, the node is labelled from 1, so the index +1 is the node's label
        chromesome = membership.membership_matrix(graph,chromesome,f=2)
        
        # print('chromesome number：{}\n\nb vector is: {}\n\nr vector is {}\n\nnode communities: {}\n\n membership matrix is:\n{}\n\n\n'
        # .format(i,pop[i][0],pop[i][1],pop[i][2],pop[i][3]))


    # print()
    # # print('chromesome community labels:')
    # for i,chromesome in enumerate(pop):
    #     print('the chromesome {}\'s label is {}'.format(i,chromesome[2].nodes.data()))
    return pop

#test
# G = nx.Graph()
# # G2 = nx.random_regular_graph(5,30)
# # G2.remove_node(0)
# G.add_edges_from([(6,7),(6,1),(6,12),(7,12),(7,1),(1,12),(12,11),(12,2),(2,11),(9,2),(9,10),(9,3),(2,10),(10,3),(3,4),(3,8),(3,5),(4,5),(4,8),(5,8)])
# pop = initialize_population(G,4,2)
# print(pop)




# %%
