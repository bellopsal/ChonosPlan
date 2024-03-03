import CDB
import Memory
import Program
from FU import funtionalUnit, funtionalUnitStore
import Registers

from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text

class Simulador_1_FU:

    def __init__(self, list_program, n_ss, n_registers, b_scoreboard, pile_size, memory_size,
                 n_add, n_mult, n_store, latency_add, latency_mult, latency_store, m):
        # set of instructions
        self.program = Program.Program(list_program)
        self.memory = Memory.Memory(memory_size)
        self.ss_size = n_ss
        self.pile_size = pile_size
        self.n_add = n_add
        self.n_mult = n_mult
        self.n_store = n_store
        self.m = m

        self.fus_add = []
        self.fus_mult = []
        self.fus_store = []

        for i in range(n_add):
            self.fus_add.append(funtionalUnit.FU(f"add_{i}", "add", n_ss, pile_size=pile_size, latency=latency_add))

        for i in range(n_mult):
            self.fus_mult.append(funtionalUnit.FU(f"mult_{i}", "mult", n_ss, pile_size=pile_size, latency=latency_mult))

        for i in range(n_store):
            self.fus_store.append(funtionalUnitStore.FU(f"store_{i}", "store", n_ss, pile_size=pile_size, latency=latency_store))


        self.registers = Registers.Registers(n_registers, b_scoreboard)
        self.CDB = CDB.CDB()
        self.PC = 0
        self.b_scoreboard = b_scoreboard

    def dump_csv(self):
        self.registers.scoreboard.dump_csv()



    def one_clock_cycle(self):
        #Do the operation in the FU
        for fu in self.fus_add: fu.operation()
        for fu in self.fus_mult: fu.operation()
        for fu in self.fus_store: fu.operation(self.memory)


        #Update the operation Queue
        self.CDB.update(add=self.moveOperationQueue(self.fus_add), store=self.moveOperationQueue(self.fus_store),
                        mult=self.moveOperationQueue(self.fus_mult))
        self.registers.one_clock_cycle(self.CDB)

        # One clock init cycle
        for i in range(self.n_add): self.fus_add[i].one_clock_cycle(self.CDB)
        for i in range(self.n_mult): self.fus_mult[i].one_clock_cycle(self.CDB)
        for i in range(self.n_store): self.fus_store[i].one_clock_cycle(self.CDB)


        res = 1


        if self.PC < self.program.n:
             # if there are still instructions in the program
            res = self.newInstruction()
        self.PC = self.PC + res

    def moveOperationQueue(self, fus):
        res = [fu.moveOperationQueue() for fu in fus]
        return res

    def find_first_non_negative_position(self, lst):
        for idx, num in enumerate(lst):
            if num >= 0:
                return idx
        return None  # If no non-negative value is found

    def newInstruction(self):
        inst = self.program.get(self.PC)
        fu_type = inst.fu_type
        fu_free = []
        if fu_type == "add": fu_free = [fu.calculateN(inst,self.registers) for fu in self.fus_add]
        if fu_type == "mult": fu_free = [fu.calculateN(inst, self.registers) for fu in self.fus_mult]
        if fu_type == "store": fu_free = [fu.calculateN(inst, self.registers) for fu in self.fus_store]

        index = self.find_first_non_negative_position(fu_free)

        if index is None: res = 0
        else:
            fu = self.getFU(inst.fu_type, index)
            res = fu.newInstruction(inst, self.registers)

        return res

    def getFU(self, fu_type, index):
        if fu_type == "add":
            return self.fus_add[index]

        if fu_type == "store":
            return self.fus_store[index]

        if fu_type == "mult":
            return self.fus_mult[index]


    def display_SS(self, title, fu, store = False):
        table = Table(title = title)
        table.add_column("SS", justify="center")
        table.add_column("bMux", justify="center")
        table.add_column("RP", justify="center")
        table.add_column("FU1", justify="center")
        table.add_column("FU2", justify="center")
        table.add_column("value", justify="center")
        if store: table.add_column("inm", justify="center")

        for i in range(self.ss_size-1 , -1, -1):
            ss = fu.SS.l_ss[i]

            if store:table.add_row(f"SS{i}", str(ss.bitMux), str(ss.RP), ss.FU1, ss.FU2, str(ss.value), str(ss.inm))
            else:table.add_row(f"SS{i}", str(ss.bitMux), str(ss.RP), ss.FU1, ss.FU2, str(ss.value))

        return table

    def display_pile(self, fu):
        table = Table()
        table.add_column("P", justify="center")
        table.add_column("RP", justify="center")
        table.add_column("FU", justify="center")
        table.add_column("value", justify="center")

        for i in range(self.pile_size-1 , -1, -1):
            ss = fu.pile.pile[i]
            table.add_row(f"P{i}", str(ss.RP), ss.fu, str(ss.value))
        return table


    def display_ints(self):
        if self.PC < self.program.n:
            text = Text()
            text.append("PC: ", style= "bold magenta")
            text.append(str(self.PC)+"\n", style = "bold")
            text.append("Instruction: ", style="bold magenta")
            text.append(str(self.program.get(self.PC)), style = "bold")
        else:
            text = Text()
            text.append("There are no more instrucctions!", style= "bold magenta")

        console = Console()

        console.print(text)



    def display(self):

        table_adds = Table(title="Functional Unit: ADD")
        for i in range(self.n_add):
            table_adds.add_column(self.display_SS(f"ADD_{i}", fu = self.fus_add[i]))

        table_mult = Table(title="Functional Unit: MULT")
        for i in range(self.n_mult):
            table_mult.add_column(self.display_SS(f"MULT_{i}", fu=self.fus_mult[i]))

        table_store = Table(title="Functional Unit: STORE")
        for i in range(self.n_store):
            table_store.add_column(self.display_SS(f"STORE_{i}", fu=self.fus_store[i]))

        console = Console()
        console.print(table_adds)
        console.print(table_mult)
        console.print(table_store)

        memory = Table(title= "MEMORY")
        memory.add_column("Line", justify="center")
        memory.add_column("values", justify="center")
        memory.add_column("ready", justify="center")
        l = [self.memory.memory[n:n + 8] for n in range(0, self.memory.size, 8)]
        r = [self.memory.ready[n:n + 8] for n in range(0, self.memory.size, 8)]
        for i in range(len(l)):
            memory.add_row(str(i), str(l[i]), str(r[i]))

        register = Table(title = "REGISTERS")
        register.add_column("Register", justify="center")
        register.add_column("TD", justify="center")
        register.add_column("FU", justify="center")
        register.add_column("value", justify="center")

        for reg in self.registers.R:
            register.add_row("R"+str(reg.number), "+"+str(reg.td), reg.fu, str(reg.value) )




        #console.print(memory)
        console.print(register)










