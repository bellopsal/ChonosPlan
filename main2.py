import tkinter as tk
import sys
from io import StringIO
from rich.console import Console

# Create a Tkinter application window
window = tk.Tk()
window.title("Rich Console Output")

# Create a Text widget to display console output
output_text = tk.Text(window, wrap="word")
output_text.pack(fill="both", expand=True)

# Redirect stdout and stderr to the Text widget
sys.stdout = StringIO()
sys.stderr = StringIO()

# Create a Rich console instance
console = Console()

# Function to write to the redirected stdout and stderr
def write_to_console(text):
    console.print(text, end="")

# Replace the default stdout and stderr write methods
sys.stdout.write = write_to_console
sys.stderr.write = write_to_console

# Example usage of printing to console
print("This is a test output to console.")

# Run the Tkinter event loop
window.mainloop()