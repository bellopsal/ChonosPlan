## We will define here the FU
## each FU will have
#       type
#       Stack of Shift Stations
#       BRT of the SS -> 0 if SS empty / 1 cc
from FU import BRT, shiftStations

n = 10  # numero pila


class FU:
    def __init__(self, name, fu_type, ss_size, latency, QSD_size, n_cycles):
        self.name = name
        self.type = fu_type
        self.QSD_size = QSD_size
        self.ss_size = ss_size
        self.SS = shiftStations.SS(ss_size)
        self.BRT = BRT.BRT(n_cycles)
        self.latency = latency
        self.QSD = shiftStations.QSD(QSD_size)
        self.operationQueue = [None] * latency
        # self.operationQueue = [1, 2, 3]

        # Registers that are going to be used for the operation next
        self.ss_side = shiftStations.ShiftStation()
        self.QSD_side = shiftStations.QSDElement()

    def operation(self):
        operand1 = self.ss_side.value
        operand2 = self.QSD_side.value

        if str(self.ss_side.type_operation).startswith("mul"):
            self.operationQueue[0] = operand1 * operand2


    def calculateN(self, inst, registers):
        if inst.function.endswith("i"):
            l = registers.rp_calculation_type1_inm(inst.r2, inst.r1)
        else:
            l = registers.rp_calculation_type1(inst.r2, inst.r3, inst.r1)
        n = self.BRT.find_first_after(l[0])

        return n

    def new_instruction(self, inst, instIndex, registers, hs, b_hs, chronogram, actual_cycle):

        if inst.function.endswith("i"):
            registersCalculation = registers.rp_calculation_type1_inm(source1=inst.r2, destination=inst.r1)

        else:
            registersCalculation = registers.rp_calculation_type1(inst.r2, inst.r3, inst.r1)

        if len(registersCalculation) == 1:
            return 0, 8
        else:

            ts_max = registersCalculation[0]
            ts_min = registersCalculation[1]
            reg_max = registersCalculation[2]
            reg_min = registersCalculation[3]
            FU1 = registersCalculation[4]
            FU2 = registersCalculation[5]
            inv = registersCalculation[6]

            rp = ts_max + self.latency
            n = self.BRT.find_first_after(ts_max)

            res = 1
            rp = rp + n
            position = ts_max + n



            if n == -1:
                # this case will never happen here, this method will not enter in this case
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
                        RP1 = ts_min
                        value1 = None
                        value2 = None
                        case_QSD = False
                        bitMux = 6

                        if ts_max != position: # alternativamente n != 0
                            case_QSD = True
                            bitMux = 7
                        if ts_min == -1:
                            value1 = inst.inm
                            RP1 = -1
                        if ts_min == 0:
                            value1 = registers.Registers[reg_min].value
                            RP1 = -1
                        if ts_max == 0:
                            value2 = registers.Registers[reg_max].value
                            RP1 = -1
                        hs.update(i = freeHS, RP1=RP1, RP2 = ts_max, position = position, value1 = value1,
                                  destination = self.name,value2 = value2, inv = inv, bitMux = bitMux, FU1= FU1,
                                  FU2 = FU2, case_QSD = case_QSD, type_operation=inst.function)

                        registers.new_inst(destination=inst.r1, rp=rp, fu_name=self.name)
                        self.BRT.occupy_i(position)

                else:
                    res = 0




            else:
                if ts_max == 0:
                    value_QSD = registers.Registers[reg_max].value
                    self.update_QSD(position=position, value=value_QSD)
                    if n == 0: bitMux = 0
                    else: bitMux = 1

                if ts_max > 0:
                    if n == 0 : bitMux = 2
                    else:
                        bitMux = 3
                        self.update_QSD(position=position, RP=ts_max, FU=FU2)
                if ts_min == -1:
                    value = inst.inm
                    RP = -1
                if ts_min == 0:
                    value = registers.Registers[reg_min].value
                    RP = -1
                if ts_min > 0:
                    value = None
                    RP = ts_min

                registers.new_inst(destination=inst.r1, rp=rp, fu_name=self.name)
                self.BRT.occupy_i(position)
                self.SS.update_i(i=position, bitMux=bitMux, FU1=FU1, FU2=FU2,
                                 RP=RP, value=value, type_operation=inst.function,instruction =instIndex,  inv=inv)
        if res == 1:

            chronogram.instruction_issued(instIndex, actual_cycle= actual_cycle, ts_max=position, rp=rp)

        else:
            chronogram.instruction_issued(instIndex, actual_cycle= actual_cycle, ts_max =actual_cycle, rp= actual_cycle )


        return res, bitMux


    def update_QSD(self, position, RP=-1, FU=None, value=None):
        self.QSD.QSD[position].RP = RP
        self.QSD.QSD[position].fu = FU
        self.QSD.QSD[position].value = value


    def move_operation_queue(self):

        self.operationQueue.pop(-1)
        self.operationQueue.insert(0, None)
        cdb = self.operationQueue[-1]
        return cdb

    def strBRT(self):
        return f"BRT {self.name}: " + str(self.BRT)

    def strOperationQueue(self):
        res = ""
        for i in range(self.latency):
            res = res + f"E{i}: " + str(self.operationQueue[i]) + " -> "
        return f"{self.name}  queue: " + res + "CDB"

    def one_clock_cycle(self, CDB):
        self.ss_side, bitMux, FU2 = self.SS.one_clock_cycle(CDB)
        self.QSD_side = self.QSD.one_clock_cycle(CDB, bitMux, FU2)

        # Update the values inside each SS, BRT and QSD and moving them one down
        self.BRT.one_clock_cycle()

