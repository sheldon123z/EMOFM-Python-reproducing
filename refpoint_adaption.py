
import mating_selection as MS
from collections import OrderedDict
import copy
import math



def origin_distance(p,origin_y,origin_x):
    return math.sqrt((p.KKM-origin_y)**2 + (p.RC-origin_x)**2) 

def get_objective_angle(p,q,kkm_rc = True):
    angle = 0
    if kkm_rc:
        angle = abs(math.atan2(p.KKM,p.RC) - math.atan2(q.KKM,q.RC))
    return angle
    
def argmin(P,r,z_kkm,z_rc):
    """ get the individual which in the population has the minimum acute angle with reference
        point r
        z_kkm, z_rc are two lowest points in two objective direction in the population
    """
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
        p, pr_angle = argmin(P,r,origin_y,origin_x)
        F_p = origin_distance(p,origin_y,origin_x)
        new_r = copy.deepcopy(r)
        new_r.RC = round(F_p * math.cos(pr_angle)*math.cos(math.atan2(r.KKM,r.RC)),5)
        new_r.KKM =round(F_p * math.cos(pr_angle)*math.sin(math.atan2(r.KKM,r.RC)),5)
        R_adapted.append(new_r)
    return R_adapted



def deleteDuplicates(listOfElems):
    uniqueList =set()
    new_list=[]
    for i in listOfElems:
        if (i.KKM,i.RC) not in uniqueList:
            uniqueList.add((i.KKM,i.RC))
            new_list.append(i)

    return new_list



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


def distance_between_points(p,q,kkm_rc = True):
    distance = 0
    if kkm_rc:
        distance = math.sqrt((p.KKM-q.KKM)**2 + (p.RC-q.RC)**2)

    return distance

def detect_valid_reference_points(A_con,R,kkm_rc = True):
    R_valid = []
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
                R_valid.append(valid_r)
    return R_valid

            

def ref_adapt(archive,reference,population):
    #copy A
    A = copy.deepcopy(archive)
    R = copy.deepcopy(reference)
    P = copy.deepcopy(population)
    '''
    operation 1: Translate A,P and scale R
    
    '''
    #translate A,P and scale R
    z_kkm = min([i.KKM for i in P])
    z_rc = min([i.RC for i in P])
    z_nad_kkm = max([i.KKM for i in P])
    z_nad_rc = max([i.RC for i in P])

    #intersection of A and P
    #TODO 注意这里，如果KKM和RC相同的话是否应该认为是重复的
    AUP = A
    for p in P:
        AUP.append(p)
    # AUP = list(set(A)|set(P))
    
    for i in AUP:
        i.KKM = i.KKM-z_kkm 
        i.RC = i.RC-z_rc
    #TODO 这个地方对原文有疑惑，R点会不断膨胀
    for R_i in R:
        R_i.KKM = R_i.KKM*(z_nad_kkm-z_kkm)
        R_i.RC = R_i.RC*(z_nad_rc-z_rc)
    '''
    operation 2 Update archive
    '''
    A = deleteDuplicates(A)
    dominated_solutions = dominated(A,kkm_rc=True)

    #delete duplicates 
    for d in dominated_solutions:
        if d in A:
            A.remove(d)

    R = adjust_location(R,P,z_kkm,z_rc)
    A_con = MS.contributing_set(A,R)
    A_prime = copy.deepcopy(A_con)

    #follow the algorithm
    minlen = min([len(R),len(A_prime)])
    while len(A_prime) < minlen:
        AP_left = copy.deepcopy(A)
        #先找到A_prime 和A中相同的个体
        same_set = []
        for a in A:
            for r in A_prime:
                if a.KKM == r.KKM and a.RC == r.RC:
                    same_set.append(a)
                    break
        #再移除这些个体
        for s in same_set:
            AP_left.remove(s)

        #这里如果采用下列方法的话，有可能会多删掉AP中原来就存在的,因为定义个体相同是定义其KKM 和RC 相同
        # same = (set(AP_left).intersection(set(A_prime)))
        # AP_left = list(AP_left-same)
        '''在这里，我对算法的理解是，找到所有p和q最小锐角中，度数最大的夹角的那一个的p'''
        min_angle_ps = []
        for q in A_prime:
            #对每一个q而言，先找到与其对应的最小p夹角，再在最小夹角中选最大的
            min_angle = math.inf
            min_angle_p = None
            for p in AP_left:
                angle = get_objective_angle(p,q,kkm_rc=True)
                if angle < min_angle:
                    min_angle = angle
                    min_angle_p = p
            #测量每个q对p的夹角，找到当前q最小夹角的p
            min_angle_ps.append((min_angle_p,min_angle))
        #所有的最小夹角p都集中再了min_angle_ps,选择夹角最大的一个加入A_prime
        if min_angle_ps:
            min_angle_ps.sort(key=lambda x:x[1])
            max_min_p = min_angle_ps
            A_prime.append(min_angle_ps[-1][0])

    '''
    operation 3: Adapt reference points
    '''
    R_valid = detect_valid_reference_points(A_con,R,True)
    R_prime = copy.deepcopy(R_valid)
    minlen = min([len(R),len(A_prime)])

    while len(R_prime) < minlen:
 
        #TODO AP——left中包含相近的
        AP_left = copy.deepcopy(A_prime)
        same_set = []
        for a in A_prime:
            for r in R_prime:
                if a.KKM == r.KKM and a.RC == r.RC:
                    same_set.append(a)
                    break
        for s in same_set:
            AP_left.remove(s)
        
        '''在这里，我对算法的理解是，找到所有p和q最小锐角中，度数最大的夹角的那一个的p'''
        min_angle_ps = []
        for r in R_prime:
            #对每一个q而言，先找到与其对应的最小p夹角，再在最小夹角中选最大的
            min_angle = math.inf
            min_angle_p = None
            if AP_left:
                for p in AP_left:
                    angle = get_objective_angle(p,r,kkm_rc=True)
                    if angle < min_angle:
                        min_angle = angle
                        min_angle_p = p
                min_angle_ps.append((min_angle_p,min_angle))
        if min_angle_ps:
            min_angle_ps.sort(key=lambda x:x[1])
            max_min_p = min_angle_ps
            R_prime.append(min_angle_ps[-1][0])
        

    R_prime = adjust_location(R_prime,P,z_kkm,z_rc)
    
    return A_prime, R_prime
import individual




    
        



