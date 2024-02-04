# Class with all the information needed for the simulator
# of the instructions
# It is not a parser -> once we get the txt parse, we will convert it to
# the class instruction

# Tipo R
#   function r1, r2, r3
#  ["add", "1", "2","3"]


class Program:
    typeInstructions = {
        "add": ["add", "sub"],
        "mult": ["mul", "div"],
        "store": ["lb", "sb"]
    }

    def __init__(self, list_instructions):
        self.instructions = [Instruction(e) for e in list_instructions]
        self.n = len(list_instructions)

    def get(self, i):
        return self.instructions[i]




class Instruction:

    def __init__(self, l):
        #self.type = "suma"
        self.r1 = int(l[1])
        self.r2 = int(l[2])
        self.r3 = int(l[3])
        self.function = l[0]


