import re
import time

from criaHTML import criaHTML

nrLinha = 1
resultadosCategorias = {}

start = time.time()

file = open("train.txt",'r')

for linha in file:

    if campos := re.search(r'B\-(\w+)[ \t]+(.+)',linha):
        if (campos.group(1)) not in resultadosCategorias:
            resultadosCategorias[campos.group(1)] = {'nrElementos':1, 'elementos':[(campos.group(2),nrLinha)]}
            nrLinha += 1
        else:
            resultadosCategorias[campos.group(1)]['nrElementos'] += 1
            resultadosCategorias[campos.group(1)]['elementos'].append((campos.group(2),nrLinha))
    
    elif campos := re.search(r'I\-(\w+)[ \t]+(.+)',linha):
        resultadosCategorias[campos.group(1)]['nrElementos'] += 1
        resultadosCategorias[campos.group(1)]['elementos'].append((campos.group(2),nrLinha))
    
    nrLinha += 1

end = time.time()

print(end-start)

criaHTML(resultadosCategorias)