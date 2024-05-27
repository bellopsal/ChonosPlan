import Program
import Simulador
from Program import Instruction as Inst

instrucciones = [Inst(operation="add", tag="bucle", r1=1, r2=1, r3=2),
                 Inst(operation="add", r1=3, r2=2, r3=1),
                 Inst(operation="mul", r1=2, r2=1, r3=3),

                 Inst(operation="mul", r1=4, r2=3, r3=2),
                 Inst(operation="add", r1=0, r2=0, r3=1),
                 Inst(operation="mul", r1=3, r2=3, r3=3),
                 Inst(operation="mul", r1=0, r2=3, r3=3),
                 Inst(operation="mul", r1=1, r2=0, r3=0),
                 Inst(operation="add", r1=3, r2=1, r3=1)]

instrucciones = Program.Program("ejemploAgotamiento.csv")
#instrucciones = Program.Program("ex.csv")
# print(instrucciones.instructions[1])
# print(instrucciones.instructions[3])
# print(instrucciones.instructions[4])
# print(instrucciones.instructions[5])

s = Simulador.Simulador_1_FU(program=instrucciones,
                             ss_size=8,
                             registers_size=10,
                             b_scoreboard=1,
                             QSD_size=3,
                             memory_size=32,
                             multiplicity=6,
                             n_alu=3,
                             n_mult=2,
                             n_trans=3,
                             n_div=3,
                             n_store=2,
                             n_load=2,
                             latency_alu=2,
                             latency_div=3,
                             latency_load=2,
                             latency_trans=5,
                             latency_mult=6,
                             latency_store=2,
                             b_hs=True)

s.memory.putValues([*range(32)])

# s.display2(btrans = True,bmux=False, bstore=False, bmemory=False, bload=True)
print(s.CDB)
s.statistics.Chronogram.plot_cycles()
s.one_clock_cycle()
s.statistics.Chronogram.plot_cycles()
s.display2(btrans=False, bmux=True, bstore=False, bmemory=False, bload=True)
print("---------------")
# print(s.CDB)
s.one_clock_cycle()
#
s.display2(balu=True, bmux=True, bstore=False, bmemory=False, bload=False)
# print("---------------")
#
#
s.one_clock_cycle()
s.display2(btrans = False,bmux=True, bstore=False, bmemory=False, bload=False,bCDB=True)
# s.one_clock_cycle()
# s.display2(btrans = False,bmux=True, bstore=False, bmemory=False, bload=False,bCDB=True)
# s.one_clock_cycle()
#
# s.display2(btrans = True,bmux=False, bstore=False, bmemory=False, bload=False,bCDB=True)
# s.one_clock_cycle()

# s.display2(btrans = True,bmux=False, bstore=False, bmemory=False, bload=False,bCDB=True)


