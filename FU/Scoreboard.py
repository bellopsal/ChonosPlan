import csv
class Scoreboard:

    def __init__(self, i):
        self.number = i
        self.T = [0,1]
        self.rp = [0]
        self.fu = [None]
        self.value = []

    def __str__(self):
        l_aux = ["+" + str(self.rp[i]) + " (" + str(self.fu[i]) + ") " for i in range(len(self.fu))]
        return f"R{self.number}: {' | '.join(l_aux)}"

    def dump_csv(self):
        return ["+" + str(self.rp[i]) + " (" + str(self.fu[i]) + ") " for i in range(len(self.fu))]

class Scoreboards:

    def __init__(self, number):
        self.scoreboard = [Scoreboard(i) for i in range(number)]
        self.n = number

    def __str__(self):


        str_a = "         "
        ciclos = [" T" + str(i) + " " for i in self.scoreboard[0].T]
        str_a += "   |   ".join(ciclos)
        str_a += "\n"

        for a in range(self.n):
            str_a += str(self.scoreboard[a])
            str_a += "\n"

        return str_a

    def dump_csv(self):
        fields = ["Register"]+["T" + str(i) + " " for i in self.scoreboard[0].T]
        rows = [["R"+str(i)]+self.scoreboard[i].dump_csv() for i in range(self.n)]


        with open("scoreboard.csv", "w") as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(rows)


    def update_i(self, i, registro):
        self.scoreboard[i].T.append(self.scoreboard[i].T[-1]+1)
        self.scoreboard[i].rp.append(registro.rp)
        self.scoreboard[i].fu.append(registro.fu)
        self.scoreboard[i].value.append(registro.value)

    def update (self, registros):
        for i in range(self.n):
            self.update_i(i, registros[i])