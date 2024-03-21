import CDB
import Memory
import Pointer
import Program
from FU import funtionalUnit, funtionalUnitStore, holdStations
import Registers


from rich.console import Console, OverflowMethod, Group
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text

class Simulador_1_FU:

    def __init__(self, list_program, n_ss, n_registers, b_scoreboard, pile_size, memory_size,
                 n_add, n_mult, n_store, latency_add, latency_mult, latency_store, m, n_hs = 10, b_hs = False, n_cycles= 120):
        # set of instructions
        self.program = Program.Program(list_program)
        self.memory = Memory.Memory(memory_size)
        self.ss_size = n_ss
        self.pile_size = pile_size
        self.n_add = n_add
        self.n_mult = n_mult
        self.n_store = n_store
        self.PC = Pointer.PC(m, self.program.n)
        self.n_cycles = n_cycles

        self.fus_add = []
        self.fus_mult = []
        self.fus_store = []

        self.b_hs = b_hs
        if b_hs:
            self.hs = holdStations.HS(n_hs)






        self.add_selecionOrder = list(range(n_add))
        self.mult_selecionOrder = list(range(n_mult))
        self.store_selecionOrder = list(range(n_store))

        for i in range(n_add):
            self.fus_add.append(funtionalUnit.FU(f"add_{i}", "add", n_ss, pile_size=pile_size, latency=latency_add, n_cycles=n_cycles))

        for i in range(n_mult):
            self.fus_mult.append(funtionalUnit.FU(f"mult_{i}", "mult", n_ss, pile_size=pile_size, latency=latency_mult,n_cycles=n_cycles))

        for i in range(n_store):
            self.fus_store.append(funtionalUnitStore.FU(f"store_{i}", "store", n_ss, pile_size=pile_size, latency=latency_store, n_cycles=n_cycles))


        self.registers = Registers.Registers(n_registers, b_scoreboard)
        self.CDB = CDB.CDB()
        self.b_scoreboard = b_scoreboard

    def dump_csv(self):
        self.registers.scoreboard.dump_csv()



    def one_clock_cycle(self):
        #Pointer
        self.PC.one_clock_cycle()


        #Do the operation in the FU
        for fu in self.fus_add: fu.operation()
        for fu in self.fus_mult: fu.operation()
        for fu in self.fus_store: fu.operation(self.memory)


        #Update the operation Queue
        self.CDB.update(add=self.moveOperationQueue(self.fus_add), store=self.moveOperationQueue(self.fus_store),
                        mult=self.moveOperationQueue(self.fus_mult))

        self.registers.one_clock_cycle(self.CDB)
        print(self.registers)

        # One clock init cycle
        for i in range(self.n_add): self.fus_add[i].one_clock_cycle(self.CDB)
        for i in range(self.n_mult): self.fus_mult[i].one_clock_cycle(self.CDB)
        for i in range(self.n_store): self.fus_store[i].one_clock_cycle(self.CDB)



        if len(self.PC.PC) > 0:
            for _ in range(len(self.PC.PC)):
                instIndex = self.PC.newInstruction()
                if instIndex < self.program.n:
                    inst = self.program.get(instIndex)
                     # if there are still instructions in the program
                    res = self.newInstruction(instIndex)

                    if res == 0:
                        self.PC.instBlock()
                        self.registers.instBlock([inst.r1,inst.r2, inst.r3])


    def moveOperationQueue(self, fus):
        res = [fu.moveOperationQueue() for fu in fus]
        return res

    def find_lowest_positive_index(self, l):
        lowest_positive = None
        lowest_positive_index = []

        for i, num in enumerate(l):
            if num >= 0 and (lowest_positive is None or num < lowest_positive):
                lowest_positive = num
                lowest_positive_index = [i]
            elif num >= 0 and num == lowest_positive:
                lowest_positive = num
                lowest_positive_index.append(i)

        return lowest_positive_index

    def newInstruction(self, instIndex):
        inst = self.program.get(instIndex)
        fu_type = inst.fu_type
        fu_free = []
        if fu_type == "add":
            fu_free = [fu.calculateN(inst, self.registers) for fu in self.fus_add]
            selectionOrder = self.add_selecionOrder
        if fu_type == "mult":
            fu_free = [fu.calculateN(inst, self.registers) for fu in self.fus_mult]
            selectionOrder = self.mult_selecionOrder
        if fu_type == "store":
            fu_free = [fu.calculateN(inst, self.registers) for fu in self.fus_store]
            selectionOrder = self.store_selecionOrder


        indexes = self.find_lowest_positive_index(fu_free)

        if len(indexes) == 0: res = 0
        else:
            index = self.selection(indexes, selectionOrder)
            print(index)
            fu = self.getFU(inst.fu_type, index)
            res = fu.newInstruction(inst,instIndex, self.registers)


        return res

    def selection(self, indexes, selectionOrder):
        keep = [e for e in selectionOrder if e in indexes]

        elementToMove = keep.pop(0)
        selectionOrder.remove(elementToMove)
        selectionOrder.append(elementToMove)

        return elementToMove



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
        table.add_column("instIndex", justify="center")
        if store: table.add_column("inm", justify="center")

        for i in range(self.ss_size-1 , -1, -1):
            ss = fu.SS.l_ss[i]

            if store: table.add_row(f"SS{i}", str(ss.bitMux), str(ss.RP), ss.FU1, ss.FU2, str(ss.value),str(ss.instruction),str(ss.inm))
            else: table.add_row(f"SS{i}", str(ss.bitMux), str(ss.RP), ss.FU1, ss.FU2, str(ss.value),str(ss.instruction))

        return table

    def display_HS(self):
        table = Table(title = "Hold Stations")
        table.add_column("HS", justify="center")
        table.add_column("RP1", justify="center")
        table.add_column("RP2", justify="center")
        table.add_column("FU1", justify="center")
        table.add_column("FU2", justify="center")
        table.add_column("value1", justify="center")
        table.add_column("value2", justify="center")
        table.add_column("occupied", justify="center")



        for i in range(self.hs.n):
            hs = self.hs.l_hs[i]
            table.add_row(f"HS{i}", str(hs.RP1), str(hs.RP2),
                          hs.FU1, hs.FU2, str(hs.value1), str(hs.value2),str(self.hs.occupied[i]))




        return table





    def display_pile(self, fu, title):
        table = Table(title= title)
        table.add_column("P", justify="center")
        table.add_column("RP", justify="center")
        table.add_column("FU", justify="center")
        table.add_column("value", justify="center")

        for i in range(self.pile_size-1 , -1, -1):
            ss = fu.pile.pile[i]
            table.add_row(f"P{i}", str(ss.RP), ss.fu, str(ss.value))

        return table


    def display_ints(self):
        text = Text()
        if self.PC.PC is None: text.append("Loading instructions")
        elif self.PC.m < self.program.n :
            text.append("PC: ", style= "bold magenta")
            text.append(str(self.PC)+"\n", style = "bold")
            text.append("Instruction: ", style="bold magenta")
            inst_list = [str(self.program.get(i)) for i in self.PC.PC]

            text.append(str(inst_list), style = "bold")
        else:
            text.append("There are no more instrucctions!", style= "bold magenta")

        console = Console()

        console.print(text)



    def display(self, badd = True, bmux = True, bstore = False, bmemory = False):
        self.display_ints()
        console = Console()



        if badd:
            table_adds = Table(title="Functional Unit: ADD")
            table_adds_pile = Table(title="Pile: ADD")
            for i in range(self.n_add):
                table_adds.add_column(self.display_SS(f"ADD_{i}", fu = self.fus_add[i]))
                table_adds_pile.add_column(self.display_pile(fu=self.fus_add[i]))
            console.print(table_adds, overflow = "fold")
            console.print(table_adds_pile, overflow = "fold")

        if bmux:
            table_mult = Table(title="Functional Unit: MULT")
            for i in range(self.n_mult):
                table_mult.add_column(self.display_SS(f"MULT_{i}", fu=self.fus_mult[i]))

            console.print(table_mult, overflow = "fold")

        if bstore:
            table_store = Table(title="Functional Unit: STORE")
            for i in range(self.n_store):
                table_store.add_column(self.display_SS(f"STORE_{i}", fu=self.fus_store[i]))
            console.print(table_store, overflow = "fold")





        if bmemory:
            memory = Table(title= "MEMORY")
            memory.add_column("Line", justify="center")
            memory.add_column("values", justify="center")
            memory.add_column("ready", justify="center")
            l = [self.memory.memory[n:n + 8] for n in range(0, self.memory.size, 8)]
            r = [self.memory.ready[n:n + 8] for n in range(0, self.memory.size, 8)]
            for i in range(len(l)):
                memory.add_row(str(i), str(l[i]), str(r[i]))
            console.print(memory)

        register = Table(title = "REGISTERS")
        register.add_column("Register", justify="center")
        register.add_column("TD", justify="center")
        register.add_column("FU", justify="center")
        register.add_column("value", justify="center")
        register.add_column("locked", justify="center")

        for reg in self.registers.R:
            register.add_row("R" + str(reg.number), "+" + str(reg.td), reg.fu, str(reg.value), str(reg.lock))

        console.print(register)

    def display2(self, badd = True, bmux = True, bstore = False, bmemory = False):
        self.display_ints()
        console = Console()
        if self.b_hs:
            console.print((self.display_HS()))

        if badd:
            alu_renderables = [Panel(Group(self.display_SS(f"ADD_{i}", fu=self.fus_add[i]),
                                     self.display_pile(fu=self.fus_add[i], title=f"Pile_{i}")))
                               for i in range(self.n_add)]

            console.print(Columns(alu_renderables, equal= True, align="center", title="Functional Unit: ADD"))

        if bmux:
            mux_renderables = [Panel(Group(self.display_SS(f"MULT_{i}", fu=self.fus_mult[i]),
                                           self.display_pile(fu=self.fus_add[i], title=f"Pile_{i}")))
                               for i in range(self.n_mult)]

            console.print(Columns(mux_renderables, equal=True, align="center", title="Functional Unit: MULT"))


        if bstore:
            store_renderables = [Panel(Group(self.display_SS(f"STORE_{i}", fu=self.fus_store[i]),
                                           self.display_pile(fu=self.fus_store[i], title=f"Pile_{i}")))
                               for i in range(self.n_store)]

            console.print(Columns(store_renderables, equal=True, align="center", title="Functional Unit: STORE"))

        if bmemory:
            memory = Table(title= "MEMORY")
            memory.add_column("Line", justify="center")
            memory.add_column("values", justify="center")
            memory.add_column("ready", justify="center")
            l = [self.memory.memory[n:n + 8] for n in range(0, self.memory.size, 8)]
            r = [self.memory.ready[n:n + 8] for n in range(0, self.memory.size, 8)]
            for i in range(len(l)):
                memory.add_row(str(i), str(l[i]), str(r[i]))
            console.print(memory)

        register = Table(title = "REGISTERS")
        register.add_column("Register", justify="center")
        register.add_column("TD", justify="center")
        register.add_column("FU", justify="center")
        register.add_column("value", justify="center")
        register.add_column("locked", justify="center")

        for reg in self.registers.R:
            register.add_row("R" + str(reg.number), "+" + str(reg.td), reg.fu, str(reg.value), str(reg.lock))





        console.print(register)









