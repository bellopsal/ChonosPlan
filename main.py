import Simulador
from Program import Instruction as Inst

#instrucciones = [["add ", "1", "2", "3"], ["add ", "2", "1", "3"], ["add ", "0", "2", "3"]]

instrucciones = [Inst("add", r1= 1, r2=2, r3=2), Inst("add", r1= 2, r2=1, r3=3)]
#print(instrucciones[0].fu_type)
s = Simulador.Simulador_1_FU(list_program = instrucciones,
                             n_ss = 10, fu_type= "INT", name = "INT_1",
                             n_registers = 5, b_scoreboard = 1, pile_size = 3, memory_size=32)


print(s.fu_add.operationQueue)
print(s.memory)
print(s.fu_add.SS)
print(s.registers)
print(s.fu_add.strBRT())
print ("-------------1--------------")

for _ in range(2):

    s.one_clock_cycle()
    print(s.registers)
    #print(s.registers.scoreboard)
    #print(s.fu_add.strBRT())
    #print(s.fu_add.operationQueue)
    print(s.fu_add.SS)
    # print(s.registers)
    # print(s.fu.pile)
    print(s.fu_add.strOperationQueue())
    #print(s.CDB)

    print ("---------------------------")







