__author__ = 'Gabriel'

from bs4 import BeautifulSoup as bs
import json
import urllib.request
import urllib.error
import model
import time

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
    pagina = 1
    while noticias != False:
        noticias = buscarnoticiasjson(pagina)
        if noticias != False:
            pagina = noticias['ultimaPagina'] + 1
            for i in noticias['noticias']:
                html = urllib.request.urlopen(i['permalink'])
                soup = bs(html, "html.parser")
                i['titulo'] = i['titulo'].strip()
                i['titulo'] = i['titulo'].replace("\n","")
                i['titulo'] = i['titulo'].replace("\t","")
                i['titulo'] = i['titulo'].replace("\r","")

                if i['titulo'] == "Munhoz e Mariano pedem orações para família de Cristiano Araújo":
                    print("carai")

                if model.verificarNoticiaInserida(i['titulo'], i['permalink']) == False:
                    if i['tipo'] == "materia":
                        paragrafos = soup.find('div', class_ = "materia-conteudo").find_all('p')
                        texto = ""
                        for j in paragrafos:
                            temp = j.get_text()
                            temp = temp.replace("\n","")
                            temp = temp.replace("\t","")
                            temp = temp.replace("\r","")
                            if len(temp) > 3:
                                texto += temp

                        texto = texto.replace('"',"'")
                        i['titulo'] = i['titulo'].replace('"', "'")
                        i['subtitulo']  = i['subtitulo'].replace('"', "'")
                    else:
                        '''Noticia do tipo Galeria que não possui texto'''
                        print("************ Noticia tipo GALERIA: " + i['permalink'] + " TIPO: " + str(i['tipo']))
                        texto = None
                    noticia = { 'titulo': i['titulo'], 'tipo': i['tipo'], 'subtitulo': i['subtitulo'], 'link': i['permalink'], 'texto': texto, 'data': i['primeira_publicacao']}
                    model.cadastrarNoticia(noticia)
processarNoticias()

