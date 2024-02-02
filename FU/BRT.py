# Binary Reservation Table

class BRT:
    def __init__(self, n_ss):
        self.table = [0]*n_ss

    def __str__(self):
        return str(self.table)

    def get(self, i):
        return self.table[i]

    def occupy_i(self, i):
        # if SS occupied -> 1 in position
        self.table[i] = 1

    def ocupy_range(self,i,tam):
        self.table[i:i+tam] = [1]*tam

    def find_first_free_after(self,ts_max ):
        for index in range(ts_max, len(self.table)):
            if self.table[index] == 0:
                return index-ts_max
        return -1

    def one_clock_cycle(self):
        self.table.pop(0)
        self.table.append(0)

    def n_clocks_cycle(self,n):
        self.table = self.table[n:]
        self.table += [0]*n

