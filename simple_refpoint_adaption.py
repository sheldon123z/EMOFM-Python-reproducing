#%%
import mating_selection
# from mating_selection import contributing_set
from collections import OrderedDict
import copy
import math

def distance_KKM_RC(A,B):
    return math.sqrt((A[1] - B[1])**2 + (A[0]-B[0])**2)

def contributing_set(P,PR):
    contributing_set = set()
    all_set = set(P)
    # match =[]
    for r in PR:
        mini = math.inf
        z = None
        for p in P:
            d = distance_KKM_RC(p,r)
            if d < mini:
                mini = d
                z = p
        contributing_set.add(z)
        # match.append((r,z))
    return contributing_set

def origin_distance(p,origin_y,origin_x):
    return math.sqrt((p[1]-origin_y)**2 + (p[0]-origin_x)**2) 

def get_objective_angle(p,q,kkm_rc = True,Q = False):
    angle = 0
    if kkm_rc:
        angle = abs(math.atan2(p[1],p[0]) - math.atan2(q[1],q[0]))
    return angle
    
def argmin(P,r,z_kkm,z_rc):
    mini = math.inf
    mini_p = None
    for p in P:
        angle = get_objective_angle(r,p,kkm_rc=True)
        F_psin = origin_distance(p,z_kkm,z_rc)*math.sin(angle)
        if F_psin < mini:
            mini_p = p
            mini = angle
    return mini_p,mini

def adjust_location(R,P,origin_y,origin_x,kkm_rc = True):
    '''
    adjust reference points location
    z_kkm,z_rc: the ideal point of kkm and rc in objective space
    '''
    R_adapted = []
    
    for r in R:
        r = list(r)
        p, pr_angle = argmin(P,r,origin_y,origin_x)
        F_p = origin_distance(p,origin_y,origin_x)
        new_r = copy.deepcopy(r)
        new_r[0] = F_p * math.cos(pr_angle)*math.cos(math.atan2(r[1],r[0]))
        new_r[1] = F_p * math.cos(pr_angle)*math.sin(math.atan2(r[1],r[0]))
        R_adapted.append(tuple(new_r))
    return R_adapted



def deleteDuplicates(listOfElems):
    uniqueList =[]
    for i in listOfElems:
        if i not in uniqueList:
            uniqueList.append(i)

    return uniqueList



def dominated(listOfElems,kkm_rc=False):
    A = copy.deepcopy(listOfElems)
    dominated = []
    if kkm_rc:
        for i in A:
            for j in A:
                if i == j:
                    continue
                if i[1]>j[1] and i[0]>j[0]:
                    dominated.append(i)
                    break
    return dominated

def object_list_intersection(A,B,kkm_rc=False,Q=False):
    result =[]
    if kkm_rc:
        result = list(set(A).intersection(B))

    return result

def distance_between_points(p,q,kkm_rc = True):
    distance = 0
    if kkm_rc:
        distance = math.sqrt((p[1]-q[1])**2 + (p[0]-q[0])**2)

    return distance

def detect_valid_reference_points(A_con,R,kkm_rc = True):
    R_valid = set()
    #对于所有的p来说，找到其最短距离的r，这个r就是valid r，需要加入到valid set中
    #但也有可能不存在，所以要避免不存在往里加None的情形
    if kkm_rc:
        for p in A_con:
            min_distance = math.inf
            valid_r = None
            for r in R:
                d = distance_between_points(p,r)
                if d < min_distance:
                    min_distance = d
                    valid_r = r
            if valid_r:
                R_valid.add(valid_r)
    return list(R_valid)

            

def ref_adapt(A,R,P):
    #copy A
    n_A = copy.deepcopy(A)
    '''
    operation 1: Translate A,P and scale R
    
    '''
    #translate A,P and scale R
    z_kkm = min([i[1] for i in P])
    z_rc = min([i[0] for i in P])
    z_nad_kkm = max([i[1] for i in P])
    z_nad_rc = max([i[0] for i in P])

    #intersection of A and P
    AUP = list(set(n_A)|set(P))
    n_AUP = []
    for t in AUP:
        i = list(t)
        i[1] = i[1]-z_kkm 
        i[0] = i[0]-z_rc
        t = tuple(i)
        n_AUP.append(t)
    AUP = n_AUP
    n_R=[]
    for r in R:
        R_i = list(r)
        R_i[1] = R_i[1]*(z_nad_kkm-z_kkm)
        R_i[0] = R_i[0]*(z_nad_rc-z_rc) 
        r = tuple(R_i)
        n_R.append(r)
    R = n_R
    '''
    operation 2 Update archive
    '''
    n_A = deleteDuplicates(n_A)
    dominated_solutions = dominated(n_A,kkm_rc=True)

    #delete duplicates 
    for d in dominated_solutions:
        if d in n_A:
            n_A.remove(d)

    R = adjust_location(R,P,z_kkm,z_rc)
    A_con = contributing_set(n_A,R)
    A_prime = copy.deepcopy(A_con)

    #follow the algorithm
    minlen = min([len(R),len(A_prime)])
    while len(A_prime) < minlen:
        A_left = object_list_intersection(A,A_prime)
        '''在这里，我对算法的理解是，找到所有p和q最小夹角中，度数最大的夹角的那一个的p'''
        max_angle = -math.inf
        max_angle_p = None
        for p in A_left:
            #对每一个p而言，先找到与其对应的最小q夹角，再在最小夹角中选最大的
            for q in A_prime:
                angle = get_objective_angle(p,q,kkm_rc=True)
                if angle > max_angle:
                    max_angle = angle
                    max_angle_p = p
        if max_angle_p:
            A_prime.append(max_angle_p)

    '''
    operation 3: Adapt reference points
    '''
    R_valid = detect_valid_reference_points(A_con,R,True)
    R_prime = copy.deepcopy(R_valid)
    minlen = min([len(R),len(A_prime)])

    while len(R_prime) < minlen:
        AR_left = object_list_intersection(A_prime,R_prime)
        max_angle = -math.inf
        max_angle_p = None
        for p in AR_left:
            #对每一个p而言，先找到与其对应的最小q夹角，再在最小夹角中选最大的
            for q in R_prime:
                angle = get_objective_angle(p,q,kkm_rc=True)
                if angle > max_angle:
                    max_angle = angle
                    max_angle_p = p
        if max_angle_p:
           R_prime.append(max_angle_p)
    R_prime = adjust_location(R_prime,P,z_kkm,z_rc)

    return A_prime, R_prime

P=[(0,17),(8,10),(9,5),(16,1),(22,0),(33,18),(24,23),(29,31),(11,17),(15,8)]
R = [(0,10),(8,5),(16,0)]
A = [(0,17),(8,10),(9,5),(16,1),(22,0)]

A_prime, R_prime = ref_adapt(A,R,P)

import matplotlib.pyplot as plt

KKM = [i[1] for i in R_prime]
RC = [i[0] for i in R_prime]

AP_KKM = [i[1] for i in A_prime]
AP_RC = [i[0] for i in A_prime]

A_KKM = [i[1] for i in A]
A_RC = [i[0] for i in A]

# plt.scatter(RC,KKM,marker='+'),
plt.scatter(A_RC,A_KKM,marker='o')
plt.scatter(AP_RC,AP_KKM,marker='^')
plt.xlabel = 'RC'
plt.ylabel = 'KKM'
plt.title = 'Objective Space'
plt.show()
print('A_prime is {}, R_prime is {}'.format(A_prime, R_prime))




    
        




# %%
