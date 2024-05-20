class PC:
    def __init__(self, multiplicity, program_size):
        self.multiplicity = multiplicity
        self.PC = None
        self.pointer = 0
        self.last = 0
        self.inst_locked = list()
        self.program_size = program_size

    def one_clock_cycle(self):
        # Initialisation for first cycle
        if self.PC is None:
            if self.program_size< self.multiplicity:
                self.PC = list(range(self.program_size))
                self.last = self.PC[-1]
            else:
                self.PC = list(range(self.multiplicity))
                self.last = self.PC[-1]

        # For the rest of the cycles
        elif len(self.PC) > 0: # check if cycle before had instructions
            self.pointer = 0
            self.PC = self.inst_locked.copy()
            self.inst_locked = list()

            while len(self.PC) < self.multiplicity and self.last < self.program_size -1:
                self.last = self.last + 1
                self.PC.append(self.last)


    def __str__(self):
        res = f"List Instructions: {self.PC}\n Blocked Instructions: {self.inst_locked}\n"
        return res

    def inst_lock(self):
        self.inst_locked.append(self.PC[self.pointer - 1])


    def new_instruction(self):
        instIndex = self.PC[self.pointer]
        self.pointer = self.pointer + 1
        return instIndex
