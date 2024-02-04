import CDB
import Memory
import Program
import funtionalUnit
import Registers


class Simulador_1_FU:

    def __init__(self, list_program, n_ss, fu_type, name, n_registers, b_scoreboard,pile_size, memory_size):
        # set of instructions
        self.program = Program.Program(list_program)
        self.memory = Memory.Memory(memory_size)

        self.fu_add = funtionalUnit.FU("add", "add", n_ss,pile_size=pile_size,latency = 2)
        self.fu_mult = funtionalUnit.FU("mult", "mult", n_ss,pile_size=pile_size,latency = 3)
        self.fu_store = funtionalUnit.FU("store", "store", n_ss,pile_size=pile_size,latency = 3)

        self.registers = Registers.Registers(n_registers, b_scoreboard)
        self.CDB = CDB.CDB()
        self.PC = 0
        self.b_scoreboard = b_scoreboard

    def dump_csv(self):
        self.registers.scoreboard.dump_csv()

    def findFirstEmptyBRT(self, fu, ts_max):
        n = fu.BRT.find_first_free_after(ts_max)
        return n

    def one_clock_cycle(self):

        #Operation queue, Move the values one space and put it on the CBD
        #self.CDB.update(add=self.fu_add.moveOperationQueue(), store=self.fu_store.moveOperationQueue(), mult=self.fu_mult.moveOperationQueue())


        # update timestamps and get values from CBD
        #self.registers.one_clock_cycle(self.CDB)
        #self.fu_add.one_clock_cycle(self.CDB)
        print(self.CDB)

        self.fu_add.operation(self.CDB)
        #self.fu_mult.operation(self.CDB)
        #self.fu_store.operation(self.CDB)

        self.CDB.update(add=self.fu_add.moveOperationQueue(), store=self.fu_store.moveOperationQueue(), mult=self.fu_mult.moveOperationQueue())
        self.registers.one_clock_cycle(self.CDB)
        self.fu_add.one_clock_cycle(self.CDB)




        if self.PC < self.program.n:
            # if there are still instructions in the program
            inst = self.program.get(self.PC)
            fu = self.getFU(inst.fu_type)

            if inst.fu_type == "add" or inst.fu_type =="mult":
                [ts_max, ts_min, reg_max, reg_min, FU1, FU2, inv] = self.registers.td_calculation(inst.r2, inst.r3)
                #print([ts_max, ts_min, reg_max, reg_min, FU1, FU2, inv])
            elif inst.fu_type == "store":
                [ts_max, ts_min, reg_max, reg_min, FU1, FU2, inv] = self.registers.td_calculation(inst.rd, inst.rs1)

            td = ts_max + fu.latency

            if ts_min == 0:
                value = self.registers.R[reg_min].value
                RP = -1

            else:
                value = None
                RP = ts_min


            n = self.findFirstEmptyBRT(fu, ts_max)

            if ts_max == 0: bitMux = 0
            else:
                if n == 0 : bitMux = 2
                if n > 0 : bitMux = 1


            td = td + n
            ts_max_aux = ts_max
            ts_max = ts_max + n
            if ts_max == 0:
                self.updatePile_case0(fu=fu, position=ts_max, value= self.registers.R[reg_max].value)
            if bitMux == 1 :
                self.updatePile_case1(fu,ts_max, ts_max_aux, FU2)


    #         # actualizamos registros, fu con los valores de la nueva instrucción

            self.registers.new_inst(destino=inst.r1, td=td, fu_name=fu.type)
            fu.BRT.occupy_i(ts_max)
            fu.SS.update_i(i=ts_max, bitMux= bitMux, FU1 = FU1, FU2 = FU2,
                                RP = RP, value = value, type_operation=inst.function, inv= inv)







    #         # operacion, por ahora solo suma
    #
    #         #self.CDB.put(self.fu.calculate(self.CDB.get(), self.registers, ss_0, pile))
    #         print(" CDB "+ str(self.CDB))
    #
    #         # actualizar valores
    #         #self.fu.update(self.CDB.get())
    #         self.registers.update(self.CDB.get())
    #         self.registers.update_scoreboard()
    #         self.pos = self.pos + 1
    #     else:
    #     # operacion, por ahora solo suma
    #         #self.CDB.put(self.fu.calculate(self.CDB.get(), self.registers, ss_0, pile))
    #
    # # actualizar valores
    #         self.fu.update(self.CDB.get())
    #         self.registers.update(self.CDB.get())
    #         self.pos = self.pos + 1
        self.PC = self.PC +1

    def getFU(self, fu_type):
        if fu_type == "add":
            return self.fu_add

        if fu_type == "store":
            return self.fu_store

        if fu_type == "mult":
            return self.fu_mult




    def updatePile_case1(self, fu, position, RP, FU):
        fu.pile.pile[position].RP = RP
        fu.pile.pile[position].fu = FU

    def updatePile_case0(selfself,fu, position, value):
        fu.pile.pile[position].value = value
        fu.pile.pile[position].RP = -1

