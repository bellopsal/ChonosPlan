# Binary Reservation Table

class BRT:
    def __init__(self, n_cycles):
        self.table = [0] * n_cycles
        #self.latency = latency

    def __str__(self):
        return str(self.table)

    def get(self, i):
        return self.table[i]

    def occupy_i(self, i):
        # if SS occupied -> 1 in position
        self.table[i] = 1

    # def ocupy_range(self,i):
    #     self.table[i:i+self.latency] = [1]*self.latency

    def find_first_after(self, ts_max):
        if ts_max >= len(self.table):
            return -1
        else:
            end = ts_max + 4 if ts_max + 4 < len(self.table) else len(self.table)-1
            for index in range(ts_max, end):
                if self.table[index] == 0:
                    return index-ts_max
            return -1

    def one_clock_cycle(self):
        self.table.pop(0)
        self.table.append(0)

    def n_clocks_cycle(self,n):
        self.table = self.table[n:]
        self.table += [0]*n

