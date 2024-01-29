class ShiftStation:
    def __init__(self):
        self.bitInUse = 0
        self.bitAvail = 0  # first operand available 1 or not
        self.bitMux = None # 0 if second taken from Register
                            # 1 if taken from other op
                            # 2 if second taken from pile


        self.FU1 = None  # which FU will generate first operand
        self.FU2 = None  # which FU will generate last operand
        self.RP = -1  # when first operand will be ready
        self.value = None  # first operand

        self.type_operation = None

    def one_clock_cycle(self):
        if self.bitInUse == 1 and self.bitAvail == 0:
            self.RP = self.RP - 1



    def __str__(self):
        return f"value = {self.value} -- bitinUse = {self.bitInUse}--bitMux {self.bitMux}-- bitAv {self.bitAvail}-- RP {self.RP}"

class SS:
    def __init__(self, n_ss):
        # the first ss is the one ex in this cycle
        self.SS = [ShiftStation() for i in range(n_ss)]
        self.n = n_ss

    def __str__(self):
        res = ""
        for i in range(self.n):
            txt = "\n" + f"SS{i}"+ str(self.SS[i])
            res = txt + res

        return res

    def one_clock_cycle(self):
        self.SS.pop(0)
        self.SS.append(ShiftStation())
        for e in self.SS:
            e.one_clock_cycle()


    def get(self,i):
        return self.SS[i]

    def update_i(self, i, bitAvail, bitMux, FU1, FU2, RP, value, type_operation):
        self.SS[i].bitInUse = 1
        self.SS[i].bitAvail = bitAvail
        self.SS[i].bitMux = bitMux
        self.SS[i].FU1 = FU1
        self.SS[i].FU2 = FU2
        self.SS[i].RP = RP
        self.SS[i].value = value
        self.SS[i].type_operation = type_operation

    def update(self, CDB):
        for ss in self.SS:
            if ss.bitInUse == 1 and ss.bitAvail == 0 and ss.RP == 0 :
                ss.value = CDB
                ss.bitAvail = 27
                ss.RP = -1


