import os
import tkinter as tk
import pandas as pd
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
        self.v = tk.Scrollbar(self.master, command=self.yscroll_text)
        self.h = tk.Scrollbar(self.master, command=self.xscroll_text)
        self.text_widget = tk.Text(self.master, width=190, wrap = "none", xscrollcommand=self.h.set, yscrollcommand=self.v.set)
        self.h.config(command=self.text_widget.xview)
        self.v.config(command=self.text_widget.yview)

        # help window


        self.px = 15
        self.py = 15

        self.h.pack(side="bottom", fill="x")
        self.v.pack(side="right", fill="y")


        self.full_frame = tk.Frame()
        l = tk.Label(self.full_frame, text="CHRONOs PLAN", font="Script 50 bold").pack()
        self.frame_a = tk.Frame(master=self.full_frame, highlightbackground="black", highlightthickness=2)
        self.frame_b = tk.Frame(master=self.full_frame,highlightbackground="black", highlightthickness=2)
        self.frame_c= tk.Frame(master=self.full_frame, highlightbackground="black", highlightthickness=2)

        l = tk.Label(self.frame_a, text="Configuration", font = "Verdana 24 bold")
        l.pack(padx=self.px/2, pady=self.py/2)
        l = tk.Label(self.frame_b, text="Display Settings",font = "Verdana 24 bold")
        l.pack(padx=self.px/2, pady=self.py/2)

        l = tk.Label(self.frame_c, text="Load Files",font = "Verdana 24 bold")
        l.pack(padx=self.px/2, pady=self.py/2)




        self.frame_inst = tk.Frame(master=self.frame_c)
        self.file_name_label = tk.Label(self.frame_inst, text="No Instructions selected")
        self.file_name_label.pack(fill=tk.Y, side=tk.RIGHT)
        self.button_inst = tk.Button(self.frame_inst, text="Import csv", command=self.open_file)
        self.button_inst.pack(fill=tk.Y, side=tk.LEFT, padx=self.px/4)
        self.frame_inst.pack(anchor="w",padx=self.px/2)

        self.frame_conf = tk.Frame(master=self.frame_c)
        self.conf_name_label = tk.Label(self.frame_conf, text="No Configuration selected")
        self.conf_name_label.pack(fill=tk.Y, side=tk.RIGHT)
        self.button_conf = tk.Button(self.frame_conf, text="Import csv", command=self.open_config)
        self.button_conf.pack(fill=tk.Y, side=tk.LEFT, padx=self.px/4)
        self.frame_conf.pack(anchor="w",padx=self.px/2,pady = self.py/2)
        self.frame_c.pack()


        self.frame_n_ss = tk.Frame(master=self.frame_a)
        self.n_ss_l = tk.Label(master = self.frame_n_ss, text="nº of SS:", justify="left")
        self.n_ss_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_ss = tk.Entry(master = self.frame_n_ss, width = 5, justify="left")
        self.n_ss.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_ss.insert(0, "8")
        self.frame_n_ss.pack(anchor="e", padx=40)

        self.frame_n_registers = tk.Frame(master=self.frame_a)
        self.n_registers_l = tk.Label(master = self.frame_n_registers, text="nº of registers:", justify="left")
        self.n_registers_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_registers = tk.Entry(master = self.frame_n_registers, width = 5, justify="left")
        self.n_registers.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_registers.insert(0, "5")
        self.frame_n_registers.pack(anchor="e", padx=40)

        self.frame_QSD_size = tk.Frame(master=self.frame_a)
        self.QSD_size_l = tk.Label(master = self.frame_QSD_size, text="QSD size:", justify="left")
        self.QSD_size_l.pack(fill=tk.Y, side=tk.LEFT)
        self.QSD_size = tk.Entry(master = self.frame_QSD_size, width = 5, justify="left")
        self.QSD_size.pack(fill=tk.Y, side=tk.RIGHT)
        self.QSD_size.insert(0, "3")
        self.frame_QSD_size.pack(anchor="e", padx=40)

        self.frame_memory_size = tk.Frame(master=self.frame_a)
        self.memory_size_l = tk.Label(master = self.frame_memory_size, text="Memory size:", justify="left")
        self.memory_size_l.pack(fill=tk.Y, side=tk.LEFT)
        self.memory_size = tk.Entry(master = self.frame_memory_size, width = 5, justify="left")
        self.memory_size.pack(fill=tk.Y, side=tk.RIGHT)
        self.memory_size.insert(0, "32")
        self.frame_memory_size.pack(anchor="e", padx=40)

        self.frame_m = tk.Frame(master=self.frame_a)
        self.m_l = tk.Label(master = self.frame_m, text="Multiplicity:", justify="left")
        self.m_l.pack(fill=tk.Y, side=tk.LEFT)
        self.multiplicity = tk.Entry(master = self.frame_m, width = 5, justify="left")
        self.multiplicity.pack(fill=tk.Y, side=tk.RIGHT)
        self.multiplicity.insert(0, "5")
        self.frame_m.pack(anchor="e", padx=40)

        self.frame_b_hs = tk.Frame(master=self.frame_a)
        self.b_hs_l = tk.Label(master = self.frame_b_hs, text="HS?:", justify="left")
        self.b_hs_l.pack(fill=tk.Y, side=tk.LEFT)
        self.b_hs = tk.BooleanVar(value=True)
        self.true_radio = tk.Radiobutton(master = self.frame_b_hs, text="True", variable=self.b_hs, value=True)
        self.true_radio.pack(fill=tk.Y, side=tk.RIGHT)
        self.false_radio = tk.Radiobutton(master = self.frame_b_hs, text="False", variable=self.b_hs, value=False)
        self.false_radio.pack(fill=tk.Y, side=tk.RIGHT)
        self.frame_b_hs.pack(anchor="e", padx=40)

        self.frame_n_hs = tk.Frame(master=self.frame_a)
        self.n_hs_l = tk.Label(master = self.frame_n_hs, text="Nº of HS:", justify="left")
        self.n_hs_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_hs = tk.Entry(master = self.frame_n_hs, width = 5)
        self.n_hs.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_hs.insert(0, "10")
        self.frame_n_hs.pack(anchor="e", padx=40)

        self.frame_n_cycle = tk.Frame(master=self.frame_a)
        self.n_cycles_l = tk.Label(master = self.frame_n_cycle, text="Nº of future cycles:", justify="left")
        self.n_cycles_l.pack(fill=tk.Y, side=tk.LEFT)
        self.n_cycles = tk.Entry(master = self.frame_n_cycle, width = 5, justify="left")
        self.n_cycles.pack(fill=tk.Y, side=tk.RIGHT)
        self.n_cycles.insert(0, "30")
        self.frame_n_cycle.pack(anchor="e", padx=40)

        self.frame_alu = tk.Frame(master=self.frame_a, highlightbackground="black", highlightthickness=1)
        frame_alu_1 = tk.Frame(master=self.frame_alu)
        frame_alu_2 = tk.Frame(master=self.frame_alu)
        frame_alu_3 = tk.Frame(master=self.frame_alu)
        frame_alu_4 = tk.Frame(master=self.frame_alu)
        frame_alu_5 = tk.Frame(master=self.frame_alu)
        frame_alu_6 = tk.Frame(master=self.frame_alu)
        frame_alu_7= tk.Frame(master=self.frame_alu)

        tk.Label(master=frame_alu_1, text=" FU ",  width = 5).pack(fill=tk.Y, side=tk.LEFT)
        tk.Label(master=frame_alu_1, text=" nº ", width = 5).pack(fill=tk.Y, side=tk.LEFT)
        tk.Label(master=frame_alu_1, text="lat", width = 5).pack(fill=tk.Y, side=tk.RIGHT)

        # Select ALU config
        tk.Label(master=frame_alu_2, text="  ALU ", justify="left").pack(fill=tk.Y, side=tk.LEFT)
        self.n_alu = tk.Entry(master = frame_alu_2, width = 5, justify="left")
        self.n_alu.pack( side=tk.LEFT)
        self.n_alu.insert(0, "3")

        self.latency_alu = tk.Entry(master = frame_alu_2, width = 5, justify="left")
        self.latency_alu.pack( side=tk.RIGHT)
        self.latency_alu.insert(0, "2")

        # Select MULT config
        tk.Label(master=frame_alu_3, text=" MULT", justify="left").pack(fill=tk.Y, side=tk.LEFT)
        self.n_mult = tk.Entry(master = frame_alu_3,  width = 5, justify="left")
        self.n_mult.pack( side=tk.LEFT)
        self.n_mult.insert(0, "3")

        self.latency_mult = tk.Entry(master = frame_alu_3, width = 5, justify="left")
        self.latency_mult.pack( side=tk.RIGHT)
        self.latency_mult.insert(0, "3")

        # Select DIV config
        tk.Label(master=frame_alu_4, text="  DIV   ", justify="left").pack(fill=tk.Y, side=tk.LEFT)
        self.n_div = tk.Entry(master = frame_alu_4,  width = 5, justify="left")
        self.n_div.pack( side=tk.LEFT)
        self.n_div.insert(0, "3")

        self.latency_div = tk.Entry(master = frame_alu_4, width = 5, justify="left")
        self.latency_div.pack( side=tk.RIGHT)
        self.latency_div.insert(0, "3")

        # Select TRANS config
        tk.Label(master=frame_alu_7, text="TRANS", justify="left").pack(fill=tk.Y, side=tk.LEFT)
        self.n_trans = tk.Entry(master = frame_alu_7,  width = 5, justify="left")
        self.n_trans.pack( side=tk.LEFT)
        self.n_trans.insert(0, "3")

        self.latency_trans = tk.Entry(master = frame_alu_7, width = 5, justify="left")
        self.latency_trans.pack( side=tk.RIGHT)
        self.latency_trans.insert(0, "5")

        # Select STORE config
        tk.Label(master=frame_alu_5, text="STORE", justify="left").pack(fill=tk.Y, side=tk.LEFT)
        self.n_store = tk.Entry(master = frame_alu_5, width = 5, justify="left")
        self.n_store.pack( side=tk.LEFT)
        self.n_store.insert(0, "3")

        self.latency_store = tk.Entry(master = frame_alu_5, width = 5, justify="left")
        self.latency_store.pack(side=tk.RIGHT)
        self.latency_store.insert(0, "2")

        # Select LOAD config
        tk.Label(master=frame_alu_6, text=" LOAD ", justify="left").pack(fill=tk.Y, side=tk.LEFT)
        self.n_load = tk.Entry(master = frame_alu_6, width = 5, justify="left")
        self.n_load.pack( side=tk.LEFT)
        self.n_load.insert(0, "3")

        self.latency_load = tk.Entry(master = frame_alu_6, width = 5, justify="left")
        self.latency_load.pack(side=tk.RIGHT)
        self.latency_load.insert(0, "2")

        #self.n_alu_l.pack(fill=tk.Y, side=tk.LEFT)

        frame_alu_1.pack()
        frame_alu_2.pack()
        frame_alu_3.pack()
        frame_alu_4.pack()
        frame_alu_5.pack()
        frame_alu_6.pack()
        frame_alu_7.pack()

        self.frame_alu.pack(padx=self.px/2, pady=self.py/2)

        self.dd_alu = tk.Frame(master=self.frame_b)
        self.display_alu = tk.Frame(master=self.dd_alu)
        alu = tk.Label(master=self.frame_b, text="Display ALU:",font = "Arial 14 bold" ).pack(anchor="w", padx = self.px*2)

        self.d_alu = tk.Label(master=self.display_alu, text="FU")
        self.d_alu.pack( side=tk.LEFT)
        self.display_alu_value = tk.BooleanVar(master = self.display_alu)
        checkbutton_alu = tk.Checkbutton(master = self.display_alu, variable=self.display_alu_value)
        checkbutton_alu.pack(side=tk.RIGHT)
        self.display_alu.pack(side=tk.LEFT)

        self.display_alu_BRT = tk.Frame(master=self.dd_alu)
        self.d_alu_BRT = tk.Label(master=self.display_alu_BRT, text="BRT")
        self.d_alu_BRT.pack( side=tk.LEFT)
        self.display_alu_BRT_value = tk.BooleanVar(master = self.display_alu_BRT)
        checkbutton_alu_BRT = tk.Checkbutton(master = self.display_alu_BRT, variable=self.display_alu_BRT_value)
        checkbutton_alu_BRT.pack( side=tk.RIGHT)
        self.display_alu_BRT.pack(side=tk.RIGHT)
        self.dd_alu.pack()

        self.dd_mul = tk.Frame(master=self.frame_b)
        self.display_MUL = tk.Frame(master=self.dd_mul)
        alu = tk.Label(master=self.frame_b, text="Display MULT:", font="Arial 14 bold").pack(anchor="w",
                                                                                            padx=self.px * 2)
        self.d_mull = tk.Label(master=self.display_MUL, text="FU")
        self.d_mull.pack(side=tk.LEFT)
        self.display_MUL_value = tk.BooleanVar(master = self.display_MUL)
        checkbutton_mull = tk.Checkbutton(master = self.display_MUL, variable=self.display_MUL_value)
        checkbutton_mull.pack(side=tk.RIGHT)
        self.display_MUL.pack(side=tk.LEFT)

        self.display_MUL_BRT = tk.Frame(master=self.dd_mul)
        self.d_MUL_BRT = tk.Label(master=self.display_MUL_BRT, text="BRT")
        self.d_MUL_BRT.pack(side=tk.LEFT)
        self.display_MUL_BRT_value = tk.BooleanVar(master = self.display_MUL_BRT)
        checkbutton_MUL_BRT = tk.Checkbutton(master = self.display_MUL_BRT, variable=self.display_MUL_BRT_value)
        checkbutton_MUL_BRT.pack(side=tk.RIGHT)
        self.display_MUL_BRT.pack(side=tk.RIGHT)
        self.dd_mul.pack()

        self.dd_div = tk.Frame(master=self.frame_b)
        self.display_DIV = tk.Frame(master=self.dd_div)
        alu = tk.Label(master=self.frame_b, text="Display DIV:", font="Arial 14 bold").pack(anchor="w",
                                                                                            padx=self.px * 2)
        self.d_div = tk.Label(master=self.display_DIV, text="FU")
        self.d_div.pack(side=tk.LEFT)
        self.display_DIV_value = tk.BooleanVar(master = self.display_DIV)
        checkbutton_div = tk.Checkbutton(master = self.display_DIV, variable=self.display_DIV_value)
        checkbutton_div.pack(side=tk.RIGHT)
        self.display_DIV.pack(side=tk.LEFT)

        self.display_DIV_BRT = tk.Frame(master=self.dd_div)
        self.d_DIV_BRT = tk.Label(master=self.display_DIV_BRT, text="BRT")
        self.d_DIV_BRT.pack(side=tk.LEFT)
        self.display_DIV_BRT_value = tk.BooleanVar(master = self.display_DIV_BRT)
        checkbutton_DIV_BRT = tk.Checkbutton(master = self.display_DIV_BRT, variable=self.display_DIV_BRT_value)
        checkbutton_DIV_BRT.pack(side=tk.RIGHT)
        self.display_DIV_BRT.pack(side=tk.RIGHT)
        self.dd_div.pack()

        # Trans
        self.dd_trans = tk.Frame(master=self.frame_b)
        self.display_TRANS = tk.Frame(master=self.dd_trans)
        alu = tk.Label(master=self.frame_b, text="Display TRANS:", font="Arial 14 bold").pack(anchor="w",
                                                                                            padx=self.px * 2)
        self.d_trans = tk.Label(master=self.display_TRANS, text="FU")
        self.d_trans.pack(side=tk.LEFT)
        self.display_TRANS_value = tk.BooleanVar(master = self.display_TRANS)
        checkbutton_trans = tk.Checkbutton(master = self.display_TRANS, variable=self.display_TRANS_value)
        checkbutton_trans.pack(side=tk.RIGHT)
        self.display_TRANS.pack(side=tk.LEFT)

        self.display_TRANS_BRT = tk.Frame(master=self.dd_trans)
        self.d_TRANS_BRT = tk.Label(master=self.display_TRANS_BRT, text="BRT")
        self.d_TRANS_BRT.pack(side=tk.LEFT)
        self.display_TRANS_BRT_value = tk.BooleanVar(master = self.display_TRANS_BRT)
        checkbutton_TRANS_BRT = tk.Checkbutton(master = self.display_TRANS_BRT, variable=self.display_TRANS_BRT_value)
        checkbutton_TRANS_BRT.pack(side=tk.RIGHT)
        self.display_TRANS_BRT.pack(side=tk.RIGHT)
        self.dd_trans.pack()

        self.dd_store = tk.Frame(master=self.frame_b)
        self.display_STORE = tk.Frame(master=self.dd_store)
        alu = tk.Label(master=self.frame_b, text="Display STORE:", font="Arial 14 bold").pack(anchor="w",padx=self.px * 2)
        self.d_store = tk.Label(master=self.display_STORE, text="FU")
        self.d_store.pack(side=tk.LEFT)
        self.display_STORE_value = tk.BooleanVar(master = self.display_STORE)
        checkbutton_store = tk.Checkbutton(master = self.display_STORE, variable=self.display_STORE_value)
        checkbutton_store.pack(side=tk.RIGHT)
        self.display_STORE.pack(side=tk.LEFT)

        self.display_STORE_BRT = tk.Frame(master=self.dd_store)
        self.d_STORE_BRT = tk.Label(master=self.display_STORE_BRT, text="BRT")
        self.d_STORE_BRT.pack(side=tk.LEFT)
        self.display_STORE_BRT_value = tk.BooleanVar(master = self.display_STORE_BRT)
        checkbutton_STORE_BRT = tk.Checkbutton(master = self.display_STORE_BRT, variable=self.display_STORE_BRT_value)
        checkbutton_STORE_BRT.pack(side=tk.RIGHT)
        self.display_STORE_BRT.pack(side=tk.RIGHT)
        self.dd_store.pack()

        self.dd_load = tk.Frame(master=self.frame_b)
        self.display_LOAD = tk.Frame(master=self.dd_load)
        alu = tk.Label(master=self.frame_b, text="Display LOAD:", font="Arial 14 bold").pack(anchor="w",
                                                                                            padx=self.px * 2)

        self.d_load = tk.Label(master=self.display_LOAD, text="FU")
        self.d_load.pack(fill=tk.Y, side=tk.LEFT)
        self.display_LOAD_value = tk.BooleanVar(master = self.display_LOAD)
        checkbutton_load = tk.Checkbutton(master = self.display_LOAD, variable=self.display_LOAD_value)
        checkbutton_load.pack( side=tk.RIGHT)
        self.display_LOAD.pack(side=tk.LEFT)

        self.display_LOAD_BRT = tk.Frame(master=self.dd_load)
        self.d_LOAD_BRT = tk.Label(master=self.display_LOAD_BRT, text="BRT")
        self.d_LOAD_BRT.pack(fill=tk.Y, side=tk.LEFT)
        self.display_LOAD_BRT_value = tk.BooleanVar(master = self.display_LOAD_BRT)
        checkbutton_LOAD_BRT = tk.Checkbutton(master = self.display_LOAD_BRT, variable=self.display_LOAD_BRT_value)
        checkbutton_LOAD_BRT.pack( side=tk.RIGHT)
        self.display_LOAD_BRT.pack(side=tk.RIGHT)
        self.dd_load.pack()





        self.display_JUMP_BRT = tk.Frame(master=self.frame_b)
        alu = tk.Label(master=self.frame_b, text="Display JUMP:", font="Arial 14 bold").pack(anchor="w",
                                                                                            padx=self.px * 2)
        self.d_JUMP_BRT = tk.Label(master=self.display_JUMP_BRT, text="BRT")
        self.d_JUMP_BRT.pack(fill=tk.Y, side=tk.LEFT)
        self.display_JUMP_BRT_value = tk.BooleanVar(master = self.display_JUMP_BRT)
        checkbutton_JUMP_BRT = tk.Checkbutton(master = self.display_JUMP_BRT, variable=self.display_JUMP_BRT_value)
        checkbutton_JUMP_BRT.pack(fill=tk.Y, side=tk.RIGHT)
        self.display_JUMP_BRT.pack()

        self.display_memory = tk.Frame(master=self.frame_b)
        self.d_memory = tk.Label(master=self.display_memory, text="Display memory", font="Arial 14 bold")
        self.d_memory.pack(fill=tk.Y, side=tk.LEFT)
        self.display_memory_value = tk.BooleanVar(master = self.display_memory)
        checkbutton_memory = tk.Checkbutton(master = self.display_memory, variable=self.display_memory_value)
        checkbutton_memory.pack(fill=tk.Y, side=tk.RIGHT)
        self.display_memory.pack(anchor="w",padx=self.px * 2)


        self.display_CDB = tk.Frame(master=self.frame_b)
        self.d_CDB = tk.Label(master=self.display_CDB, text="Display CDB", font="Arial 14 bold")
        self.d_CDB.pack(fill=tk.Y, side=tk.LEFT)
        self.display_CDB_value = tk.BooleanVar(master = self.display_CDB)
        checkbutton_CDB = tk.Checkbutton(master = self.display_CDB, variable=self.display_CDB_value)
        checkbutton_CDB.pack(fill=tk.Y, side=tk.RIGHT)
        self.display_CDB.pack(anchor="w",padx=self.px * 3.5)

        self.display_HS = tk.Frame(master=self.frame_b)
        self.d_HS = tk.Label(master=self.display_HS, text="Display HS", font="Arial 14 bold")
        self.d_HS.pack(fill=tk.Y, side=tk.LEFT)
        self.display_HS_value = tk.BooleanVar(master = self.display_HS)
        checkbutton_HS = tk.Checkbutton(master = self.display_HS, variable=self.display_HS_value)
        checkbutton_HS.pack(fill=tk.Y, side=tk.RIGHT)
        self.display_HS.pack(anchor="w",padx=self.px * 4.2)

        self.save_config_button = tk.Button(self.frame_a, text="SAVE config", command=self.save_conf)
        self.save_config_button.pack(padx=self.px/2, pady=self.py/2)

        self.frame_a.pack(fill=tk.Y, side=tk.LEFT, padx=self.px, pady=self.py)
        self.frame_b.pack(fill=tk.Y, side=tk.RIGHT, padx=self.px, pady=self.py)

        self.full_frame.pack()


        self.start_button = tk.Button(master, text="START", command=self.start)
        self.start_button.pack(padx=self.px/4, pady=self.py/4)


    def save_conf(self):
        r = pd.DataFrame({
        "n_ss": [self.n_ss.get()],
        "n_registers": [self.n_registers.get()],
        "QSD_size":[ self.QSD_size.get()],
        "memory_size":[ self.memory_size.get()],
        "n_alu":[ self.n_alu.get()],
        "n_mult":[ self.n_mult.get()],
        "n_div": [self.n_div.get()],
        "n_trans": [self.n_trans.get()],
        "n_load": [self.n_load.get()],
        "n_store":[ self.n_store.get()],
        "latency_alu":[ self.latency_alu.get()],
        "latency_mult":[ self.latency_mult.get()],
        "latency_div": [self.latency_div.get()],
        "latency_trans": [self.latency_trans.get()],
        "latency_store":[ self.latency_store.get()],
        "latency_load": [self.latency_load.get()],
        "n_cycles":[ self.n_cycles.get()],
        "multiplicity":[ self.multiplicity.get()],
        "b_hs":[ self.b_hs.get()]

        })
        r.to_csv("config_sim.csv")


    def yscroll_text(self, *args):
        self.text_widget.yview(*args)

    def xscroll_text(self, *args):
        self.text_widget.xview(*args)

    def start(self):


        self.simulador =Simulador.Simulador_1_FU(program = self.program,
                                                 ss_size = int(self.n_ss.get()),
                                                 registers_size= int(self.n_registers.get()),

                                                 QSD_size = int(self.QSD_size.get()),
                                                 memory_size=int(self.memory_size.get()),
                                                 n_alu= int(self.n_alu.get()),
                                                 n_mult= int(self.n_mult.get()),
                                                 n_div = int(self.n_div.get()),
                                                 n_trans=int(self.n_trans.get()),
                                                 n_load = int(self.n_load.get()),
                                                 n_store = int(self.n_store.get()),
                                                 latency_alu = int(self.latency_alu.get()),
                                                 latency_load=int(self.latency_load.get()),
                                                 latency_div=int(self.latency_div.get()),
                                                 latency_trans=int(self.latency_trans.get()),
                                                 latency_mult =int(self.latency_mult.get()),
                                                 latency_store= int(self.latency_store.get()),
                                                 n_cycles=int(self.n_cycles.get()),
                                                 multiplicity=int(self.multiplicity.get()),
                                                 b_hs= self.b_hs.get()

                                                 )
        self.config = pd.DataFrame({
            "n_ss": [self.n_ss.get()],
            "n_registers": [self.n_registers.get()],
            "QSD_size": [self.QSD_size.get()],
            "memory_size": [self.memory_size.get()],
            "n_alu": [self.n_alu.get()],
            "n_mult": [self.n_mult.get()],
            "n_div": [self.n_div.get()],
            "n_trans": [self.n_trans.get()],
            "n_load": [self.n_load.get()],
            "n_store": [self.n_store.get()],
            "latency_alu": [self.latency_alu.get()],
            "latency_mult": [self.latency_mult.get()],
            "latency_div": [self.latency_div.get()],
            "latency_trans": [self.latency_trans.get()],
            "latency_store": [self.latency_store.get()],
            "latency_load": [self.latency_load.get()],
            "n_cycles": [self.n_cycles.get()],
            "multiplicity": [self.multiplicity.get()],
            "b_hs": [self.b_hs.get()]

        })

        self.re_start_button = tk.Button(self.master, text="re-start", command=self.re_start)
        self.re_start_button.pack(padx=self.px/4, pady=self.py/4)


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
        self.next_cycle_button.pack(padx=self.px/4, pady=self.py/4)

        from PIL import ImageTk, Image



        sys.stdout = ConsoleRedirector(self.text_widget)
        sys.stderr = ConsoleRedirector(self.text_widget)



        self.text_widget.pack(side="left", padx=self.px, pady=self.py, fill="y")

        self.simulador.display2(balu=self.display_alu_value.get(),
                                bmux=self.display_MUL_value.get(),
                                bdiv=self.display_DIV_value.get(),
                                bstore=self.display_STORE_value.get(),
                                bload=self.display_LOAD_value.get(),
                                btrans=self.display_TRANS_value.get(),
                                bmemory=self.display_memory_value.get(),
                                bhs = self.display_HS_value.get(),
                                bCDB=self.display_CDB_value.get(),
                                balu_brt=self.display_alu_BRT_value.get(),
                                btrans_brt=self.display_TRANS_BRT_value.get(),
                                bdiv_brt=self.display_DIV_BRT_value.get(),
                                bmux_brt=self.display_MUL_BRT_value.get(),
                                bstore_brt = self.display_STORE_BRT_value.get(),
                                bload_brt=self.display_LOAD_BRT_value.get(),
                                bjump_brt=self.display_JUMP_BRT_value.get())

        self.open_statistics()

    def open_statistics(self):
        self.new_window = tk.Toplevel(self.master)
        self.new_window.title("Statistics")

        self.left_size = tk.Label(self.new_window)
        self.right_size = tk.Label(self.new_window)

        aux_top = tk.Frame(self.left_size)
        aux_botton = tk.Frame(self.left_size)

        aux = tk.Frame(aux_top, highlightbackground="black", highlightthickness=2)
        tk.Label(aux, text=f"STATISTICS", font="Script 20 bold").pack()

        self.label1 = tk.Label(aux, text=f"Nº cycles: {self.simulador.statistics.cycles}")
        self.label1.pack()

        self.label2 = tk.Label(aux, text=f"Multiplicity: {self.simulador.multiplicity}")
        self.label2.pack()

        self.label3 = tk.Label(aux, text=f"inst Issued: {self.simulador.statistics.instIssued}")
        self.label3.pack()

        self.label4 = tk.Label(aux, text=f"Total Locks: {self.simulador.statistics.totalLock}")
        self.label4.pack()

        #self.label5 = tk.Label(self.left_size, text=f"Type Instrucctions: {self.simulador.statistics.typeInst}")
        #self.label5.pack()
        self.label5 = tk.Label(aux, text=f"Mean Latency: {self.simulador.statistics.mean_latency}")
        self.label5.pack()

        self.label8 = tk.Label(aux, text=f"CPI: {self.simulador.statistics.CPI}")
        self.label8.pack()

        aux.pack(side = tk.RIGHT, padx=self.px/4, pady=self.py/4)


        #aux_r = tk.Label(aux_top)
        #aux_r.pack(side = tk.RIGHT)
        #aux_l = tk.Label(aux_top)
        #aux_l.pack(side=tk.LEFT)
        a = tk.Frame(aux_top, highlightbackground="black", highlightthickness=2)
        tk.Label(a, text=f"SIMULATION CONFIG", font="Script 20 bold").pack()

        tk.Label(a,text = self.simulador.program).pack(side = tk.RIGHT)
        df_dict = self.config.iloc[0].to_dict()
        config_string = "\n ".join([f"{key}: {value}" for key, value in df_dict.items()])
        tk.Label(a,text = config_string).pack(side = tk.RIGHT)

        a.pack(padx=self.px/4, pady=self.py/4)
        self.left_size.pack(side=tk.LEFT)
        self.right_size.pack(side = tk.RIGHT)

        self.simulador.statistics.plot_graphs()
        img = Image.open("stats.png")
        photo = ImageTk.PhotoImage(img.convert('RGB'))
        self.label7 = tk.Label(aux_botton,image=photo)
        self.label7.image = photo
        self.label7.pack()
        img.close()

        self.simulador.statistics.Chronogram.plot_cycles()
        img = Image.open("figure.png")
        photo = ImageTk.PhotoImage(img.convert('RGB'))
        self.label6 = tk.Label(self.right_size,image=photo)
        self.label6.image = photo
        self.label6.pack(side = tk.RIGHT)
        img = img.resize((350,700))
        photo = ImageTk.PhotoImage(img.convert('RGB'))
        self.label = tk.Label(self.master,image=photo)
        self.label.image = photo  # keep a reference!
        self.label.pack()
        self.labelCPI = tk.Label(self.master, text=f"CPI: {self.simulador.statistics.CPI}")
        self.labelCPI.pack()
        img.close()

        aux_top.pack()
        aux_botton.pack()







    def updateStatistics(self):
        self.label1.config(text=f"Nº cycles: {self.simulador.statistics.cycles}")
        self.label3.config(text=f"inst Issued: {self.simulador.statistics.instIssued}")
        self.label4.config(text=f"Total Locks: {self.simulador.statistics.totalLock}")
        self.label5.config(text=f"Mean Latency: {self.simulador.statistics.mean_latency}")
        self.label8.config(text=f"CPI: {self.simulador.statistics.CPI}")

        self.label.config(image = None)
        self.label.image = None
        self.simulador.statistics.Chronogram.plot_cycles()

        img = Image.open("figure.png")
        photo = ImageTk.PhotoImage(img.convert('RGB'))
        self.label6.config(image=photo)
        self.label6.image = photo

        img = img.resize((350,700))
        photo = ImageTk.PhotoImage(img.convert('RGB'))
        self.label.config(image=photo)
        self.label.image = photo  # keep a reference!
        self.labelCPI.config(text=f"CPI: {self.simulador.statistics.CPI}")

        img.close()


        self.simulador.statistics.plot_graphs()
        img = Image.open("stats.png")
        photo = ImageTk.PhotoImage(img.convert('RGB'))
        self.label7.config(image=photo)
        self.label7.image = photo

        img.close()


        #self.canvas.pack()


    def next_cycle(self):
        self.simulador.one_clock_cycle()
        self.simulador.display2(balu=self.display_alu_value.get(),
                                bmux=self.display_MUL_value.get(),
                                bdiv=self.display_DIV_value.get(),
                                bstore=self.display_STORE_value.get(),
                                bload=self.display_LOAD_value.get(),
                                btrans=self.display_TRANS_value.get(),
                                bmemory=self.display_memory_value.get(),
                                bhs = self.display_HS_value.get(),
                                bCDB=self.display_CDB_value.get(),
                                balu_brt=self.display_alu_BRT_value.get(),
                                btrans_brt=self.display_TRANS_BRT_value.get(),
                                bdiv_brt=self.display_DIV_BRT_value.get(),
                                bmux_brt=self.display_MUL_BRT_value.get(),
                                bstore_brt = self.display_STORE_BRT_value.get(),
                                bload_brt=self.display_LOAD_BRT_value.get(),
                                bjump_brt=self.display_JUMP_BRT_value.get())
        self.updateStatistics()

    def n_next_cycle(self, n):
        self.simulador.n_next_cycles(n)
        self.simulador.display2(balu=self.display_alu_value.get(),
                                bmux=self.display_MUL_value.get(),
                                bdiv=self.display_DIV_value.get(),
                                bstore=self.display_STORE_value.get(),
                                bload=self.display_LOAD_value.get(),
                                btrans=self.display_TRANS_value.get(),
                                bmemory=self.display_memory_value.get(),
                                bhs = self.display_HS_value.get(),
                                bCDB=self.display_CDB_value.get(),
                                balu_brt=self.display_alu_BRT_value.get(),
                                btrans_brt=self.display_TRANS_BRT_value.get(),
                                bdiv_brt=self.display_DIV_BRT_value.get(),
                                bmux_brt=self.display_MUL_BRT_value.get(),
                                bstore_brt = self.display_STORE_BRT_value.get(),
                                bload_brt=self.display_LOAD_BRT_value.get(),
                                bjump_brt=self.display_JUMP_BRT_value.get())

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
        self.label.pack_forget()
        self.labelCPI.pack_forget()
        #self.stats.pack_forget()

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

    def open_config(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            file_name = os.path.basename(file_path)
            self.conf_name_label.config(text="Selected file: " + file_name)

            # set config values
            conf = pd.read_csv(file_name)
            self.n_ss.delete(0, tk.END)
            self.n_ss.insert(0, str(conf["n_ss"][0]))

            self.n_registers.delete(0, tk.END)
            self.n_registers.insert(0, str(conf["n_registers"][0]))

            self.QSD_size.delete(0, tk.END)
            self.QSD_size.insert(0, str(conf["QSD_size"][0]))

            self.memory_size.delete(0, tk.END)
            self.memory_size.insert(0, str(conf["memory_size"][0]))

            self.n_alu.delete(0, tk.END)
            self.n_alu.insert(0, str(conf["n_alu"][0]))

            self.n_div.delete(0, tk.END)
            self.n_div.insert(0, str(conf["n_div"][0]))

            self.n_load.delete(0, tk.END)
            self.n_load.insert(0, str(conf["n_load"][0]))

            self.n_mult.delete(0, tk.END)
            self.n_mult.insert(0, str(conf["n_mult"][0]))

            self.n_trans.delete(0, tk.END)
            self.n_trans.insert(0, str(conf["n_trans"][0]))

            self.n_store.delete(0, tk.END)
            self.n_store.insert(0, str(conf["n_store"][0]))

            self.latency_alu.delete(0, tk.END)
            self.latency_alu.insert(0, str(conf["latency_alu"][0]))

            self.latency_div.delete(0, tk.END)
            self.latency_div.insert(0, str(conf["latency_div"][0]))

            self.latency_load.delete(0, tk.END)
            self.latency_load.insert(0, str(conf["latency_load"][0]))

            self.latency_mult.delete(0, tk.END)
            self.latency_mult.insert(0, str(conf["latency_mult"][0]))

            self.latency_trans.delete(0, tk.END)
            self.latency_trans.insert(0, str(conf["latency_trans"][0]))

            self.latency_store.delete(0, tk.END)
            self.latency_store.insert(0, str(conf["latency_store"][0]))

            self.n_cycles.delete(0, tk.END)
            self.n_cycles.insert(0, str(conf["n_cycles"][0]))

            self.multiplicity.delete(0, tk.END)
            self.multiplicity.insert(0, str(conf["multiplicity"][0]))

            self.b_hs = tk.BooleanVar(value=bool(conf["b_hs"][0]))





            print("Selected file:", file_path)
        else:
            print("No file selected")




def main():
    root = tk.Tk()
    root.title("Simulador")
    calculator = app(root)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry("%dx%d+-10+0" % (screen_width, screen_height))
    root.mainloop()


if __name__ == "__main__":
    main()