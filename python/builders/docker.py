"""
Modulo que engloba a classe do builder Docker
"""

from os import getenv

from python.artefato import Artefato
from python.assistentes.SSH import SSH


class Docker(Artefato):
    """
    Classe que representa o Docker e suas acoes
    """

    def __init__(self):
        self.SENHA = getenv("SENHA")
        self.USUARIO = getenv("USUARIO")
        self.SERVIDOR = getenv("SERVIDOR")
        self.NOME_IMAGEM = getenv("NOME_IMAGEM")
        self.TAG_IMAGEM = getenv("PIPELINE_LABEL").split('-')[1]
        self.COMANDO = getenv("COMANDO")

    def get_versao(self):
        pass

    def get_atributos(self):
        pass

    def executa_testes(self):
        pass

    def fechar_artefato(self):
        ssh = SSH(self.SERVIDOR, self.USUARIO)
        ssh.senha(self.SENHA)
        comando_ssh = ""
        ssh.abrir_conexao()
        ssh.executar_comando(comando_ssh)
        ssh.fechar_conexao()

    def executa_scanner_sonar(self):
        pass
