Luf_int = 2
Luf_mult = 4

from FU import Scoreboard


class Register:
    def __init__(self, i):
        self.number = i  # numero de registro
        self.rp = 0  # tiempo en llegar value desde fu
        self.fu = None  # fu de donde proveendrá el value
        self.value = i*2
        #self.type = None
        self.lock = False

    def __str__(self):
        return f"R{self.number}: +{self.rp} ({self.fu}) value: {self.value} lock: {self.lock}"






class Registers:
    def __init__(self, registers_size, b_scoreboard):
        self.registers_size = registers_size
        self.Registers = [Register(i) for i in range(registers_size)]
        self.scoreboard = Scoreboard.Scoreboards(registers_size)

    def __str__(self):
        str_a = ""
        for a in range(self.registers_size):
            str_a += str(self.Registers[a])
            str_a += "\n"

        return str_a

    def one_clock_cycle(self, CDB):
        for reg in self.Registers:
            reg.lock = False
            if reg.rp == 1:
                separated_list = reg.fu.split("_")
                type = separated_list[0].strip()
                index = int(separated_list[1].strip())
                reg.value = CDB.get(type, index)
                reg.fu = None
                reg.rp = 0

            if reg.rp > 0:
                reg.rp = reg.rp - 1

    def new_inst(self, destination, rp, fu_name):
        # primero tengo que actualizar los registros que serán destino
        # asi tengo en cuenta el tiempo anterior y en el caso de escalaridad
        # no perder el orden de las instrucciones!!!

        self.Registers[destination].rp = rp
        self.Registers[destination].fu = fu_name
        self.Registers[destination].value = None
        self.Registers[destination].lock = False

        self.update_scoreboard()

    def lock(self, register):
        self.Registers[register].lock = True

    def unlock(self):
        for r in self.Registers: r.lock = False

    def get_R_i(self, i):
        return self.Registers[i]

    def get_value(self, i):
        return self.Registers[i].value

    def get_td(self, i):
        return self.Registers[i].rp


    def rp_calculation_type1(self, source1, source2, destination):
        if source2 is None:
            return self.rp_calculation_type2(source1,destination)
        else:
            if self.Registers[source1].lock or self.Registers[source2].lock or self.Registers[destination].lock:
                return [True]
            else:
                t1 = self.Registers[source1].rp
                t2 = self.Registers[source2].rp

                # primero tengo que actualizar los registros que serán destino
                # asi tengo en cuenta el tiempo anterior y en el caso de escalaridad
                # no perder el orden de las instrucciones!!!
                if t1 >= t2:
                    ts_max = t1
                    ts_min = t2
                    reg_max = source1
                    reg_min = source2
                    inv = True

                else:
                    ts_max = t2
                    ts_min = t1
                    reg_max = source2
                    reg_min = source1
                    inv = False

                FU1 = f"R{reg_min}" if self.Registers[reg_min].fu == None else self.Registers[reg_min].fu
                FU2 = f"R{reg_max}" if self.Registers[reg_max].fu == None else self.Registers[reg_max].fu

                return [ts_max, ts_min, reg_max, reg_min, FU1, FU2, inv ]

    def rp_calculation_type1_inm(self, source1, destination):

        if self.Registers[source1].lock or self.Registers[destination].lock:
            return [True]
        else:
            t1 = self.Registers[source1].rp
            ts_max = t1
            ts_min = -1
            reg_max = source1
            reg_min = "inm"
            inv = True
            FU1 = "inm"
            FU2 = f"R{reg_max}" if self.Registers[reg_max].fu == None else self.Registers[reg_max].fu

            return [ts_max, ts_min, reg_max, reg_min, FU1, FU2, inv]



    def rp_calculation_type2(self, source, destination):
        if self.Registers[source].lock or self.Registers[destination].lock:
            return [True]
        else:
            ts_max = self.Registers[source].rp
            FU = self.Registers[source].fu
        #[ts_max, 0, source, 0, 0, FU, 0]
        return [ts_max,0,source,-2, "N/A", FU, 0]

    def inst_block(self, lBlock):
        for r in lBlock:
            if r!= None:
                self.Registers[r].lock= True


    def update_scoreboard(self):
        self.scoreboard.update(self.Registers)
