import csv


class Memory:
    def __init__(self, size):
        self.memory = [0] * size
        self.ready = [0] * size
        self.size = size

        with open("memory.csv", "w") as f:
            write = csv.writer(f)
            write.writerow(range(size))
            write.writerow(self.memory)

    def one_clock_cycle(self):
        self.ready = [e - 1 if e > 0 else e for e in self.ready]

    def putValues(self, values):
        self.memory = values


    def put(self, pos, value, ready):
        self.memory[pos] = value
        self.ready[pos] = ready

    def get(self, pos):
        return self.memory[pos]

    def __str__(self):
        txt = "---Memory---\n"
        l = [self.memory[n:n + 8] for n in range(0, self.size, 8)]
        for i in range(len(l)):
            txt = txt + f"{i} | {str(l[i])} \n"
        return txt

    def dump_csv(self):
        with open("memory.csv", "a") as f:
            write = csv.writer(f)
            write.writerow(self.memory)
