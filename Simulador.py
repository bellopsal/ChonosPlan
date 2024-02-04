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

        self.fu_add = funtionalUnit.FU("add_1", "add", n_ss,pile_size=pile_size,latency = 3)
        self.fu_mult = funtionalUnit.FU("mult_1", "mult", n_ss,pile_size=pile_size,latency = 3)
        self.fu_store = funtionalUnit.FU("store_1", "store", n_ss,pile_size=pile_size,latency = 3)

        self.registers = Registers.Registers(n_registers, b_scoreboard)
        self.CDB = CDB.CDB()
        self.PC = 0
        self.b_scoreboard = b_scoreboard

    def one_clock_cycle(self):

        #Operation queue
        self.CDB.update(add=self.fu.moveOperationQueue(), store=self.fu_store.moveOperationQueue(), mux=self.fu_mult.moveOperationQueue())

        # update timestamps and get values from CBD
        self.registers.one_clock_cycle(self.CDB)
        self.fu.one_clock_cycle_ini()

        # data that will be use for the alu


    #
    #     if self.pos < self.program.n:
    #         # if there are still instructions in the program
    #         inst = self.program.get(self.pos)
    #         [td, ts_max, ts_min, arg_max, arg_min, FU1, FU2] = self.registers.td_calculation(inst.r2, inst.r3)
    #
    #
    #         if ts_min == 0:
    #             value = self.registers.R[arg_min].value
    #             RP = 0
    #             bitAvail = 1
    #
    #         else:
    #             value = None
    #             RP = ts_min
    #             bitAvail = 0
    #
    #         if ts_max == 0:
    #             bitMux = 0
    #
    #         else:
    #             bitMux = 1
    #
    #         n = 0
    #         if self.fu.BRT.get(ts_max) != 0:
    #             n = self.fu.BRT.find_first_free_after(ts_max)
    #
    #             if n != -1:
    #                 bitMux = 2
    #
    #         td = td + n
    #         ts_max_aux = ts_max + 1
    #         ts_max = ts_max + n
    #         if bitMux == 2:
    #             self.fu.pile[ts_max] = (None, ts_max_aux)
    #
    #                 # actualizamos registros, fu con los valores de la nueva instrucción
    #         self.registers.new_inst(destino=inst.r1, td=td, fu_name=self.fu.name)
    #         self.fu.BRT.ocupy_range(ts_max,n)
    #         self.fu.SS.update_i(i=ts_max, bitAvail=bitAvail, bitMux= bitMux, FU1 = FU1, FU2 = FU2,
    #                             RP = RP, value = value, type_operation=inst.type)
    #
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

    def dump_csv(self):
        self.registers.scoreboard.dump_csv()