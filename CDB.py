
class CDB:

    def __init__(self):
        self.add = []
        self.store = []
        self.mult = []

    def __str__(self):
        txt= f"CBD: \n     add: {self.add} \n     store: {self.store} \n     mult: {self.mult }"
        return txt

    def get(self,strValue, index):
        if strValue == "add":
            return self.add[index]
        elif strValue == "store":
            return self.store[index]
        elif strValue == "mult":
            return self.mult[index]

    def update(self, add, store, mult):
        self.add = add
        self.store = store
        self.mult = mult
