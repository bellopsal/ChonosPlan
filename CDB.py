
class CDB:

    def __init__(self):
        self.add = None
        self.store = None
        self.mux = None

    def __str__(self):
        txt= f"CBD: \n     add: {self.add} \n     store: {self.store} \n     mux: {self.mux }"
        return txt

    def update(self, add, store, mux):
        self.add = add
        self.store = store
        self.mux = mux
