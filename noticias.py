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
                    time.sleep(5)


def processarNoticias(noticias):
    for i in noticias:
        try:
            html = urllib.request.urlopen(i['permalink'])
            soup = bs(html, "html.parser")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print("Noticia não encontrada. (Erro 404) - Proxima noticia... ")
                model.gravarLog(idMensagens=11, link=i['permalink'])
                continue
        i['titulo'] = i['titulo'].replace("\n","")
        i['titulo'] = i['titulo'].replace("\t","")
        i['titulo'] = i['titulo'].replace("\r","")
        i['titulo'] = i['titulo'].replace('"', "'")
        i['titulo'] = i['titulo'].replace("\u266a","")
        i['titulo'] = i['titulo'].replace("\u200f","")
        i['titulo'] = i['titulo'].strip()

        if model.verificarNoticiaInserida(i['titulo'], i['permalink']) == False:
            if i['tipo'] == "materia":
                try:
                    paragrafos = soup.find('div', class_ = "materia-conteudo").find_all('p')
                except:
                    print("Noticia sem paragrafos. **********************************")
                    model.gravarLog(idMensagens=27,tituloNoticia=i['titulo'], link= i['permalink'])
                    continue
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

def extrairCitadosTexto():
    listaFamosos = model.buscarListaFamoso()
    listaNoticias = model.buscarListaNoticias()
    f = open("arquivoTeste.txt", "w")
    f2 = open("arquivoTeste2.txt", "w")
    if listaNoticias != False and listaFamosos != False:
        for i in listaNoticias[:50]:
            f.writelines(str(i[1]) + "\n")
            noticia = {'id': i[0], 'titulo': i[1], 'subtitulo': i[2], 'link': i[3], 'tipo': i[4], 'texto': i[5]}
            print(str(noticia['titulo']))

            bestExtract = extrairCitadosTextoBestExtract(noticia['link'],f2)

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

                '''print(str(nomeCompleto) + "," + str(mediaRatio))'''
                if mediaRatio > 20:
                    f.writelines(str(nomeCompleto) + "," + str(round(mediaRatio,1))+"\n")

                if mediaRatio > 85:
                    '''model.relacionarFamosoNoticia(famoso['nome'], noticia['id'])'''
                    '''print(" - " + str(nomeCompleto))'''
        f.close()
        f2.close()

def extrairCitadosTextoBestExtract(link,f):
    listaFamosos = model.buscarListaFamoso()
    noticiaDB = model.buscarNoticia(link)

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
            f.writelines(str(r[0])+","+str(round(r[1],1))+"\n")

        return result

def alterarTituloNoticias():
    listaNoticias = model.buscarListaNoticias()
    for noticia in listaNoticias:
        titulo = noticia[1]

        if "\u200f" in titulo:
            titulo = titulo.replace("\u200f", "")
            titulo = titulo.strip()
            model.atualizarTituloNoticia(idNoticia = noticia[0], novoTitulo = titulo)
            print(str(noticia[0]) + "/" + str(len(listaNoticias)) + " - Titulo atualizado")
        else:
            print(str(noticia[0]) + "/" + str(len(listaNoticias)))


'''
pagina = 2000; ultima pagina: 5364
tentarNovamente = True
qtd = 0
while tentarNovamente == True:
    try:
        conteudo = buscarnoticiasjson(pagina)
        if conteudo == False:
            tentarNovamente = False
        processarNoticias(conteudo['noticias'])
        pagina = conteudo['ultimaPagina'] + 1
        qtd = 0
    except Exception as e:
        print(str(e))
        print("erro aqui")
        print("Esperando 5 segundos.....")
        time.sleep(5)
        qtd += 1
        if qtd > 5:
            tentarNovamente = False
'''
'''extrairCitadosTexto()'''

print("Fim da execucao")