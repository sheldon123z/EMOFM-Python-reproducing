
import mating_selection
from Mating_selection import contributing_set
from collections import OrderedDict
import copy
import math



def origin_distance(p,origin_y,origin_x):
    return math.sqrt((p.KKM-origin_y)**2 + (p.RC-origin_x)**2) 

def get_objective_angle(p,q,kkm_rc = True,Q = False):
    angle = 0
    if kkm_rc:
        angle = abs(math.atan2(p.KKM,p.RC) - math.atan2(q.KKM,q.RC))
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
    
    for r in range(len(R)):
        p, pr_angle = argmin(P,r,origin_y,origin_x)
        F_p = origin_distance(p,origin_y,origin_x)
        new_r = copy.deepcopy(r)
        new_r.RC = F_p * math.cos(pr_angle)*math.cos(math.atan2(r.KKM,r.RC))
        new_r.KKM = F_p * math.cos(pr_angle)*math.sin(math.atan2(r.KKM,r.RC))
        R_adapted.append(new_r)
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
                if i.KKM>j.KKM and i.RC>j.RC:
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
        distance = math.sqrt((p.KKM-q.KKM)**2 + (p.RC-q.RC)**2)

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
    z_kkm = min([i.KKM for i in P])
    z_rc = min([i.RC for i in P])
    z_nad_kkm = max([i.KKM for i in P])
    z_nad_rc = max([i.RC for i in P])

    #intersection of A and P
    AUP = list(set(n_A)|set(P))
    
    for i in AUP:
        i.KKM = i.KKM-z_kkm 
        i.RC = i.RC-z_rc

    for R_i in R:
        R_i.KKM = R_i.kkm*(z_nad_kkm-z_kkm)
        R_i.RC = R_i.RC*(z_nad_rc-z_rc) 
    '''
    operation 2 Update archive
    '''
    deleteDuplicates(n_A)
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
    R_prime = adjust_location(R_prime,P)
    


import individual




    
        



