from enum import Enum

TypeInst = Enum["TypeInst", ["I", "S", "U", "J"]]

class Tags:
    def __init__(self):
        self.tags=



class Instruction:
    def __init__(self, typeInst, typeNum, rs, r1, r2, r3, inm, function):
        self.typeInst = typeInst
        self.typeNum = typeNum
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.rs = rs
        self.inm = inm
        self.function = function

class Instructions:
    def __init__(self):
        self.instList = []
        self.size = 0
    def addInstI1(self, op, r1, r2, r3):
        # Type I -> add x1,x2,x3
        self.instList.append(Instruction(typeInst=TypeInst.I, typeNum=1, r1=r1, r2=r2, r3=r3, function=op))
        self.size = self.size + 1

    def addInstI2(self, op, r1, r2, inm):
        # Tipo I:    Op rd, rs1, Inm12
        self.instList.append(Instruction(typeInst=TypeInst.I, typeNum=2, r1=r1, r2=r2, inm=inm, function=op))
        self.size = self.size + 1

    def addInstI3(self, op, r1, r2, inm):
        # Tipo I:    Op rd, rs1, Shamt5
        self.instList.append(Instruction(typeInst=TypeInst.I, typeNum=3, r1=r1, r2=r2, inm=inm, function=op))
        self.size = self.size + 1

    def addInstI4(self, op, r1, inm, rs):
        # Tipo I:    Op rd, Inm12(rs1)
        self.instList.append(Instruction(typeInst=TypeInst.I, typeNum=4, r1=r1, inm=inm, rs=rs, function=op))
        self.size = self.size + 1

    def addInstI5(self, op):
        # Tipo I:    Op
        self.instList.append(Instruction(typeInst=TypeInst.I, typeNum=5, function=op))
        self.size = self.size + 1

    def addInstI6(self, op, r1, r2, inm):
        # Tipo I: jalr rd, rs1, Inm12 / Etiq
        self.instList.append(Instruction(typeInst=TypeInst.I, typeNum=6, function=op, r1=r1, r2=r2, inm=inm))
        self.size = self.size + 1

    def addInstI7(self, op, r1, inm, rs):
        # Tipo I:    jalr rd, Inm12/Etiq(rs1)
        self.instList.append(Instruction(typeInst=TypeInst.I, typeNum=7, function=op, r1=r1, rs=rs, inm=inm))
        self.size = self.size +1

    def addInstS1(self,op,r1,inm,rs):
        self.instList.append(Instruction(typeInst=TypeInst.S, typeNum=1, function=op, r1=r1, inm=inm, rs=rs))
        self.size = self.size + 1
    def addInstB1(self,op, r1,r2,inm):
        self.instList.append(Instruction(typeInst=TypeInst.B, typeNum=1, function=op, r1=r1, inm=inm, r2=r2))
        self.size = self.size + 1

    def addInstU1(self, op, r1, inm):
        self.instList.append(Instruction(typeInst=TypeInst.U, typeNum=1, function=op, r1=r1, inm=inm))
        self.size = self.size + 1

    def addInstJ1(self, op, r1, inm):
        self.instList.append(Instruction(typeInst=TypeInst.J, typeNum=1, function=op, r1=r1, inm=inm))
        self.size = self.size + 1
