class Scoreboard:

    def __init__(self, i):
        self.number = i
        self.T = [0]
        self.td = []
        self.fu = []
        self.value = []

    def __str__(self):
        l_aux = ["+" + str(self.td[i]) + " (" + str(self.fu[i]) + ") " for i in range(len(self.fu))]
        return f"R{self.number}: {' | '.join(l_aux)}"


class Scoreboards:

    def __init__(self, number):
        self.scoreboard = [Scoreboard(i) for i in range(number)]
        self.n = number

    def __str__(self):
        r0 = len(self.scoreboard[0].T)

        str_a = "       "
        ciclos = [" T" + str(i) + " " for i in range(r0)]
        str_a += "    |    ".join(ciclos)
        str_a += "\n"

        for a in range(self.n):
            str_a += str(self.scoreboard[a])
            str_a += "\n"

        return str_a

    def update_i(self, i, registro):
        self.scoreboard[i].T.append(self.scoreboard[i].T[-1]+1)
        self.scoreboard[i].td.append(registro.td)
        self.scoreboard[i].fu.append(registro.fu)
        self.scoreboard[i].value.append(registro.value)

    def update (self, registros):
        for i in range(self.n):
            self.update_i(i, registros[i])