
#%% overlapping modularity
import networkx as nx
from itertools import product
from itertools import permutations
from itertools import combinations



def overlapping_modularity(graph,cover):
    m = len(nx.edges(graph))
    A = nx.to_numpy_array(graph,dtype=int)
    k =  len(cover)
    node_dict = {}
    # 统计每个节点的社团个数
    for i in range(len(cover)):
        for node in cover[i]:
            node_dict[node] = node_dict.get(node,0) + 1

    list1 =[]
    list2 =[]
    for i in range(k):
        for v,w in combinations(cover[i],2):
            # print(v,w)
            list1.append((1/(node_dict[v]*node_dict[w])) * (A[v-1][w-1] - (G2.degree(v)*G2.degree(w)/(m*2))))
        list2 .append(sum(list1))
    Qov = 1/(2*m)*sum(list2)
    return Qov


# G2 = nx.Graph()
# from itertools import combinations
# net1 = combinations(range(1,5),2)
# net2 = combinations(range(4,8),2)
# G2.add_edges_from([x for x in net1])
# G2.add_edges_from([x for x in net2])
# G2.remove_edge(4,6)
# nx.draw(G2)
# cover3=[{1,2,3,4},{4,5,6,7}]
# cover4 = [{1,2,3,4},{5,6,7}]

# print(overlapping_modularity(G2,cover3))
# %%

import networkx as nx
import copy
from itertools import combinations,product,chain



#get the nodes in the input community_labels vector, but the label information is lost


def Cal_KKM_RC(graph,cover):

    k = len(cover)
    n = len(graph.nodes())
    A = nx.convert_matrix.to_numpy_array(graph)
    
    Ls =[]
    for i in range(k):
        L = sum([A[v-1][w-1] for v,w in combinations(cover[i],2)])
        Ls.append(L/len(cover[i]))
    
    KKM = 2*(n-k)-sum(Ls)
    Ls = []
    for i in range(k):
        C_j = copy.deepcopy(cover)
        C_j.remove(cover[i])
        C_j = set(chain.from_iterable(C_j))
        L = sum([A[v-1][w-1] for v,w in product(cover[i],C_j)])
        Ls.append(L/len(cover[i]))
    RC = sum(Ls)
    return KKM, RC



G2 = nx.Graph()
net1 = combinations(range(1,5),2)
net2 = combinations(range(4,8),2)
G2.add_edges_from([x for x in net1])
G2.add_edges_from([x for x in net2])
G2.remove_edge(4,6)
nx.draw(G2)
cover3=[{1,2,3,4},{4,5,6,7}]
cover4 = [{1,2,3,4},{5,6,7}]

KKM, RC = Cal_KKM_RC(G2,cover4)
print(KKM,RC)


# %%
