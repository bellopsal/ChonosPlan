import pandas as pd

class Chronogram:

    def __init__(self):
        self.chronogram = pd.DataFrame(columns=["instruction", "IF_start", "IS_start","EX_start", "WB_start", "total_cycles" ])


    def instruction_issued(self, inst, actual_cycle= None, ts_max= None,rp = None ):
        if self.chronogram[(self.chronogram["instruction"] == inst) & (self.chronogram["EX_start"] == None)].shape[0] == 0:
            # just issued for the first time
            d = pd.DataFrame.from_dict({"instruction":[inst], "IF_start":[actual_cycle-2], "IS_start":[actual_cycle-1],"EX_start":[actual_cycle+ ts_max],"WB_start":[actual_cycle-1+ rp], "total_cycles":[None]})
            #d = pd.DataFrame.from_dict({"instruction":[1], "IF_start":[1], "IS_start":[2],"EX_start":[3],"WB_start":[4], "total_cycles":[4]})
            self.chronogram = pd.concat([self.chronogram, d])
            print(self.chronogram)
        else:
            print("else")
            self.chronogram[(self.chronogram["instruction"] == inst) & (self.chronogram["IS_start"] == None)][0][
                "IS_start"] = actual_cycle
            self.chronogram[(self.chronogram["instruction"] == inst) & (self.chronogram["IS_start"] == None)][0][
                "EX_start"] = ts_max
            self.chronogram[(self.chronogram["instruction"] == inst) & (self.chronogram["IS_start"] == None)][0][
                "WB_start"] = rp
            self.chronogram[(self.chronogram["instruction"] == inst) & (self.chronogram["IS_start"] == None)][0][
                "EX_start"] = rp-self.chronogram[(self.chronogram["instruction"] == inst) and (self.chronogram["IS_start"] == None)][0][
                "IF_start"]

            print(self.chronogram)



