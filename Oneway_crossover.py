#%% one_Way_crossover
import random
import networkx as nx
import membership
from initialization import initialize_population
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
pop = initialize_population(G2,4,2)
pi = pop[0]
pj = pop[1]
community_labels = one_way_crossover(random.choice(pop),random.choice(pop))