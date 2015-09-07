__author__ = 'Gabriel Gusmao'


'''
def extrairCitadosTexto(qtdNoticiaAtual = 0):
    listaFamosos = model.buscarListaFamoso()
    listaNoticias = model.buscarListaNoticias()
    qtdTotalNoticias = len(listaNoticias) - 1

    file = open("arquivo.txt","w")

    if listaNoticias != False and listaFamosos != False:
        for i in listaNoticias[qtdNoticiaAtual:]:
            noticia = {'id': i[0], 'titulo': i[1], 'subtitulo': i[2], 'link': i[3], 'tipo': i[4], 'texto': i[5]}
            print(str(qtdNoticiaAtual) + "/" + str(qtdTotalNoticias) + " - " + str(noticia['titulo']))

            file.write(str(noticia['titulo'])))

            for j in listaFamosos:
                famoso = {'id': j[0], 'nome': j[1], 'link': j[2], 'dataNascimento': j[3], 'idade': j[4], 'signo': j[5], 'relacionamento': j[6], 'conjuge': j[7]}
                ratioTotal = 0
                mediaRatio = 0
                nomeCompleto = famoso['nome']
                todosNomes = famoso['nome'].split(" ")
                textoTotal = noticia['titulo'] + " " + noticia['subtitulo'] + " " + noticia['texto']

                if len(todosNomes) == 1:
                    textoQuebrado = set(textoTotal.lower().split(" "))
                    conjuntoNomeCompleto = { nomeCompleto.lower() }
                    if conjuntoNomeCompleto.issubset(textoQuebrado):

                        file.write(str(nomeCompleto))

                        if model.relacionarFamosoNoticia(famoso['nome'], noticia['id']) == False:
                            print(" - " + str(nomeCompleto) + " ja relacionado com a noticia.")
                        else:
                            print(" - " + str(nomeCompleto))
                else:
                    if nomeCompleto.lower() in textoTotal.lower():

                        file.write(str(nomeCompleto))

                        if model.relacionarFamosoNoticia(famoso['nome'], noticia['id']) == False:
                            print(" - " + str(nomeCompleto) + " ja relacionado com a noticia.")
                        else:
                            print(" - " + str(nomeCompleto))

                )

                ''
                ratioTotal += fuzz.token_set_ratio(nomeCompleto, textoTotal)

                if len(todosNomes) == 1:
                    mediaRatio = ratioTotal
                elif len(todosNomes) > 1:
                    for nome in todosNomes:
                        ratioTotal += fuzz.token_set_ratio(nome, textoTotal)

                    mediaRatio = ratioTotal / (len(todosNomes) + 1)

                if mediaRatio > 85:
                    if model.relacionarFamosoNoticia(famoso['nome'], noticia['id']) == False:
                        print(" - " + str(nomeCompleto) + " ja relacionado com a noticia.")
                    else:
                        print(" - " + str(nomeCompleto))
                ''
            qtdNoticiaAtual += 1
'''

'''
def extrairCitadosTextoProcess():
    listaFamosos = model.buscarListaFamoso()
    listaNoticias = model.buscarListaNoticias()
    noticia =
    f = open("arquivoTeste2.txt", "w")
    if listaNoticias != False and listaFamosos != False:
        for i in listaNoticias:
            f.writelines(str(i[1]) + "\n")
            noticia = {'id': i[0], 'titulo': i[1], 'subtitulo': i[2], 'link': i[3], 'tipo': i[4], 'texto': i[5]}
            print(str(noticia['titulo']))
            famosos = []
            for j in listaFamosos:
                famosos.append(j[1])

            textoTotal = noticia['titulo'] + " " + noticia['subtitulo'] + " " + noticia['texto']

            qtdProcessamento = 1
            while qtdProcessamento < 3:

                if qtdProcessamento == 1:
                    listaNomes = famosos
                else:
                    listaNomesTemp = []
                    for j in listaNomes:
                        listaNomesTemp.append(j[0])
                    listaNomes = listaNomesTemp
                listaNomes = process.extractBests(textoTotal, listaNomes,None,None,57,limit=10000)
                qtdProcessamento += 1

            for r in listaNomes:
                f.writelines(str(r[0])+","+str(r[1])+"\n")

        f.close()
'''