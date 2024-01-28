## We will define here the FU
## each FU will have
#       type
#       Stack of Shift Stations
#       BRT of the SS -> 0 if SS empty / 1 cc
import BRT
import shiftStations

n = 10 # numero pila


class FU:
    def __init__(self, name, fu_type, n_ss):
        self.name = name
        self.type = fu_type
        self.SS = shiftStations.SS(n_ss)
        self.BRT = BRT.BRT(n_ss)
        self.pile = [(None, -1)]*n_ss

    def one_clock_cycle_ini(self):
        self.SS.one_clock_cycle()
        self.BRT.one_clock_cycle()
        self.pile.pop(0)
        self.pile.append((None, -1))

    def calculate(self, CDB, registers,ss_0, pile):
        if ss_0.bitInUse == 1:
            if ss_0.bitMux == 0:
                return ss_0.value + registers.get_value(int(ss_0.FU2))
            elif ss_0.bitMux == 1:
                return ss_0.value + CDB
            else:
               return ss_0.value + pile



    def update(self, CDB):
        #update pile
        for i in range(len(self.pile)):
            if self.pile[i][1] == 0:
                self.pile[i] = (CDB, None)

        self.SS.update(CDB)

