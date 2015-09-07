__author__ = 'Gabriel'

from bs4 import BeautifulSoup as bs
import model
import urllib.request
import urllib.error
import time

def limpezaNome(i):
    i = str(i)
    i = i.replace("'",""); '''Retirada de aspas simples dos nomes '''

    '''Retirada de conectivos dos nomes (exemplo: "do da de") '''
    todosNomes = i.split(" ")
    i = ""
    for j in todosNomes:
        if len(j) > 3 or j == todosNomes[0] or j == todosNomes[len(todosNomes) - 1]:
            if len(i) == 0:
                i = j
            else:
                i += " " + j

    ''' fim da retirada doss conectivos '''

    return i

def crawlerFamosoRelacionados(i):
        famoso = {'id': i[0], 'nome': i[1].strip(), 'link': i[2], 'nascimento': i[3], 'idade': i[4], 'signo': i[5], 'relacionamento': i[6], 'conjuge': i[7]}
        try:
            html = urllib.request.urlopen("http://ego.globo.com" + famoso['link'])
            soup = bs(html, "html.parser")
            listaRelacionados = soup.find("ul", class_ = "famosos-relacionados")

            print(str(famoso['nome']))
            if listaRelacionados != None:
                listaRelacionados = listaRelacionados.find_all("a")

                for j in listaRelacionados:
                    linkRelacionado = j.attrs['href']
                    nomeRelacionado = j.find("img").attrs['alt']
                    '''nomeRelacionado = limpezaNome(nomeRelacionado)'''
                    famosoRelacionado = {"idFamoso1": famoso['id'], "nome": nomeRelacionado, "link": linkRelacionado }

                    if model.verificarFamosoRelacionadoJaInserido(famosoRelacionado['idFamoso1'],famosoRelacionado['nome']) == False:
                        if model.inserirFamosoRelacionado(famosoRelacionado) == True:
                            print("  - Famoso: " + str(famosoRelacionado['nome']) + " inserido com sucesso.")
                    else:
                        print("  - Famoso: " + str(famosoRelacionado['nome']) + " já inserido.")

            return True
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print("Pagina do famoso nao encontrada")
                model.gravarLog(idMensagens = 11, idFamoso = famoso['id'])
                return False
            else:
                print(str(e) + " Famoso: " + str(famoso['nome']))
                return False
        except Exception as e:
            print(str(e))
            return False


def crawlerListaFamosos():
    html = urllib.request.urlopen("http://ego.globo.com/famosos/")
    soup = bs(html, "html.parser")
    listahtmlfamosos = soup.find(id = 'main').find_all("a")
    qtdAtualFamosos = 0
    qtdTotalFamosos = len(listahtmlfamosos)
    for i in listahtmlfamosos:
        qtdAtualFamosos += 1
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
                else:
                    relacionamento = 0

                conjuge = detalheshtml.find("li", class_="relacionamento")
                if conjuge != None:
                    conjuge = conjuge.find("a")
                    if conjuge != None:
                        conjugeNome = conjuge.get_text()
                        '''conjugeNome = limpezaNome(conjugeNome)'''

                        conjuge = model.inserirConjuge(conjugeNome, famoso['nome'])
                    else:
                        conjuge = 0
                else:
                    conjuge = 0

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

            '''famoso['nome'] = limpezaNome(famoso['nome'])'''
            famoso.update({'nome': famoso['nome'].strip(), 'idade': idade, 'datanascimento': datanascimento, 'signo': signo, 'relacionamento': relacionamento, 'conjuge': conjuge })

            model.inserirfamososdb(famoso,qtdAtualFamosos, qtdTotalFamosos)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                model.gravarLog(idMensagens = 11, nomeFamoso = famoso['nome'])
                print("Página não encontrada. Gravado no log com sucesso! Famoso: " + famoso['nome'])

                relacionamento = conjuge = idade = datanascimento = signo = ''

                '''famoso['nome'] = limpezaNome(famoso['nome'])'''
                famoso.update({'nome': famoso['nome'], 'idade': idade, 'datanascimento': datanascimento, 'signo': signo, 'relacionamento': relacionamento, 'conjuge': conjuge })
                model.inserirfamososdb(famoso)

            else:
                model.gravarLog(idMensagens = 12, nomeFamoso = famoso['nome'])
                print("Erro inesperado ao obter detalhes do famoso. Gravado no log com sucesso! Famoso: " + famoso['nome'])
'''
tentarNovamente = True
qtd = 0
while tentarNovamente == True:
    try:
        crawlerListaFamosos()
        tentarNovamente = False
    except Exception as e:
        print(str(e))
        print("Esperando 5 segundos.....")
        time.sleep(5)
        qtd += 1
        if qtd > 5:
            tentarNovamente = False
'''
print("*****************************************************")
print("*****************************************************")
print("***********INICIO FAMOSO RELACIONADO*****************")
print("*****************************************************")
print("*****************************************************")

tentarNovamente = True
posicaoFamoso = qtdTentativas = 1830
listafamosos = model.buscarListaFamoso()
while posicaoFamoso <= (len(listafamosos) - 1):
    print("Famoso: " + str(posicaoFamoso + 1) + "/" + str(len(listafamosos)))
    if crawlerFamosoRelacionados(listafamosos[posicaoFamoso]) == True:
        posicaoFamoso += 1
    else:
        print("Esperando 5 segundos.....")
        time.sleep(5)
        qtdTentativas += 1
        if qtdTentativas > 5:
            posicaoFamoso += 1

