from src.FU import Scoreboard


class Register:
    """
    Represents a single register with its associated properties and state.

    Attributes:
        number (int): Register number.
        rp (int): Remaining cycles to obtain the value from the functional unit.
        fu (str): Name of the functional unit providing the value.
        value (int): Current value stored in the register.
        lock (bool): Whether the register is locked.
    """

    def __init__(self, i):
        self.number = i
        self.rp = 0
        self.fu = None
        self.value = i * 2
        self.lock = False

    def __str__(self):
        return f"R{self.number}: +{self.rp} ({self.fu}) value: {self.value} lock: {self.lock}"


class Registers:
    """
    Manages a collection of registers and their state, supporting scoreboard updates and clock cycles.

    Attributes:
        registers_size (int): Number of registers.
        Registers (list): List of `Register` objects.
        scoreboard (Scoreboard.Scoreboards): The scoreboard managing register usage.
    """

    def __init__(self, registers_size, b_scoreboard):
        self.registers_size = registers_size
        self.Registers = [Register(i) for i in range(registers_size)]
        self.scoreboard = Scoreboard.Scoreboards(registers_size)

    def __str__(self):
        return "\n".join(str(reg) for reg in self.Registers)

    def one_clock_cycle(self, CDB):
        """
        Simulate one clock cycle, updating the state of all registers.

        Args:
            CDB (CDB): Central Data Bus instance for retrieving values.
        """
        for reg in self.Registers:
            reg.lock = False
            if reg.rp == 1:
                type_, index = reg.fu.split("_")
                reg.value = CDB.get(type_.strip(), int(index.strip()))
                reg.fu = None
                reg.rp = 0

            if reg.rp > 0:
                reg.rp -= 1

    def new_inst(self, destination, rp, fu_name):
        """
        Assign a new instruction to a register.

        Args:
            destination (int): Register index.
            rp (int): Remaining cycles to get value from the functional unit.
            fu_name (str): Functional unit name.
        """
        reg = self.Registers[destination]
        reg.rp = rp
        reg.fu = fu_name
        reg.value = None
        reg.lock = False

        self.update_scoreboard()

    def lock(self, register):
        """
        Lock a specific register.

        Args:
            register (int): Register index.
        """
        self.Registers[register].lock = True

    def unlock(self):
        """Unlock all registers."""
        for reg in self.Registers:
            reg.lock = False

    def get_R_i(self, i):
        """
        Retrieve a specific register.

        Args:
            i (int): Register index.

        Returns:
            Register: The requested register.
        """
        return self.Registers[i]

    def get_value(self, i):
        """
        Retrieve the value of a specific register.

        Args:
            i (int): Register index.

        Returns:
            int: Value of the register.
        """
        return self.Registers[i].value

    def get_td(self, i):
        """
        Retrieve the remaining cycles for a specific register.

        Args:
            i (int): Register index.

        Returns:
            int: Remaining cycles.
        """
        return self.Registers[i].rp

    def rp_calculation_type1(self, source1, source2, destination):
        """
        Calculate read and write delays for two source registers and a destination.

        Args:
            source1 (int): Index of the first source register.
            source2 (int): Index of the second source register.
            destination (int): Index of the destination register.

        Returns:
            list: Timing details for scheduling.
        """
        if source2 is None:
            return self.rp_calculation_type2(source1, destination)

        if self.Registers[source1].lock or self.Registers[source2].lock or self.Registers[destination].lock:
            return [True]

        t1 = self.Registers[source1].rp
        t2 = self.Registers[source2].rp

        if t1 >= t2:
            ts_max, ts_min = t1, t2
            reg_max, reg_min = source1, source2
            inv = True
        else:
            ts_max, ts_min = t2, t1
            reg_max, reg_min = source2, source1
            inv = False

        FU1 = f"R{reg_min}" if self.Registers[reg_min].fu is None else self.Registers[reg_min].fu
        FU2 = f"R{reg_max}" if self.Registers[reg_max].fu is None else self.Registers[reg_max].fu

        return [ts_max, ts_min, reg_max, reg_min, FU1, FU2, inv]

    def rp_calculation_type1_inm(self, source1, destination):
        """
        Calculate delays for a source register and an immediate value.

        Args:
            source1 (int): Index of the source register.
            destination (int): Index of the destination register.

        Returns:
            list: Timing details for scheduling.
        """
        if self.Registers[source1].lock or self.Registers[destination].lock:
            return [True]

        t1 = self.Registers[source1].rp
        FU2 = f"R{source1}" if self.Registers[source1].fu is None else self.Registers[source1].fu

        return [t1, -1, source1, "inm", "inm", FU2, True]

    def rp_calculation_type2(self, source, destination):
        """
        Calculate delays for a single source and a destination register.

        Args:
            source (int): Index of the source register.
            destination (int): Index of the destination register.

        Returns:
            list: Timing details for scheduling.
        """
        if self.Registers[source].lock or self.Registers[destination].lock:
            return [True]

        ts_max = self.Registers[source].rp
        FU = self.Registers[source].fu

        return [ts_max, 0, source, -2, "N/A", FU, 0]

    def inst_block(self, lBlock):
        """
        Lock all registers specified in the list.

        Args:
            lBlock (list): List of register indices to lock.
        """
        for reg in lBlock:
            if reg is not None:
                self.Registers[reg].lock = True

    def update_scoreboard(self):
        """Update the scoreboard with the current state of the registers."""
        self.scoreboard.update(self.Registers)
