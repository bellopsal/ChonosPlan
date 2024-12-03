import csv

class Memory:
    """Simulates a memory module with storage, retrieval, and CSV export capabilities.

    Attributes:
        size (int): The size of the memory.
        memory (list): A list representing the memory contents.
    """

    def __init__(self, size):
        """Initializes the memory with a given size and writes the initial state to a CSV file.

        Args:
            size (int): The size of the memory.
        """
        self.size = size
        self.memory = list(range(size))

        with open("./files/memory.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(range(size))  # Write header
            writer.writerow(self.memory)  # Write initial memory values

    def put_values(self, values):
        """Replaces the entire memory contents with new values.

        Args:
            values (list): A list of values to set in memory.
        """
        self.memory = values

    def put(self, pos, value):
        """Sets a value at a specific memory position.

        Args:
            pos (int): The position in memory to update.
            value (int): The value to set at the specified position.
        """
        self.memory[pos] = value

    def get(self, pos):
        """Retrieves the value at a specific memory position.

        Args:
            pos (int): The position in memory to retrieve.

        Returns:
            int: The value stored at the specified position.
        """
        return self.memory[pos]

    def __str__(self):
        """Returns a string representation of the memory in 8-value chunks.

        Returns:
            str: A formatted string showing the memory contents.
        """
        txt = "---Memory---\n"
        chunks = [self.memory[i:i + 8] for i in range(0, self.size, 8)]
        for i, chunk in enumerate(chunks):
            txt += f"{i} | {chunk} \n"
        return txt

    def dump_csv(self):
        """Appends the current state of memory to a CSV file."""
        with open("./files/memory.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(self.memory)
