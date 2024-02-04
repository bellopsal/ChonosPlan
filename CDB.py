
class CDB:

    def __init__(self):
        self.add = None
        self.store = None
        self.mult = None

    def __str__(self):
        txt= f"CBD: \n     add: {self.add} \n     store: {self.store} \n     mult: {self.mult }"
        return txt

    def get(self,strValue):
        if strValue == "add":
            return self.add
        elif strValue == "store":
            return self.store
        elif strValue == "mult":
            return self.mult

    def update(self, add, store, mult):
        self.add = add
        self.store = store
        self.mult = mult
