__author__ = 'Gabriel'

import threading
import time
import queue
import noticias
from bs4 import BeautifulSoup as bs
import urllib.request
import urllib.error
import model

exitFlag = False
'''model.cnx = model.conexao()'''

class myThread (threading.Thread):
    def __init__(self, threadID, name, queue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.queue = queue

    def run(self):
        print("Iniciando " + str(self.name))
        processarNoticia(self.name, self.queue)
        print("Finalizando " + str(self.name))

def processarNoticia(threadName, queue):
    while not exitFlag or not workQueue.empty():
        queueLock.acquire()
        if not workQueue.empty():
            noticia = queue.get()
            print("  -- Queue: " + str(workQueue.qsize()))
            queueLock.release()
            buscarPagina = True
            while buscarPagina:
                try:
                    html = urllib.request.urlopen(noticia['permalink'])
                    soup = bs(html, "html.parser")
                    buscarPagina = False
                except urllib.error.HTTPError as e:
                    if e.code == 404:
                        print(str(threadName) + " - Noticia nao encontrada. (Erro 404) - Proxima noticia... ")
                        '''model.gravarLog(idMensagens=11, link=noticia['permalink'])'''
                        return
                    else:
                        print("httpError *********************************************** " + str(e.code) + " -- " + str(e))
                except urllib.error.URLError as ee:
                    print(" --> Noticia: " + noticia['titulo'] + str(threadName) + " - Pagina negada")
                    time.sleep(5)
                    buscarPagina = True

                except Exception as eee:
                    print(" --> Noticia: " + noticia['titulo'] + "*********************************************** " + str(eee))
                    time.sleep(5)
                    buscarPagina = True

            noticia['titulo'] = noticia['titulo'].replace("\n","")
            noticia['titulo'] = noticia['titulo'].replace("\t","")
            noticia['titulo'] = noticia['titulo'].replace("\r","")
            noticia['titulo'] = noticia['titulo'].replace('"', "'")
            noticia['titulo'] = noticia['titulo'].replace("\u266a","")
            noticia['titulo'] = noticia['titulo'].replace("\u200f","")
            noticia['titulo'] = noticia['titulo'].strip()

            if model.verificarNoticiaInseridaComThread(noticia['titulo'], noticia['permalink'], threadName) == False:
                if noticia['tipo'] == "materia":
                    try:
                        paragrafos = soup.find('div', class_ = "materia-conteudo").find_all('p')
                    except:
                        print(str(threadName) + " - Noticia sem paragrafos. **********************************")
                        '''model.gravarLog(idMensagens=27,tituloNoticia=noticia['titulo'], link= noticia['permalink'])'''
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
                    noticia['subtitulo'] = noticia['subtitulo'].replace('"', "'")

                else:
                    '''Noticia do tipo Galeria que nao possui texto'''
                    print(str(threadName) + " - ************ Noticia tipo GALERIA: " + noticia['permalink'] + " TIPO: " + str(noticia['tipo']))
                    texto = None
                    noticia['subtitulo'] = noticia['subtitulo'].replace('"',"'")
                noticia = { 'titulo': noticia['titulo'], 'tipo': noticia['tipo'], 'subtitulo': noticia['subtitulo'], 'link': noticia['permalink'], 'texto': texto, 'data': noticia['primeira_publicacao']}
                model.cadastrarNoticiaComThread(noticia, threadName)

                listaCategorias = soup.find('ul', class_ = 'lista-categorias')
                if listaCategorias != None:
                    listaCategorias = listaCategorias.findAll("span", class_ = "borda-interna")
                    if listaCategorias != None:
                        idNoticia = model.buscarNoticiaComThread(noticia['link'])
                        if idNoticia != False:
                            idNoticia = idNoticia[0]
                            for i in listaCategorias:
                                idCategoria = model.buscarCategoria(i.get_text())
                                if idCategoria == None:
                                    model.cadastrarCategoriaNoticia(i.get_text())
                                    idCategoria = model.buscarCategoria(i.get_text())

                                idCategoria = idCategoria[0]
                                model.vincularCategoriaNoticia(idCategoria, idNoticia)
        else:
            queueLock.release()

threadList = []
numero = 1
while numero <= 20:
    threadList.append("Thread-" + str(numero))
    numero += 1

queueLock = threading.Lock()
workQueue = queue.Queue(0)
threads = []
threadID = 1

for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1


pagina = 5450;
tentarNovamente = True
qtd = 0
time.clock()
while tentarNovamente == True:
    try:
        listaNoticias = noticias.buscarnoticiasjson(pagina)
        if listaNoticias == False:
            tentarNovamente = False
            continue

        '''queueLock.acquire()'''
        for noticia in listaNoticias['noticias']:
            workQueue.put(noticia)
        print("  --> Queue: " + str(workQueue.qsize()))
        '''queueLock.release()'''

        if workQueue.qsize() >= 1000:
            print("####################################################### Ultima pagina: " + str(pagina))
            time.sleep(10)
        '''
        if pagina == 100:
            tentarNovamente = False
            exitFlag = True
        '''
        pagina = listaNoticias['ultimaPagina'] + 1
        qtd = 0


    except Exception as e:
        print(str(e))
        print("Esperando 5 segundos.....")
        time.sleep(5)
        qtd += 1
        if qtd > 5:
            tentarNovamente = False
            exitFlag = True

for t in threads:
    t.join()
print(str(time.clock()))
print("Fim")