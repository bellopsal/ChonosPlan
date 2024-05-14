
class CDB:

    def __init__(self):
        self.alu = []
        self.div = []
        self.store = []
        self.load = []
        self.mult = []

    def __str__(self):
        txt= f"CBD: \n     alu: {self.alu} \n     store: {self.store}\n     load: {self.load } \n     mult: {self.mult }\n     div: {self.div }"
        return txt

    def get(self, FU_type, index):
        if FU_type == "alu":
            return self.alu[index]
        elif FU_type == "store":
            return self.store[index]
        elif FU_type == "mult":
            return self.mult[index]
        elif FU_type == "div":
            return self.div[index]
        elif FU_type == "load":
            return self.load[index]

    def update(self, alu, store, mult, div, load):
        self.alu = alu
        self.store = store
        self.mult = mult
        self.load = load
        self.div = div
