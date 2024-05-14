import CDB
import Memory
import Pointer

from FU import holdStations, funtionalUnitStore, funtionalUnitJump, ALU_funtionalUnit, STORE_funtionalUnitStore, LOAD_funtionalUnitStore, DIV_funtionalUnit, MULT_funtionalUnit
import Registers

from rich.console import Console,Group
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel
from statistics import Statistics
from rich.text import Text


class Simulador_1_FU:

    def __init__(self, program, ss_size, n_registers, pile_size, memory_size,
                 n_alu, n_mult, n_div, n_load, n_store,
                 latency_alu, latency_mult,latency_div,latency_load, latency_store,
                 multiplicity, n_hs=10, b_hs=False, n_cycles=120,
                 b_scoreboard=1):
        # set of instructions
        self.recent_cycle = 0
        self.program = program

        self.memory = Memory.Memory(memory_size)
        self.ss_size = ss_size
        self.pile_size = pile_size

        self.n_alu = n_alu
        self.n_mult = n_mult
        self.n_div = n_div
        self.n_load = n_load
        self.n_store = n_store

        self.PC = Pointer.PC(multiplicity, self.program.n)
        self.n_cycles = n_cycles
        self.multiplicity = multiplicity

        self.fus_alu = []
        self.fus_mult = []
        self.fus_div = []
        self.fus_load = []
        self.fus_store = []
        self.fu_jump = funtionalUnitJump.FU(name="jump_0", fu_type="jump", ss_size=self.ss_size,
                                            pile_size = self.pile_size, n_cycles=self.n_cycles)

        self.b_hs = b_hs
        self.hs = holdStations.HS(n_hs, ss_size, pile_size)

        self.alu_selectionOrder = list(range(n_alu))
        self.mult_selectionOrder = list(range(n_mult))
        self.div_selectionOrder = list(range(n_div))
        self.store_selectionOrder = list(range(n_store))
        self.load_selectionOrder = list(range(n_load))

        self.statistics = Statistics()

        #Creates all the FU
        for i in range(n_alu):
            self.fus_alu.append(
                ALU_funtionalUnit.FU(f"alu_{i}", "alu", ss_size,
                                 pile_size=pile_size, latency=latency_alu, n_cycles=n_cycles))

        for i in range(n_mult):
            self.fus_mult.append(
                MULT_funtionalUnit.FU(f"mult_{i}", "mult", ss_size,
                                                  pile_size=pile_size, latency=latency_mult, n_cycles=n_cycles))
        for i in range(n_div):
            self.fus_div.append(
                DIV_funtionalUnit.FU(f"div_{i}", "div", ss_size,
                                                  pile_size=pile_size, latency=latency_div, n_cycles=n_cycles))

        for i in range(n_load):
            self.fus_load.append(
                LOAD_funtionalUnitStore.FU(f"load_{i}", "load", ss_size,
                                                  pile_size=pile_size, latency=latency_load, n_cycles=n_cycles))

        for i in range(n_store):
            self.fus_store.append(
                STORE_funtionalUnitStore.FU(f"store_{i}", "store", ss_size,
                                      pile_size=pile_size, latency=latency_store,n_cycles=n_cycles))

        self.registers = Registers.Registers(n_registers, b_scoreboard)
        self.CDB = CDB.CDB()
        self.b_scoreboard = b_scoreboard

    def dump_csv(self):
        self.registers.scoreboard.dump_csv()

    def n_next_cycles(self, n):
        for _ in range(n):
            self.one_clock_cycle()

    def one_clock_cycle(self):
        # Pointer
        self.PC.one_clock_cycle()
        self.recent_cycle = self.recent_cycle + 1
        self.statistics.newCycle()

        # Do the operation in the FU
        for fu in self.fus_alu: fu.operation()
        for fu in self.fus_div: fu.operation()
        for fu in self.fus_mult: fu.operation()
        for fu in self.fus_store: fu.operation(self.memory)
        for fu in self.fus_load: fu.operation(self.memory)

        # Update the operation Queue
        self.CDB.update(alu=self.moveOperationQueue(self.fus_alu),
                        store=self.moveOperationQueue(self.fus_store, self.memory),
                        load=self.moveOperationQueue(self.fus_load, self.memory),
                        mult=self.moveOperationQueue(self.fus_mult),
                        div=self.moveOperationQueue(self.fus_div))

        self.registers.one_clock_cycle(self.CDB)

        # One clock init cycle
        for i in range(self.n_alu): self.fus_alu[i].one_clock_cycle(self.CDB)
        for i in range(self.n_mult): self.fus_mult[i].one_clock_cycle(self.CDB)
        for i in range(self.n_div): self.fus_div[i].one_clock_cycle(self.CDB)
        for i in range(self.n_store): self.fus_store[i].one_clock_cycle(self.CDB)
        for i in range(self.n_load): self.fus_load[i].one_clock_cycle(self.CDB)

        self.fu_jump.one_clock_cycle()

        if self.b_hs:
            toUpdateSS = self.hs.one_clock_cycle(self.CDB)
            if len(toUpdateSS) > 0: self.fromHSToSS(toUpdateSS)

        if len(self.PC.PC) > 0:
            for _ in range(len(self.PC.PC)):
                instIndex = self.PC.newInstruction()
                if instIndex < self.program.n:
                    inst = self.program.get(instIndex)
                    # if there are still instructions in the program
                    res, bitMux = self.newInstruction(instIndex)
                    self.statistics.updateTypeInst(bitMux)

                    if res == 0:
                        self.statistics.increaseTotalLock()
                        self.PC.instBlock()
                        self.registers.instBlock([inst.r1, inst.r2, inst.r3, inst.rs1, inst.rd])
                        self.dump_csv()
                    else:
                        self.statistics.increaseInstIssued()
                        self.dump_csv()
                        if inst.fu_type == "jump" and inst.BTB == True:
                            self.PC.last = self.program.dict_names[inst.offset] - 1
                            break


    def moveOperationQueue(self, fus, mem = None):
        if mem == None:
            res = [fu.move_operation_queue() for fu in fus]
        else:
            res = [fu.move_operation_queue(mem) for fu in fus]
        return res

    def fromHSToSS(self, lUpdate):
        for e in lUpdate:
            hs = self.hs.l_hs[e]
            aux = hs.destination.split("_")

            fu_type, fu_pos = aux[0].strip(), int(aux[1].strip())

            if fu_type == "alu": fu = self.fus_alu[fu_pos]
            if fu_type == "mult": fu = self.fus_mult[fu_pos]
            if fu_type == "div": fu = self.fus_div[fu_pos]
            if fu_type == "load": fu = self.fus_load[fu_pos]
            if fu_type == "store": fu = self.fus_store[fu_pos]
            if fu_type == "jump": fu = self.fu_jump

            if hs.casePile:
                i = self.pile_size - 1
                fu.SS.update_i(i=i, bitMux=hs.bitMux, FU1=hs.FU1, RP=hs.RP1, FU2=hs.FU2, value=hs.value1,
                               type_operation=hs.type_operation, inv=hs.inv, inm=hs.inm)
                fu.update_pile(position=i, RP=hs.RP2, FU=hs.FU2, value=hs.value2)

            else:
                i = self.ss_size - 1
                fu.SS.update_i(i=i, bitMux=hs.bitMux, RP=hs.RP1, FU1=hs.FU1, FU2=hs.FU2, value=hs.value1,
                               type_operation=hs.type_operation, inv=hs.inv, inm=hs.inm)

            hs.empty()


    def newInstruction(self, instIndex):
        inst = self.program.get(instIndex)
        fu_type = inst.fu_type
        fus_free = []
        if fu_type == "jump":
            res, bitMux = self.fu_jump.newInstruction(inst,  self.registers, self.hs, self.b_hs)
        else:
            if fu_type == "alu":
                fus_free = [fu.calculateN(inst, self.registers) for fu in self.fus_alu]
                selectionOrder = self.alu_selectionOrder
            if fu_type == "mult":
                fus_free = [fu.calculateN(inst, self.registers) for fu in self.fus_mult]
                selectionOrder = self.mult_selectionOrder
            if fu_type == "div":
                fus_free = [fu.calculateN(inst, self.registers) for fu in self.fus_div]
                selectionOrder = self.div_selectionOrder
            if fu_type == "store":
                fus_free = [fu.calculateN(inst, self.registers) for fu in self.fus_store]
                selectionOrder = self.store_selectionOrder
            if fu_type == "load":
                fus_free = [fu.calculateN(inst, self.registers) for fu in self.fus_load]
                selectionOrder = self.load_selectionOrder


            indexes = self.find_lowest_positive_index(fus_free)

            if len(indexes) == 0:
                # if there are no elements in the indexes its means that there are no free slots in the next 4 slots
                # this is a complete lock in our instruction
                res = 0
                self.registers.lock(inst.r1)
                bitMux = 4
            else:

                index = self.selection(indexes, selectionOrder)
                fu = self.getFU(inst.fu_type, index)
                res, bitMux = fu.new_instruction(inst, instIndex, self.registers, self.hs, self.b_hs)

        return res, bitMux


    def find_lowest_positive_index(self, l):
        # Find the "best" fu to put the new instruction
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

    def selection(self, indexes, selectionOrder):
        keep = [e for e in selectionOrder if e in indexes]

        elementToMove = keep.pop(0)
        selectionOrder.remove(elementToMove)
        selectionOrder.append(elementToMove)

        return elementToMove

    def getFU(self, fu_type, index):
        if fu_type == "alu":
            return self.fus_alu[index]

        if fu_type == "store":
            return self.fus_store[index]

        if fu_type == "load":
            return self.fus_load[index]

        if fu_type == "mult":
            return self.fus_mult[index]

        if fu_type == "div":
            return self.fus_div[index]


    ## Display functions

    def display_SS(self, title, fu, store=False):
        table = Table(title=title,  expand = True)
        table.add_column("SS", justify="center")
        table.add_column("bMux", justify="center")
        table.add_column("RP", justify="center")
        table.add_column("FU1", justify="center")
        table.add_column("FU2", justify="center")
        table.add_column("value", justify="center")
        table.add_column("instIndex", justify="center")
        if store: table.add_column("inm", justify="center")

        for i in range(self.ss_size - 1, -1, -1):
            ss = fu.SS.l_ss[i]

            if store:
                table.add_row(f"SS{i}", "" if ss.bitMux is None else str(ss.bitMux), str(ss.RP),
                              "" if ss.RP == -1 else str(ss.RP),
                              "" if ss.FU1 is None else str(ss.FU1),
                              "" if ss.FU2 is None else str(ss.FU2),
                              "" if ss.value is None else str(ss.value),
                              "" if ss.instruction is None else str(ss.instruction),
                              "" if ss.inm is None else str(ss.inm))
            else:
                table.add_row(f"SS{i}", "" if ss.bitMux is None else str(ss.bitMux),
                              "" if ss.RP==-1 else str(ss.RP),
                              "" if ss.FU1 is None else str(ss.FU1),
                              "" if ss.FU2 is None else str(ss.FU2),
                              "" if ss.value is None else str(ss.value),
                              "" if ss.instruction is None else str(ss.instruction))

        return table

    def display_HS(self):
        table = Table(title="Hold Stations")
        table.add_column("occupied", justify="center")
        table.add_column("HS", justify="center")
        table.add_column("case Pile?", justify="center")
        table.add_column("bitMux", justify="center")
        table.add_column("RP1", justify="center")
        table.add_column("RP2", justify="center")
        table.add_column("position", justify="center")
        table.add_column("destination", justify="center")
        table.add_column("FU1", justify="center")
        table.add_column("FU2", justify="center")
        table.add_column("value1", justify="center")
        table.add_column("value2", justify="center")

        for i in range(self.hs.n):
            hs = self.hs.l_hs[i]
            table.add_row(str(self.hs.occupied[i]),
                          f"HS{i}",
                          "" if hs.casePile is None else str(hs.casePile),
                          "" if hs.bitMux is None else str(hs.bitMux),
                          "" if hs.RP1 == -1 else str(hs.RP1),
                          "" if hs.RP2 == -1 else str(hs.RP2),
                          "" if hs.position is None else str(hs.position),
                          "" if hs.destination is None else str(hs.destination),
                          "" if hs.FU1 is None else hs.FU1,
                          "" if hs.FU2 is None else hs.FU2,
                          "" if hs.value1 is None else str(hs.value1),
                          "" if hs.value2 is None else str(hs.value2))

        return table

    def display_pile(self, fu, title):
        table = Table(title=title)
        table.add_column("P", justify="center")
        table.add_column("RP", justify="center")
        table.add_column("FU", justify="center")
        table.add_column("value", justify="center")

        for i in range(self.pile_size - 1, -1, -1):
            ss = fu.pile.pile[i]
            table.add_row(f"P{i}", str(ss.RP), ss.fu, str(ss.value))

        return table

    def display_ints(self):
        text = Text()
        if self.PC.PC is None:
            text.append("Loading instructions")
        #elif self.PC.last >= self.PC.programSize:
        elif len(self.PC.PC) == 0:
            text.append("There are no more instructions")
        else:
            text.append("PC: ", style="bold magenta")
            text.append(str(self.PC) + "\n", style="bold")
            text.append("Instruction: ", style="bold magenta")
            inst_list = [str(self.program.get(i)) for i in self.PC.PC]

            text.append(str(inst_list), style="bold")

        console = Console(record=True, width=200, height=200)

        console.print(text)

    def display(self, balu=True, bmux=True, bstore=False, bmemory=False):
        self.display_ints()
        console = Console(record=True, width=200, height=200)

        if balu:
            table_alus = Table(title="Functional Unit: alu")
            table_alus_pile = Table(title="Pile: alu")
            for i in range(self.n_alu):
                table_alus.add_column(self.display_SS(f"alu_{i}", fu=self.fus_alu[i]))
                table_alus_pile.add_column(self.display_pile(fu=self.fus_alu[i]))
            console.print(table_alus)
            console.print(table_alus_pile)

        if bmux:
            table_mult = Table(title="Functional Unit: MULT")
            for i in range(self.n_mult):
                table_mult.add_column(self.display_SS(f"MULT_{i}", fu=self.fus_mult[i]))
            console.print(table_mult, overflow="fold")


        if bstore:
            table_store = Table(title="Functional Unit: STORE")
            for i in range(self.n_store):
                table_store.add_column(self.display_SS(f"STORE_{i}", fu=self.fus_store[i]))
            console.print(table_store, overflow="fold")

        if bmemory:
            memory = Table(title="MEMORY")
            memory.add_column("Line", justify="center")
            memory.add_column("values", justify="center")
            memory.add_column("ready", justify="center")
            l = [self.memory.memory[n:n + 8] for n in range(0, self.memory.size, 8)]
            r = [self.memory.ready[n:n + 8] for n in range(0, self.memory.size, 8)]
            for i in range(len(l)):
                memory.add_row(str(i), str(l[i]), str(r[i]))
            console.print(memory)

        register = Table(title="REGISTERS")
        register.add_column("Register", justify="center")
        register.add_column("TD", justify="center")
        register.add_column("FU", justify="center")
        register.add_column("value", justify="center")
        register.add_column("locked", justify="center")

        for reg in self.registers.R:
            register.add_row("R" + str(reg.number), "+" + str(reg.td), reg.fu, str(reg.value), str(reg.lock))

        console.print(register)

    def display2(self, balu=True, bmux=True, bstore=False, bmemory=False, bhs = False, bCDB = False, balu_brt=False, bmux_brt = False, bstore_brt = False, bjump_brt = False):
        console = Console(record= True, width=190)

        #console.rule("[bold red]")
        console.rule(f"[bold red] {self.recent_cycle}", align="left")
        #console.rule("[bold red]\n")


        self.display_ints()

        if self.b_hs and bhs:
            console.print(self.display_HS())


        if balu:
            alu_renderables = [Panel(Group(self.display_SS(f"alu_{i}", fu=self.fus_alu[i]),
                                           self.display_pile(fu=self.fus_alu[i], title=f"Pile_{i}")))
                               for i in range(self.n_alu)]

            console.print(Columns(alu_renderables, equal=True, align="center", title="Functional Unit: alu", expand = True))

        if bmux:
            mux_renderables = [Panel(Group(self.display_SS(f"MULT_{i}", fu=self.fus_mult[i]),
                                           self.display_pile(fu=self.fus_mult[i], title=f"Pile_{i}")))
                               for i in range(self.n_mult)]

            console.print(Columns(mux_renderables, equal=True, align="center", title="Functional Unit: MULT"))

        if bstore:
            store_renderables = [Panel(Group(self.display_SS(f"STORE_{i}", fu=self.fus_store[i]),
                                             self.display_pile(fu=self.fus_store[i], title=f"Pile_{i}")))
                                 for i in range(self.n_store)]

            console.print(Columns(store_renderables, equal=True, align="center", title="Functional Unit: STORE"))

        register = Table(title="REGISTERS")
        register.add_column("Register", justify="center")
        register.add_column("TD", justify="center")
        register.add_column("FU", justify="center")
        register.add_column("value", justify="center")
        register.add_column("locked", justify="center")

        for reg in self.registers.R:
            register.add_row("R" + str(reg.number), "+" + str(reg.td), reg.fu, str(reg.value), str(reg.lock))

        console.print(register)

        console.save_html("test.html")
        console.save_svg("test.svg")
        console.save_text("test.txt")

        if bmemory:
            memory = Table(title="MEMORY")
            memory.add_column("Line", justify="center")
            memory.add_column("values", justify="center")

            l = [self.memory.memory[n:n + 8] for n in range(0, self.memory.size, 8)]
            #r = [self.memory.ready[n:n + 8] for n in range(0, self.memory.size, 8)]
            for i in range(len(l)):
                memory.add_row(str(i), str(l[i]))
            console.print(memory)



        if bCDB:
            text = Text()
            text.append(self.CDB.__str__()+ "\n" )
            console.print(text)

        if balu_brt:
            text = Text()
            for fu in self.fus_alu:
                text.append(fu.name, style="bold magenta underline")
                text.append( fu.BRT.__str__() + "\n")
            console.print(text)

        if bmux_brt:
            text = Text()
            for fu in self.fus_mult:
                text.append(fu.name + fu.BRT.__str__() + "\n")
            console.print(text)

        if bstore_brt:
            text = Text()
            for fu in self.fus_store:
                text.append(fu.name + fu.BRT.__str__() + "\n")
            console.print(text)

        if bjump_brt:
            text = Text()
            text.append(self.fu_jump.name + self.fu_jump.BRT.__str__() + "\n")
            console.print(text)



