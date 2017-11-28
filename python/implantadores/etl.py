from os import listdir, path
from shutil import copy
from time import sleep

from python.assistentes.linha_de_comando import LinhaDeComando, Log
from python.settings import getenv, NOME_PROJETO, PIPELINE_NAME


class ImplantadorETL:

    def __init__(self):
        self.chave_seguranca_pacote = getenv("CHAVE_SEGURANCA_PACOTE")
        self.senha_banco_de_dados = getenv("SENHA_BANCO_DE_DADOS")
        self.caminho_package = getenv("CAMINHO_PACKAGES")
        self.caminho_dtsconfig = "C:\\dwconfig"
        if PIPELINE_NAME.split("_")[-1].lower() == "producao":
            self.ambiente = "prd"
            self.servidor = "azrssisprd"
            self.usuario_banco_de_dados = "INFG_Jenkins"
        else:
            self.ambiente = "stg"
            self.servidor = "azrssisdsv"
            self.usuario_banco_de_dados = "DEV_INFG_Jenkins"

    def implantar_artefato(self):
        Log.imprime("INICIANDO DEPLOY DO ETL " + NOME_PROJETO, "INCIANDO DEPLOY DO ETL")
        self.copiar_arquivos_dtsconfig()
        self.copiar_arquivos_dtsx()
        Log.imprime("DEPLOY ENCERRADO", "DEPLOY ENCERRADO COM SUCESSO")

    def copiar_arquivos_dtsconfig(self):
        caminho = path.join("xml_configuracao", self.ambiente)
        lista_arquivos = listdir(caminho)

        Log.imprime("COPIANDO ARQUIVOS .DTSCONFIG", "COPIANDO ARQUIVOS .DTSCONFIG")

        for arquivo in lista_arquivos:
            if arquivo.endswith(".dtsConfig"):
                arquivo_config = path.join(caminho, arquivo)
                copy(arquivo_config, self.caminho_dtsconfig)

    def copiar_arquivos_dtsx(self):
        lista_arquivos = listdir(NOME_PROJETO)
        for arquivo_dtsx in lista_arquivos:
            if arquivo_dtsx.endswith(".dtsx"):
                comando_dtutil_copy = "dtutil /FILE " + path.join(NOME_PROJETO, arquivo_dtsx) + " /COPY SQL;" + \
                                 path.join(self.caminho_package, arquivo_dtsx.replace(".dtsx", "")) + \
                                 " /QUIET /DestS " + self.servidor + " /DECRYPT " + self.chave_seguranca_pacote + \
                                 " /DestU " + self.usuario_banco_de_dados + " /DestP " + self.senha_banco_de_dados

                # TROCAR O CAMINHO => (Integracao\CRM\ExpurgoDiario\pckExpurgoDiarioSalesForceLead) POR VARIAVEL DE AMBIENTE

                # comando_dtutil_exists = "dtutil /SQL Integracao\CRM\ExpurgoDiario\pckExpurgoDiarioSalesForceLead" \
                #                       " /SOURCESERVER " + self.servidor + " /SOURCEUSER " \
                #                       + self.usuario_banco_de_dados + " /SOURCEPASSWORD " + self.senha_banco_de_dados\
                #                       + " /EXISTS"

                # comando_dtutil_delete = "dtutil /SQL Integracao\CRM\ExpurgoDiario\pckExpurgoDiarioSalesForceAtividade" \
                #                        " /SOURCESERVER " + self.servidor + " /SOURCEUSER "\
                #                        + self.usuario_banco_de_dados + " /SOURCEPASSWORD " + self.senha_banco_de_dados\
                #                        + " /DELETE"

                # retorno_exists = LinhaDeComando.executar_com_output(comando_dtutil_exists)
                # if "Error" not in retorno_exists:
                #    retorno_delete = LinhaDeComando.executar_com_output(comando_dtutil_delete)
                #    Log.imprime("PACKAGE ATUAL DELETADA " + arquivo_dtsx, "PACKAGE ATUAL DELETADA " + arquivo_dtsx)
                #    retorno_copy = LinhaDeComando.executar_com_output(comando_dtutil_copy)
                #    Log.imprime("PACKAGE NOVA COPIADA " + arquivo_dtsx, "PACKAGE NOVA COPIADAA " + arquivo_dtsx)
                # else:
                retorno_copy = LinhaDeComando.executar_com_output(comando_dtutil_copy)
                #   Log.imprime("PACKAGE NOVA COPIADA " + arquivo_dtsx, "PACKAGE NOVA COPIADA " + arquivo_dtsx)

                sleep(1)
                if "The operation completed successfully." in retorno_copy:
                    Log.imprime("SUCESSO - ARQUIVO " + arquivo_dtsx + " FOI ENVIADO. RETORNO: " + retorno_copy,
                                "SUCESSO - ARQUIVO " + arquivo_dtsx + " FOI ENVIADO.")
                else:
                    Log.imprime("FALHA - ARQUIVO " + arquivo_dtsx + " NAO FOI ENVIADO. RETORNO: " + retorno_copy,
                                "FALHA - ARQUIVO " + arquivo_dtsx + " NAO FOI ENVIADO. RETORNO: " + retorno_copy)
                    exit(1)
