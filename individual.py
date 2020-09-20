class chromesome():

    def __init__(self,N):
        self.b = [0]*N
        self.r = [0]*N
        self.cover = list(range(1,N+1))
        self.membership_metrix=None
        self.KKM = 0
        self.RC = 0
        self.fitness = None
