import Chronogram
import pandas as pd
import matplotlib.pyplot as plt

class Statistics:
    def __init__(self):
        self.stats = pd.DataFrame.from_dict({"cycle":[0], "inst_issued":[0], "inst_lock": [0],
                                             "CPI":[0], "type_0":[0], "type_1":[0], "type_2":[0],
                                             "type_3":[0],"type_4":[0], "type_5":[0], "type_6":[0],
                                             "type_7":[0], "type_8":[0],"mean_latency":[0]})
        self.totalLock = 0
        self.typeInst = {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
        self.instIssued = 0
        self.cycles = 0
        self.Chronogram = Chronogram.Chronogram()
        self.CPI = 0
        self.mean_latency = 0

    def newCycle(self):
        self.cycles += 1

    def updateTypeInst(self, bitMux):
        self.typeInst[bitMux] += 1

    def increaseTotalLock(self):
        self.totalLock += 1

    def increaseInstIssued(self):
        self.instIssued += 1

    def update_statistics(self):
        self.CPI, self.mean_latency = self.Chronogram.get_statistics(self.cycles)

        stats_aux = pd.DataFrame.from_dict({"cycle":[self.cycles], "inst_issued":[self.instIssued], "inst_lock": [self.totalLock],
                                             "CPI":[self.CPI], "type_0":[self.typeInst.get(0)], "type_1":[self.typeInst.get(1)],
                                            "type_2":[self.typeInst.get(2)],"type_3":[self.typeInst.get(3)],
                                            "type_4":[self.typeInst.get(4)], "type_5":[self.typeInst.get(5)],
                                            "type_6":[self.typeInst.get(6)],
                                             "type_7":[self.typeInst.get(7)], "type_8":[self.typeInst.get(8)],
                                            "mean_latency":[self.mean_latency]})
        self.stats = pd.concat([self.stats, stats_aux])


    def plot_graphs(self):

        fig, axs = plt.subplots(3, 1)
        # Plot on the first subplot
        x = self.stats["cycle"]
        issued_aux = self.stats["inst_issued"].diff().fillna(0)
        lock_aux = self.stats["inst_lock"].diff().fillna(0)
        axs[0].plot(x,issued_aux, label='issued')
        axs[0].plot(x,lock_aux, label='locked')
        #axs[0].set_title('Sine Function')
        axs[0].legend()
        axs[0].grid(True)
        axs[0].set_xticks(x, x)

        axs[1].plot(x,self.stats["CPI"])
        axs[1].set_title('CPI')
        axs[1].grid(True)
        axs[1].set_xticks(x, x)



        axs[2].plot(x,self.stats["type_0"].diff().fillna(0), label = "type_0")
        axs[2].plot(x,self.stats["type_1"].diff().fillna(0), label="type_1")
        axs[2].plot(x,self.stats["type_2"].diff().fillna(0), label="type_2")
        axs[2].plot(x,self.stats["type_3"].diff().fillna(0), label="type_3")
        axs[2].plot(x,self.stats["type_4"].diff().fillna(0), label="type_4")
        axs[2].plot(x,self.stats["type_5"].diff().fillna(0), label="type_5")
        axs[2].plot(x,self.stats["type_6"].diff().fillna(0), label="type_6")
        axs[2].plot(x,self.stats["type_7"].diff().fillna(0), label="type_7")
        axs[2].plot(x,self.stats["type_8"].diff().fillna(0), label="type_8")
        axs[2].set_title('BitMUX')
        axs[2].legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True,  ncol=5, borderpad=0, labelspacing=0)
        axs[2].grid(True)

        #plt.show()
        plt.xticks(x, x)
        plt.tight_layout()
        fig.savefig('stats.png')

