from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from python.assistentes.log import Log


class Conexao:

    def __init__(self, usuario, senha, nome_banco=None, nome_colecao=None):
        self.__conexao = None
        self.__banco = None
        self.__colecao = None
        self.__SERVIDOR = 'infogocd'
        self.__PORTA = 27017

        self.__abrir_conexao(usuario, senha)
        if nome_banco:
            self.acessar_banco(nome_banco)
            if nome_colecao:
                self.acessar_colecao(nome_colecao)
            else:
                Log.imprime("COLECAO NAO INFORMADA.", "ERRO NA CONEXAO COM O MONGO.", classe=Conexao)
        else:
            Log.imprime("BANCO NAO INFORMADO.", "ERRO NA CONEXAO COM O MONGO.", classe=Conexao)

    def __abrir_conexao(self, usuario, senha):
        self.__conexao = MongoClient(self.__SERVIDOR, self.__PORTA)

        if not usuario or not senha:
            Log.imprime("USUARIO/SENHA NAO INFORMADO.", "ERRO NA CONEXAO COM O MONGO.", classe=Conexao)
            exit(1)

        if self.__conexao:
            autenticado = self.__conexao.admin.authenticate(usuario, senha, mechanism='SCRAM-SHA-1')
            if autenticado:
                Log.imprime("CONEXAO ABERTA COM SUCESSO")
                return True
            else:
                Log.imprime("USUARIO NAO PODE SER AUTENTICADO. CHECAR SENHA NO KEEPASS. VALOR RECEBIDO PARA USUARIO: " +
                            str(usuario), "ERRO DE AUTENTICACAO NO MONGO.", classe=Conexao)
                exit(1)
        else:
            Log.imprime("CONEXAO PARECE NAO TER SIDO INICIADA DA MANEIRA CORRETA. VALOR RECEBIDO: " +
                        str(self.__conexao), "ERRO NA CONEXAO COM O MONGO.", classe=Conexao)
            exit(2)

    def acessar_banco(self, nome_banco):
        if not nome_banco:
            Log.imprime("O NOME DO BANCO NAO FOI INFORMADO.", "ERRO NA CONEXAO COM O MONGO.", classe=Conexao)
            exit(1)

        if not self.__conexao:
            Log.imprime("CONEXAO PARECE NAO TER SIDO INICIADA DA MANEIRA CORRETA. VALOR RECEBIDO: " +
                        str(self.__conexao), "ERRO NA CONEXAO COM O MONGO.", classe=Conexao)
            exit(2)

        if nome_banco not in self.__conexao.database_names():
            Log.imprime("BANCO NAO EXISTE NO MONGODB. VALOR RECEBIDO: " + str(self.__conexao) +
                        "\nLISTA DE BANCOS ENCONTRADOS: " + str(self.__conexao.database_names()),
                        "ERRO NA CONEXAO COM O MONGO.", classe=Conexao)
            exit(3)

        self.__banco = Database(self.__conexao, nome_banco)
        Log.imprime("CONECTADO AO BANCO " + nome_banco)
        return True

    def acessar_colecao(self, nome_colecao):
        if not nome_colecao:
            Log.imprime("COLECAO NAO INFORMADA.", "ERRO NA CONEXAO COM O MONGO.", classe=Conexao)
            exit(1)

        if not self.__banco:
            Log.imprime("BANCO NAO INFORMADO.", "ERRO NA CONEXAO COM O MONGO.", classe=Conexao)
            exit(2)

        if nome_colecao not in self.__banco.collection_names():
            Log.imprime("COLECAO NAO EXISTE NO BANCO.\nVALOR RECEBIDO PARA BANCO: " + str(self.__banco) +
                        "\nVALOR RECEBIDO PARA COLECAO: " + str(nome_colecao) +
                        "\nLISTA DE COLECOES DO BANCO: " + str(self.__banco.collection_names()),
                        "ERRO NA CONEXAO COM O MONGO.", classe=Conexao)
            exit(3)

        self.__colecao = Collection(self.__banco, nome_colecao)
        Log.imprime("CONECTADO A COLECAO " + nome_colecao)
        return True

    def fechar_conexao(self):
        if not self.__conexao:
            Log.imprime("CONEXAO PARECE NAO TER SIDO INICIADA DA MANEIRA CORRETA.\nVALOR RECEBIDO: " +
                        str(self.__conexao), "ERRO NA CONEXAO COM O MONGO.", classe=Conexao)
            return False
        else:
            self.__conexao.close()
            Log.imprime("CONEXAO ENCERRADA COM SUCESSO")
            return True

    def obter_colecao(self):
        return self.__colecao

