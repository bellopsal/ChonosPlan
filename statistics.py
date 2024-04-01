class Statistics:
    def __init__(self):
        self.totalLock = 0
        self.typeInst = {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8:0 }
        self.instIssued = 0
        #self.instFetch = 0
        self.cycles = 0

    def newCycle(self):
        self.cycles += 1

    def updateTypeInst(self, bitMux):
        self.typeInst[bitMux] += 1

    def increaseTotalLock(self):
        self.totalLock += 1

    def increaseInstIssued(self):
        self.instIssued += 1
