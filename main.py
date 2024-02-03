import Simulador

instrucciones = [["add ", "1", "2", "3"], ["add ", "2", "1", "3"], ["add ", "0", "2", "3"]]
s = Simulador.Simulador_1_FU(list_program = instrucciones,
                             n_ss = 10, fu_type= "INT", name = "INT_1",
                             n_registers = 5, b_scoreboard = 1, pile_size = 3, memory_size=32)


print(s.fu.operationQueue)
print(s.memory)

for _ in range(3):

    s.one_clock_cycle()
    #print(s.registers)
    #print(s.registers.scoreboard)
    print(s.fu.operationQueue)
    # print(s.fu.SS)
    # print(s.registers)
    # print(s.fu.pile)
    # print(s.fu.strOperationQueue())
    print(s.CDB)

    print ("---------------------------")







