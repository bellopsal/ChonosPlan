# Class with all the information needed for the simulator
# of the instructions
# It is not a parser -> once we get the txt parse, we will convert it to
# the class instruction

# Tipo R
#   function r1, r2, r3
#  ["add", "1", "2","3"]

typeInstructions = {
    "add": ["add", "sub"],
    "mult": ["mul", "div"],
    "store": ["lb", "sb"]
}



class Program:


    def __init__(self, list_instructions):
        self.instructions = list_instructions
        self.n = len(list_instructions)

    def get(self, i):
        return self.instructions[i]




class Instruction:

    def __init__(self, operation, r1=None, r2=None, r3=None, rd=None, rs1=None, inm=None):
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.rd = rd
        self.rs1 = rs1
        self.inm = inm

        self.function = operation

        for key, values in typeInstructions.items():
            if operation in values:
                self.fu_type = key

    def __str__(self):
        txt = self.function + " "
        if self.r1 != None: txt = txt + "R"+str(self.r1) + ", "
        if self.r2 != None: txt = txt + "R"+str(self.r2) + ", "
        if self.r2 != None: txt = txt + "R"+str(self.r3) + ""
        if self.rd != None: txt = txt + "R"+str(self.rd) + ", "
        if self.inm != None: txt = txt + str(self.inm) +"("
        if self.rs1 != None: txt = txt + "R"+str(self.rs1) + ")"
        return txt



