from initialization import initialize_population
import ARMOEA




def SubInitialization(chromesome,Nsub):
    pass

def delete_dominated_individuals(P):
    pass


def general_framework(Gen,R,N_pop,N_sub,graph):
    
    P = initialize_population(graph,N_pop)
    P = ARMOEA.AR_MOEA(P,R,Gen,1)
    # delete_dominated_individuals(P)
    
    # subs = []
    # for i in P:
    #     sub_i = SubInitialization(i,N_sub)
    #     sub_i = ARMOEA(sub_i,Gen,2)
    #     delete_dominated_individuals(sub_i)
    #     subs.append(sub_i)
    
    # FR = set()
    # for i in subs:
    #     for k in i:
    #         FR.add(k)
    # return FR
        
