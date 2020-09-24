#%%
import networkx as nx
import numpy as np
import copy
import itertools
from scipy.linalg import expm

def get_communities_list(community_labels):
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
    # print()

    adjacent_matrix = nx.convert_matrix.to_numpy_array(graph)

    # print('adjacency matrix of the graph is:',adjacent_matrix)

    L = 0.0
    # since the adjacent matrix is synmmetric so it can be done like this
    for i in communities:
        node_combs = itertools.combinations(i,2)
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

    return round(KKM,5),round(RC,5)



#heat distance
def DK_distance(G,i,j,beta=1):
    L = nx.linalg.laplacian_matrix(G).todense()
    K = expm(-beta*L)
    DK = np.max(K)-K
    DK = np.asarray(DK)
    return DK[j-1][i-1]

def get_NC(chromesome):
    NC = [i+1 for i, x in enumerate(chromesome.b) if x == 0]
    return NC

def get_CN(chromesome):
    CN = [i+1 for i, x in enumerate(chromesome.b) if x == 1]
    return CN

def membership_7(G,f,CN,NC,i,j):
    u_ij = 1/(sum(nx.resistance_distance(G,NC[i],CN[j])**(2/(f-1))/nx.resistance_distance(G,NC[i],CN[l]) for l in range(len(CN))))
    # u = 1/(sum(DK_distance(G,NC[i],CN[j])**2/DK_distance(G,NC[i],CN[l]) for l in range(len(CN))))
    return u_ij


def generate_cover(chromesome,CN,NC):

    binary_membership_matrix = chromesome.membership_metrix 
    for i in range(len(binary_membership_matrix)):
        for j in range(len(binary_membership_matrix[0])):
            chromesome.cover[CN[j]-1] = CN[j]
            if binary_membership_matrix[i][j] == 1:
                chromesome.cover[NC[i]-1] = CN[j]
    return chromesome
    


def factor_individual(graph,chromesome,f=2):

    CN = get_CN(chromesome)
    NC = get_NC(chromesome)
    #initialize membership matrix with filled 0s
    u = np.full(shape=(len(NC),len(CN)),dtype=float,fill_value=0)
    #calculate each NC node membership
    for i in range(len(NC)):
        for j in range(len(CN)):
            u[i][j] = membership_7(graph,2,CN,NC,i, j) 
    # print(u)
    binary_membership_matrix = np.zeros_like(u,dtype=int)

    #set the max number of the row as 1
    binary_membership_matrix[np.arange(len(u)),u.argmax(1)]=1
    chromesome.membership_metrix = binary_membership_matrix

    # for i in range(len(binary_membership_matrix)):
    #     for j in range(len(binary_membership_matrix[0])):
    #         chromesome.cover[CN[j]-1] = CN[j]
    #         if binary_membership_matrix[i][j] == 1:
    #             chromesome.cover[NC[i]-1] = CN[j]
    chromesome = generate_cover(chromesome,CN,NC)
    
    chromesome.KKM, chromesome.RC = Cal_KKM_RC(graph,chromesome)

    return chromesome


