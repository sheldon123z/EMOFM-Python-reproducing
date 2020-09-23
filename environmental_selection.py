import nondominated_sort as ns
from mating_selection import IGD_NS

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
    for i in range(k-1):
        for p in Fronts[i]:
            Q.append(p)
    
    while len(Fronts[k]) > N - len(Q):
        p=0
        while p < len(Fronts[k]):
            Fronts[k].remove(p)
            p = IGD_NS(Fronts[k],R_prime)
            p+=1
            
    for p in Fronts[k]:
        Q.append(p)
    return Q
     
        
