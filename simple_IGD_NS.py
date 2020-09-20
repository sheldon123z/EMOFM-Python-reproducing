
#%%
import math
import random
'''
as stated in the paper
'''
def distance(A,B):
    return math.sqrt((A[0] - B[0])**2 + (A[1]-B[1])**2)

def non_contributing_set(P,PR):
    contributing_set = set()
    all_set = set(P)
    match =[]
    for r in PR:
        mini = math.inf
        z = None
        for p in P:
            d = distance(p,r)
            if d < mini:
                mini = d
                z = p
        contributing_set.add(z)
        match.append((r,z))
    non_contributing_set = all_set - contributing_set
    print(non_contributing_set)
    print()
    print(match)
    return non_contributing_set

def IGD_NS(P, PR):
    non_contributing = non_contributing_set(P,PR)
    sum1 = 0
    for x in PR:
        mini = math.inf
        for y in P:
            d = distance(x,y)
            if d < mini:
                mini = d
        sum1 += mini

    sum2 = 0
    for y in non_contributing:
        mini = math.inf
        for x in PR:
            d = distance(x,y)
            if d < mini:
                mini = d
        sum2 += mini

    return sum1+sum2     
    
# def fitness(p,P,PR):
#     p_set = set(P)
#     new_pop = p_set.remove(P)
#     return IGD_NS(new_pop,PR)


# def mating(P,PR):
#     mini = math.inf
#     n_P = P
#     for i in range(2):
#         for k in n_P:
#             if mini > k[i]:
#                 mini = k[i]
#         for k in n_P:
#             k[i] = k[i] - mini
#     P_prime = []
#     for i in range(len(n_P)):
#         p = random.choice(n_P)
#         q = random.choice(P)
#         if fitness(p,n_P,PR)>fitness(q,n_P,PR):
#             P_prime.append(p)
#         else:
#             P_prime.append(q)
#     return P_prime
    



P=[(0,17),(8,10),(9,5),(16,1),(22,0)]
PR = [(0,10),(8,5),(16,0)]



non_cont = non_contributing_set(P,PR)
i = IGD_NS(P,PR)
print(i)
# P_prime = mating(P,PR)
# print(P_prime)
# %%
