import csv

# Define the instruction types and their classifications.
typeInstructions = {
    "jump": ["j", "beq"],
    "alu": [
        "add", "sub", "addi", "subi", "xor", "xori", "and", "andi",
        "or", "ori", "sll", "srl", "slt", "slli", "srli", "slti", "not"
    ],
    "mult": ["mult", "multi"],
    "div": ["div", "divi"],
    "store": ["sb"],
    "load": ["lb"],
    "trans": ["sqrt", "log", "sin", "cos"]
}


class Program:
    """
    Represents a program consisting of a sequence of instructions and their associated tags.

    Attributes:
        instructions (list): List of `Instruction` objects.
        program_size (int): Number of instructions in the program.
        dict_tags (dict): Dictionary mapping tags to their corresponding instruction indices.
    """

    def __init__(self, file):
        """
        Initialize the Program by reading instructions from a CSV file.

        Args:
            file (str): Path to the CSV file containing the program instructions.
        """
        self.program_size = 0
        self.instructions = []
        self.dict_tags = {}

        with open(file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                tag = row["tag"].strip() if row.get("tag") else None
                inst = Instruction(
                    operation=row["operation"],
                    tag=tag,
                    r1=int(row["r1"]) if row.get("r1") and row["r1"].strip() else None,
                    r2=int(row["r2"]) if row.get("r2") and row["r2"].strip() else None,
                    r3=int(row["r3"]) if row.get("r3") and row["r3"].strip() else None,
                    rs1=int(row["rs1"]) if row.get("rs1") and row["rs1"].strip() else None,
                    inm=int(row["inm"]) if row.get("inm") and row["inm"].strip() else None,
                    offset=row["offset"].strip() if row.get("offset") else None,
                    BTB=bool(int(row["BTB"])) if row.get("BTB") and row["BTB"].strip() else True
                )

                if tag is not None:
                    self.dict_tags[tag] = self.program_size

                self.instructions.append(inst)
                self.program_size += 1

    def get(self, i):
        """
        Retrieve an instruction at a specific index.

        Args:
            i (int): Index of the instruction.

        Returns:
            Instruction: The instruction at the specified index.
        """
        return self.instructions[i]

    def __str__(self):
        """
        String representation of the program, listing all instructions.

        Returns:
            str: Formatted string of all instructions.
        """
        return "\n".join(f"{i}: {self.get(i)}" for i in range(self.program_size))


class Instruction:
    """
    Represents a single instruction with its associated attributes and metadata.

    Attributes:
        tag (str): Instruction tag, if any.
        r1, r2, r3 (int): Register indices for the instruction.
        rs1 (int): Single source register for certain instruction types.
        inm (int): Immediate value for the instruction.
        offset (str): Offset value for certain instructions.
        BTB (bool): Branch Target Buffer prediction (for jump instructions).
        function (str): The operation of the instruction.
        fu_type (str): Functional unit type for the instruction (e.g., "alu", "jump").
    """

    def __init__(self, operation, tag=None, r1=None, r2=None, r3=None, rs1=None, inm=None, offset=None, BTB=True):
        """
        Initialize an Instruction with all possible fields.

        Args:
            operation (str): The operation or function of the instruction.
            tag (str, optional): Tag for the instruction. Defaults to None.
            r1, r2, r3 (int, optional): Register indices. Defaults to None.
            rs1 (int, optional): Single source register. Defaults to None.
            inm (int, optional): Immediate value. Defaults to None.
            offset (str, optional): Offset value. Defaults to None.
            BTB (bool, optional): Branch Target Buffer prediction. Defaults to True.
        """
        self.tag = tag
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.rs1 = rs1
        self.inm = inm
        self.offset = offset
        self.BTB = BTB
        self.function = operation

        # Determine functional unit type based on the operation.
        self.fu_type = next((key for key, values in typeInstructions.items() if operation in values), None)

    def __str__(self):
        """
        String representation of the instruction.

        Returns:
            str: Formatted string describing the instruction.
        """
        parts = []
        if self.tag:
            parts.append(f"{self.tag}:")
        parts.append(self.function)

        if self.r1 is not None:
            parts.append(f"R{self.r1}")
        if self.r2 is not None:
            parts.append(f", R{self.r2}")
        if self.r3 is not None:
            parts.append(f", R{self.r3}")
        if self.inm is not None:
            parts.append(f", {self.inm}")
        if self.rs1 is not None:
            parts.append(f", R{self.rs1}")
        if self.offset is not None:
            parts.append(f", {self.offset}")
        if self.fu_type == "jump":
            parts.append(f"(BTB: {self.BTB})")

        return " ".join(parts)
