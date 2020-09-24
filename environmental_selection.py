import nondominated_sort as ns
from mating_selection import IGD_NS
import copy
import math
import membership
def environmental_selection(G,P,R_prime,N):
    
    minKKM = min([p.KKM for p in P])
    minRC = min([p.RC for p in P])
    for p in P:
        p.KKM = p.KKM - minKKM
        p.RC = p.RC - minRC
    
    Fronts = ns.produce_fronts(G,P)
    k = 0 # the layer's index number 
    n = 0 # the union set length
    #select the minimum layers
    for i,f in enumerate(Fronts):
        n += len(f)
        if n >= N:
            k = i
            break
    
    Q = []
    if k == 0:
        while len(Fronts[0]) > N:
            min_igd = math.inf
            p_delete = 0
            for index,p in enumerate(Fronts[0]):
                temp =copy.deepcopy(Fronts[0])
                temp.remove(p)
                i = IGD_NS(temp,R_prime)
                if min_igd > i:
                    min_igd = i
                    p_delete = index
            Fronts[0].pop(index)

    else:
        for i in range(k):
            for p in Fronts[i]:
                Q.append(p)
        print('length Q {}, k {}'.format(len(Q),k))
        while len(Fronts[k]) > N - len(Q):
            min_igd = math.inf
            p_delete = 0
            for index,p in enumerate(Fronts[k]):
                temp =copy.deepcopy(Fronts[k])
                temp.remove(p)
                i = IGD_NS(temp,R_prime)
                if min_igd > i:
                    min_igd = i
                    p_delete = index
            Fronts[k].pop(index)


    for p in Fronts[k]:
        p.KKM += minKKM
        p.RC += minRC
        Q.append(p)
    return Q
     
        
