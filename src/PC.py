class PC:
    """Simulates a program counter (PC) for instruction sequencing.

    Attributes:
        multiplicity (int): The number of instructions that can be processed concurrently.
        program_size (int): The total number of instructions in the program.
        PC (list): The list of instructions currently being processed.
        pointer (int): The current pointer to the instruction being processed.
        last (int): The index of the last instruction added to the PC.
        inst_locked (list): List of instructions that are blocked.
    """

    def __init__(self, multiplicity, program_size):
        """Initializes the PC with program and processing constraints.

        Args:
            multiplicity (int): Number of instructions to process concurrently.
            program_size (int): Total number of instructions in the program.
        """
        self.multiplicity = multiplicity
        self.program_size = program_size
        self.PC = None
        self.pointer = 0
        self.last = 0
        self.inst_locked = []

    def one_clock_cycle(self):
        """Advances the PC by one clock cycle, adding and unlocking instructions."""
        # Initialization for the first cycle
        if self.PC is None:
            if self.program_size < self.multiplicity:
                self.PC = list(range(self.program_size))
            else:
                self.PC = list(range(self.multiplicity))
            self.last = self.PC[-1]

        # Handling subsequent cycles
        elif self.PC:  # Check if the previous cycle had instructions
            self.pointer = 0
            self.PC = self.inst_locked.copy()
            self.inst_locked = []

            # Fill PC until reaching multiplicity or program limit
            while len(self.PC) < self.multiplicity and self.last < self.program_size - 1:
                self.last += 1
                self.PC.append(self.last)

    def __str__(self):
        """Returns a string representation of the PC state.

        Returns:
            str: A string showing the current and blocked instructions.
        """
        return f"List Instructions: {self.PC}\nBlocked Instructions: {self.inst_locked}\n"

    def inst_lock(self):
        """Locks the last accessed instruction, marking it as blocked."""
        self.inst_locked.append(self.PC[self.pointer - 1])

    def new_instruction(self):
        """Fetches the next instruction to be processed.

        Returns:
            int: The index of the next instruction.
        """
        inst_index = self.PC[self.pointer]
        self.pointer += 1
        return inst_index
