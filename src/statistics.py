import pandas as pd
import matplotlib.pyplot as plt
import Chronogram


class Statistics:
    """
    Tracks and analyzes simulation statistics, including cycles, instructions issued,
    locked instructions, CPI, and latency.

    Attributes:
        stats (pd.DataFrame): DataFrame storing simulation statistics over cycles.
        totalLock (int): Count of locked instructions.
        typeInst (dict): Counts of instructions by type (BitMUX values).
        instIssued (int): Total number of instructions issued.
        cycles (int): Total number of cycles elapsed.
        Chronogram (Chronogram): Instance for tracking and retrieving cycle statistics.
        CPI (float): Cycles Per Instruction.
        mean_latency (float): Mean latency across all instructions.
    """

    def __init__(self):
        """
        Initializes the Statistics object with default values and an empty stats DataFrame.
        """
        self.stats = pd.DataFrame.from_dict({
            "cycle": [0], "inst_issued": [0], "inst_lock": [0],
            "CPI": [0], "type_0": [0], "type_1": [0], "type_2": [0],
            "type_3": [0], "type_4": [0], "type_5": [0], "type_6": [0],
            "type_7": [0], "type_8": [0], "mean_latency": [0]
        })
        self.totalLock = 0
        self.typeInst = {i: 0 for i in range(-1, 9)}
        self.instIssued = 0
        self.cycles = 0
        self.Chronogram = Chronogram.Chronogram()
        self.CPI = 0
        self.mean_latency = 0

    def new_cycle(self):
        """
        Advances the simulation to the next cycle.
        """
        self.cycles += 1

    def update_type_inst(self, bitMux):
        """
        Updates the count of instructions for a given type.

        Args:
            bitMux (int): The type identifier of the instruction.
        """
        self.typeInst[bitMux] += 1
        if bitMux in [4, 5, 8]:
            self.increase_total_lock()
        else:
            self.increase_inst_issued()

    def increase_total_lock(self):
        """
        Increments the total count of locked instructions.
        """
        self.totalLock += 1

    def increase_inst_issued(self):
        """
        Increments the total count of issued instructions.
        """
        self.instIssued += 1

    def update_statistics(self):
        """
        Updates the statistics DataFrame with current metrics.
        """
        self.CPI, self.mean_latency = self.Chronogram.get_statistics(self.cycles)
        self.CPI = self.cycles / self.instIssued if self.instIssued > 0 else float("inf")

        stats_aux = pd.DataFrame.from_dict({
            "cycle": [self.cycles], "inst_issued": [self.instIssued], "inst_lock": [self.totalLock],
            "CPI": [self.CPI], "type_0": [self.typeInst.get(0)], "type_1": [self.typeInst.get(1)],
            "type_2": [self.typeInst.get(2)], "type_3": [self.typeInst.get(3)],
            "type_4": [self.typeInst.get(4)], "type_5": [self.typeInst.get(5)],
            "type_6": [self.typeInst.get(6)], "type_7": [self.typeInst.get(7)],
            "type_8": [self.typeInst.get(8)], "mean_latency": [self.mean_latency]
        })

        self.stats = pd.concat([self.stats, stats_aux])

    def plot_graphs(self):
        """
        Generates and saves visualizations of the simulation statistics.
        """
        fig, axs = plt.subplots(3, 1, figsize=(10, 8))

        # Plot instructions issued and locked
        x = self.stats["cycle"]
        issued_aux = self.stats["inst_issued"].diff().fillna(0)
        lock_aux = self.stats["inst_lock"].diff().fillna(0)
        axs[0].plot(x, issued_aux, label='Issued')
        axs[0].plot(x, lock_aux, label='Locked')
        axs[0].set_title('Instructions Issued vs Locked')
        axs[0].legend()
        axs[0].grid(True)
        axs[0].set_xticks(x)

        # Plot CPI
        axs[1].plot(x, self.stats["CPI"], label='CPI')
        axs[1].set_title('CPI (Cycles Per Instruction)')
        axs[1].grid(True)
        axs[1].set_xticks(x)

        # Plot instruction types (BitMUX)
        for i in range(9):
            axs[2].plot(x, self.stats[f"type_{i}"].diff().fillna(0), label=f"Type {i}")
        axs[2].set_title('Instruction Types (BitMUX)')
        axs[2].legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                      fancybox=True, ncol=5, borderpad=0, labelspacing=0.2)
        axs[2].grid(True)

        # Layout adjustments and save the figure
        plt.tight_layout()
        fig.savefig('../files/stats.png')
        plt.close(fig)
