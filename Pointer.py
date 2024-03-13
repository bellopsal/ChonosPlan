class PC:
    def __init__(self, m, programSize):
        self.m = m
        self.PC = None
        self.pointer = 0
        self.inst_blocked = list()
        self.programSize = programSize

    def __str__(self):
        res = f"List Instructions: {self.PC}\n Blocked Instructions: {self.inst_blocked}\n"
        return res

    def instBlock(self):
        self.inst_blocked.append(self.PC[self.pointer - 1])

    def one_clock_cycle(self):
        if self.PC is None: self.PC = list(range(self.m))
        elif len(self.PC) > 0:
            self.pointer = 0
            last = self.PC[-1] + 1

            self.PC = self.inst_blocked.copy()
            self.inst_blocked = list()

            while len(self.PC) < self.m and last < self.programSize:
                self.PC.append(last)
                last = last + 1



    def newInstruction(self):
        instIndex = self.PC[self.pointer]
        self.pointer = self.pointer + 1
        return instIndex
