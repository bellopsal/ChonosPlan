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

print(instrucciones[0])