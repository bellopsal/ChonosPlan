import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

class Chronogram:

    def __init__(self):
        self.chronogram = pd.DataFrame(columns=["instruction", "IF_start", "IS_start","EX_start", "WB_start", "total_cycles" ])


    def instruction_issued(self, inst, actual_cycle= -1, ts_max= -1,rp = -1):
        if self.chronogram[(self.chronogram["instruction"] == inst) & (self.chronogram["EX_start"] == -1)].shape[0] == 0:
            # just issued for the first time
            d = pd.DataFrame.from_dict({"instruction":[inst], "IF_start":[actual_cycle-1],
                                        "IS_start":[actual_cycle],"EX_start":[ -1 if ts_max == -1 else actual_cycle+ts_max+1],
                                        "WB_start":[-1 if rp == -1 else actual_cycle + rp], "total_cycles":[0]})
            #d = pd.DataFrame.from_dict({"instruction":[1], "IF_start":[1], "IS_start":[2],"EX_start":[3],"WB_start":[4], "total_cycles":[4]})
            self.chronogram = pd.concat([self.chronogram, d], ignore_index=True)
            #print(self.chronogram)
        else:
            first_index = self.chronogram[(self.chronogram["instruction"] == inst) & (self.chronogram["EX_start"]==-1)]
            if ts_max != -1:
                self.chronogram.iloc[first_index.index[0], [2, 3, 4]] = [actual_cycle,actual_cycle+ts_max+1, actual_cycle +rp]

    def plot_cycles(self):

        def hat_graph(ax, xlabels, values, group_labels, color, label):
            """
            Create a hat graph.

            Parameters
            ----------
            ax : matplotlib.axes.Axes
                The Axes to plot into.
            xlabels : list of str
                The category names to be displayed on the x-axis.
            values : (M, N) array-like
                The data values.
                Rows are the groups (len(group_labels) == M).
                Columns are the categories (len(xlabels) == N).
            group_labels : list of str
                The group labels displayed in the legend.
            """
            self.chronogram["total_cycles"] = self.chronogram["WB_start"] - self.chronogram["IS_start"] + 1

            values = np.asarray(values)
            x = np.arange(values.shape[1])
            ax.set_xticks(x, labels=xlabels)
            max_value = self.chronogram.max(skipna=True).max(skipna=True)
            max_value = 4 if max_value is np.nan else max_value +2
            ax.set_yticks(np.arange(0, int(max_value), 1))
            spacing = 0.3  # spacing between hat groups
            width = 1
            heights0 = values[0]
            for i, (heights, group_label) in enumerate(zip(values, group_labels)):
                style = {'fill': False} if i == 0 else {'edgecolor': 'black','color':color }
                if heights is not None:

                    if i == 1:
                        p = ax.bar(x, heights - heights0, width, bottom=heights0, label=label, **style)
                    else:
                        p = ax.bar(x, heights - heights0, width, bottom=heights0, **style)


            plt.grid()


        xlabels = self.chronogram["instruction"]
        playerA = self.chronogram["IF_start"]
        playerB = self.chronogram["IS_start"]

        fig, ax = plt.subplots()
        ax.grid(axis="y")
        plt.xticks(rotation=90)
        plt.yticks(rotation=90)
        plt.xlabel("Instructions")
        plt.ylabel("Cycles")
        hat_graph(ax, xlabels, [playerA, playerB], ['Player A', 'Player B'], "plum", "IF")

        playerA = self.chronogram["IS_start"]
        playerB = self.chronogram["EX_start"]
        hat_graph(ax, xlabels, [playerA, playerB], ['Player A', 'Player B'], "aquamarine", "IS")

        playerA = self.chronogram["EX_start"]
        playerB = self.chronogram["WB_start"]
        hat_graph(ax, xlabels, [playerA, playerB], ['Player A', 'Player B'], "lightblue", "EX")

        playerA = self.chronogram["WB_start"]
        playerB = self.chronogram["WB_start"] + 1
        hat_graph(ax, xlabels, [playerA, playerB], ['Player A', 'Player B'], "teal", "WB")

        # plt.grid(axis="y")
        # plt.show()
        plt.tight_layout()
        legend = plt.legend(reverse = True)
        for text in legend.get_texts():
            text.set_rotation(90)
        fig.savefig('figure.png')
        image = Image.open('figure.png',)

        rotated_image = image.rotate(270, expand=True)
        rotated_image.save('figure.png')
        #plt.tight_layout()
        #rotated_image.show()

        return image



