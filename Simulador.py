import CDB
import Memory
import Program
from FU import funtionalUnit, funtionalUnitStore
import Registers


class Simulador_1_FU:

    def __init__(self, list_program, n_ss, fu_type, name, n_registers, b_scoreboard,pile_size, memory_size):
        # set of instructions
        self.program = Program.Program(list_program)
        self.memory = Memory.Memory(memory_size)

        self.fu_add = funtionalUnit.FU("add", "add", n_ss, pile_size=pile_size, latency = 2)
        self.fu_mult = funtionalUnit.FU("mult", "mult", n_ss, pile_size=pile_size, latency = 3)
        self.fu_store = funtionalUnitStore.FU("store", "store", n_ss, pile_size=pile_size, latency = 3)

        self.registers = Registers.Registers(n_registers, b_scoreboard)
        self.CDB = CDB.CDB()
        self.PC = 0
        self.b_scoreboard = b_scoreboard

    def dump_csv(self):
        self.registers.scoreboard.dump_csv()



    def one_clock_cycle(self):

        #Operation queue, Move the values one space and put it on the CBD
        #self.CDB.update(add=self.fu_add.moveOperationQueue(), store=self.fu_store.moveOperationQueue(), mult=self.fu_mult.moveOperationQueue())


        # update timestamps and get values from CBD
        #self.registers.one_clock_cycle(self.CDB)
        #self.fu_add.one_clock_cycle(self.CDB)
        #print(self.CDB)

        self.fu_add.operation(self.CDB)
        self.fu_mult.operation(self.CDB)
        self.fu_store.operation(self.CDB, self.memory)

        self.CDB.update(add=self.fu_add.moveOperationQueue(), store=self.fu_store.moveOperationQueue(), mult=self.fu_mult.moveOperationQueue())
        self.registers.one_clock_cycle(self.CDB)
        self.fu_add.one_clock_cycle(self.CDB)
        self.fu_mult.one_clock_cycle(self.CDB)
        self.fu_store.one_clock_cycle(self.CDB)
        print(self.CDB)
        res = 1


        if self.PC < self.program.n:
            # if there are still instructions in the program

            inst = self.program.get(self.PC)
            fu = self.getFU(inst.fu_type)

            res = fu.newInstruction(inst, self.registers)

        self.PC = self.PC + res

    def getFU(self, fu_type):
        if fu_type == "add":
            return self.fu_add

        if fu_type == "store":
            return self.fu_store

        if fu_type == "mult":
            return self.fu_mult






