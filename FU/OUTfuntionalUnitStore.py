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
        self.SS = shiftStations.SS(ss_size)
        self.BRT = BRT.BRT(ss_size)
        self.latency = latency
        self.pile = shiftStations.Pile(pile_size)
        self.operationQueue = [None]*latency

        #self.operationQueue = [1, 2, 3]

        # Registers that are going to be used for the operation next
        self.ss_side = shiftStations.ShiftStation()
        self.pile_side = shiftStations.PileElement()

    def calculateN(self, inst, registers):
        [ts_max, _, _, _, _, _, _] = registers.td_calculation_type1(inst.r1, inst.rs1, inst.r1)
        return self.findFirstEmptyBRT(ts_max)

    def newInstruction(self, inst, registers):
        if inst.function == "sb":
            [ts_max, ts_min, reg_max, reg_min, FU1, FU2, inv] = registers.td_calculation_type1(inst.r1, inst.rs1,inst.r1)
            td = ts_max + self.latency

            if ts_min == 0:
                value = registers.R[reg_min].value
                RP = -1

            else:
                value = None
                RP = ts_min

            n = self.findFirstEmptyBRT(ts_max)

            if ts_max == 0:
                bitMux = 0
                value_pile = registers.R[reg_max].value
            else:
                if n == 0: bitMux = 2
                if n > 0: bitMux = 1

            if n > self.pile_size - 1:
                res = 0
            else:
                res = 1
                td = td + n
                ts_max_aux = ts_max
                ts_max = ts_max + n
                if ts_max_aux == 0:
                    self.updatePile_case0(position=ts_max, value=value_pile)
                if bitMux == 1:
                    self.updatePile_case1(ts_max, ts_max_aux, FU2)

                #         # actualizamos registros, fu con los valores de la nueva instrucción


                self.BRT.occupy_i(ts_max)
                self.SS.update_i(i=ts_max, bitMux=bitMux, FU1=FU1, FU2=FU2, inm = inst.inm,
                                 RP=RP, value=value, type_operation=inst.function, inv=inv)
        elif inst.function == "lb":
            [ts, FU] = registers.td_calculation_type2(inst.rs1)
            td = ts + self.latency

            n = self.findFirstEmptyBRT(ts)

            if ts == 0:
                bitMux = 0
                value_pile = registers.R[inst.rs1].value
            else:
                if n == 0: bitMux = 2
                if n > 0: bitMux = 1

            if n > self.pile_size:
                res = 0
            else:
                res = 1
                td = td + n
                ts_max_aux = ts
                ts_max = ts + n
                if ts_max_aux == 0:
                    self.updatePile_case0(position=ts_max, value=value_pile)
                if bitMux == 1:
                    self.updatePile_case1(ts_max, ts_max_aux, FU)

                registers.new_inst(destino=inst.r1, td=td, fu_name=self.name)
                self.BRT.occupy_i(ts_max)
                self.SS.update_i(i=ts_max, bitMux=bitMux,  FU2=FU, FU1= FU, RP = -1, value= None, inv = False, inm = inst.inm,
                                  type_operation=inst.function)


        return res

    def operation(self, mem):
        operand1 = self.ss_side.value  # first to arrive
        inm = self.ss_side.inm

        operand2 = self.pile_side.value  # second to arrive

        if self.ss_side.type_operation == "sb":


            if self.ss_side.inv:
                pos = operand1 + inm
                value = operand2
            else:
                pos = operand2 + inm
                value = operand1
            mem.putBuffer(pos=pos, value= value)

        if self.ss_side.type_operation == "lb":
            pos = inm + operand2
            self.operationQueue[0] = mem.get(pos)







    def moveOperationQueue(self):

        self.operationQueue.pop(-1)
        self.operationQueue.insert(0, None)
        cdb = self.operationQueue[-1]

        return cdb

    def updatePile_case1(self, position, RP, FU):
        self.pile.pile[position].RP = RP
        self.pile.pile[position].fu = FU

    def updatePile_case0(self, position, value):
        self.pile.pile[position].value = value
        self.pile.pile[position].RP = -1

    def strBRT(self):
        return f"BRT {self.name}: " + str(self.BRT)

    def strOperationQueue(self):
        res = ""
        for i in range(self.latency):
            res = res + f"E{i}: " + str(self.operationQueue[i]) + " -> "
        return f"{self.name}  queue: " + res + "CBD"

    def one_clock_cycle(self, CBD):
        self.ss_side, bitMux, FU2= self.SS.one_clock_cycle(CBD)
        self.pile_side = self.pile.one_clock_cycle(CBD, bitMux,FU2)

        # Update the values inside each SS, BRT and pile and moving them one down
        self.BRT.one_clock_cycle()


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

    def findFirstEmptyBRT(self,ts_max):
        n = self.BRT.findFirstAfter(ts_max)
        return n
