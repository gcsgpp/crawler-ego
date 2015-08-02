__author__ = 'Gabriel'

from bs4 import BeautifulSoup as bs
import json
import urllib.request
import urllib.error
import model
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def buscarnoticiasjson(pagina):
    tentarOutraPagina = True
    noticiaErro = 0

    while tentarOutraPagina == True:
        noticias = None
        tentativas = 1
        tentarNovamente = True

        while tentarNovamente == True:
            try:
                listaNoticias = urllib.request.urlopen("http://ego.globo.com/api/ultimas/todos/" + str(pagina) + "/20.json")

                noticias = listaNoticias.read().decode("utf-8")
                noticias = json.loads(noticias)
                noticias = noticias['ultimas']

                if listaNoticias.code == 200:
                    print("************Pagina " + str(pagina) + " encontrada com sucesso.")
                    return {'noticias': noticias, 'ultimaPagina': pagina}

            except urllib.request.HTTPError as err:
                if err.code == 404:
                    print("************Pagina " + str(pagina) + " nao encontrada. Tentativa: " + str(tentativas))
                    if tentativas >= 5:
                        tentarNovamente = False
                        print("************Tentativas esgotadas, tentando proxima pagina")
                        pagina += 1
                        if noticiaErro >= 5:
                            return False
                        noticiaErro += 1
                    tentativas += 1
                    time.sleep(2)


def processarNoticias():
    noticias = {}
    pagina = 479; ''' 496; ultima pagina: 5364'''
    while noticias != False:
        noticias = buscarnoticiasjson(pagina)
        if noticias != False:
            pagina = noticias['ultimaPagina'] + 1
            for i in noticias['noticias']:
                html = urllib.request.urlopen(i['permalink'])
                soup = bs(html, "html.parser")
                i['titulo'] = i['titulo'].replace("\n","")
                i['titulo'] = i['titulo'].replace("\t","")
                i['titulo'] = i['titulo'].replace("\r","")
                i['titulo'] = i['titulo'].replace('"', "'")
                i['titulo'] = i['titulo'].replace("\u266a","")
                i['titulo'] = i['titulo'].strip()

                if model.verificarNoticiaInserida(i['titulo'], i['permalink']) == False:
                    if i['tipo'] == "materia":
                        paragrafos = soup.find('div', class_ = "materia-conteudo").find_all('p')
                        texto = ""
                        for j in paragrafos:
                            temp = j.get_text()
                            temp = temp.replace("\n","")
                            temp = temp.replace("\t","")
                            temp = temp.replace("\r","")
                            temp = temp.replace("\u266a","")
                            if len(temp) > 3:
                                texto += temp

                        texto = texto.replace('"',"'")
                        i['subtitulo'] = i['subtitulo'].replace('"', "'")
                    else:
                        '''Noticia do tipo Galeria que não possui texto'''
                        print("************ Noticia tipo GALERIA: " + i['permalink'] + " TIPO: " + str(i['tipo']))
                        texto = None
                        i['subtitulo'] = i['subtitulo'].replace('"',"'")
                    noticia = { 'titulo': i['titulo'], 'tipo': i['tipo'], 'subtitulo': i['subtitulo'], 'link': i['permalink'], 'texto': texto, 'data': i['primeira_publicacao']}
                    model.cadastrarNoticia(noticia)
        else:
            tentarNovamente = False
'''
def extrairCitadosTexto():
    listaFamosos = model.buscarListaFamoso()
    listaNoticias = model.buscarListaNoticias()
    f = open("arquivoTeste.txt", "w")
    if listaNoticias != False and listaFamosos != False:
        for i in listaNoticias[:5]:
            f.writelines(str(i[1]) + "\n")
            noticia = {'id': i[0], 'titulo': i[1], 'subtitulo': i[2], 'link': i[3], 'tipo': i[4], 'texto': i[5]}
            print(str(noticia['titulo']))

            bestExtract = extrairCitadosTextoBestExtract(noticia['link'])

            for j in bestExtract:
                famoso = {'nome': j[0]}
                ratioTotal = 0
                mediaRatio = 0
                nomeCompleto = famoso['nome']
                todosNomes = famoso['nome'].split(" ")
                textoTotal = noticia['titulo'] + " " + noticia['subtitulo'] + " " + noticia['texto']

                ratioTotal += fuzz.token_set_ratio(nomeCompleto, textoTotal)
                if len(todosNomes) > 1:
                    for nome in todosNomes:
                        ratioTotal += fuzz.token_set_ratio(nome, textoTotal)

                if len(todosNomes) == 1:
                    mediaRatio = ratioTotal
                elif len(todosNomes) > 1:
                    mediaRatio = ratioTotal / (len(todosNomes) + 1)

                'comentario'print(str(nomeCompleto) + "," + str(mediaRatio))'comentario'
                if mediaRatio > 20:
                    f.writelines(str(nomeCompleto) + "," + str(mediaRatio)+"\n")

                if mediaRatio > 85:
                    'comentario'model.relacionarFamosoNoticia(famoso['nome'], noticia['id'])'comentario'
                    'comentario'print(" - " + str(nomeCompleto))'comentario'
        f.close()

def extrairCitadosTextoBestExtract(link):
    listaFamosos = model.buscarListaFamoso()
    noticiaDB = model.buscarNoticia(link)
    f = open("arquivoTeste2.txt", "w")
    if noticiaDB != False and listaFamosos != False:
        f.writelines(str(noticiaDB[1]) + "\n")
        noticia = {'id': noticiaDB[0], 'titulo': noticiaDB[1], 'subtitulo': noticiaDB[2], 'link': noticiaDB[3], 'tipo': noticiaDB[4], 'texto': noticiaDB[5]}
        print(str(noticia['titulo']))
        famosos = []
        for j in listaFamosos:
            famosos.append(j[1])

        textoTotal = noticia['titulo'] + " " + noticia['subtitulo'] + " " + noticia['texto']

        result = process.extractBests(textoTotal, famosos,None,None,57,limit=10000)

        for r in result:
            f.writelines(str(r[0])+","+str(r[1])+"\n")

        f.close()
        return result
'''

def extrairCitadosTexto():
    listaFamosos = model.buscarListaFamoso()
    listaNoticias = model.buscarListaNoticias()
    qtdNoticiaAtual =0
    qtdTotalNoticias = len(listaNoticias)
    if listaNoticias != False and listaFamosos != False:
        for i in listaNoticias:
            qtdNoticiaAtual += 1
            noticia = {'id': i[0], 'titulo': i[1], 'subtitulo': i[2], 'link': i[3], 'tipo': i[4], 'texto': i[5]}
            print(str(qtdNoticiaAtual) + "/" + str(qtdTotalNoticias) + " - " + str(noticia['titulo']))
            for j in listaFamosos:
                famoso = {'id': j[0], 'nome': j[1], 'link': j[2], 'dataNascimento': j[3], 'idade': j[4], 'signo': j[5], 'relacionamento': j[6], 'conjuge': j[7]}
                ratioTotal = 0
                mediaRatio = 0
                nomeCompleto = famoso['nome']
                todosNomes = famoso['nome'].split(" ")
                textoTotal = noticia['titulo'] + " " + noticia['subtitulo'] + " " + noticia['texto']

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


tentarNovamente = True
qtd = 0
while tentarNovamente == True:
    try:
        processarNoticias()
        qtd = 0
    except Exception as e:
        print(str(e))
        print("Esperando 5 segundos.....")
        time.sleep(5)
        qtd += 1
        if qtd > 5:
            tentarNovamente = False
'''extrairCitadosTexto()'''
print("Fim da execucao")