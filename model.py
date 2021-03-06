__author__ = 'Gabriel'
import mysql.connector
import pyodbc

cnx = ""

def conexao():
    conn = pyodbc.connect(Driver='{SQL Server}', server='DESKTOP-0PK4UDR\SQLEXPRESS', Database='famososdb', uid='sa', pwd='12345')
    return conn
    '''return mysql.connector.connect(host = "localhost", user = "root", database = "famososdb", charset="utf8")'''

def gravarLog(idMensagens, idFamoso = '', idFamoso2 = '', idNoticia = '', nomeFamoso = '', tituloNoticia = '', link = ''):
    cnx = conexao()
    cursor = cnx.cursor()
    nomeFamoso = nomeFamoso.replace("'", "''")
    tituloNoticia = tituloNoticia.replace("'", "''")
    sql = "INSERT INTO log(idMensagensLog, idFamoso, idFamoso2, idNoticia, nomeFamoso, tituloNoticia, link) VALUES('" + str(idMensagens) + "','" + str(idFamoso) + "','" + str(idFamoso2) + "','" + str(idNoticia) + "','" + str(nomeFamoso) + "','" + str(tituloNoticia) + "','" + str(link) + "')"

    cursor.execute(sql)
    cnx.commit()
    cursor.close()
    cnx.close()

def inserirFamosoRelacionado(famosoRelacionado):
    cnx = conexao()
    cursor = cnx.cursor()

    famosoRelacionado['nome'] = famosoRelacionado['nome'].replace("'", "''")

    id = buscarFamosoPorNome(famosoRelacionado['nome'])
    if id != False and id > 0:
        sql = "INSERT INTO famoso_relacionado (idFamoso1, idFamoso2) VALUES(" + str(famosoRelacionado['idFamoso1']) + " , " + str(id )+ ")"

        try:
            cursor.execute(sql)
            cnx.commit()
            return True
        except Exception as e:
            print(str(e))
            print("inserirFamosoRelacionado - " + "Erro ao inserir famoso relacionado")
            gravarLog(idMensagens = 15, idFamoso = famosoRelacionado['idFamoso1'], idFamoso2 = id)
            return False
    elif  id >= 1:
        return False
        print(" - Famoso relacionado já inserido no BD. Famoso relacionado: " + str(famosoRelacionado))
    elif id == False:
        print("Famoso relacionado não encontrado no BD.")
        gravarLog(idMensagens = 22, idFamoso = famosoRelacionado['idFamoso1'], nomeFamoso = famosoRelacionado['nome'])
    else:
        print("Erro ao encontrar famoso pelo nome. ***********************************************")
        gravarLog(idMensagens = 14, nomeFamoso = famosoRelacionado['nome'])
        return False

    cursor.close()
    cnx.close()

def verificarFamosoRelacionadoJaInserido(idFamoso, nomeFamosoRelacionado):
    cnx = conexao()
    cursor = cnx.cursor()

    nomeFamosoRelacionado = nomeFamosoRelacionado.replace("'", "''")

    idFamoso2 = buscarFamosoPorNome(nomeFamosoRelacionado)
    sql = "SELECT * FROM famoso_relacionado WHERE (idFamoso1 = '" + str(idFamoso) + "' and idFamoso2 = '" + str(idFamoso2) + "') or (idFamoso1 = '" + str(idFamoso2) + "' and idFamoso2 = '" + str(idFamoso) + "')"

    try:
        cursor.execute(sql)
        result = cursor.fetchone()

        cursor.close()
        cnx.close()

        if result != None:
            return True
        else:
            return False
    except Exception as e:
        print("Erro ao verificar Famoso relacionado já existe.")
        print("verificarFamosoRelacionadoJaInserido - " + str(e))
        gravarLog(idMensagens = 21,idFamoso = idFamoso, idFamoso2 = idFamoso2)




def buscarFamosoPorNome(nomeFamoso):
    cnx = conexao()
    cursor = cnx.cursor()

    try:
        query = "SELECT * FROM famoso where nome = '" + str(nomeFamoso) + "'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result != None:
            return result[0]
        else:
            return 0
    except:
        gravarLog(idMensagens = 14, nomeFamoso = nomeFamoso)
        print("buscarFamosoPorNome" + "Erro ao buscar famoso pelo nome. ************************************************")

    cursor.close()
    cnx.close()

def verificarFamosoInserido(cnx, nomeFamoso):
    cnx = conexao()
    cursor = cnx.cursor()

    try:
        query = "SELECT * FROM famoso where nome = '" + nomeFamoso + "'"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        else:
            return True
    except:
        gravarLog(idMensagens = 2, nomeFamoso = nomeFamoso)
        print("verificarFamosoInserido - " + "Erro ao verificar famoso já inserido. ************************************************")

    cursor.close()
    cnx.close()


def inserirfamososdb(famoso, qtdAtualFamoso = 0, qtdTotalFamosos = 0):
    cnx = conexao()
    cursor = cnx.cursor()

    famoso['nome'] = famoso['nome'].replace("'", "''")

    if verificarFamosoInserido(cnx, famoso['nome']) == True:
        print(famoso['nome'] + " -> JA INSERIDO NO BD")
    else:
        '''if famoso['conjuge'] != None:
            try:
                query = "SELECT id FROM famoso WHERE famoso.id = '" + str(famoso['conjuge']) + "'"
                cursor.execute(query)
                result = cursor.fetchall()
                idConjuge = result[0]
            except:
                print("inserirfamososdb1 - " + "Nao foi possivel encontrar conjuge na tabela de famosos")
                gravarLog(idMensagens = 9, nomeFamoso = famoso['nome'])
        else:
            idConjuge = 0'''
        try:
            query = "INSERT INTO famoso(nome, link, datanascimento, idade, signo, relacionamento, conjuge) VALUES('" + str(famoso['nome']) + "' , '" + str(famoso['link']) + "' , '" + str(famoso['datanascimento']) + "' , '" + str(famoso['idade']) + "' , '" + str(famoso['signo']) + "' , '" + str(famoso['relacionamento']) + "' , '" + str(famoso['conjuge']) + "')"

            cursor.execute(query)
            cnx.commit()
            '''gravarLog(idMensagens = 3, idFamoso = cursor.lastrowid)'''
            print(str(qtdAtualFamoso) + "/" + str(qtdTotalFamosos) + " - " + famoso['nome'] + " INSERIDO COM SUCESSO.")
        except Exception as e:
            print(str(e))
            gravarLog(idMensagens = 8, nomeFamoso = famoso['nome'])
            print("inserirfamososdb - " +"Erro ao inserir famoso na lista. Famoso: " + famoso['nome'] + "**********************************")

    cursor.close()
    cnx.close()

def buscarTipoRelacionamento(descricaoRelacionamento, nomeFamoso):
    cnx = conexao()
    cursor = cnx.cursor()

    nomeFamoso = nomeFamoso.replace("'", "''")

    try:
        sql = "SELECT * FROM tipos_relacionamentos WHERE descricao = '" + str(descricaoRelacionamento) + "'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result != None:
            cursor.close()
            cnx.close()

            return result[0]
        else:
            sql = "INSERT INTO tipos_relacionamentos(descricao) VALUES('" + str(descricaoRelacionamento) + "')"
            cursor.execute(sql)
            cnx.commit()
            lastrowid = cursor.lastrowid

            cursor.close()
            cnx.close()

            return lastrowid
    except Exception as e:
        print("buscarTipoRelacionamento - " + str(e))
        gravarLog(idMensagens = 16, nomeFamoso = nomeFamoso)
        print("Erro ao descobrir/inserir relacionamento.")

        cursor.close()
        cnx.close()

        return 0

def buscarConjugeJaInserido(nomeConjuge, nomeFamoso):
    cnx = conexao()
    cursor = cnx.cursor()

    nomeFamoso = nomeFamoso.replace("'", "''")
    nomeConjuge = nomeConjuge.replace("'", "''")

    sql = "SELECT * FROM conjuge WHERE nome = '" + str(nomeConjuge) + "'"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        if result != None:
            return result[0]
        else:
            return False
    except Exception as e:
        print("buscarConjugeJaInserido - " + str(e))
        print("Erro ao buscar conjuge já inserido.")
        gravarLog(idMensagens = 20, nomeFamoso = str(nomeFamoso))
        cursor.close()
        cnx.close()
        return False

def inserirConjuge(conjugeNome, nomeFamoso):
    cnx = conexao()
    cursor = cnx.cursor()

    nomeFamoso = nomeFamoso.replace("'", "''")
    conjugeNome = conjugeNome.replace("'", "''")

    try:
        conjugeId = buscarConjugeJaInserido(conjugeNome,nomeFamoso)
        if conjugeId == False:
            sql = "INSERT INTO conjuge (nome) VALUES('" + str(conjugeNome) + "')"
            cursor.execute(sql)
            cnx.commit()

            id = cursor.lastrowid
            cursor.close()
            cnx.close()
            return id
        else:
            cursor.close()
            cnx.close()
            return conjugeId

    except Exception as e:
        gravarLog(idMensagens = 17, nomeFamoso = str(nomeFamoso))
        print("************************************************** Erro ao inserir conjuge no BD.")

        cursor.close()
        cnx.close()

        return 0

def buscarSigno(signo, nomeFamoso):
    cnx = conexao()
    cursor = cnx.cursor()

    nomeFamoso = nomeFamoso.replace("'", "''")

    sql = "SELECT * FROM signos WHERE signo = '" + str(signo) + "'"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        if result != None:
            return result[0]
        else:
            print("Nao foi possivel encontrar o signo do Famoso: " + str(nomeFamoso)+ " na lista do BD. Signo: " + str(signo))
            return 0
    except Exception as e:
        print("buscarSigno - " +str(e))
        print("Erro ao buscar id do signo.")
        gravarLog(idMensagens = 19, nomeFamoso = str(nomeFamoso))
        cursor.close()
        cnx.close()
        return 0

def buscarListaFamoso():
    cnx = conexao()
    cursor = cnx.cursor()
    sql = "SELECT * from famoso"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()

        cursor.close()
        cnx.close()

        result = converterListaUTF8(result)

        return result
    except Exception as e:
        print("buscarListaFamoso - " +str(e))
        print("Erro ao buscar lista de famosos")
        gravarLog(idMensagens = 24)
        cursor.close()
        cnx.close()
        return False


def cadastrarNoticia(noticia):
    cnx = conexao()
    cursor = cnx.cursor()

    if noticia['tipo'] == "materia": noticia['tipo'] = 1
    elif noticia['tipo'] == "galeria": noticia['tipo'] = 2

    noticia['titulo'] = noticia['titulo'].replace("'", "''")
    noticia['subtitulo'] = noticia['subtitulo'].replace("'", "''")
    noticia['texto'] = noticia['texto'].replace("'", "''")


    sql = 'INSERT INTO noticia(titulo, subtitulo, link, tipo, texto, dataPrimeiraPublicacao) VALUES("' + str(noticia['titulo']) + '","' + str(noticia['subtitulo']) + '","' + str(noticia['link']) + '","' + str(noticia['tipo']) + '","' + str(noticia['texto']) + '","' + str(noticia['data']) + '")'

    try:
        cursor.execute(sql)
        cnx.commit()
        print("Noticia: " + noticia['titulo'])
        '''gravarLog(idMensagens = 4, idNoticia = cursor.lastrowid)'''
    except Exception as e:
        print("cadastrarNoticia - " +str(e))
        print("Não foi possivel cadastrar a noticia: " + noticia['link'] + "    *********")
        gravarLog(idMensagens = 13, tituloNoticia = noticia['titulo'])

    cursor.close()
    cnx.close()

def cadastrarNoticiaComThread(noticia, threadName):
    cnx = conexao()
    cursor = cnx.cursor()

    if noticia['tipo'] == "materia": noticia['tipo'] = 1
    elif noticia['tipo'] == "galeria": noticia['tipo'] = 2
    else:
        tipoNoticia = buscarTipoNoticia(str(noticia['tipo']))
        if tipoNoticia == None:
            cadastrarTipoNoticia(str(noticia['tipo']))
            tipoNoticia = buscarTipoNoticia(str(noticia['tipo']))

        noticia['tipo'] = tipoNoticia[0]

    noticia['titulo'] = noticia['titulo'].replace("'", "''")
    noticia['subtitulo'] = noticia['subtitulo'].replace("'", "''")
    if noticia['tipo'] == 1:
        noticia['texto'] = noticia['texto'].replace("'", "''")

    sql = "INSERT INTO noticia4(titulo, subtitulo, link, tipo, texto, dataPrimeiraPublicacao) VALUES('" + str(noticia['titulo']) + "','" + str(noticia['subtitulo']) + "','" + str(noticia['link']) + "','" + str(noticia['tipo']) + "','" + str(noticia['texto']) + "','" + str(noticia['data']) + "')"

    try:
        cursor.execute(sql)
        cnx.commit()
        print(str(threadName) + " - Noticia: " + noticia['titulo'])
        '''gravarLog(idMensagens = 4, idNoticia = cursor.lastrowid)'''
    except Exception as e:
        print("cadastrarNoticiaComThread - " + str(e))
        print("Não foi possivel cadastrar a noticia: " + noticia['link'] + "    *********")
        gravarLog(idMensagens = 13, tituloNoticia = noticia['titulo'])

    cursor.close()
    cnx.close()

def verificarNoticiaInserida(titulo, link):
    cnx = conexao()
    cursor = cnx.cursor()

    titulo = titulo.replace("'", "''")

    sql = "SELECT * from noticia WHERE noticia.titulo = '" + str(titulo) + "' or noticia.link = '" + str(link) + "'"

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
    except Exception as e:
        print("verificarNoticiaInserida - " + str(e))
        print("Erro ao verificar se a noticia ja esta cadastrada")
        cursor.close()
        cnx.close()

    if len(result) == 0:
        return False
    else:
        print("Noticia já cadastrada. Titulo: " + str(titulo))
        return True

def verificarNoticiaInseridaComThread(titulo, link, threadName):
    cnx = conexao()
    cursor = cnx.cursor()

    titulo = titulo.replace("'", "''")

    sql = "SELECT * from noticia4 WHERE noticia4.titulo = '" + str(titulo) + "' or noticia4.link = '" + str(link) + "'"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        cnx.close()

        if len(result) == 0:
            return False
        else:
            print(str(threadName) + " - Noticia ja cadastrada. Titulo: " + str(titulo))
            return True
    except Exception as e:
        print("verificarNoticiaInseridaComThread - " + str(e))
        print(str(threadName) + " - Erro ao verificar se a noticia ja esta cadastrada")
        cursor.close()
        cnx.close()



def buscarListaNoticias():
    cnx = conexao()
    cursor = cnx.cursor()

    sql = "SELECT * FROM noticia4"

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

        cursor.close()
        cnx.close()

        result = converterListaUTF8(result)

        return result
    except Exception as e:
        print("buscarListaNoticias - " + str(e))
        print("Erro ao buscar lista de noticias")
        gravarLog(idMensagens = 23)
        cursor.close()
        cnx.close()
        return False
def verificarRelacionamentoFamosoNoticia(idFamoso, idNoticia, cnx):
    cursor = cnx.cursor()
    sql = "SELECT * FROM famoso_noticia2 WHERE idFamoso = '" + str(idFamoso) + "' and idNoticia = '" + str(idNoticia) + "'"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print("verificarRelacionamentoFamosoNoticia - " + str(e))
        print("Erro ao executar verificação se famoso ja esta relacionado")
        gravarLog(idMensagens=26, idFamoso = idFamoso, idNoticia = idNoticia)
        cursor.close()
        return False

def relacionarFamosoNoticia(nomeFamoso, idNoticia):
    cnx = conexao()


    nomeFamoso = nomeFamoso.replace("'", "''")
    idFamoso = buscarFamosoPorNome(nomeFamoso)

    famosoJaRelacionadoNoticia = verificarRelacionamentoFamosoNoticia(idFamoso, idNoticia, cnx)
    cursor = cnx.cursor()


    if len(famosoJaRelacionadoNoticia) > 0:
        return False

    sql = "INSERT INTO famoso_noticia2(idFamoso, idNoticia) VALUES(" + str(idFamoso) + " , " + str(idNoticia) + ")"
    try:
        cursor.execute(sql)
        cnx.commit()

        cursor.close()
        cnx.close()
    except Exception as e:
        print("relacionarFamosoNoticia - " + str(e))
        print("Erro ao inserir relacionamento do Famoso com a Noticia. Famoso: " + str(nomeFamoso) + " idNoticia: " + str(idNoticia))
        gravarLog(idMensagens = 25, idFamoso = idFamoso, idNoticia = idNoticia)
        cursor.close()
        cnx.close()

def converterListaUTF8(lista):
    listaConvertida = []
    for i in lista:
        if type(i) == list or type(i) == tuple:
            result = converterListaUTF8(i)
        elif type(i) == bytearray or type(i) == bytes:
            result = i.decode("UTF-8")
        else:
            result = i

        listaConvertida.append(result)

    return tuple(listaConvertida)

def buscarNoticia(link):
    cnx = conexao()
    cursor = cnx.cursor()
    sql = "SELECT * from noticia4 WHERE link = '" + str(link) + "'"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        if result != None:
            return converterListaUTF8(result)
        else:
            return False
    except Exception as e:
        print("buscarNoticia - " + str(e))
        cursor.close()
        cnx.close()
        return False

def buscarNoticiaComThread(link):
    cnx = conexao()
    cursor = cnx.cursor()
    sql = "SELECT * from noticia4 WHERE link = '" + str(link) + "'"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        if result != None:
            return converterListaUTF8(result)
        else:
            return False
    except Exception as e:
        print("buscarNoticiaComThread - " + str(e))
        cursor.close()
        cnx.close()
        return False

def atualizarTituloNoticia(idNoticia, novoTitulo):
    cnx = conexao()
    cursor = cnx.cursor()

    novoTitulo = novoTitulo.replace("'", "''")

    sql = 'UPDATE noticia4 SET titulo = "' + str(novoTitulo) + '" WHERE id = "' + str(idNoticia) + '"'
    try:
        cursor.execute(sql)
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as e:
        cursor.close()
        cnx.close()
        print("atualizarTituloNoticia - " + str(e))

def buscarCategoria(categoria):
    cnx = conexao()
    cursor = cnx.cursor()
    sql = "SELECT * FROM tipos_categorias WHERE categoria = '" + str(categoria) + "'"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return result
    except Exception as e:
        cursor.close()
        cnx.close()
        print("buscarCategoria - " + str(e))

def cadastrarCategoriaNoticia(categoria):
    cnx = conexao()
    cursor = cnx.cursor()
    sql = "INSERT INTO tipos_categorias(categoria) VALUES('" + str(categoria) + "')"
    try:
        cursor.execute(sql)
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as e:
        cursor.close()
        cnx.close()
        print("cadastrarCategoriaNoticia - " + str(e))

def cadastrarTipoNoticia(tipo):
    cnx = conexao()
    cursor = cnx.cursor()
    sql = "INSERT INTO tipo_noticia(descricao) VALUES('" + str(tipo) + "')"
    try:
        cursor.execute(sql)
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as e:
        cursor.close()
        cnx.close()
        print("cadastrarTipoNoticia - " + str(e))

def buscarTipoNoticia(tipo):
    cnx = conexao()
    cursor = cnx.cursor()
    sql = "SELECT * FROM tipo_noticia WHERE descricao = '" + str(tipo) + "'"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return result
    except Exception as e:
        cursor.close()
        cnx.close()
        print("buscarTipoNoticia - " + str(e))

def vincularCategoriaNoticia(idCategoria, idNoticia):
    cnx = conexao()
    cursor = cnx.cursor()
    sql = "INSERT INTO noticias_categorias(idCategoria, idNoticia) VALUES('" + str(idCategoria) + "','" + str(idNoticia) + "')"
    try:
        cursor.execute(sql)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    except Exception as e:
        print("vincularCategoriaNoticia - " + str(e))
        cursor.close()
        cnx.close()
        return False