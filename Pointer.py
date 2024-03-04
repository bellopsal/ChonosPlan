class PC:
    def __init__(self, m):
        self.m = m
        self.PC = list()
        self.pointer = 0
        self.inst_blocked = list()

    def instBlock(self):
        self.inst_blocked.append(self.PC[self.pointer - 1])

    def one_clock_cycle(self):
        if len(self.PC) == 0:
            self.PC = list(range(self.m))
        else:
            self.pointer = 0
            last = self.PC[-1] + 1

            self.PC = self.inst_blocked.copy()
            self.inst_blocked = list()

            while len(self.PC) < self.m:
                self.PC.append(last)
                last = last + 1

    def newInstruction(self):
        instIndex = self.PC[self.pointer]
        self.pointer = self.pointer + 1
        return instIndex
