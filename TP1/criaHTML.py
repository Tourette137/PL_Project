import re

def criaHTMLPages(categoria, elementos):
    
    pathFicheiro = 'pages/'+categoria.lower()+'.html'

    with open (pathFicheiro,'w') as ficheiro:
        ficheiro.write(f'''<!DOCTYPE html>
<html>
   <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{categoria}</title>
    </head>
    <body>
        <h1>{categoria}</h1>
        <h3><a href=\"../index.html\"> <b>Voltar á Página Inicial</b></a></h3>
        <h2>Elementos da Categoria {categoria} ({elementos['nrElementos']} elementos):</h2>''')

        for (elemento,nrLinha) in elementos['elementos']:
            ficheiro.write(f'''\n\t\t<p><b>{elemento}</b> - Linha {nrLinha}</p>''')

        ficheiro.write(f'''
    </body>
</html>
''')


def criaHTML(resultadosCategorias):

    with open ("index.html",'w') as ficheiro:

        ficheiro.write(f'''<!DOCTYPE html>
<html>
   <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Trabalho TP1 PL - Enunciado 5</title>
    </head>
    <body>
        <h1>Trabalho TP1 PL - Enunciado 5</h1>
        <h3>Categorias encontradas: </h3>''')

        for (categoria, elementosCategoria) in resultadosCategorias.items():
            criaHTMLPages(categoria, elementosCategoria)
            nrElementos = elementosCategoria['nrElementos']
            pathFicheiro = 'pages/'+categoria.lower()+'.html'
            ficheiro.write(f'''\n\t\t<p>Categoria <a href=\"{pathFicheiro}\"> <b>{categoria}</b></a> - {nrElementos} elementos</p>''')

        ficheiro.write(f'''
    </body>
</html>
''')
