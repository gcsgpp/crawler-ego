__author__ = 'Gabriel'
import mysql.connector

def conexao():
    return mysql.connector.connect(host = "localhost", user = "root", database = "famososdb", charset="utf8")

def gravarLog(idMensagens, idFamoso = '', idFamoso2 = '', idNoticia = '', nomeFamoso = '', tituloNoticia = '', link = ''):
    cnx = conexao()
    cursor = cnx.cursor(buffered = True)

    sql = 'INSERT INTO log(idMensagensLog, idFamoso, idFamoso2, idNoticia, nomeFamoso, tituloNoticia, link) VALUES("' + str(idMensagens) + '","' + str(idFamoso) + '","' + str(idFamoso2) + '","' + str(idNoticia) + '","' + str(nomeFamoso) + '","' + str(tituloNoticia) + '","' + str(link) + '")'

    cursor.execute(sql)
    cnx.commit()
    cursor.close()
    cnx.close()

def inserirFamosoRelacionado(famosoRelacionado):
    cnx = conexao()
    cursor = cnx.cursor(buffered = True)

    id = buscarFamosoPorNome(famosoRelacionado['nome'])
    if id != False and id > 0:
        sql = "INSERT INTO famoso_relacionado (idFamoso1, idFamoso2) VALUES(" + str(famosoRelacionado['idFamoso1']) + " , " + str(id )+ ")"

        try:
            cursor.execute(sql)
            cnx.commit()
            return True
        except Exception as e:
            print(str(e))
            print("Erro ao inserir famoso relacionado")
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
    cursor = cnx.cursor(buffered = True)

    idFamoso2 = buscarFamosoPorNome(nomeFamosoRelacionado)
    sql = "SELECT * FROM famoso_relacionado WHERE (" + "idFamoso1 = '" + str(idFamoso) + "' and idFamoso2 = '" + str(idFamoso2) + "') or (" + "idFamoso1 = '" + str(idFamoso2) + "' and idFamoso2 = '" + str(idFamoso) + "')"

    try:
        cursor.execute(sql)
        result = cursor.fetchone()

        if result != None:
            return True
        else:
            return False

        cursor.close()
        cnx.close()
    except Exception as e:
        print("Erro ao verificar Famoso relacionado já existe.")
        print(str(e))
        gravarLog(idMensagens = 21,idFamoso = idFamoso, idFamoso2 = idFamoso2)




def buscarFamosoPorNome(nomeFamoso):
    cnx = conexao()
    cursor = cnx.cursor(buffered = True)
    try:
        query = 'SELECT * FROM famoso where nome = "' + str(nomeFamoso) + '"'
        cursor.execute(query)
        result = cursor.fetchone()
        if result != None:
            return result[0]
        else:
            return False
    except:
        gravarLog(idMensagens = 14, nomeFamoso = nomeFamoso)
        print("Erro ao buscar famoso pelo nome. ************************************************")

    cursor.close()
    cnx.close()

def verificarFamosoInserido(cnx, nomeFamoso):
    cnx = conexao()
    cursor = cnx.cursor(buffered = True)
    try:
        query = 'SELECT * FROM famoso where nome = "' + nomeFamoso + '"'
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        else:
            return True
    except:
        gravarLog(idMensagens = 2, nomeFamoso = nomeFamoso)
        print("Erro ao verificar famoso já inserido. ************************************************")

    cursor.close()
    cnx.close()


def inserirfamososdb(famoso, qtdAtualFamoso = 0, qtdTotalFamosos = 0):
    cnx = conexao()
    cursor = cnx.cursor(buffered = True)

    if verificarFamosoInserido(cnx, famoso['nome']) == True:
        print(famoso['nome'] + " -> JA INSERIDO NO BD")
    else:
        if famoso['conjuge'] != None:
            try:
                query = 'SELECT id FROM famoso WHERE famoso.link = "' + str(famoso['conjuge']) + '"'
                cursor.execute(query)
                result = cursor.fetchall()
                result = result[0]
            except:
                print("Nao foi possivel encontrar conjuge na tabela de famosos")
                gravarLog(idMensagens = 9, nomeFamoso = famoso['nome'])

        try:
            query = 'INSERT INTO famoso(nome, link, datanascimento, idade, signo, relacionamento, conjuge) VALUES("' + str(famoso['nome']) + '" , "' + str(famoso['link']) + '" , "' + str(famoso['datanascimento']) + '" , "' + str(famoso['idade']) + '" , "' + str(famoso['signo']) + '", "' + str(famoso['relacionamento']) + '" , "' + str(famoso['conjuge']) + '")'

            cursor.execute(query)
            cnx.commit()
            '''gravarLog(idMensagens = 3, idFamoso = cursor.lastrowid)'''
            print(str(qtdAtualFamoso) + "/" + str(qtdTotalFamosos) + " - " + famoso['nome'] + " INSERIDO COM SUCESSO.")
        except:
            gravarLog(idMensagens = 8, nomeFamoso = famoso['nome'])
            print("Erro ao inserir famoso na lista. Famoso: " + famoso['nome'] + "**********************************")

    cursor.close()
    cnx.close()

def buscarTipoRelacionamento(descricaoRelacionamento, nomeFamoso):
    cnx = conexao()
    cursor = cnx.cursor(buffered = True)

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

            cursor.close()
            cnx.close()

            return cursor.lastrowid
    except Exception as e:
        print(str(e))
        gravarLog(idMensagens = 16, nomeFamoso = nomeFamoso)
        print("Erro ao descobrir/inserir relacionamento.")

        cursor.close()
        cnx.close()

        return 0

def buscarConjugeJaInserido(nomeConjuge, nomeFamoso):
    cnx = conexao()
    cursor = cnx.cursor(buffered = True)
    sql = 'SELECT * FROM conjuge WHERE nome = "' + str(nomeConjuge) + '"'
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        if result != None:
            cursor.close()
            cnx.close()
            return result[0]
        else:
            return False
    except Exception as e:
        print(str(e))
        print("Erro ao buscar conjuge já inserido.")
        gravarLog(idMensagens = 20, nomeFamoso = str(nomeFamoso))
        return False

def inserirConjuge(conjugeNome, nomeFamoso):
    cnx = conexao()
    cursor = cnx.cursor(buffered = True)

    try:
        conjugeId = buscarConjugeJaInserido(conjugeNome,nomeFamoso)
        if conjugeId == False:
            sql = 'INSERT INTO conjuge (nome) VALUES("' + str(conjugeNome) + '")'
            cursor.execute(sql)
            cnx.commit()

            id = cursor.lastrowid
            return id
        else:
            return conjugeId

    except Exception as e:
        print(str(e))
        gravarLog(idMensagens = 17, nomeFamoso = str(nomeFamoso))
        print("Erro ao inserir conjuge no BD.")

        cursor.close()
        cnx.close()

        return 0

def buscarSigno(signo, nomeFamoso):
    cnx = conexao()
    cursor = cnx.cursor(buffered = True)
    sql = "SELECT * FROM signos WHERE signo = '" + str(signo) + "'"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        if result != None:
            cursor.close()
            cnx.close()
            return result[0]
        else:
            print("Nao foi possivel encontrar o signo do Famoso: " + str(nomeFamoso)+ " na lista do BD. Signo: " + str(signo))
            return 0
    except Exception as e:
        print(str(e))
        print("Erro ao buscar id do signo.")
        gravarLog(idMensagens = 19, nomeFamoso = str(nomeFamoso))
        return 0

def buscarListaFamoso():
    cnx = conexao()
    cursor = cnx.cursor(buffered = True)
    sql = "SELECT * from famoso"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()

        cursor.close()
        cnx.close()

        result = converterListaUTF8(result)

        return result
    except Exception as e:
        print(str(e))
        print("Erro ao buscar lista de famosos")
        gravarLog(idMensagens = 24)
        return False


def cadastrarNoticia(noticia):
    cnx = conexao()
    cursor = cnx.cursor(buffered = True)

    if noticia['tipo'] == "materia": noticia['tipo'] = 1
    elif noticia['tipo'] == "galeria": noticia['tipo'] = 2

    sql = 'INSERT INTO noticia(titulo, subtitulo, link, tipo, texto, dataPrimeiraPublicacao) VALUES("' + str(noticia['titulo']) + '","' + str(noticia['subtitulo']) + '","' + str(noticia['link']) + '","' + str(noticia['tipo']) + '","' + str(noticia['texto']) + '","' + str(noticia['data']) + '")'

    try:
        cursor.execute(sql)
        cnx.commit()
        print("Noticia: " + noticia['titulo'])
        '''gravarLog(idMensagens = 4, idNoticia = cursor.lastrowid)'''
    except Exception as e:
        print(str(e))
        print("Não foi possivel cadastrar a noticia: " + noticia['link'] + "    *********")
        gravarLog(idMensagens = 13, tituloNoticia = noticia['titulo'])

    cursor.close()
    cnx.close()

def verificarNoticiaInserida(titulo, link):
    cnx = conexao()
    cursor = cnx.cursor(buffered = True)

    sql = 'SELECT * from noticia WHERE noticia.titulo = "' + str(titulo) + '" or noticia.link = "' + str(link) + '"'

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
    except Exception as e:
        print(str(e))
        print("Erro ao verificar se a noticia ja esta cadastrada")

    if len(result) == 0:
        return False
    else:
        print("Noticia já cadastrada. Titulo: " + str(titulo))
        return True

def buscarListaNoticias():
    cnx = conexao()
    cursor = cnx.cursor(buffered = True)

    sql = "SELECT * FROM noticia"

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

        cursor.close()
        cnx.close()

        result = converterListaUTF8(result)

        return result
    except Exception as e:
        print(str(e))
        print("Erro ao buscar lista de noticias")
        gravarLog(idMensagens = 23)
        return False
def verificarRelacionamentoFamosoNoticia(idFamoso, idNoticia):
    cnx = conexao()
    cursor = cnx.cursor()
    sql = "SELECT * FROM famoso_noticia WHERE idFamoso = '" + str(idFamoso) + "' and idNoticia = '" + str(idNoticia) + "'"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        return result
    except Exception as e:
        print(str(e))
        print("Erro ao executar verificação se famoso ja esta relacionado")
        gravarLog(idMensagens=26, idFamoso = idFamoso, idNoticia = idNoticia)
        return False

def relacionarFamosoNoticia(nomeFamoso, idNoticia):
    cnx = conexao()
    cursor = cnx.cursor(buffered = True)
    idFamoso = buscarFamosoPorNome(nomeFamoso)

    famosoJaRelacionadoNoticia = verificarRelacionamentoFamosoNoticia(idFamoso, idNoticia)

    if len(famosoJaRelacionadoNoticia) > 0:
        return False


    sql = "INSERT INTO famoso_noticia(idFamoso, idNoticia) VALUES(" + str(idFamoso) + " , " + str(idNoticia) + ")"
    try:
        cursor.execute(sql)
        cnx.commit()

        cursor.close()
        cnx.close()
    except Exception as e:
        print(str(e))
        print("Erro ao inserir relacionamento do Famoso com a Noticia. Famoso: " + str(nomeFamoso) + " idNoticia: " + str(idNoticia))
        gravarLog(idMensagens = 25, idFamoso = idFamoso, idNoticia = idNoticia)

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
    cursor = cnx.cursor(buffered = True)
    sql = "SELECT * from noticia WHERE link = '" + str(link) + "'"
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return converterListaUTF8(result)
    except Exception as e:
        print(str(e))
        return False
