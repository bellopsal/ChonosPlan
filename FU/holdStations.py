import csv

def CDBhelper(FU,CDB):
    sep_list = FU.split("_")
    fu = sep_list[0].strip()
    index = int(sep_list[1].strip())
    return CDB.get(fu,index)

class HoldStation:
    def __init__(self):
        #self.bitInUse = 0   # if the ss is in use ( with data in it)
        #self.bitAvail = 0  # first operand available 1 or not
        self.bitMux = 0  # 0 if second taken from Register
                        # 1 if second taken from pile
                        # 2 if taken from CDB
        self.inm = None
        self.inv = False
        self.bitUse = False


        self.FU1 = None  # which FU will generate first operand
        self.FU2 = None  # which FU will generate second operand

        self.RP1 = - 1  # when first operand will be ready
        self.RP2 = - 1  # when first operand will be ready

        self.value1 = None  # first operand
        self.value1 = None  # first operand

        self.type_operation = None

    def one_clock_cycle(self, CDB, n_ss, n_pile):
        res = None
        if self.bitUse:
            if self.RP1 == 1:
                self.RP1 = -1
                self.value1 = CDBhelper(self.FU1,CDB)
            elif self.RP1 > 1:
                self.RP1 = self.RP1 - 1

            if self.RP2 == 1:
                self.RP2 = -1
                self.value2 = CDBhelper(self.FU2,CDB)
            elif self.RP2 > 1:
                self.RP2 = self.RP2 - 1

            if self.RP2 < n_pile and self.RP1 < n_ss:
                res = self
                self.bitUse = False
        return res





    def __str__(self):
        return f"    {self.bitMux}   | {self.RP1} | {self.RP2} | {self.FU1} | {self.FU2} | {self.value1}| {self.value2}"


class HS:
    def __init__(self, n_hs):
        # the first ss is the one ex in this cycle
        self.l_hs = [HoldStation() for i in range(n_hs)]
        self.n = n_hs
        self.csv = "hs.csv"

        with open("ss.csv", "w") as f:
            write = csv.writer(f)
            fields = ["SS", "bitMux","RP1","RP2","FU1", "FU2", "value1","value1"]
            rows = [[str(i), self.l_hs[i].bitMux, self.l_hs[i].RP1, self.l_hs[i].RP2, self.l_hs[i].FU1, self.l_hs[i].FU2, self.l_hs[i].value1,self.l_hs[i].value2] for i in range(n_hs - 1, -1, -1)]
            write.writerow(fields)
            write.writerows(rows)


    def get(self,i):
        return self.l_hs[i]


    def __str__(self):
        res = ""
        for i in range(self.n):
            txt = "\n" + f"SS{i} "+ str(self.get(i))
            res = txt + res
        res = "      bitMux | RP1 | RP2 | FU1 | FU2 | value1 | value2" + res
        return res



    def one_clock_cycle(self,CDB,n_ss, n_pile):
        exitHS = []
        for e in self.l_hs:
            exitHS.append(e.one_clock_cycle(CDB))

        return exitHS



    def get(self,i):
        return self.l_ss[i]

    def update_i(self, i, bitMux, FU1, FU2, RP, value, type_operation, inv, inm= None):
        self.l_ss[i].bitMux = bitMux
        self.l_ss[i].FU1 = FU1
        self.l_ss[i].FU2 = FU2
        self.l_ss[i].RP = RP
        self.l_ss[i].value = value
        self.l_ss[i].inv = inv
        self.l_ss[i].inm = inm
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

    def one_clock_cycle(self, CDB):
        if self.RP == 1:
            self.RP = -1
            self.value = CDBhelper(self.fu,CDB)
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


    def one_clock_cycle(self, CDB, bitMux, FU2):
        if bitMux == 2:
            self.pile[1].value = CDBhelper(FU2, CDB)
            self.pile[1].RP = -1

        for element in self.pile:
            element.one_clock_cycle(CDB)

        self.pile.append(PileElement())
        res = self.pile[0]
        self.pile.pop(0)

        return res

    # def update(self, CDB):
    # #     for element in self.pile:
    # #         if element.RP == 0:
    # #             element.value = CDB.get(FU2)
    # #             element.RP = -1
    #
    #     with open(self.csv, "a") as f:
    #         write = csv.writer(f)
    #         fields = ["Element", "RP", "FU",  "value"]
    #         rows = [[str(i), self.pile[i].RP, self.pile[i].fu,self.pile[i].value] for i
    #                 in range(self.n - 1, -1, -1)]
    #         write.writerow(fields)
    #         write.writerows(rows)