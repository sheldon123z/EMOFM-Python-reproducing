#种群initialization算法

#%%
import networkx as nx
import random
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

    ''' 
    Initialize population
    '''

    N = len(graph.nodes())
    pop = []

    for i in range(int(N_pop)):
        pop.append(individual.chromesome(N))

    #Step 1 
    K = get_central_nodes(graph)
    print('candidate central nodes:',K)
    
    #Step 2
    # select ith chromesome from the first half of the population
    for i in range(int(N_pop/2)):
        K_copy = copy.deepcopy(K)
        #choose random number of nodes in K to initialize the b vecotr
        for j in range(random.randint(1,len(K))):
            rand_node = K_copy.pop(random.randint(0,len(K_copy)-1))
            #rand_node is the index of the node, so it has to minus 1 to find the correct central node
            pop[i].b[rand_node-1] = 1
    # randomly initialize the second half of the population 
    randBinaryList = lambda n: [random.randint(0,1) for b in range(1,n+1)]
    for i in range(int(N_pop/2),N_pop):
        while all(v==0 for v in pop[i].b):
            pop[i].b = randBinaryList(N)

    #factor the node in population
    for chromesome in pop:
        chromesome = membership.factor_individual(graph,chromesome,f=2)
 
    return pop


""" Test the initialization """
# if __name__ == "__main__":
#     G = nx.Graph()
#     G.add_edges_from([(6,7),(6,1),(6,12),(7,12),(7,1),(1,12),(12,11),(12,2),(2,11),(9,2),(9,10),(9,3),(2,10),(10,3),(3,4),(3,8),(3,5),(4,5),(4,8),(5,8)])
#     pop = initialize_population(G,4,2)
#     print(pop)

