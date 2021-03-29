import re
import time

from criaHTML import criaHTML

def adicionaElemento(categoria,indiceLinha,elemento,resultadosCategorias):
    resultadosCategorias[categoria]['nrElementos'] += 1
    if elemento not in resultadosCategorias[categoria]['elementos']:
        resultadosCategorias[categoria]['elementos'][elemento] = [indiceLinha]
    else:
        
        resultadosCategorias[categoria]['elementos'][elemento].append(indiceLinha)


#{'ACTOR': { nrElementos : 1, elementos:{ elemento:[linhaIndice] }}}

nrLinha = 1
resultadosCategorias = {}

elementoAtual = ""
categoriaAtual = ""
linhaElemento = 0


file = open("train.txt",'r', encoding="utf-8")

startData = time.time()

for linha in file:

    if campos := re.search(r'B\-(\w+)[ \t]+(.+)',linha):

        if categoriaAtual:
            adicionaElemento(categoriaAtual,linhaElemento,elementoAtual,resultadosCategorias)

        linhaElemento = nrLinha
        categoriaAtual = campos.group(1)
        elementoAtual = campos.group(2)

        if (campos.group(1)) not in resultadosCategorias:
            resultadosCategorias[campos.group(1)] = {'nrElementos':0, 'elementos':{}}
    

    elif campos := re.search(r'I\-(\w+)[ \t]+(.+)',linha):

        elementoAtual += (" " + campos.group(2))
    
    else:
        pass
    
    nrLinha += 1

adicionaElemento(categoriaAtual,linhaElemento,elementoAtual,resultadosCategorias)

endData = time.time()
print(endData-startData," seconds to get necessary data.")

startHTML = time.time()

criaHTML(resultadosCategorias)

endHTML = time.time()
print(endHTML-startHTML," seconds to create HTML's.")