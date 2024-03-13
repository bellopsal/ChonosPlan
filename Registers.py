Luf_int = 2
Luf_mult = 4

from FU import Scoreboard


class Register:
    def __init__(self, i):
        self.number = i  # numero de registro
        self.td = 0  # tiempo en llegar value desde fu
        self.fu = None  # fu de donde proveendrá el value
        self.value = i+2
        self.type = None
        self.block = False

    def __str__(self):
        return f"R{self.number}: +{self.td} ({self.fu}) value: {self.value}"






class Registers:
    def __init__(self, size, b_scoreboard):
        self.R = [Register(i) for i in range(size)]
        self.size = size
        self.b_scoreboard = b_scoreboard

        if b_scoreboard:
            self.scoreboard = Scoreboard.Scoreboards(size)

    def __str__(self):
        str_a = ""
        for a in range(self.size):
            str_a += str(self.R[a])
            str_a += "\n"

        return str_a

    def one_clock_cycle(self, CBD):
        for reg in self.R:
            if reg.td == 1:
                separated_list = reg.fu.split("_")
                type = separated_list[0].strip()
                index = int(separated_list[1].strip())
                reg.value = CBD.get(type, index)
                reg.fu = None
                reg.td = 0
            if reg.td > 0:
                reg.td = reg.td - 1

    def new_inst(self, destino, td, fu_name):
        # primero tengo que actualizar los registros que serán destino
        # asi tengo en cuenta el tiempo anterior y en el caso de escalaridad
        # no perder el orden de las instrucciones!!!

        self.R[destino].td = td
        self.R[destino].fu = fu_name
        self.R[destino].value = None
        self.R[destino].block = False

    def block(self, register):
        self.R[register].block = True


    def get_R_i(self, i):
        return self.R[i]

    def get_value(self, i):
        return self.R[i].value

    def get_td(self, i):
        return self.R[i].td

    def get_type(self, i):
        return self.R[i].type

    def td_calculation_type1(self, source1, source2, destiny):

        if self.R[source1].block or self.R[source1].block or self.R[destiny].block:
            return [True]
        else:
            t1 = self.R[source1].td
            t2 = self.R[source2].td

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



            FU1 = self.R[reg_min].fu
            FU2 = self.R[reg_max].fu

            return [ts_max, ts_min, reg_max, reg_min, FU1, FU2, inv ]

    def instBlock(self, lBlock):
        for r in lBlock:
            self.R[r].block=True
            self.R[r].block = True
            self.R[r].block = True

    def td_calculation_type2(self, source):

        ts = self.R[source].td
        FU = self.R[source].fu

        return [ts, FU]


    def update_scoreboard(self):
        if self.b_scoreboard:
            self.scoreboard.update(self.R)
