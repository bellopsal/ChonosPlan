
class CDB:

    def __init__(self):
        self.add = None
        self.store = None
        self.mult = None

    def __str__(self):
        txt= f"CBD: \n     add: {self.add} \n     store: {self.store} \n     mult: {self.mux }"
        return txt

    def get(self,strValue):
        if strValue == "add":
            return self.add
        elif strValue == "store":
            return self.store
        elif strValue == "mult":
            return self.mult

    def update(self, add, store, mux):
        self.add = add
        self.store = store
        self.mux = mux
