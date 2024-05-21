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
        self.bitMux = None  # 0 if second taken from Register
                        # 1 if second taken from QSD
                        # 2 if taken from CDB
        self.inm = None
        self.inv = False

        self.destination = None
        self.position = None

        self.FU1 = None  # which FU will generate first operand
        self.FU2 = None  # which FU will generate second operand

        self.RP1 = - 1  # when first operand will be ready
        self.RP2 = - 1  # when first operand will be ready

        self.value1 = None  # first operand
        self.value2= None  # first operand

        self.type_operation = None
        self.case_QSD = False


    def empty(self):
        self.bitMux = None
        self.inm = None
        self.inv = False
        self.destination = None
        self.position = None
        self.FU1 = None  # which FU will generate first operand
        self.FU2 = None  # which FU will generate second operand
        self.RP1 = - 1  # when first operand will be ready
        self.RP2 = - 1  # when first operand will be ready
        self.value1 = None  # first operand
        self.value2= None  # first operand
        self.type_operation = None
        self.case_QSD = False


    def one_clock_cycle(self, CDB, updateSS, updateQSD):
        res = False
        self.position = self.position - 1

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

        if (self.case_QSD and self.position == updateQSD) or ((not self.case_QSD) and self.position <= updateSS):
            # time to update SS
            res = True

        return res



    def __str__(self):
        return f"    {self.bitMux}   | {self.RP1} | {self.RP2} | {self.FU1} | {self.FU2} | {self.value1}| {self.value2}"


class HS:
    def __init__(self, n_hs, n_ss, QSD_size):
        # the first ss is the one ex in this cycle
        self.l_hs = [HoldStation() for i in range(n_hs)]
        self.n = n_hs
        self.occupied = [0]*n_hs

        self.updateSS = n_ss - 1
        self.updateQSD = QSD_size -1


    def freeHS(self):
        for index, value in enumerate(self.occupied):
            if value == 0:
                return index
        return -1


    def update(self,i, bitMux, inv,RP1, RP2,destination,position, value1, value2 ,
               FU1 , FU2 , case_QSD, type_operation, inm = None):
        hs = self.l_hs[i]
        hs.bitUse = True
        hs.bitMux = bitMux
        hs.inv = inv
        hs.RP1 = RP1
        hs.RP2 = RP2
        hs.value1 = value1
        hs.value2 = value2
        hs.FU1 = FU1
        hs.inm = inm
        hs.FU2 = FU2
        hs.destination = destination
        hs.position = position
        hs.case_QSD = case_QSD
        hs.type_operation = type_operation
        self.occupied[i] = 1




    def get(self,i):
        return self.l_hs[i]


    def __str__(self):
        res = ""
        for i in range(self.n):
            txt = "\n" + f"SS{i} "+ str(self.get(i))
            res = txt + res
        res = "      bitMux | RP1 | RP2 | FU1 | FU2 | value1 | value2" + res
        return res



    def one_clock_cycle(self,CDB):
        res = []
        #only update if ocuppied
        for i in range(self.n):
            if self.occupied[i] == 1:
                update =self.l_hs[i].one_clock_cycle(CDB, self.updateSS, self.updateQSD)
                if update:
                    self.occupied[i] = 0
                    res.append(i)
                    #self.empty(i)

        return res




    def get(self,i):
        return self.l_hs[i]

    def empty(self, i):
        self.update_i(i,bitMux=None, FU1=None, FU2=None, RP1=-1,RP2=-1,
                      value1=None,value2=None, type_operation=None, inv=None ,destination=None, inm= None)

    def update_i(self, i, bitMux, FU1, FU2, RP1,RP2, value1,value2, type_operation, inv, destination, inm= None):
        self.l_hs[i].bitMux = bitMux
        self.l_hs[i].FU1 = FU1
        self.l_hs[i].FU2 = FU2
        self.l_hs[i].RP1 = RP1
        self.l_hs[i].RP2 = RP2
        self.l_hs[i].value1 = value1
        self.l_hs[i].value2 = value2
        self.l_hs[i].inv = inv
        self.l_hs[i].inm = inm
        self.l_hs[i].destination = destination
        self.l_hs[i].type_operation = type_operation


        with open("hs.csv", "a") as f:
            write = csv.writer(f)
            fields = ["SS", "bitMux", "RP", "FU1", "FU2", "value"]
            rows = [[str(i), self.l_hs[i].bitMux, self.l_hs[i].RP1,self.l_hs[i].RP2, self.l_hs[i].FU1, self.l_hs[i].FU2, self.l_hs[i].value1, self.l_hs[i].value2] for i
                    in range(self.n - 1, -1, -1)]
            write.writerow(fields)
            write.writerows(rows)

