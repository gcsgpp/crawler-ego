__author__ = 'Gabriel'

from bs4 import BeautifulSoup as bs
import model
import urllib.request
import urllib.error

def limpezaNome(i):
    i['nome'] = i['nome'].replace("'",""); '''Retirada de aspas simples dos nomes '''

    '''Retirada de conectivos dos nomes (exemplo: "do da de") '''
    todosNomes = i['nome'].split(" ")
    i['nome'] = ""
    for j in todosNomes:
        if len(j) > 3 or j == todosNomes[0] or j == todosNomes[len(todosNomes) - 1]:
            if len(i['nome']) == 0:
                i['nome'] = j
            else:
                i['nome'] += " " + j

    ''' fim da retirada doss conectivos '''

    return i['nome']

def crawlerFamosoRelacionados():
    listafamosos = model.buscarListaFamoso()
    for i in listafamosos:
        famoso = {'id': i[0], 'nome': i[1].decode("utf-8"), 'link': i[2].decode("utf-8"), 'nascimento': i[3], 'idade': i[4], 'signo': i[5], 'relacionamento': i[6], 'conjuge': i[7]}
        html = urllib.request.urlopen("http://ego.globo.com" + famoso['link'])
        soup = bs(html, "html.parser")
        listaRelacionados = soup.find("ul", class_ = "famosos-relacionados").find_all("a")

        print("Inserindo famosos relacionados de: " + str(famoso['nome']))
        for j in listaRelacionados:
            linkRelacionado = j.attrs['href']
            nomeRelacionado = j.find("img").attrs['alt']
            famosoRelacionado = {"idFamoso1": famoso['id'], "nome": nomeRelacionado, "link": linkRelacionado }

            if model.verificarFamosoRelacionadoJaInserido(famosoRelacionado['idFamoso1'],famosoRelacionado['nome']) == False:
                model.inserirFamosoRelacionado(famosoRelacionado)
                print("  - Famoso: " + str(famosoRelacionado['nome']) + " inserido com sucesso.")
            else:
                print("  - Famoso: " + str(famosoRelacionado['nome']) + " já inserido.")

def crawlerListaFamosos():
    html = urllib.request.urlopen("http://ego.globo.com/famosos/")
    soup = bs(html, "html.parser")
    listahtmlfamosos = soup.find(id = 'main').find_all("a")
    listafamosos = []
    for i in listahtmlfamosos:
        famoso = { 'link': i.get('href'), 'nome': i.get_text() }

        try:
            htmldetalhes = urllib.request.urlopen("http://ego.globo.com" + famoso['link'])

            soupdetalhes = bs(htmldetalhes, "html.parser")

            detalheshtml = soupdetalhes.find("ul", class_ = "detalhes")
            if detalheshtml != None:
                relacionamento = detalheshtml.find("li", class_="relacionamento")
                if relacionamento != None:
                    relacionamento = relacionamento.get_text()
                    relacionamento = relacionamento.split(" ")
                    relacionamento = relacionamento[0]
                    relacionamento = relacionamento.replace("\n", "")

                    if relacionamento == "casada": relacionamento = "casado"
                    if relacionamento == "solteira": relacionamento = "solteiro"
                    if relacionamento == "divorciada": relacionamento = "divorciado"

                    relacionamento = model.buscarTipoRelacionamento(relacionamento, famoso['nome'])

                conjuge = detalheshtml.find("li", class_="relacionamento")
                if conjuge != None:
                    conjuge = conjuge.find("a")
                    if conjuge != None:
                        conjugeNome = conjuge.get_text()
                        conjugeNome = limpezaNome({"nome": conjugeNome})
                        conjuge = model.inserirConjuge(conjugeNome, famoso['nome'])

                idade = detalheshtml.find("li", class_ = "aniversario")
                if idade != None:
                    idade = idade.get_text()
                    idade = idade.split("(")
                    idade = idade[len(idade) - 1]
                    idade = int(idade[:2])

                datanascimento = detalheshtml.find("time")
                if datanascimento != None:
                    datanascimento = datanascimento['datetime']

                signo = detalheshtml.find("li", class_ = "signo")
                if signo != None:
                    signo = signo.find("a").get_text()
                    signo = model.buscarSigno(signo, famoso['nome'])


            famoso.update({'idade': limpezaNome(famoso), 'idade': idade, 'datanascimento': datanascimento, 'signo': signo, 'relacionamento': relacionamento, 'conjuge': conjuge })


            model.inserirfamososdb(famoso)


        except urllib.error.HTTPError as err:
            if err.code == 404:
                model.gravarLog(idMensagens = 11, nomeFamoso = famoso['nome'])
                print("Página não encontrada. Gravado no log com sucesso! Famoso: " + famoso['nome'])
            else:
                model.gravarLog(idMensagens = 12, nomeFamoso = famoso['nome'])
                print("Erro inesperado ao obter detalhes do famoso. Gravado no log com sucesso! Famoso: " + famoso['nome'])

'''crawlerListaFamosos()'''
crawlerFamosoRelacionados()