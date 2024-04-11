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
        self.text_widget = tk.Text(self.master, wrap="none")
        v = tk.Scrollbar(self.master, command=self.scroll_text)
        v.pack(side="right", fill="y")

        h = tk.Scrollbar(self.master, command=self.scroll_text)
        h.pack(side="bottom", fill="x")
        self.full_frame = tk.Frame()
        self.frame_a = tk.Frame(master=self.full_frame, highlightbackground="black", highlightthickness=2)
        self.frame_b = tk.Frame(master=self.full_frame,highlightbackground="black", highlightthickness=2)

        l = tk.Label(self.frame_a, text="Configuration")
        l.pack()
        l = tk.Label(self.frame_b, text="Display Settings")
        l.pack()

        self.frame_inst = tk.Frame(master=self.frame_a)
        self.file_name_label = tk.Label(self.frame_inst, text="No file selected")
        self.file_name_label.pack(fill=tk.Y, side=tk.RIGHT)
        self.button_inst = tk.Button(self.frame_inst, text="Import Instructions csv", command=self.open_file)
        self.button_inst.pack(fill=tk.Y, side=tk.LEFT)
        self.frame_inst.pack()

        self.frame_n_ss = tk.Frame(master=self.frame_a)
        self.n_ss_l = tk.Label(master = self.frame_n_ss, text="nº of SS:")
        self.n_ss_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_ss = tk.Entry(master = self.frame_n_ss)
        self.n_ss.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_ss.insert(0, "8")
        self.frame_n_ss.pack()

        self.frame_n_registers = tk.Frame(master=self.frame_a)
        self.n_registers_l = tk.Label(master = self.frame_n_registers, text="nº of registers:")
        self.n_registers_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_registers = tk.Entry(master = self.frame_n_registers)
        self.n_registers.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_registers.insert(0, "5")
        self.frame_n_registers.pack()

        self.frame_pile_size = tk.Frame(master=self.frame_a)
        self.pile_size_l = tk.Label(master = self.frame_pile_size, text="Pile size:")
        self.pile_size_l.pack(fill=tk.Y, side=tk.LEFT)
        self.pile_size = tk.Entry(master = self.frame_pile_size)
        self.pile_size.pack(fill=tk.Y, side=tk.RIGHT)
        self.pile_size.insert(0, "3")
        self.frame_pile_size.pack()

        self.frame_memory_size = tk.Frame(master=self.frame_a)
        self.memory_size_l = tk.Label(master = self.frame_memory_size, text="Memory size:")
        self.memory_size_l.pack(fill=tk.Y, side=tk.LEFT)
        self.memory_size = tk.Entry(master = self.frame_memory_size)
        self.memory_size.pack(fill=tk.Y, side=tk.RIGHT)
        self.memory_size.insert(0, "32")
        self.frame_memory_size.pack()

        self.frame_n_add = tk.Frame(master=self.frame_a)
        self.n_add_l = tk.Label(master = self.frame_n_add, text="Nº of add FU :")
        self.n_add_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_add = tk.Entry(master = self.frame_n_add)
        self.n_add.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_add.insert(0, "4")
        self.frame_n_add.pack()

        self.frame_latency_add = tk.Frame(master=self.frame_a)
        self.latency_add_l = tk.Label(master = self.frame_latency_add, text="Latency of add FU :")
        self.latency_add_l.pack(fill=tk.Y, side=tk.LEFT)
        self.latency_add = tk.Entry(master = self.frame_latency_add)
        self.latency_add.pack(fill=tk.Y, side=tk.RIGHT)
        self.latency_add.insert(0, "2")
        self.frame_latency_add.pack()

        self.frame_n_mult = tk.Frame(master=self.frame_a)
        self.n_mult_l = tk.Label(master = self.frame_n_mult, text="Nº of mult FU:")
        self.n_mult_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_mult = tk.Entry(master = self.frame_n_mult)
        self.n_mult.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_mult.insert(0, "3")
        self.frame_n_mult.pack()

        self.frame_latency_mult = tk.Frame(master=self.frame_a)
        self.latency_mult_l = tk.Label(master = self.frame_latency_mult, text="Latency of mult FU :")
        self.latency_mult_l.pack(fill=tk.Y, side=tk.LEFT)
        self.latency_mult = tk.Entry(master = self.frame_latency_mult)
        self.latency_mult.pack(fill=tk.Y, side=tk.RIGHT)
        self.latency_mult.insert(0, "3")
        self.frame_latency_mult.pack()

        self.frame_n_store = tk.Frame(master=self.frame_a)
        self.n_store_l = tk.Label(master = self.frame_n_store, text="Nº of store FU:")
        self.n_store_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_store = tk.Entry(master = self.frame_n_store)
        self.n_store.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_store.insert(0, "2")
        self.frame_n_store.pack()

        self.frame_latency_store = tk.Frame(master=self.frame_a)
        self.latency_store_l = tk.Label(master = self.frame_latency_store, text="Latency of store FU :")
        self.latency_store_l.pack(fill=tk.Y, side=tk.LEFT)
        self.latency_store = tk.Entry(master = self.frame_latency_store)
        self.latency_store.pack(fill=tk.Y, side=tk.RIGHT)
        self.latency_store.insert(0, "2")
        self.frame_latency_store.pack()

        self.frame_m = tk.Frame(master=self.frame_a)
        self.m_l = tk.Label(master = self.frame_m, text="Multiplicity:")
        self.m_l.pack(fill=tk.Y, side=tk.LEFT)
        self.m = tk.Entry(master = self.frame_m)
        self.m.pack(fill=tk.Y, side=tk.RIGHT)
        self.m.insert(0, "5")
        self.frame_m.pack()

        self.frame_b_hs = tk.Frame(master=self.frame_a)
        self.b_hs_l = tk.Label(master = self.frame_b_hs, text="HS?:")
        self.b_hs_l.pack(fill=tk.Y, side=tk.LEFT)
        self.b_hs = tk.BooleanVar(value=True)
        self.true_radio = tk.Radiobutton(master = self.frame_b_hs, text="True", variable=self.b_hs, value=True)
        self.true_radio.pack(fill=tk.Y, side=tk.RIGHT)
        self.false_radio = tk.Radiobutton(master = self.frame_b_hs, text="False", variable=self.b_hs, value=False)
        self.false_radio.pack(fill=tk.Y, side=tk.RIGHT)
        self.frame_b_hs.pack()

        self.frame_n_hs = tk.Frame(master=self.frame_a)
        self.n_hs_l = tk.Label(master = self.frame_n_hs, text="Nº of HS:")
        self.n_hs_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_hs = tk.Entry(master = self.frame_n_hs)
        self.n_hs.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_hs.insert(0, "10")
        self.frame_n_add.pack()

        self.frame_n_cycle = tk.Frame(master=self.frame_a)
        self.n_cycles_l = tk.Label(master = self.frame_n_cycle, text="Nº of future cycles:")
        self.n_cycles_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_cycles = tk.Entry(master = self.frame_n_cycle)
        self.n_cycles.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_cycles.insert(0, "120")
        self.frame_n_cycle.pack()

        self.display_ADD = tk.Frame(master=self.frame_b)
        self.d_add = tk.Label(master=self.display_ADD, text="Display ADD FU")
        self.d_add.pack(fill=tk.Y, side=tk.LEFT)
        self.display_ADD_value = tk.BooleanVar(master = self.display_ADD)
        checkbutton_add = tk.Checkbutton(master = self.display_ADD, variable=self.display_ADD_value)
        checkbutton_add.pack(fill=tk.Y, side=tk.RIGHT)
        self.display_ADD.pack()

        self.display_ADD_BRT = tk.Frame(master=self.frame_b)
        self.d_add_BRT = tk.Label(master=self.display_ADD_BRT, text="Display ADD BRT")
        self.d_add_BRT.pack(fill=tk.Y, side=tk.LEFT)
        self.display_ADD_BRT_value = tk.BooleanVar(master = self.display_ADD_BRT)
        checkbutton_add_BRT = tk.Checkbutton(master = self.display_ADD_BRT, variable=self.display_ADD_BRT_value)
        checkbutton_add_BRT.pack(fill=tk.Y, side=tk.RIGHT)
        self.display_ADD_BRT.pack()


        self.display_MUL = tk.Frame(master=self.frame_b)
        self.d_mull = tk.Label(master=self.display_MUL, text="Display MULT FU")
        self.d_mull.pack(fill=tk.Y, side=tk.LEFT)
        self.display_MUL_value = tk.BooleanVar(master = self.display_MUL)
        checkbutton_mull = tk.Checkbutton(master = self.display_MUL, variable=self.display_MUL_value)
        checkbutton_mull.pack(fill=tk.Y, side=tk.RIGHT)
        self.display_MUL.pack()

        self.display_MUL_BRT = tk.Frame(master=self.frame_b)
        self.d_MUL_BRT = tk.Label(master=self.display_MUL_BRT, text="Display MUL BRT")
        self.d_MUL_BRT.pack(fill=tk.Y, side=tk.LEFT)
        self.display_MUL_BRT_value = tk.BooleanVar(master = self.display_MUL_BRT)
        checkbutton_MUL_BRT = tk.Checkbutton(master = self.display_MUL_BRT, variable=self.display_MUL_BRT_value)
        checkbutton_MUL_BRT.pack(fill=tk.Y, side=tk.RIGHT)
        self.display_MUL_BRT.pack()

        self.display_STORE = tk.Frame(master=self.frame_b)
        self.d_store = tk.Label(master=self.display_STORE, text="Display STORE FU")
        self.d_store.pack(fill=tk.Y, side=tk.LEFT)
        self.display_STORE_value = tk.BooleanVar(master = self.display_STORE)
        checkbutton_store = tk.Checkbutton(master = self.display_STORE, variable=self.display_STORE_value)
        checkbutton_store.pack(fill=tk.Y, side=tk.RIGHT)
        self.display_STORE.pack()

        self.display_STORE_BRT = tk.Frame(master=self.frame_b)
        self.d_STORE_BRT = tk.Label(master=self.display_STORE_BRT, text="Display STORE BRT")
        self.d_STORE_BRT.pack(fill=tk.Y, side=tk.LEFT)
        self.display_STORE_BRT_value = tk.BooleanVar(master = self.display_STORE_BRT)
        checkbutton_STORE_BRT = tk.Checkbutton(master = self.display_STORE_BRT, variable=self.display_STORE_BRT_value)
        checkbutton_STORE_BRT.pack(fill=tk.Y, side=tk.RIGHT)
        self.display_STORE_BRT.pack()

        self.display_memory = tk.Frame(master=self.frame_b)
        self.d_memory = tk.Label(master=self.display_memory, text="Display memory")
        self.d_memory.pack(fill=tk.Y, side=tk.LEFT)
        self.display_memory_value = tk.BooleanVar(master = self.display_memory)
        checkbutton_memory = tk.Checkbutton(master = self.display_memory, variable=self.display_memory_value)
        checkbutton_memory.pack(fill=tk.Y, side=tk.RIGHT)
        self.display_memory.pack()


        self.display_CDB = tk.Frame(master=self.frame_b)
        self.d_CDB = tk.Label(master=self.display_CDB, text="Display CDB")
        self.d_CDB.pack(fill=tk.Y, side=tk.LEFT)
        self.display_CDB_value = tk.BooleanVar(master = self.display_CDB)
        checkbutton_CDB = tk.Checkbutton(master = self.display_CDB, variable=self.display_CDB_value)
        checkbutton_CDB.pack(fill=tk.Y, side=tk.RIGHT)
        self.display_CDB.pack()

        self.display_HS = tk.Frame(master=self.frame_b)
        self.d_HS = tk.Label(master=self.display_HS, text="Display HS")
        self.d_HS.pack(fill=tk.Y, side=tk.LEFT)
        self.display_HS_value = tk.BooleanVar(master = self.display_HS)
        checkbutton_HS = tk.Checkbutton(master = self.display_HS, variable=self.display_HS_value)
        checkbutton_HS.pack(fill=tk.Y, side=tk.RIGHT)
        self.display_HS.pack()


        self.frame_a.pack(fill=tk.Y, side=tk.LEFT)
        self.frame_b.pack(fill=tk.Y, side=tk.RIGHT)

        self.full_frame.pack()


        self.start_button = tk.Button(master, text="START", command=self.start)
        self.start_button.pack()




    def scroll_text(self, *args):
        self.text_widget.yview(*args)

    def start(self):

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
        self.open_statistics()

        self.re_start_button = tk.Button(self.master, text="re-start", command=self.re_start)
        self.re_start_button.pack()


        self.button_frame = tk.Frame()
        self.next_cycle_button = tk.Button(self.button_frame, text="next cycle", command=self.next_cycle)
        self.next_cycle_button.pack(side=tk.LEFT)

        self.next_cycle_button = tk.Button(self.button_frame, text="3 next cycle", command=self.n3_cycles)
        self.next_cycle_button.pack(side=tk.LEFT)

        self.next_cycle_button = tk.Button(self.button_frame, text="5 next cycle", command=self.n5_cycles)
        self.next_cycle_button.pack(side=tk.LEFT)

        self.next_cycle_button = tk.Button(self.button_frame, text="10 next cycle", command=self.n10_cycles)
        self.next_cycle_button.pack(side=tk.LEFT)

        #self.statistics_button = tk.Button(self.button_frame, text="statistics", command=self.open_statistics)
        #self.statistics_button.pack(fill=tk.Y, side=tk.RIGHT)

        self.button_frame.pack()

        self.hide()
        self.start_button.pack_forget()
        self.next_cycle_button.pack()

        sys.stdout = ConsoleRedirector(self.text_widget)
        sys.stderr = ConsoleRedirector(self.text_widget)

        self.text_widget.pack(side="left", fill="both", expand=True)

        self.simulador.display2(bmux=self.display_MUL_value.get(), bstore=self.display_STORE_value.get(),
                                bmemory=self.display_memory_value.get(),badd=self.display_ADD_value.get(),
                                bhs = self.display_HS_value.get(), bCDB=self.display_CDB_value.get(),
                                badd_brt = self.display_ADD_BRT_value.get())

    def open_statistics(self):
        self.new_window = tk.Toplevel(self.master)
        self.new_window.title("Statistics")

        self.label1 = tk.Label(self.new_window, text=f"Nº cycles: {self.simulador.statistics.cycles}")
        self.label1.pack()

        self.label2 = tk.Label(self.new_window, text=f"Multiplicity: {self.simulador.m}")
        self.label2.pack()

        self.label3 = tk.Label(self.new_window, text=f"inst Issued: {self.simulador.statistics.instIssued}")
        self.label3.pack()

        self.label4 = tk.Label(self.new_window, text=f"Total Locks: {self.simulador.statistics.totalLock}")
        self.label4.pack()

        self.label5 = tk.Label(self.new_window, text=f"Type Instrucctions: {self.simulador.statistics.typeInst}")
        self.label5.pack()

    def updateStatistics(self):
        self.label1.config(text=f"Nº cycles: {self.simulador.statistics.cycles}")
        self.label3.config(text=f"inst Issued: {self.simulador.statistics.instIssued}")
        self.label4.config(text=f"Total Locks: {self.simulador.statistics.totalLock}")
        self.label5.config(text=f"Type Instrucctions: {self.simulador.statistics.typeInst}")


    def next_cycle(self):
        self.simulador.one_clock_cycle()
        self.simulador.display2(bmux=self.display_MUL_value.get(), bstore=self.display_STORE_value.get(),
                                bmemory=self.display_memory_value.get(),badd=self.display_ADD_value.get(),
                                bhs = self.display_HS_value.get(), bCDB=self.display_CDB_value.get(),
                                badd_brt = self.display_ADD_BRT_value.get())
        self.updateStatistics()

    def n_next_cycle(self, n):
        self.simulador.n_next_cycles(n)
        self.simulador.display2(bmux=self.display_MUL_value.get(), bstore=self.display_STORE_value.get(),
                                bmemory=self.display_memory_value.get(),badd=self.display_ADD_value.get(),
                                bhs = self.display_HS_value.get(), bCDB=self.display_CDB_value.get(),
                                badd_brt = self.display_ADD_BRT_value.get())
        self.updateStatistics()

    def n3_cycles(self):
        self.n_next_cycle(3)

    def n5_cycles(self):
        self.n_next_cycle(5)

    def n10_cycles(self):
        self.n_next_cycle(10)


    def re_start(self):
        self.text_widget.pack_forget()
        self.button_frame.pack_forget()
        self.re_start_button.pack_forget()

        self.full_frame.pack()

        self.start_button.pack()


    def hide(self):
        # Hide all the values
        self.full_frame.pack_forget()

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
    root.title("Simulador")
    calculator = app(root)
    root.mainloop()


if __name__ == "__main__":
    main()