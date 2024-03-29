import tkinter as tk
#from tkinter.tix import ScrolledWindow

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


        self.n_ss_l = tk.Label(master, text="nº of SS:")
        self.n_ss_l.pack()
        self.n_ss = tk.Entry(master)
        self.n_ss.pack()
        self.n_ss.insert(0, "8")

        self.n_registers_l = tk.Label(master, text="nº of registers:")
        self.n_registers_l.pack()
        self.n_registers = tk.Entry(master)
        self.n_registers.pack()
        self.n_registers.insert(0, "5")

        self.pile_size_l = tk.Label(master, text="Pile size:")
        self.pile_size_l.pack()
        self.pile_size = tk.Entry(master)
        self.pile_size.pack()
        self.pile_size.insert(0, "3")

        self.memory_size_l = tk.Label(master, text="Memory size:")
        self.memory_size_l.pack()
        self.memory_size = tk.Entry(master)
        self.memory_size.pack()
        self.memory_size.insert(0, "32")

        self.n_add_l = tk.Label(master, text="Nº of add FU :")
        self.n_add_l.pack()
        self.n_add = tk.Entry(master)
        self.n_add.pack()
        self.n_add.insert(0, "4")

        self.latency_add_l = tk.Label(master, text="Latency of add FU :")
        self.latency_add_l.pack()
        self.latency_add = tk.Entry(master)
        self.latency_add.pack()
        self.latency_add.insert(0, "2")

        self.n_mult_l = tk.Label(master, text="Nº of mult FU:")
        self.n_mult_l.pack()
        self.n_mult = tk.Entry(master)
        self.n_mult.pack()
        self.n_mult.insert(0, "3")

        self.latency_mult_l = tk.Label(master, text="Latency of mult FU :")
        self.latency_mult_l.pack()
        self.latency_mult = tk.Entry(master)
        self.latency_mult.pack()
        self.latency_mult.insert(0, "3")

        self.n_store_l = tk.Label(master, text="Nº of store FU:")
        self.n_store_l.pack()
        self.n_store = tk.Entry(master)
        self.n_store.pack()
        self.n_store.insert(0, "2")

        self.latency_store_l = tk.Label(master, text="Latency of store FU :")
        self.latency_store_l.pack()
        self.latency_store = tk.Entry(master)
        self.latency_store.pack()
        self.latency_store.insert(0, "2")

        self.m_l = tk.Label(master, text="Multiplicity:")
        self.m_l.pack()
        self.m = tk.Entry(master)
        self.m.pack()
        self.m.insert(0, "5")

        self.b_hs_l = tk.Label(master, text="HS?:")
        self.b_hs_l.pack()
        self.b_hs = tk.BooleanVar(value=True)
        self.true_radio = tk.Radiobutton(master, text="True", variable=self.b_hs, value=True)
        self.true_radio.pack()

        self.false_radio = tk.Radiobutton(master, text="False", variable=self.b_hs, value=False)
        self.false_radio.pack()

        self.n_hs_l = tk.Label(master, text="Nº of HS:")
        self.n_hs_l.pack()
        self.n_hs = tk.Entry(master)
        self.n_hs.pack()
        self.n_hs.insert(0, "10")

        self.n_cycles_l = tk.Label(master, text="Nº of future cycles:")
        self.n_cycles_l.pack()
        self.n_cycles = tk.Entry(master)
        self.n_cycles.pack()
        self.n_cycles.insert(0, "120")

        self.b_hs_l = tk.Label(master, text="Keep past cycles?:")
        self.b_hs_l.pack()
        self.b_hs = tk.BooleanVar(value=True)
        self.true_radio = tk.Radiobutton(master, text="True", variable=self.b_hs, value=True)
        self.true_radio.pack()
        self._radio = tk.Radiobutton(master, text="True", variable=self.b_hs, value=True)
        self.true_radio.pack()



        self.start_button = tk.Button(master, text="START", command=self.start)
        self.start_button.pack()

        self.next_cycle_button = tk.Button(self.master, text="next cycle", command=self.next_cycle)
        self.next_cycle_button.pack()


    def scroll_text(self, *args):
        self.text_widget.yview(*args)

    def start(self):
        self.hide()
        self.next_cycle_button.pack()
        scrollbar = tk.Scrollbar(self.master, command=self.scroll_text)
        scrollbar.pack(side="right", fill="y")


        instrucciones = [Inst("add", r1=1, r2=1, r3=2),
                         Inst("add", r1=3, r2=2, r3=1),
                         Inst("mul", r1=2, r2=1, r3=3),

                         Inst("mul", r1=4, r2=3, r3=2),
                         Inst("add", r1=0, r2=0, r3=1),
                         Inst("mul", r1=3, r2=3, r3=3),
                         Inst("mul", r1=0, r2=3, r3=3),
                         Inst("mul", r1=1, r2=0, r3=0),
                         Inst("add", r1=3, r2=1, r3=1)]

        self.simulador =Simulador.Simulador_1_FU(list_program = instrucciones,
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





        '''with open("test.html", "r") as f:
            html_content = f.read()

        self.html_label = HTMLLabel(self.master, html=html_content)
        #self.html_label.pack()
        self.html_label.grid(row=0, columnspan=2)'''

        '''
        with open("test.txt", "r") as f:
            text_content = f.read()

        # Create text widget and insert content
        self.text_widget = tk.Text(self.master)
        self.text_widget.insert(tk.END, text_content)
        self.text_widget.grid(row=0, columnspan = 2)
        
        '''

    def next_cycle(self):
        self.simulador.one_clock_cycle()
        self.simulador.display2(bmux=True)

    def hide(self):
        # Hide all the values
        self.n_ss.pack_forget()
        self.n_registers.pack_forget()
        self.pile_size.pack_forget()
        self.memory_size.pack_forget()
        self.n_add.pack_forget()
        self.n_mult.pack_forget()
        self.n_store.pack_forget()
        self.latency_add.pack_forget()
        self.latency_store.pack_forget()
        self.latency_mult.pack_forget()
        self.m.pack_forget()
        self.n_hs.pack_forget()
        self.true_radio.pack_forget()
        self.false_radio.pack_forget()
        self.n_cycles.pack_forget()

        self.n_ss_l.pack_forget()
        self.n_registers_l.pack_forget()
        self.pile_size_l.pack_forget()
        self.memory_size_l.pack_forget()
        self.n_add_l.pack_forget()
        self.n_mult_l.pack_forget()
        self.n_store_l.pack_forget()
        self.latency_add_l.pack_forget()
        self.latency_store_l.pack_forget()
        self.latency_mult_l.pack_forget()
        self.m_l.pack_forget()
        self.n_hs_l.pack_forget()
        self.true_radio.pack_forget()
        self.false_radio.pack_forget()
        self.n_cycles_l.pack_forget()
        self.b_hs_l.pack_forget()







def main():
    root = tk.Tk()
    calculator = app(root)
    root.mainloop()


if __name__ == "__main__":
    main()