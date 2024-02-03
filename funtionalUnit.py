## We will define here the FU
## each FU will have
#       type
#       Stack of Shift Stations
#       BRT of the SS -> 0 if SS empty / 1 cc
from FU import BRT, shiftStations

n = 10  # numero pila


class FU:
    def __init__(self, name, fu_type, ss_size, latency, pile_size):
        self.name = name
        self.type = fu_type
        self.SS = shiftStations.SS(ss_size)
        self.BRT = BRT.BRT(ss_size)
        self.latency = latency
        self.pile = shiftStations.Pile(pile_size)
        self.operationQueue = [None]*latency
        #self.operationQueue = [1, 2, 3]

        # Registers that are going to be used for the operation next
        self.ss_side = None
        self.pile_side = None

    def moveOperationQueue(self):
        cbd = self.operationQueue[-1]
        self.operationQueue.pop(-1)
        self.operationQueue.insert(0, None)

        return cbd

    def strBRT(self):
        return f"BRT {self.name}: " + str(self.BRT)

    def strOperationQueue(self):
        res = ""
        for i in range(self.latency):
            res = res + f"E{i}: " + str(self.operationQueue[i]) + " -> "
        return f"Operation queue: " + res + "CBD"

    def one_clock_cycle_ini(self):
        # Get the registers that will be used for the operation
        self.ss_side = self.SS.get(0)
        # self.pile_side = self.pile.get(0)

        # Update the values inside each SS, BRT and pile and moving them one down
        self.SS.one_clock_cycle()
        self.BRT.one_clock_cycle()
        self.pile.one_clock_cycle()

    def calculate(self, CDB, registers):
        if self.ss_side.bitInUse == 1:
            if self.ss_side.bitMux == 0:
                return self.ss_side.value + registers.get_value(int(self.ss_side.FU2))
            elif self.ss_side.bitMux == 1:
                return self.ss_side.value + CDB
            else:
                return self.ss_side.value + self.pile_side

    def update(self, CDB):
        # update pile
        for i in range(len(self.pile)):
            if self.pile[i][1] == 0:
                self.pile[i] = (CDB, None)

        self.SS.update(CDB)
