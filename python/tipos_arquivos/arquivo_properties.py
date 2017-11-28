# coding=utf-8
from os import path


class ArquivoProperties:
    def __init__(self, diretorio_completo_arquivo_properties):
        self.arquivo_properties = diretorio_completo_arquivo_properties
        if not path.isfile(self.arquivo_properties):
            with open(self.arquivo_properties, "a+") as arquivo:
                arquivo.write("")

    def obter_valor_chave(self, chave):
        with open(self.arquivo_properties, "r") as arquivo:
            linha = arquivo.readline()
            while linha:
                if linha.upper().startswith(chave.upper() + "="):
                    valor = linha.split("=")
                    return valor[1].strip()
                linha = arquivo.readline()

    def existe_chave(self, chave):
        with open(self.arquivo_properties, "r+") as arquivo:
            linha = arquivo.readline()
            existe = False
            while linha:
                if linha.upper().startswith(chave.upper() + "="):
                    existe = True
                    break
                linha = arquivo.readline()
        return existe

    def adicionar_chave(self, chave, valor):
        if path.isfile(self.arquivo_properties) and self.existe_chave(chave):
            return
        with open(self.arquivo_properties, "a+") as arquivo:
            arquivo.write("\n" + str(chave) + "=" + str(valor))

    def alterar_valor_chave(self, chave, valor):
        if not self.existe_chave(chave):
            self.adicionar_chave(chave, valor)
            return
        dicionario_propriedades = self.carregar_properties_para_dicionario()
        dicionario_propriedades[chave] = valor
        self.dicionario_para_properties(dicionario_propriedades)

    def dicionario_para_properties(self, dicionario):
        with open(self.arquivo_properties, "w") as arquivo:
            primeira_linha = True
            for propriedade in dicionario:
                linha = ""
                if not primeira_linha:
                    linha += "\n"
                linha += "%s=%s" % (propriedade, dicionario[propriedade])
                arquivo.write(linha)
                primeira_linha = False

    def carregar_properties_para_dicionario(self):
        with open(self.arquivo_properties, "r+") as arquivo:
            propriedades = {}
            linha = arquivo.readline()
            while linha:
                if linha.__contains__("="):
                    chave = linha.split("=")[0].strip()
                    valor = linha.split("=")[1].strip()
                    propriedades[chave] = valor
                linha = arquivo.readline()
        return propriedades
