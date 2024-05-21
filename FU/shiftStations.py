import csv


def CDBhelper(FU, CDB):
    sep_list = FU.split("_")
    fu = sep_list[0].strip()
    index = int(sep_list[1].strip())
    return CDB.get(fu, index)


class ShiftStation:
    def __init__(self):
        # self.bitInUse = 0   # if the ss is in use ( with data in it)
        # self.bitAvail = 0  # first operand available 1 or not
        self.bitMux = None 

        self.inv = False  # true if last operand is the first in order
        self.inm = None

        self.FU1 = None  # which FU will generate first operand
        self.FU2 = None  # which FU will generate last operand
        self.RP = - 1  # when first operand will be ready
        self.value = None  # first operand

        self.type_operation = None

        self.instruction = None

    def one_clock_cycle(self, CDB):
        if self.RP == 1:
            self.RP = -1
            self.value = CDBhelper(self.FU1, CDB)
        elif self.RP > 1:
            self.RP = self.RP - 1

    def __str__(self):
        return f"    {self.bitMux}   | {self.RP} | {self.FU1} | {self.FU2} | {self.value}"


class SS:
    def __init__(self, ss_size):
        # the first ss is the one ex in this cycle
        self.l_ss = [ShiftStation() for i in range(ss_size)]
        self.ss_size = ss_size
        self.csv = "ss.csv"

        with open("ss.csv", "w") as f:
            write = csv.writer(f)
            fields = ["SS", "bitMux", "RP", "FU1", "FU2", "value"]
            rows = [
                [str(i), self.l_ss[i].bitMux, self.l_ss[i].RP, self.l_ss[i].FU1, self.l_ss[i].FU2, self.l_ss[i].value]
                for i in range(ss_size - 1, -1, -1)]
            write.writerow(fields)
            write.writerows(rows)

    def one_clock_cycle(self, CDB): 
        # Update internal values of SS
        bitMux, FU2 = self.l_ss[1].bitMux, self.l_ss[1].FU2
        for e in self.l_ss:
            e.one_clock_cycle(CDB)

        self.l_ss.append(ShiftStation())
        res = self.l_ss[0]
        self.l_ss.pop(0)

        return res, bitMux, FU2

    def get(self, i):
        return self.l_ss[i]

    def __str__(self):
        res = ""
        for i in range(self.ss_size):
            txt = "\n" + f"SS{i} " + str(self.get(i))
            res = txt + res
        res = "      bitMux | RP | FU1 | FU2 | value" + res
        return res

    def get(self, i):
        return self.l_ss[i]

    def update_i(self, i, bitMux, FU1, FU2, RP, value, type_operation, inv, instruction=None, inm=None):
        self.l_ss[i].bitMux = bitMux
        self.l_ss[i].FU1 = FU1
        self.l_ss[i].FU2 = FU2
        self.l_ss[i].RP = RP
        self.l_ss[i].value = value
        self.l_ss[i].inv = inv
        self.l_ss[i].inm = inm
        self.l_ss[i].instruction = instruction
        self.l_ss[i].type_operation = type_operation

        with open("ss.csv", "a") as f:
            write = csv.writer(f)
            fields = ["SS", "bitMux", "RP", "FU1", "FU2", "value"]
            rows = [
                [str(i), self.l_ss[i].bitMux, self.l_ss[i].RP, self.l_ss[i].FU1, self.l_ss[i].FU2, self.l_ss[i].value]
                for i
                in range(self.ss_size - 1, -1, -1)]
            write.writerow(fields)
            write.writerows(rows)


class QSDElement:
    def __init__(self):
        self.value = None
        self.fu = None
        self.RP = -1

    def __str__(self):
        return f"     {self.RP} | {self.fu} | {self.value}"

    def __int__(self, value, fu, RP):
        self.value = value
        self.fu = fu
        # self.bitUse = -1
        self.RP = RP

    def one_clock_cycle(self, CDB):
        if self.RP == 1:
            self.RP = -1
            self.value = CDBhelper(self.fu, CDB)
        elif self.RP > 1:
            self.RP = self.RP - 1

    def setValue(self, value):
        self.value = value

    def setFu(self, fu):
        self.fu = fu

    def setRP(self, RP):
        self.RP = RP

    def getValue(self):
        return self.value

    def getFU(self):
        return self.fu

    def getRP(self):
        return self.RP


class QSD:
    def __init__(self, size):
        self.QSD = [QSDElement() for i in range(size)]
        self.n = size
        self.csv = "QSD.csv"

        with open("QSD.csv", "w") as f:
            write = csv.writer(f)
            fields = ["Element", "RP", "FU", "value"]
            rows = [[str(i), self.QSD[i].RP, self.QSD[i].fu, self.QSD[i].value] for i
                    in range(self.n - 1, -1, -1)]
            write.writerow(fields)
            write.writerows(rows)

    def __str__(self):
        res = ""
        for i in range(self.n):
            txt = "\n" + f"QSD{i} " + str(self.QSD[i])
            res = txt + res
        res = "      RP | FU |value" + res
        return res

    def get(self, i):
        return self.QSD[i]

    def one_clock_cycle(self, CDB, bitMux, FU2):
        if bitMux == 2 or bitMux == 6:
            self.QSD[1].value = CDBhelper(FU2, CDB)
            self.QSD[1].RP = -1

        for element in self.QSD:
            element.one_clock_cycle(CDB)

        self.QSD.append(QSDElement())
        res = self.QSD[0]
        self.QSD.pop(0)

        return res

