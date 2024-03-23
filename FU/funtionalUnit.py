## We will define here the FU
## each FU will have
#       type
#       Stack of Shift Stations
#       BRT of the SS -> 0 if SS empty / 1 cc
from FU import BRT, shiftStations

n = 10  # numero pila


class FU:
    def __init__(self, name, fu_type, ss_size, latency, pile_size, n_cycles):
        self.name = name
        self.type = fu_type
        self.pile_size = pile_size
        self.ss_size = ss_size
        self.SS = shiftStations.SS(ss_size)
        self.BRT = BRT.BRT(n_cycles, latency)
        self.latency = latency
        self.pile = shiftStations.Pile(pile_size)
        self.operationQueue = [None] * latency
        # self.operationQueue = [1, 2, 3]

        # Registers that are going to be used for the operation next
        self.ss_side = shiftStations.ShiftStation()
        self.pile_side = shiftStations.PileElement()

    def operation(self):
        operand1 = self.ss_side.value
        operand2 = self.pile_side.value

        if self.ss_side.type_operation == "add":
            self.operationQueue[0] = operand1 + operand2

        if self.ss_side.type_operation == "sub":
            if self.ss_side.inv:
                self.operationQueue[0] = operand2 - operand1
            else:
                self.operationQueue[0] = operand1 - operand2

        if self.ss_side.type_operation == "mul":
            self.operationQueue[0] = operand1 * operand2

        if self.ss_side.type_operation == "div":
            if self.ss_side.inv:
                self.operationQueue[0] = operand2 / operand1
            else:
                self.operationQueue[0] = operand1 / operand2

    def calculateN(self, inst, registers):

        l = registers.td_calculation_type1(inst.r2, inst.r3, inst.r1)
        n = self.findFirstEmptyBRT(l[0])

        return n

    def newInstruction(self, inst,instIndex , registers, hs, b_hs):
        registersCalculation = registers.td_calculation_type1(inst.r2, inst.r3, inst.r1)

        if len(registersCalculation) == 1:
            return 0
        else:

            ts_max = registersCalculation[0]
            ts_min = registersCalculation[1]
            reg_max = registersCalculation[2]
            reg_min = registersCalculation[3]
            FU1 = registersCalculation[4]
            FU2 = registersCalculation[5]
            inv = registersCalculation[6]

            td = ts_max + self.latency
            n = self.findFirstEmptyBRT(ts_max)

            res = 1
            td = td + n
            position = ts_max + n

            print(position)


            if n == -1:
                # this case will never happen
                res = 0
                bitMux = 4

            elif (position > self.pile_size - 1 and n>0) or position > self.ss_size - 1:
                # two cases: there is a need for store the data in a pile or the time exceed the ss
                if b_hs:
                    freeHS = hs.freeHS()
                    if(freeHS == -1):
                        # caso de bloqueo total!!! There are no free HS
                        res = 0
                        bitMux = 4
                    else:

                        value1 = None
                        value2 = None
                        casePile = False
                        bitMux = 5

                        if ts_max != position: # alternativamente n == 0
                            casePile = True
                            bitMux = 6

                        if ts_min == 0:
                            value1 = registers.R[reg_min].value
                            RP1 = -1
                        if ts_max == 0:
                            value2 = registers.R[reg_max].value
                            RP1 = -1
                        hs.update(i = freeHS, RP1=ts_min, RP2 = ts_max, position = position, value1 = value1, destination = self.name,
                                  value2 = value2, inv = inv, bitMux = bitMux, FU1= FU1, FU2 = FU2, casePile = casePile, type_operation=inst.function)

                        registers.new_inst(destino=inst.r1, td=td, fu_name=self.name)
                        self.BRT.occupy_i(position)

                else:
                    res = 0




            else:
                if ts_max == 0:
                    value_pile = registers.R[reg_max].value
                    self.updatePile(position=position, value=value_pile)
                    if n == 0: bitMux = 0
                    else: bitMux = 1

                if ts_max > 0:
                    if n == 0 : bitMux = 2
                    else:
                        bitMux = 3
                        self.updatePile(position=position, RP=ts_max, FU=FU2)
                if ts_min == 0:
                    value = registers.R[reg_min].value
                    RP = -1
                if ts_min > 0:
                    value = None
                    RP = ts_min

                registers.new_inst(destino=inst.r1, td=td, fu_name=self.name)
                self.BRT.occupy_i(position)
                self.SS.update_i(i=position, bitMux=bitMux, FU1=FU1, FU2=FU2,
                                 RP=RP, value=value, type_operation=inst.function,instruction =instIndex,  inv=inv)

            return res

    def findFirstEmptyBRT(self, ts_max):
        n = self.BRT.findFirstAfter(ts_max)
        return n

    def updatePile(self, position, RP=-1, FU=None, value=None):
        self.pile.pile[position].RP = RP
        self.pile.pile[position].fu = FU
        self.pile.pile[position].value = value

    def updatePile_case0(self, position, value):
        self.pile.pile[position].value = value
        self.pile.pile[position].RP = -1

    def moveOperationQueue(self):

        self.operationQueue.pop(-1)
        self.operationQueue.insert(0, None)
        cbd = self.operationQueue[-1]
        return cbd

    def strBRT(self):
        return f"BRT {self.name}: " + str(self.BRT)

    def strOperationQueue(self):
        res = ""
        for i in range(self.latency):
            res = res + f"E{i}: " + str(self.operationQueue[i]) + " -> "
        return f"{self.name}  queue: " + res + "CBD"

    def one_clock_cycle(self, CBD):
        self.ss_side, bitMux, FU2 = self.SS.one_clock_cycle(CBD)
        self.pile_side = self.pile.one_clock_cycle(CBD, bitMux, FU2)

        # Update the values inside each SS, BRT and pile and moving them one down
        self.BRT.one_clock_cycle()

