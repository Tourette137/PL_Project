def criaHTMLPages(categoria, elementos):
    
    pathFicheiro = 'pages/'+categoria.lower()+'.html'

    with open (pathFicheiro, 'w', encoding="utf-8") as ficheiro:
        ficheiro.write(f'''<!DOCTYPE html>
<html>
   <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css ">
        <link rel="stylesheet" href="../style.css">
        <title>{categoria}</title>
    </head>
    <body>
        <h1>{categoria}</h1>
        <h3><a href=\"../index.html\"> <b>Voltar á Página Inicial</b></a></h3>
        <h2>Elementos da Categoria {categoria} ({elementos['nrElementos']} elementos -> {len(elementos['elementos'])} distintos):</h2>''')

        for (elemento,linhas) in elementos['elementos'].items():
            ficheiro.write(f'''\n\t\t<p><b>{elemento}</b> - Linhas {linhas}</p>''')

        ficheiro.write(f'''
    </body>
</html>
''')


def criaHTML(resultadosCategorias):

    nrCategorias = len(resultadosCategorias)
    categoriaNr = 1

    with open ("index.html", 'w', encoding="utf-8") as ficheiro:

        ficheiro.write(f'''<!DOCTYPE html>
<html>
   <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css ">
        <link rel="stylesheet" href="css/style.css">
        <title>Trabalho TP1 PL - Enunciado 5</title>
    </head>
    <body>
        
        <div class="w3-bar w3-black w3-top">
            <span class="marca w3-bar-item w3-mobile">Processamento de Linguagens <b>(Grupo 59)</b></span>
            <span class="w3-right w3-mobile">
                <a href="../index.html" class="marca w3-bar-item w3-button w3-mobile w3-hover-orange">Voltar á Página Inicial</a>
            </span>
        </div>

        <section class="showcase">
            <div class="w3-container w3-center">
                <h1 class="w3-text-shadow w3-animate-opacity">Trabalho TP1 PL - Enunciado 5</h1>
                <h2 class="w3-text-shadow w3-animate-opacity">Grupo 59</h2>
                <hr class="w3-animate-opacity">
                <p class="w3-animate-opacity">Trabalho realizado no âmbito de Processamento de Linguagens</p>
            </div>
        </section>

        <section class="listagemCategorias">
            <h2 class="w3-center w3-text-shadow">Categorias encontradas: </h2>
            <ul class="w3-ul w3-deep-orange w3-mobile w3-hoverable">''')

        for (categoria, elementosCategoria) in resultadosCategorias.items():
            criaHTMLPages(categoria, elementosCategoria)
            nrElementos = elementosCategoria['nrElementos']
            pathFicheiro = 'pages/'+categoria.lower()+'.html'
            ficheiro.write(f'''
                <a href="{pathFicheiro}">
                    <li class="w3-bar w3-mobile w3-hover-orange">
                        <span class="categoria w3-bar-item w3-mobile">{categoria}</span>
                        <span class="nrElementos w3-bar-item w3-right w3-mobile">{nrElementos} elementos</span>
                    </li>
                </a>''')
            if categoriaNr != nrCategorias:
                ficheiro.write('''
                <hr>''')
            categoriaNr += 1

        ficheiro.write(f'''
            </ul>
        </section>
    </body>
</html>
''')
