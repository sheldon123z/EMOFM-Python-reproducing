#%%
import networkx as nx
import numpy as np
from numpy import linalg
from scipy.linalg import expm




# graph.add_edges_from([(1,2),(1,3),(2,3),(2,4)])
# lp = nx.linalg.laplacian_matrix(graph)
#heat distance
def DK_distance(G,i,j,beta=1):
    L = nx.linalg.laplacian_matrix(G).todense()
    K = expm(-beta*L)
    DK = np.max(K)-K
    DK = np.asarray(DK)
    return DK[j-1][i-1]

def get_CN(chrosome):
    return [i for i, x in enumerate(chrosome[0]) if x ==1]

def get_NC(chrosome):
    return [i for i, x in enumerate(chrosome[0]) if x == 0]



def membership_7(G,f,NC,CN,i,j):
    u_ij = 1/(sum(nx.resistance_distance(G,NC[i],CN[j])**(2/(f-1))/nx.resistance_distance(G,NC[i],CN[l]) for l in range(len(CN))))
    # u = 1/(sum(DK_distance(G,NC[i],CN[j])**2/DK_distance(G,NC[i],CN[l]) for l in range(len(CN))))
    return u_ij


def membership_matrix(graph,CN, NC):
    #initialize membership matrix with filled 0s
    u = np.full(shape=(len(NC),len(CN)),dtype=float,fill_value=0)
    #calculate each NC node membership
    for i in range(len(NC)):
        for j in range(len(CN)):
            u[i][j] = membership_7(graph,2,NC,CN, i, j) 

    out = np.zeros_like(u)
    out[np.arange(len(u)),u.argmax(1)]=1

    for i in range(len(NC)):
        for j in range(len(CN)):
            graph.nodes[CN[j]]['community'] = CN[j]
            if out[i][j] == 1:
                graph.nodes[NC[i]]['community'] = CN[j]
            

    print('memebrship matrix is:',u)
    print()
    # print(np.amax(u,axis=1))


    return out





if __name__ == "__main__":
    
    graph = nx.Graph()
    graph.add_edges_from([(6,7),(6,1),(6,12),(7,12),(7,1),(1,12),(12,11),(12,2),(2,11),(9,2),(9,10),(9,3),(2,10),(10,3),(3,4),(3,8),(3,5),(4,5),(4,8),(5,8)])
    CN = [6,8,10]
    NC = [1,2,3,4,5,7,9,11,12]

    out  = membership_matrix(graph,CN,NC)
    print('Binary membership matrix:')
    print(out)
    print()

    print('nodes data:',graph.nodes.data())


# print(graph.nodes.data())
# nx.draw(graph)
# %%