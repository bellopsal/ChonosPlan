import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


class Chronogram:
    """Class to track and visualize instruction cycles in a CPU pipeline.

    Attributes:
        chronogram (pd.DataFrame): A DataFrame tracking instruction states and cycle counts.
    """

    def __init__(self):
        """Initializes the Chronogram with an empty DataFrame."""
        self.chronogram = pd.DataFrame(
            columns=["instruction", "IF_start", "IS_start", "EX_start", "WB_start", "total_cycles"]
        )

    def instruction_issued(self, inst, actual_cycle=-1, ts_max=-1, rp=-1):
        """Updates the chronogram when an instruction is issued.

        Args:
            inst (str): The instruction being issued.
            actual_cycle (int): The current cycle when the instruction is issued.
            ts_max (int): Maximum time for an operation to be scheduled.
            rp (int): Register pipeline delay.
        """
        if self.chronogram[
            (self.chronogram["instruction"] == inst) & (self.chronogram["WB_start"] == -1)
        ].shape[0] == 0:
            # First-time issue
            filter_condition = (actual_cycle == ts_max) & (actual_cycle == rp)
            data = pd.DataFrame.from_dict({
                "instruction": [inst],
                "IF_start": [actual_cycle - 1],
                "IS_start": [actual_cycle],
                "EX_start": [-1 if filter_condition else actual_cycle + ts_max + 1],
                "WB_start": [-1 if filter_condition else actual_cycle + rp],
                "total_cycles": [0]
            })
            self.chronogram = pd.concat([self.chronogram, data], ignore_index=True)
        else:
            first_index = self.chronogram[
                (self.chronogram["instruction"] == inst) & (self.chronogram["EX_start"] == -1)
            ]
            if ts_max != actual_cycle:
                self.chronogram.iloc[first_index.index[0], [2, 3, 4]] = [
                    actual_cycle,
                    actual_cycle + ts_max + 1,
                    actual_cycle + rp
                ]

    def plot_cycles(self):
        """Plots a bar chart showing the cycles for each instruction stage.

        Returns:
            PIL.Image.Image: The generated chart as a rotated image.
        """
        def hat_graph(ax, xlabels, values, group_labels, color, label):
            """Creates a hat graph for visualizing cycles.

            Args:
                ax (matplotlib.axes.Axes): The axes to plot on.
                xlabels (list): Labels for the x-axis.
                values (array-like): Data values for the bar plot.
                group_labels (list): Labels for the groups in the legend.
                color (str): Bar color.
                label (str): Label for the bars.
            """
            self.chronogram["total_cycles"] = self.chronogram["WB_start"] - self.chronogram["IS_start"] + 1
            values = np.asarray(values)
            x = np.arange(values.shape[1])
            ax.set_xticks(x, labels=xlabels)
            max_value = self.chronogram.max(skipna=True).max(skipna=True)
            max_value = 4 if max_value is np.nan else max_value + 2
            ax.set_yticks(np.arange(0, int(max_value), 1))
            spacing = 0.3  # Spacing between bar groups
            width = 1
            heights0 = values[0]
            for i, (heights, group_label) in enumerate(zip(values, group_labels)):
                style = {'fill': False} if i == 0 else {'edgecolor': 'black', 'color': color}
                if heights is not None:
                    ax.bar(x, heights - heights0, width, bottom=heights0, label=label if i == 1 else None, **style)

            plt.grid()

        # Adjust stages for plotting
        c_aux = self.chronogram.copy()
        f_same = c_aux[c_aux["WB_start"] == -1].index
        c_aux.iloc[f_same, [3, 4]] = c_aux.iloc[f_same, 1].values.reshape(-1, 1)

        # Plot setup
        fig, ax = plt.subplots()
        fig.set_figheight(10)
        fig.set_figwidth(7)
        ax.grid(axis="y")
        plt.xticks(rotation=90)
        plt.yticks(rotation=90)
        plt.xlabel("Instructions")
        plt.ylabel("Cycles")
        xlabels = self.chronogram["instruction"]

        # Plot each stage
        playerA, playerB = c_aux["WB_start"], c_aux["WB_start"] + 1
        hat_graph(ax, xlabels, [playerA, playerB], ['Player A', 'Player B'], "teal", "WB")

        playerA, playerB = c_aux["EX_start"], c_aux["WB_start"]
        hat_graph(ax, xlabels, [playerA, playerB], ['Player A', 'Player B'], "lightblue", "EX")

        playerA, playerB = c_aux["IS_start"], c_aux["EX_start"]
        hat_graph(ax, xlabels, [playerA, playerB], ['Player A', 'Player B'], "aquamarine", "IS")

        playerA, playerB = c_aux["IF_start"], c_aux["IS_start"]
        hat_graph(ax, xlabels, [playerA, playerB], ['Player A', 'Player B'], "plum", "IF")

        # Finalize plot
        plt.tight_layout()
        legend = plt.legend()
        for text in legend.get_texts():
            text.set_rotation(90)

        fig.savefig('../files/figure.png')
        image = Image.open('../files/figure.png')

        # Rotate the image for better display
        rotated_image = image.rotate(270, expand=True)
        rotated_image.save('../files/figure.png')
        plt.close(fig)

        return rotated_image

    def get_statistics(self, total_cycles):
        """Calculates CPI and mean latency from the recorded chronogram.

        Args:
            total_cycles (int): Total cycles spent for executing instructions.

        Returns:
            tuple: A tuple containing:
                - CPI (float): Cycles per instruction.
                - mean_latency (float): Average latency of instructions.
        """
        self.chronogram["total_cycles"] = self.chronogram["WB_start"] - self.chronogram["IF_start"] + 1
        n_instructions = len(self.chronogram)
        cpi = total_cycles / n_instructions
        mean_latency = self.chronogram[self.chronogram["total_cycles"] >= 0]["total_cycles"].mean()
        return cpi, mean_latency
