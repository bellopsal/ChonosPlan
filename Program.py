# Class with all the information needed for the simulator
# of the instructions
# It is not a parser -> once we get the txt parse, we will convert it to
# the class instruction

# Tipo R
#   function r1, r2, r3
#  ["add", "1", "2","3"]
import csv

typeInstructions = {
    "jump": ["j","beq"],
    "add": ["add", "sub", "addi", "subi"],
    "mult": ["mul", "div","muli", "divi"],
    "store": ["lb", "sb"]
}



class Program:
    def __init__(self, list_instructions, dict_names):
        self.instructions = list_instructions
        self.n = len(list_instructions)
        self.dict_names = dict_names

    def get(self, i):
        return self.instructions[i]

    def __init__(self, file):
        self.n = 0
        self.instructions = []
        self.dict_names = {}
        with open(file, newline='') as csvfile:
            # Create a CSV DictReader
            reader = csv.DictReader(csvfile)

            for row in reader:
                tag = row["tag"] if row["tag"] is not None and row["tag"].strip() else None
                inst = Instruction(operation= row["operation"],
                                   tag = tag,
                                   r1=int(row["r1"]) if row["r1"] is not None and row["r1"].strip() else None,
                                   r2=int(row["r2"]) if row["r2"] is not None and row["r2"].strip() else None,
                                   r3=int(row["r3"]) if row["r3"] is not None and row["r3"].strip() else None,
                                   rd=int(row["rd"]) if row["rd"] is not None and row["rd"].strip() else None,
                                   rs1=int(row["rs1"]) if row["rs1"] is not None and row["rs1"].strip() else None,
                                   inm=int(row["inm"]) if row["inm"] is not None and row["inm"].strip() else None,
                                   offset=row["offset"] if row["offset"] is not None and row["offset"].strip() else None,
                                   BTB=bool(int(row["BTB"])) if row["BTB"] is not None and row["BTB"].strip() else True)

                if tag != None:
                    self.dict_names[tag]=self.n

                self.instructions.append(inst)

                self.n = self.n + 1















class Instruction:

    def __init__(self , operation,tag = None, r1=None, r2=None, r3=None, rd=None, rs1=None, inm=None, offset = None, BTB= True):
        self.tag = tag
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.rd = rd
        self.rs1 = rs1
        self.inm = inm

        self.offset = offset
        self.BTB = BTB

        self.function = operation

        for key, values in typeInstructions.items():
            if operation in values:
                self.fu_type = key

    def __str__(self):
        txt = ""
        if self.tag != None: txt = txt + self.tag + ":  "
        txt = txt + self.function + " "
        if self.r1 != None: txt = txt + "R"+str(self.r1) + ", "
        if self.r2 != None: txt = txt + "R"+str(self.r2) + ", "
        if self.r3 != None: txt = txt + "R"+str(self.r3) + ""
        if self.rd != None: txt = txt + "R"+str(self.rd) + ", "
        if self.inm != None: txt = txt + str(self.inm)
        if self.rs1 != None: txt = txt + "R"+str(self.rs1)
        if self.offset != None: txt = txt + "" + str(self.offset)
        if self.fu_type=="jump": txt = txt+ f"(BTB: {self.BTB})"
        return txt



