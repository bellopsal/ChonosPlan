import csv


class ShiftStation:
    def __init__(self):
        #self.bitInUse = 0   # if the ss is in use ( with data in it)
        #self.bitAvail = 0  # first operand available 1 or not
        self.bitMux = 0 # 0 if second taken from Register
                            # 1 if second taken from pile
                            # 2 if taken from CDB

        self.inv = False # true if last operand is the first in order


        self.FU1 = None  # which FU will generate first operand
        self.FU2 = None  # which FU will generate last operand
        self.RP = -1  # when first operand will be ready
        self.value = None  # first operand

        self.type_operation = None

    def one_clock_cycle(self, CBD):
        if self.RP == 1:
            self.RP = -1
            self.value = CBD.get(self.FU1)
        elif self.RP > 1:
            self.RP = -1



    def __str__(self):
        return f"    {self.bitMux}   | {self.RP} | {self.FU1} | {self.FU2} | {self.value}"


class SS:
    def __init__(self, n_ss):
        # the first ss is the one ex in this cycle
        self.l_ss = [ShiftStation() for i in range(n_ss)]
        self.n = n_ss
        self.csv = "ss.csv"

        with open("ss.csv", "w") as f:
            write = csv.writer(f)
            fields = ["SS", "bitMux","RP","FU1", "FU2", "value"]
            rows = [[str(i), self.l_ss[i].bitMux, self.l_ss[i].RP, self.l_ss[i].FU1, self.l_ss[i].FU2, self.l_ss[i].value] for i in range(n_ss - 1, -1, -1)]
            write.writerow(fields)
            write.writerows(rows)


    def get(self,i):
        return self.l_ss[i]


    def __str__(self):
        res = ""
        for i in range(self.n):
            txt = "\n" + f"SS{i} "+ str(self.get(i))
            res = txt + res
        res = "      bitMux | RP | FU1 | FU2 | value" + res
        return res



    def one_clock_cycle(self,CBD):
        # Update internal values of SS
        for e in self.l_ss:
            e.one_clock_cycle(CBD)

        self.l_ss.append(ShiftStation())
        res = self.l_ss[0]
        self.l_ss.pop(0)

        return res



    def get(self,i):
        return self.l_ss[i]

    def update_i(self, i, bitMux, FU1, FU2, RP, value, type_operation, inv):
        self.l_ss[i].bitMux = bitMux
        self.l_ss[i].FU1 = FU1
        self.l_ss[i].FU2 = FU2
        self.l_ss[i].RP = RP
        self.l_ss[i].value = value
        self.l_ss[i].inv = inv
        self.l_ss[i].type_operation = type_operation


        with open("ss.csv", "a") as f:
            write = csv.writer(f)
            fields = ["SS", "bitMux", "RP", "FU1", "FU2", "value"]
            rows = [[str(i), self.l_ss[i].bitMux, self.l_ss[i].RP, self.l_ss[i].FU1, self.l_ss[i].FU2, self.l_ss[i].value] for i
                    in range(self.n - 1, -1, -1)]
            write.writerow(fields)
            write.writerows(rows)


class PileElement:
    def __init__(self):
        self.value = None
        self.fu = None
        #self.bitUse = -1
        self.RP = -1

    def __str__(self):
        return f"     {self.RP} | {self.fu} | {self.value}"


    def __int__(self, value, fu,RP):
        self.value = value
        self.fu = fu
        #self.bitUse = -1
        self.RP = RP

    def one_clock_cycle(self, CBD):
        if self.RP == 1:
            self.RP = -1
            self.value = CBD.get(self.fu)
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



class Pile:
    def __init__(self, size):
        self.pile = [PileElement() for i in range(size)]
        self.n = size
        self.csv = "pile.csv"

        with open("pile.csv", "w") as f:
            write = csv.writer(f)
            fields = ["Element", "RP", "FU",  "value"]
            rows = [[str(i), self.pile[i].RP, self.pile[i].fu,self.pile[i].value] for i
                    in range(self.n - 1, -1, -1)]
            write.writerow(fields)
            write.writerows(rows)

    def __str__(self):
        res = ""
        for i in range(self.n):
            txt = "\n" + f"Pile{i} "+ str(self.pile[i])
            res = txt + res
        res = "      RP | FU |value" + res
        return res

    def get(self,i):
        return self.pile[i]


    def one_clock_cycle(self, CBD):
        for element in self.pile:
            element.one_clock_cycle(CBD)

        self.pile.append(PileElement())
        res = self.pile[0]
        self.pile.pop(0)

        return res

    def update(self, CDB):
        for element in self.pile:
            if element.RP == 0:
                element.value = CDB
                element.RP = -1

        with open(csv, "a") as f:
            write = csv.writer(f)
            fields = ["Element", "RP", "FU",  "value"]
            rows = [[str(i), self.pile[i].RP, self.pile[i].fu,self.pile[i].value] for i
                    in range(self.n - 1, -1, -1)]
            write.writerow(fields)
            write.writerows(rows)