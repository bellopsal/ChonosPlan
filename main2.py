import os
import tkinter as tk
#from tkinter.tix import ScrolledWindow
from tkinter import filedialog

import Program
import Simulador
from Program import Instruction as Inst
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import io
from tkhtmlview import HTMLLabel
from tkinter import scrolledtext
import sys

class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget


    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Auto-scroll to the end of the text widget

    def flush(self):
        pass





class app:

    def __init__(self, master):
        self.image = None
        self.master = master
        self.frame_a = tk.Frame()
        self.frame_b = tk.Frame()

        self.frame_inst = tk.Frame()
        self.file_name_label = tk.Label(self.frame_inst, text="No file selected")
        self.file_name_label.pack(fill=tk.Y, side=tk.RIGHT)
        self.button_inst = tk.Button(self.frame_inst, text="Import Instructions csv", command=self.open_file)
        self.button_inst.pack(fill=tk.Y, side=tk.LEFT)
        self.frame_inst.pack()

        self.frame_n_ss = tk.Frame()
        self.n_ss_l = tk.Label(master = self.frame_n_ss, text="nº of SS:")
        self.n_ss_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_ss = tk.Entry(master = self.frame_n_ss)
        self.n_ss.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_ss.insert(0, "8")
        self.frame_n_ss.pack()

        self.frame_n_registers = tk.Frame()
        self.n_registers_l = tk.Label(master = self.frame_n_registers, text="nº of registers:")
        self.n_registers_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_registers = tk.Entry(master = self.frame_n_registers)
        self.n_registers.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_registers.insert(0, "5")
        self.frame_n_registers.pack()

        self.frame_pile_size = tk.Frame()
        self.pile_size_l = tk.Label(master = self.frame_pile_size, text="Pile size:")
        self.pile_size_l.pack(fill=tk.Y, side=tk.LEFT)
        self.pile_size = tk.Entry(master = self.frame_pile_size)
        self.pile_size.pack(fill=tk.Y, side=tk.RIGHT)
        self.pile_size.insert(0, "3")
        self.frame_pile_size.pack()

        self.frame_memory_size = tk.Frame()
        self.memory_size_l = tk.Label(master = self.frame_memory_size, text="Memory size:")
        self.memory_size_l.pack(fill=tk.Y, side=tk.LEFT)
        self.memory_size = tk.Entry(master = self.frame_memory_size)
        self.memory_size.pack(fill=tk.Y, side=tk.RIGHT)
        self.memory_size.insert(0, "32")
        self.frame_memory_size.pack()

        self.frame_n_add = tk.Frame()
        self.n_add_l = tk.Label(master = self.frame_n_add, text="Nº of add FU :")
        self.n_add_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_add = tk.Entry(master = self.frame_n_add)
        self.n_add.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_add.insert(0, "4")
        self.frame_n_add.pack()

        self.frame_latency_add = tk.Frame()
        self.latency_add_l = tk.Label(master = self.frame_latency_add, text="Latency of add FU :")
        self.latency_add_l.pack(fill=tk.Y, side=tk.LEFT)
        self.latency_add = tk.Entry(master = self.frame_latency_add)
        self.latency_add.pack(fill=tk.Y, side=tk.RIGHT)
        self.latency_add.insert(0, "2")
        self.frame_latency_add.pack()

        self.frame_n_mult = tk.Frame()
        self.n_mult_l = tk.Label(master = self.frame_n_mult, text="Nº of mult FU:")
        self.n_mult_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_mult = tk.Entry(master = self.frame_n_mult)
        self.n_mult.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_mult.insert(0, "3")
        self.frame_n_mult.pack()

        self.frame_latency_mult = tk.Frame()
        self.latency_mult_l = tk.Label(master = self.frame_latency_mult, text="Latency of mult FU :")
        self.latency_mult_l.pack(fill=tk.Y, side=tk.LEFT)
        self.latency_mult = tk.Entry(master = self.frame_latency_mult)
        self.latency_mult.pack(fill=tk.Y, side=tk.RIGHT)
        self.latency_mult.insert(0, "3")
        self.frame_latency_mult.pack()

        self.frame_n_store = tk.Frame()
        self.n_store_l = tk.Label(master = self.frame_n_store, text="Nº of store FU:")
        self.n_store_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_store = tk.Entry(master = self.frame_n_store)
        self.n_store.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_store.insert(0, "2")
        self.frame_n_store.pack()

        self.frame_latency_store = tk.Frame()
        self.latency_store_l = tk.Label(master = self.frame_latency_store, text="Latency of store FU :")
        self.latency_store_l.pack(fill=tk.Y, side=tk.LEFT)
        self.latency_store = tk.Entry(master = self.frame_latency_store)
        self.latency_store.pack(fill=tk.Y, side=tk.RIGHT)
        self.latency_store.insert(0, "2")
        self.frame_latency_store.pack()

        self.frame_m = tk.Frame()
        self.m_l = tk.Label(master = self.frame_m, text="Multiplicity:")
        self.m_l.pack(fill=tk.Y, side=tk.LEFT)
        self.m = tk.Entry(master = self.frame_m)
        self.m.pack(fill=tk.Y, side=tk.RIGHT)
        self.m.insert(0, "5")
        self.frame_m.pack()

        self.frame_b_hs = tk.Frame()
        self.b_hs_l = tk.Label(master = self.frame_b_hs, text="HS?:")
        self.b_hs_l.pack(fill=tk.Y, side=tk.LEFT)
        self.b_hs = tk.BooleanVar(value=True)
        self.true_radio = tk.Radiobutton(master = self.frame_b_hs, text="True", variable=self.b_hs, value=True)
        self.true_radio.pack(fill=tk.Y, side=tk.RIGHT)
        self.false_radio = tk.Radiobutton(master = self.frame_b_hs, text="False", variable=self.b_hs, value=False)
        self.false_radio.pack(fill=tk.Y, side=tk.RIGHT)
        self.frame_b_hs.pack()

        self.frame_n_hs = tk.Frame()
        self.n_hs_l = tk.Label(master = self.frame_n_hs, text="Nº of HS:")
        self.n_hs_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_hs = tk.Entry(master = self.frame_n_hs)
        self.n_hs.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_hs.insert(0, "10")
        self.frame_n_add.pack()

        self.frame_n_cycle = tk.Frame()
        self.n_cycles_l = tk.Label(master = self.frame_n_cycle, text="Nº of future cycles:")
        self.n_cycles_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_cycles = tk.Entry(master = self.frame_n_cycle)
        self.n_cycles.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_cycles.insert(0, "120")
        self.frame_n_cycle.pack()





        self.start_button = tk.Button(master, text="START", command=self.start)
        self.start_button.pack()




    def scroll_text(self, *args):
        self.text_widget.yview(*args)

    def start(self):
        self.re_start_button = tk.Button(self.master, text="re-start", command=self.re_start)
        self.re_start_button.pack()
        self.next_cycle_button = tk.Button(self.master, text="next cycle", command=self.next_cycle)
        self.next_cycle_button.pack()
        self.hide()
        self.start_button.pack_forget()
        self.next_cycle_button.pack()
        v = tk.Scrollbar(self.master, command=self.scroll_text)
        v.pack(side="right", fill="y")

        h = tk.Scrollbar(self.master, command=self.scroll_text)
        h.pack(side="bottom", fill="x")


        instrucciones = [Inst("add", r1=1, r2=1, r3=2),
                         Inst("add", r1=3, r2=2, r3=1),
                         Inst("mul", r1=2, r2=1, r3=3),

                         Inst("mul", r1=4, r2=3, r3=2),
                         Inst("add", r1=0, r2=0, r3=1),
                         Inst("mul", r1=3, r2=3, r3=3),
                         Inst("mul", r1=0, r2=3, r3=3),
                         Inst("mul", r1=1, r2=0, r3=0),
                         Inst("add", r1=3, r2=1, r3=1)]

        self.simulador =Simulador.Simulador_1_FU(program = self.program,
                             n_ss = int(self.n_ss.get()),
                             n_registers = int(self.n_registers.get()),

                             pile_size = int(self.pile_size.get()),
                             memory_size=int(self.memory_size.get()),
                             n_add = int(self.n_add.get()),
                             n_mult= int(self.n_mult.get()),
                             n_store = int(self.n_store.get()),
                             latency_add = int(self.latency_add.get()),
                             latency_mult =int(self.latency_mult.get()),
                             latency_store= int(self.latency_store.get()),
                             m=int(self.m.get()),
                             b_hs= self.b_hs.get(),

                             )



        self.text_widget = tk.Text(self.master, wrap="none")
        self.text_widget.pack(side="left", fill="both", expand=True)
        #self.text_widget.grid(row=0, column=0)

        sys.stdout = ConsoleRedirector(self.text_widget)
        sys.stderr = ConsoleRedirector(self.text_widget)

        self.simulador.display2()



    def next_cycle(self):
        self.simulador.one_clock_cycle()
        self.simulador.display2(bmux=True)

    def re_start(self):
        self.text_widget.pack_forget()
        self.re_start_button.pack_forget()

        self.frame_inst.pack()
        self.frame_n_ss.pack()
        self.frame_n_registers.pack()
        self.frame_pile_size.pack()
        self.frame_memory_size.pack()
        self.frame_n_add.pack()
        self.frame_n_mult.pack()
        self.frame_n_store.pack()
        self.frame_latency_add.pack()
        self.frame_latency_store.pack()
        self.frame_latency_mult.pack()
        self.frame_m.pack()
        self.frame_b_hs.pack()
        self.frame_n_hs.pack()
        self.frame_n_cycle.pack()

        self.start_button.pack()
        self.next_cycle_button.pack_forget()

    def hide(self):
        # Hide all the values
        self.frame_inst.pack_forget()
        self.frame_n_ss.pack_forget()
        self.frame_n_registers.pack_forget()
        self.frame_pile_size.pack_forget()
        self.frame_memory_size.pack_forget()
        self.frame_n_add.pack_forget()
        self.frame_n_mult.pack_forget()
        self.frame_n_store.pack_forget()
        self.frame_latency_add.pack_forget()
        self.frame_latency_store.pack_forget()
        self.frame_latency_mult.pack_forget()
        self.frame_m.pack_forget()
        self.frame_b_hs.pack_forget()
        self.frame_n_hs.pack_forget()
        self.frame_n_cycle.pack_forget()

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            file_name = os.path.basename(file_path)
            self.file_name_label.config(text="Selected file: " + file_name)
            self.program = Program.Program(file_path)
            print("Selected file:", file_path)
        else:
            print("No file selected")



def main():
    root = tk.Tk()
    calculator = app(root)
    root.mainloop()


if __name__ == "__main__":
    main()