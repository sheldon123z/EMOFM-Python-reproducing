#%%
import networkx as nx
import numpy as np
from numpy import linalg
from scipy.linalg import expm


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


def membership_matrix(graph,chromesome,f):

    CN = get_CN(chromesome)
    NC = get_NC(chromesome)
    #initialize membership matrix with filled 0s
    u = np.full(shape=(len(NC),len(CN)),dtype=float,fill_value=0)
    #calculate each NC node membership
    for i in range(0,len(NC),1):
        for j in range(0,len(CN),1):
            u[i][j] = membership_7(graph,2,CN,NC,i, j) 
    # print(u)
    binary_membership_matrix = np.zeros_like(u,dtype=int)
    #set the max number of the row as 1
    binary_membership_matrix[np.arange(len(u)),u.argmax(1)]=1
    
    for i in range(len(binary_membership_matrix)):
        for j in range(len(binary_membership_matrix[0])):
            chromesome.cover[CN[j]-1] = CN[j]
            if binary_membership_matrix[i][j] == 1:
                chromesome.cover[NC[i]-1] = CN[j]
                
    chromesome.membership_metrix = binary_membership_matrix
    return chromesome


