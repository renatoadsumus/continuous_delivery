""""
Modulo que engloba a classe Arquivo, responsavel por acoes de arquivos
"""
from os import path, rename, remove


class Arquivo(object):
    """"
    Classe que representa o objeto arquivo de um sistema de arquivos e serve para
    fazer acessos a arquivos e outras operacoes
    """
    def __init__(self, diretorio_completo):
        self.diretorio_completo = str(diretorio_completo)
        self.vetor_partes_diretorio = self.diretorio_completo.split("\\")

    def diretorio_pai(self):
        if len(self.vetor_partes_diretorio) > 1:
            return self.vetor_partes_diretorio[-2]
        return None

    def nome(self):
        return str(self.vetor_partes_diretorio[-1])

    def extensao(self):
        partes_nome = self.nome().split(".")
        if len(partes_nome) > 1:
            return partes_nome[-1]
        return None

    def nome_sem_extensao(self, ignorar_todas_extensoes=None):
        nome_com_extensao = self.nome()
        if ignorar_todas_extensoes:
            partes_nome = self.nome().split(".")
            return partes_nome[0]
        if "." in nome_com_extensao:
            extensao_completa = "." + self.extensao()
            return nome_com_extensao.replace(extensao_completa, "")
        return self.nome()

    def diferenca_diretorio(self, parte_remover):
        return self.diretorio_completo.replace(parte_remover, "")

    def existe(self):
        return path.isfile(self.diretorio_completo)

    def renomear(self, novo_nome):
        rename(self.diretorio_completo, self.diretorio_completo.replace(self.nome(), novo_nome))

    def excluir(self):
        remove(self.diretorio_completo)
