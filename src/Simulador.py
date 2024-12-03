import CDB
import Memory
import PC
from src.FU import (
    holdStations,
    STORE_funtionalUnitStore,
    ALU_funtionalUnit,
    DIV_funtionalUnit,
    MULT_funtionalUnit,
    TRANS_funtionalUnit,
    LOAD_funtionalUnitStore,
)
from src.FU.aux import funtionalUnitJump
import Registers
from rich.console import Console, Group
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel
from statistics import Statistics
from rich.text import Text


class Simulator:
    """
    A simulator for managing and executing instructions across multiple functional units.

    Attributes:
        program (Program): The program containing instructions.
        ss_size (int): Size of station sets.
        registers_size (int): Size of registers.
        QSD_size (int): Queue size for each functional unit.
        memory_size (int): Size of memory.
        n_alu, n_mult, n_div, n_load, n_store, n_trans (int): Number of functional units of each type.
        latency_* (int): Latency for each functional unit type.
        multiplicity (int): Level of multiplicity for parallel execution.
        n_hs (int): Number of hold stations.
        b_hs (bool): Enable or disable hold stations.
        n_cycles (int): Maximum number of cycles to simulate.
        b_scoreboard (bool): Enable or disable scoreboard.
    """

    def __init__(
        self,
        program,
        ss_size,
        registers_size,
        QSD_size,
        memory_size,
        n_alu,
        n_mult,
        n_div,
        n_load,
        n_store,
        n_trans,
        latency_alu,
        latency_mult,
        latency_div,
        latency_load,
        latency_store,
        latency_trans,
        multiplicity,
        n_hs=10,
        b_hs=False,
        n_cycles=120,
        b_scoreboard=1,
    ):
        self.program = program
        self.ss_size = ss_size
        self.QSD_size = QSD_size
        self.memory = Memory.Memory(memory_size)
        self.recent_cycle = 0
        self.n_cycles = n_cycles
        self.multiplicity = multiplicity
        self.memory_last = -1
        self.b_hs = b_hs
        self.b_scoreboard = b_scoreboard

        # Initialize functional units
        self.fus_alu = [
            ALU_funtionalUnit.FU(
                f"alu_{i}", "alu", ss_size, QSD_size, latency=latency_alu, n_cycles=n_cycles
            )
            for i in range(n_alu)
        ]
        self.fus_mult = [
            MULT_funtionalUnit.FU(
                f"mult_{i}", "mult", ss_size, QSD_size, latency=latency_mult, n_cycles=n_cycles
            )
            for i in range(n_mult)
        ]
        self.fus_div = [
            DIV_funtionalUnit.FU(
                f"div_{i}", "div", ss_size, QSD_size, latency=latency_div, n_cycles=n_cycles
            )
            for i in range(n_div)
        ]
        self.fus_load = [
            LOAD_funtionalUnitStore.FU(
                f"load_{i}", "load", ss_size, QSD_size, latency=latency_load, n_cycles=n_cycles
            )
            for i in range(n_load)
        ]
        self.fus_store = [
            STORE_funtionalUnitStore.FU(
                f"store_{i}", "store", ss_size, QSD_size, latency=latency_store, n_cycles=n_cycles
            )
            for i in range(n_store)
        ]
        self.fus_trans = [
            TRANS_funtionalUnit.FU(
                f"trans_{i}", "trans", ss_size, QSD_size, latency=latency_trans, n_cycles=n_cycles
            )
            for i in range(n_trans)
        ]

        self.fu_jump = funtionalUnitJump.FU(
            name="jump_0", fu_type="jump", ss_size=self.ss_size, QSD_size=self.QSD_size, n_cycles=self.n_cycles
        )

        # Initialize supporting structures
        self.PC = PC.PC(multiplicity, self.program.program_size)
        self.hs = holdStations.HS(n_hs, ss_size, QSD_size)
        self.registers = Registers.Registers(registers_size, b_scoreboard)
        self.CDB = CDB.CDB()
        self.statistics = Statistics()

        # Initialize selection orders
        self.alu_selection_order = list(range(n_alu))
        self.mult_selection_order = list(range(n_mult))
        self.div_selection_order = list(range(n_div))
        self.store_selection_order = list(range(n_store))
        self.load_selection_order = list(range(n_load))
        self.trans_selection_order = list(range(n_trans))

    def one_clock_cycle(self):
        """
        Execute one clock cycle of the simulation, updating all functional units, registers, and memory.
        """
        self.PC.one_clock_cycle()
        self.recent_cycle += 1
        self.statistics.new_cycle()

        # Functional unit operations
        for fu_list in [
            self.fus_alu,
            self.fus_mult,
            self.fus_div,
            self.fus_load,
            self.fus_store,
            self.fus_trans,
        ]:
            for fu in fu_list:
                fu.operation()

        # Update CDB
        self.CDB.update(
            alu=self.move_operation_queue(self.fus_alu),
            mult=self.move_operation_queue(self.fus_mult),
            div=self.move_operation_queue(self.fus_div),
            load=self.move_operation_queue(self.fus_load, self.memory),
            store=self.move_operation_queue(self.fus_store, self.memory),
            trans=self.move_operation_queue(self.fus_trans),
        )

        self.registers.one_clock_cycle(self.CDB)

        # Increment clock cycles in functional units
        for fu_list in [
            self.fus_alu,
            self.fus_mult,
            self.fus_div,
            self.fus_store,
            self.fus_load,
            self.fus_trans,
        ]:
            for fu in fu_list:
                fu.one_clock_cycle(self.CDB)

        if self.memory_last > 0:
            self.memory_last -= 1

        self.fu_jump.one_clock_cycle()

        # Update hold stations if enabled
        if self.b_hs:
            to_update_ss = self.hs.one_clock_cycle(self.CDB)
            if to_update_ss:
                self.from_hs_to_ss(to_update_ss)

        # Issue new instructions
        while len(self.PC.PC) > 0:
            inst_index = self.PC.new_instruction()
            if inst_index < self.program.program_size:
                inst = self.program.get(inst_index)
                res, bit_mux, pos = self.new_instruction(inst_index)
                self.statistics.update_instruction_type(bit_mux)

                if res == 0:
                    self.PC.inst_lock()
                    self.registers.inst_block([inst.r1, inst.r2, inst.r3, inst.rs1])
                else:
                    if inst.fu_type in ["store", "load"] and pos > self.memory_last:
                        self.memory_last = pos
                    if inst.fu_type == "jump" and inst.BTB:
                        self.PC.last = self.program.dict_tags[inst.offset] - 1
                        break

        self.statistics.update_statistics()

    def move_operation_queue(self, fus, mem=None):
        """
        Move operations in the queue of each functional unit.

        Args:
            fus (list): List of functional units.
            mem (Memory, optional): Memory object.

        Returns:
            list: Results of moving operations for each functional unit.
        """
        if mem:
            return [fu.move_operation_queue(mem) for fu in fus]
        return [fu.move_operation_queue() for fu in fus]

    # Additional methods follow with docstrings and clean formatting...
