Luf_int = 2
Luf_mult = 4

from FU import Scoreboard


class Register:
    def __init__(self, i):
        self.number = i  # numero de registro
        self.disp = 1
        self.td = 0  # tiempo en llegar value desde fu
        self.fu = None  # fu de donde proveendrá el value
        self.value = i
        self.type = None

    def __str__(self):
        return f"R{self.number}: +{self.td} ({self.fu}) value: {self.value}"

    def one_clock_ini(self):
        if self.td > 0:
            self.td = self.td - 1


class Registers:
    def __init__(self, number, b_scoreboard):
        self.R = [Register(i) for i in range(number)]
        self.n = number
        self.b_scoreboard = b_scoreboard

        if b_scoreboard:
            self.scoreboard = Scoreboard.Scoreboards(number)

    def __str__(self):
        str_a = ""
        for a in range(self.n):
            str_a += str(self.R[a])
            str_a += "\n"

        return str_a

    def one_clock_cycle_ini(self):
        for reg in self.R:
            reg.one_clock_ini()

    def new_inst(self, destino, td, fu_name):
        # primero tengo que actualizar los registros que serán destino
        # asi tengo en cuenta el tiempo anterior y en el caso de escalaridad
        # no perder el orden de las instrucciones!!!

        self.R[destino].td = td
        self.R[destino].disp = 0
        self.R[destino].fu = fu_name
        self.R[destino].value = None

    def get_R_i(self, i):
        return self.R[i]

    def get_value(self, i):
        return self.R[i].value

    def get_td(self, i):
        return self.R[i].td

    def get_type(self, i):
        return self.R[i].type

    def td_calculation(self, source1, source2):

        t1 = self.R[source1].td
        t2 = self.R[source2].td

        # primero tengo que actualizar los registros que serán destino
        # asi tengo en cuenta el tiempo anterior y en el caso de escalaridad
        # no perder el orden de las instrucciones!!!
        if (t1 >= t2):
            ts_max = t1
            ts_min = t2
            arg_min = source1
            arg_max = source2
        else:
            ts_max = t2
            ts_min = t1
            arg_min = source2
            arg_max = source1

        td = ts_max + Luf_int
        if t1 == t2 == 0:
            FU1 = arg_min
            FU2 = arg_max
        else:
            FU1 = self.R[arg_min].fu
            FU2 = self.R[arg_max].fu

        return [td, ts_max, ts_min, arg_max, arg_min, FU1, FU2]

    def update(self, CDB):
        for reg in self.R:
            if reg.disp == 0 and reg.td == 0:
                reg.value = CDB
                reg.disp = 1

    def update_scoreboard(self):
        if self.b_scoreboard:
            self.scoreboard.update(self.R)
