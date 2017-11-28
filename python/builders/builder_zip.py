from os import path
from shutil import rmtree
from traceback import format_exc

from python.artefato import Artefato
from python.assistentes.log import Log
from python.assistentes.zip import ZIP
from python.settings import NOME_PROJETO, WORKING_DIRECTORY


class BuilderZip(Artefato):

    def fechar_artefato(self):
        Log.imprime("CRIANDO ZIP DO DIRETORIO " + NOME_PROJETO, "CRIANDO ZIP DO DIRETORIO DO PROJETO")

        pasta_svn = path.join(NOME_PROJETO, ".svn")

        if path.isdir(pasta_svn):
            rmtree(pasta_svn)
        destino_diretorio_compactado = path.join(WORKING_DIRECTORY, NOME_PROJETO + ".zip")
        zp = ZIP()
        try:
            zp.compactar_arquivos(NOME_PROJETO, destino_diretorio_compactado)
            Log.imprime("CRIADO O ZIP DO PROJETO " + NOME_PROJETO + "\nCAMINHO DO ARQUIVO: " +
                        destino_diretorio_compactado)
        except:
            Log.imprime("FALHA\n" + format_exc(), "FALHA -- ARQUIVO ZIP NAO FOI CRIADO", classe=BuilderZip)

    def get_versao(self):
        pass

    def get_atributos(self):
        pass

    def executa_testes(self):
        pass

    def executa_scanner_sonar(self):
        pass
