import csv


class Memory:
    def __init__(self, size):
        self.memory = [0]*size
        self.size = size

        with open("memory.csv", "w") as f:
            write = csv.writer(f)
            write.writerow(range(size))
            write.writerow(self.memory)

    def __str__(self):
        txt = "---Memory---\n"
        l = [self.memory[n:n+8] for n in range(0,self.size, 8)]
        for i in range(len(l)):
            txt = txt + f"{i} | {str(l[i])} \n"
        return txt

    def get(self,i):
        return self.memory[i]

    def put(self, i, value):
        self.memory[i]=value

    def dump_csv(self):
        with open("memory.csv", "a") as f:
            write = csv.writer(f)
            write.writerow(self.memory)

