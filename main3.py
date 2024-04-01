import Program
import Simulador
from Program import Instruction as Inst

instrucciones = [Inst(operation="add", tag = "bucle", r1= 1, r2=1, r3=2),
                Inst(operation="add", r1= 3, r2=2, r3=1),
                 Inst(operation="mul", r1= 2, r2=1, r3=3),

                 Inst(operation="mul", r1= 4, r2=3, r3=2),
                 Inst(operation="add", r1= 0, r2=0, r3=1),
                 Inst(operation="mul", r1= 3, r2=3, r3=3),
                 Inst(operation="mul", r1= 0, r2=3, r3=3),
                 Inst(operation="mul", r1= 1, r2=0, r3=0) ,
                 Inst(operation="add", r1= 3, r2=1, r3=1) ]

instrucciones = Program.Program("exampleOP2.csv")

#print(instrucciones.instructions[1])
#print(instrucciones.instructions[3])
#print(instrucciones.instructions[4])
#print(instrucciones.instructions[5])

s = Simulador.Simulador_1_FU(program = instrucciones,
                             n_ss = 8,
                             n_registers = 5,
                             b_scoreboard = 1,
                             pile_size = 3,
                             memory_size=32,
                             n_add = 4,
                             n_mult= 3,
                             n_store = 2,
                             latency_add = 2,
                             latency_mult =3,
                             latency_store= 2,
                             m=3,
                             b_hs= False,

                             )

s.one_clock_cycle()
s.display_ints()
print("---------------")
s.one_clock_cycle()
s.display_ints()
print("---------------")
s.one_clock_cycle()
s.display_ints()
print("---------------")
s.one_clock_cycle()
s.display2(bmux=True)
print("---------------")
s.one_clock_cycle()
s.display2(bmux=True)