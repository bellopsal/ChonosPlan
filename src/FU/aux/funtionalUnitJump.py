## We will define here the FU
## each FU will have
#       type
#       Stack of Shift Stations
#       BRT of the SS -> 0 if SS empty / 1 cc
from src.FU import BRT


class FU:
    def __init__(self, name, fu_type, ss_size, QSD_size, n_cycles):
        self.name = name
        self.type = fu_type
        self.QSD_size = QSD_size
        self.ss_size = ss_size
        #self.SS = shiftStations.SS(ss_size)
        self.BRT = BRT.BRT(n_cycles)
        #self.latency = latency
        #self.QSD = shiftStations.QSD(QSD_size)
        #self.operationQueue = [None] * latency
        #self.memoryQueue = [(None,None)] * latency
        # self.operationQueue = [1, 2, 3]

        # Registers that are going to be used for the operation next
        #self.ss_side = shiftStations.ShiftStation()
        #self.QSD_side = shiftStations.QSDElement()


    def calculateN(self, inst, registers):
        if inst.function == "j":
            #l = registers.rp_calculation_type2(inst.rs1, inst.r1)
            ts_max = 0

        else:
            l = registers.rp_calculation_type1(inst.r1, inst.r2, inst.r1)
            ts_max = l[0]

        n = self.findFirstEmptyBRT(ts_max)

        return n

    def newInstruction(self, inst, instIndex, registers, hs, b_hs,  chronogram, actual_cycle):
        bitMux = -1
        if inst.function == "j":
            ts_max = 0
            bitMux = 0

        else:
            registersCalculation = registers.rp_calculation_type1(inst.r1, inst.rs1, inst.r1)
            if len(registersCalculation) == 1:
                return 0, 8
            else:

                ts_max = registersCalculation[0]

        n = self.findFirstEmptyBRT(ts_max)

        res = 1

        position = ts_max + n


        if n == -1:
            # this case will never happen
            res = 0
            bitMux = 4

        elif (position > self.QSD_size - 1 and n>0) or position > self.ss_size - 1:
            # two cases: there is a need for store the data in a QSD or the time exceed the ss
            if b_hs:
                freeHS = hs.freeHS()
                if(freeHS == -1):
                    # caso de bloqueo total!!! There are no free HS
                    res = 0
                    bitMux = 5
                else:
                    res = 1
                    bitMux = 6

            else:
                res = 0
                bitMux = 4

        else:
            res = 1
            bitMux = 0


        if res == 1:

            chronogram.instruction_issued(instIndex, actual_cycle= actual_cycle, ts_max=position, rp=position+1)

        else:
            chronogram.instruction_issued(instIndex, actual_cycle= actual_cycle)

        return res, bitMux

    def findFirstEmptyBRT(self, ts_max):
        n = self.BRT.find_first_after(ts_max)
        return n


    def one_clock_cycle(self):
        # Update the values inside each SS, BRT and QSD and moving them one down
        self.BRT.one_clock_cycle()

