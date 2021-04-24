#%%实现membership功能
import networkx as nx
import numpy as np
import copy
import itertools
from scipy.linalg import expm

def decode_cover_to_lists(community_labels):
    '''
    解码社团划分的结构
    example:
    input: community_labels =[12, 2, 4, 4, 5, 12, 7, 4, 9, 9, 2, 12]
    output [[0, 5, 11], [1, 10], [2, 3, 7], [4], [6], [8, 9]]
    '''
    appeared = set()
    cover = []
    for i in community_labels:
        if i not in appeared:
            temp = []
            appeared.add(i)
            for j,k in enumerate(community_labels):
                if k == i:
                    temp.append(j)
            cover.append(temp)
    return cover

def Cal_KKM_RC(graph,chromesome):
    '''
    计算个体的KKM和RC
    '''
    community_labels = chromesome.cover
    k = len(set(community_labels))
    n = len(community_labels)
    cover = decode_cover_to_lists(community_labels)

    adjacent_matrix = nx.convert_matrix.to_numpy_array(graph)

    L = 0.0
    for C_i in cover:
        node_combs = itertools.combinations(C_i,2)
        inside_sum = 0.0
        for v,w in node_combs:
            inside_sum += adjacent_matrix[v-1][w-1] #由于node的编码是从1开始的，所以再矩阵中要减去1找到index
        L += inside_sum/len(C_i)

    KKM = 2*float((n-k)) - L

    RC = 0.0
    nodes = list(range(1,n+1))
    for C_i in cover:
        temp = 0
        omega = cover.copy()
        omega.remove(C_i)
        diff = list(itertools.chain.from_iterable(omega))
        for v in C_i:
            for w in diff:
                temp += adjacent_matrix[v-1][w-1]
        RC += temp /len(C_i)   

    return round(KKM,5),round(RC,5)


def DK_distance(G,i,j,beta=1):
    '''
    计算DK 距离
    '''
    L = nx.linalg.laplacian_matrix(G).todense()
    K = expm(-beta*L)
    DK = np.max(K)-K
    DK = np.asarray(DK)
    return DK[j-1][i-1]

def get_NC(chromesome):
    '''
    得到非中心节点的list
    '''
    NC = [i+1 for i, x in enumerate(chromesome.b) if x == 0]
    return NC

def get_CN(chromesome):
    '''
    得到中心节点list
    '''
    CN = [i+1 for i, x in enumerate(chromesome.b) if x == 1]
    return CN

def membership_7(G,f,CN,NC,i,j):
    '''
    根据公式7计算节点的membership coefficient
    '''
    u_ij = 1/(sum(nx.resistance_distance(G,NC[i],CN[j])**(2/(f-1))/nx.resistance_distance(G,NC[i],CN[l]) for l in range(len(CN))))
    # u = 1/(sum(DK_distance(G,NC[i],CN[j])**2/DK_distance(G,NC[i],CN[l]) for l in range(len(CN))))
    return u_ij


def generate_cover(chromesome,CN,NC):
    '''
    根据中心节点和非中心节点生成个体的cover
    '''
    binary_membership_matrix = chromesome.membership_metrix 
    for i in range(len(binary_membership_matrix)):
        for j in range(len(binary_membership_matrix[0])):
            chromesome.cover[CN[j]-1] = CN[j]
            if binary_membership_matrix[i][j] == 1:
                chromesome.cover[NC[i]-1] = CN[j]
    return chromesome
    


def factor_individual(graph,chromesome,f=2):
    '''
    设置一个个体的各项参数
    '''
    CN = get_CN(chromesome)
    NC = get_NC(chromesome)
    #initialize membership matrix with filled 0s
    u = np.full(shape=(len(NC),len(CN)),dtype=float,fill_value=0)
    #calculate each NC node membership
    for i in range(len(NC)):
        for j in range(len(CN)):
            u[i][j] = membership_7(graph,2,CN,NC,i, j) 
    binary_membership_matrix = np.zeros_like(u,dtype=int)
    #set the max number of the row as 1
    binary_membership_matrix[np.arange(len(u)),u.argmax(1)]=1
    chromesome.membership_metrix = binary_membership_matrix

    chromesome = generate_cover(chromesome,CN,NC)
    
    chromesome.KKM, chromesome.RC = Cal_KKM_RC(graph,chromesome)

    return chromesome


