import CDB
import Program
import funtionalUnit
import Registers


class Simulador_1_FU:

    def __init__(self, list_program, n_ss, fu_type, name, n_registers, b_scoreboard):
        # set of instructions
        self.program = Program.Program(list_program)

        # Iniciate SS
        self.fu = funtionalUnit.FU(name, fu_type, n_ss)

        # Registers
        self.registers = Registers.Registers(n_registers, b_scoreboard)

        self.CDB = CDB.CDB()

        self.pos = 0
        self.b_scoreboard = b_scoreboard

    def one_clock_cycle(self):

        # update timestamps
        self.registers.one_clock_cycle_ini()
        self.fu.one_clock_cycle_ini()



        if self.pos < self.program.n:
            inst = self.program.get(self.pos)
            [td, ts_max, ts_min, arg_max, arg_min, FU1, FU2] = self.registers.td_calculation(inst.r2, inst.r3)


            if ts_min == 0:
                value = self.registers.R[arg_min].value
                RP = 0
                bitAvail = 1

            else:
                value = None
                RP = ts_min
                bitAvail = 0

            if ts_max == 0:
                bitMux = 0

            else:
                bitMux = 1

            n = 0
            if self.fu.BRT.get(ts_max) != 0:
                n = self.fu.BRT.find_first_free_after(ts_max)

                if n != -1:
                    bitMux = 2
            td = td + n
            ts_max_aux = ts_max
            ts_max = ts_max + n
            if bitMux == 2:
                self.fu.pile[ts_max] = (None, ts_max_aux)

                    # actualizamos registros, fu con los valores de la nueva instrucción
            self.registers.new_inst(destino=inst.r1, td=td, fu_name=self.fu.name)
            self.fu.BRT.occupied_i(ts_max)
            self.fu.SS.update_i(i=ts_max, bitAvail=bitAvail, bitMux= bitMux, FU1 = FU1, FU2 = FU2,
                                RP = RP, value = value, type_operation=inst.type)

            # operacion, por ahora solo suma
            self.CDB.put(self.fu.calculate(self.CDB.get(), self.registers, ss_0, pile))
            print(" CDB "+ str(self.CDB))

            # actualizar valores
            self.fu.update(self.CDB.get())
            self.registers.update(self.CDB.get())
            self.registers.update_scoreboard()
            self.pos = self.pos + 1
        else:
        # operacion, por ahora solo suma
            self.CDB.put(self.fu.calculate(self.CDB.get(), self.registers, ss_0, pile))

    # actualizar valores
            self.fu.update(self.CDB.get())
            self.registers.update(self.CDB.get())
            self.pos = self.pos + 1

