# calculadora de versão

form version_calculation import cal

só e possivel calcular esse padrão:
numero.numero.numero

cal(numero da versão,quantidade de casas de cada numero).calculo(vc deve fazer um calculo ilusorio em forma de string com um n)
exemplo:

from version_calculation import cal

x = cal('0.11.',3).calculo('n+15')

print(x) #0.1.115

o 0.11. é a versão,
o 3 é o numero de casas
e o n+15 é a operação

então some 15 a minha versão