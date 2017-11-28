"""Modulo que engloba a classe ArquivoGroovy"""

__author__ = 'ssouza'


class ArquivoGroovy(object):
    """Classe que representa o arquivo do Groovy e suas acoes"""
    def __init__(self, diretorio_completo_arquivo_groovy):
        #Inicializador do objeto ArquivoGroovy
        self.arquivo_groovy = diretorio_completo_arquivo_groovy

    def obter_valor_chave(self, chave):
        #Metodo para obter valor de uma chave dentro do arquivo Groovy
        with open(self.arquivo_groovy, "r") as arquivo:
            linha = str(arquivo.readline()).replace(" ", "")
            #Abre o arquivo, retira os espacos da linha e le todo o arquivo
            while linha:
                if linha.upper().startswith(chave.upper() + "="):
                    valor = linha.split("=")
                    valor_sem_aspas = valor[1].strip()
                    #Retorna o valor da chave desejada
                    return valor_sem_aspas[1:-1]
                linha = str(arquivo.readline()).replace(" ", "")
