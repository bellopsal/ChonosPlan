class CDB:
    """Centralized Data Bus (CDB) for functional unit communication.

    Attributes:
        alu (list): List of ALU functional unit outputs.
        div (list): List of DIV functional unit outputs.
        store (list): List of STORE functional unit outputs.
        load (list): List of LOAD functional unit outputs.
        mult (list): List of MULT functional unit outputs.
        trans (list): List of TRANS functional unit outputs.
    """

    def __init__(self):
        """Initializes the CDB with empty lists for each functional unit."""
        self.alu = []
        self.div = []
        self.store = []
        self.load = []
        self.mult = []
        self.trans = []

    def __str__(self):
        """Returns a string representation of the CDB state.

        Returns:
            str: A formatted string showing the current state of the CDB.
        """
        return (
            f"CDB: \n"
            f"    alu: {self.alu}\n"
            f"    store: {self.store}\n"
            f"    load: {self.load}\n"
            f"    mult: {self.mult}\n"
            f"    div: {self.div}\n"
            f"    trans: {self.trans}"
        )

    def get(self, fu_type, index):
        """Retrieves a value from a specific functional unit by index.

        Args:
            fu_type (str): The type of functional unit ("alu", "store", "load", "mult", "div", "trans").
            index (int): The index of the desired value.

        Returns:
            object: The value at the specified index in the specified functional unit.

        Raises:
            ValueError: If `fu_type` is not a recognized functional unit type.
        """
        if fu_type == "alu":
            return self.alu[index]
        elif fu_type == "store":
            return self.store[index]
        elif fu_type == "mult":
            return self.mult[index]
        elif fu_type == "div":
            return self.div[index]
        elif fu_type == "load":
            return self.load[index]
        elif fu_type == "trans":
            return self.trans[index]
        else:
            raise ValueError(f"Unknown functional unit type: {fu_type}")

    def update(self, alu, store, mult, div, load, trans):
        """Updates the CDB with new lists for each functional unit.

        Args:
            alu (list): New list of ALU functional unit outputs.
            store (list): New list of STORE functional unit outputs.
            mult (list): New list of MULT functional unit outputs.
            div (list): New list of DIV functional unit outputs.
            load (list): New list of LOAD functional unit outputs.
            trans (list): New list of TRANS functional unit outputs.
        """
        self.alu = alu
        self.store = store
        self.mult = mult
        self.load = load
        self.div = div
        self.trans = trans
