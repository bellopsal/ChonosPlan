import Simulador

instrucciones = [["add ", "1", "2", "3"], ["add ", "2", "1", "3"], ["add ", "0", "2", "3"]]
s = Simulador.Simulador_1_FU(list_program = instrucciones,
                             n_ss = 10, fu_type= "INT", name = "INT_1",
                             n_registers = 5, b_scoreboard = 1)



s.one_clock_cycle()
print(s.registers.scoreboard)
print(s.fu.SS)
print(s.registers)
print(s.CDB)

print ("---------------------------")
s.one_clock_cycle()

print(s.registers.scoreboard)
print(s.fu.SS)
print(s.registers)
print(s.CDB)




