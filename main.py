import Simulador
from Program import Instruction as Inst




#instrucciones = [["add ", "1", "2", "3"], ["add ", "2", "1", "3"], ["add ", "0", "2", "3"]]

#instrucciones = [Inst("sb", r1 = 1, inm = 0, rs1=3),Inst("add", r1= 1, r2=2, r3=2), Inst("add", r1= 2, r2=1, r3=3), Inst("lb", r1 = 0, inm = 0, rs1=3), Inst("sub", r1= 4, r2=4, r3=4), Inst("sub", r1= 0, r2=2, r3=3)]
#print(instrucciones[0].fu_type)

#instrucciones = [Inst("add", r1= 1, r2=2, r3=2),  Inst("mul", r1= 4, r2=4, r3=4), Inst("div", r1 = 2, r2=4, r3 = 1)]

#instrucciones= [Inst("sb", r1 = 1, inm = 0, rs1=3), Inst("lb", r1 = 0, inm = 0, rs1=3)]

# instrucciones = [Inst("add", r1= 1, r2=1, r3=2),
#                 Inst("add", r1= 3, r2=2, r3=1),
#                  Inst("mul", r1= 2, r2=1, r3=3),
#
#                  Inst("mul", r1= 4, r2=3, r3=2),
#                  Inst("add", r1= 0, r2=0, r3=1),
#                  Inst("mul", r1= 3, r2=3, r3=3),
#                  Inst("mul", r1= 0, r2=3, r3=3),
#                  Inst("mul", r1= 1, r2=0, r3=0) ,
#                  Inst("add", r1= 3, r2=1, r3=1) ]

instrucciones = [Inst("add", r1= 1, r2=1, r3=2),
                Inst("add", r1= 2, r2=1, r3=3),
                Inst("add", r1= 1, r2=3, r3=3),
                Inst("add", r1= 2, r2=1, r3=3),
                Inst("add", r1= 1, r2=2, r3=3),
                 Inst("add", r1=2, r2=1, r3=3),
                 Inst("add", r1=1, r2=2, r3=3),
                 Inst("add", r1=4, r2=2, r3=3),
                 Inst("add", r1=1, r2=2, r3=3),
                 Inst("add", r1=1, r2=2, r3=3)
                 ]

s = Simulador.Simulador_1_FU(list_program = instrucciones,
                             n_ss = 8,
                             n_registers = 5,
                             b_scoreboard = 1,
                             pile_size = 3,
                             memory_size=32,
                             n_add = 2,
                             n_mult= 3,
                             n_store = 2,
                             latency_add = 2,
                             latency_mult =3,
                             latency_store= 2,
                             m=4
                             )

s.memory.putValues([*range(32)])
s.display2(bmux=False)

#print(s.fu_add.operationQueue)
#print(s.memory)

#print(s.fu_add.strBRT())
#print ("-------------empieza --------------")

for i in range(12):
    print(f"-------------T{i+1} ------------------------------------------------------------------------------------------------")
    s.one_clock_cycle()
    s.display2(bmux=False) 


    #print(s.registers)
    #print(s.memory)
    #print(s.fu_store.SS)
    #print(s.fu_store.pile)
    #print(s.registers.scoreboard)
    #print(s.fu_add.strBRT())
    #print(s.fu_add.operationQueue)
    #print(s.fu_mult.SS)
    # print(s.registers)
    #print(s.fu_add.pile)
    #print(s.fu_add.strOperationQueue())
    #print(s.CDB)









