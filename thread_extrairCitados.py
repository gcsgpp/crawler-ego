__author__ = 'Gabriel'

import threading
import time
import queue
import noticias
import model
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

exitFlag = False
listaFamosos = []
for j in model.buscarListaFamoso():
    listaFamosos.append(j[1])

class myThread (threading.Thread):
    def __init__(self, threadID, name, queue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.queue = queue

    def run(self):
        print("Iniciando " + str(self.name))
        extrairCitadosTexto(self.name, self.queue, listaFamosos)
        print("Finalizando " + str(self.name))

def extrairCitadosTexto(threadName, queue, listaFamosos):
    queueLock.acquire()
    while not workQueue.empty():
        n = queue.get()
        print("Queue: " + str(workQueue.qsize()))
        queueLock.release()

        noticia = {'id': n[0], 'titulo': n[1], 'subtitulo': n[2], 'link': n[3], 'tipo': n[4], 'texto': n[5]}
        tempoBest = time.clock()
        textoTotal = noticia['titulo'] + " " + noticia['subtitulo'] + " " + noticia['texto']
        bestExtract = process.extractBests(textoTotal, listaFamosos,None,None,57,limit=10000)
        print("tempoBest:" + str(time.clock() - tempoBest))

        tempoLoop = time.clock()
        for j in bestExtract:
            ratioTotal = 0
            mediaRatio = 0
            nomeCompleto = j[0]
            todosNomes = nomeCompleto.split(" ")
            textoTotal = noticia['titulo'] + " " + noticia['subtitulo'] + " " + noticia['texto']

            ratioTotal += fuzz.token_set_ratio(nomeCompleto, textoTotal)
            if len(todosNomes) > 1:
                for nome in todosNomes:
                    ratioTotal += fuzz.token_set_ratio(nome, textoTotal)

            if len(todosNomes) == 1:
                mediaRatio = ratioTotal
            elif len(todosNomes) > 1:
                mediaRatio = ratioTotal / (len(todosNomes) + 1)

            if mediaRatio > 85:
                model.relacionarFamosoNoticia(nomeCompleto, noticia['id'])
        print("tempo loop:" + str(time.clock() - tempoLoop))

        print(str(threadName) + " - " + str(noticia['titulo']))
        queueLock.acquire()
    queueLock.release()

threadList = []
numero = 1
while numero <= 1:
    threadList.append("Thread-" + str(numero))
    numero += 1

queueLock = threading.Lock()
workQueue = queue.Queue(0)

listaNoticias = model.buscarListaNoticias()
for noticia in listaNoticias:
    workQueue.put(noticia)

threads = []
threadID = 1

for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

time.clock()

for t in threads:
    t.join()
print(str(time.clock()))
print("Fim")