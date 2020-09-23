import networkx as nx
import copy
import itertools
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

def Cal_KKM_RC(graph,chromesome):

    community_labels = chromesome.cover
    k = len(set(community_labels))
    n = len(community_labels)

    communities = get_communities_list(community_labels)

    # print('communities division is:',communities)  
    print()

    adjacent_matrix = nx.convert_matrix.to_numpy_array(graph)

    # print('adjacency matrix of the graph is:',adjacent_matrix)

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

    # print('KKM {} RC {}'.format(KKM,RC))

    return round(KKM,2),round(RC,2)

