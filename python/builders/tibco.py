# coding=utf-8

from python.artefato import Artefato
from python.assistentes.linha_de_comando import LinhaDeComando
from python.assistentes.log import Log
from python.settings import WORKING_DIRECTORY, NOME_PROJETO

__author__ = 'apinto'


class Tibco(Artefato):

    def __init__(self):
        self.__ALIAS_PROPERTIES = WORKING_DIRECTORY + "\\infoglobo_commons\\alias.properties"
        self.__LOG_VALIDACAO = WORKING_DIRECTORY + "\\log-validacao.log"
        self.__TEXTO_VERICAR_FALHA_VALIDACAO = "Found 0 errors"

    def executa_testes(self):
        comando_dos = 'C: && cd C:\\tibco\\designer\\5.8\\bin && validateproject.exe -a "%s" -project "%s\\%s" > "%s"' \
                      % (self.__ALIAS_PROPERTIES, WORKING_DIRECTORY, NOME_PROJETO, self.__LOG_VALIDACAO)
        Log.imprime("INICIANDO OS TESTES DO TIBCO", "INICIANDO OS TESTES DO TIBCO.")
        LinhaDeComando.executar(comando_dos)
        Log.imprime("TESTES ENCERRADOS.", "TESTES ENCERRADOS")
        comando_dos = 'findstr /n /c:"%s" "%s"' % (self.__TEXTO_VERICAR_FALHA_VALIDACAO, self.__LOG_VALIDACAO)
        dos_return_code = LinhaDeComando.executar(comando_dos, True)
        if not dos_return_code == 0:
            LinhaDeComando.lancar_erro("O servico nao passou na validacao")
            Log.imprime("SERVICO NAO PASSOU NA VALIDACAO.", "SERVICO NAO PASSOU NA VALIDACAO.", classe=Tibco)

        Log.imprime("TESTES ENCERRADOS COM SUCESSO.", "TESTES ENCERRADOS COM SUCESSO.")

    def fechar_artefato(self):
        archive_utilizado = "/eAI/Deploy/%s.archive" % NOME_PROJETO
        diretorio_build_ear = '%s\\%s.ear' % (WORKING_DIRECTORY, NOME_PROJETO)
        mensagem = "##### INICIANDO O BUILD DO SERVICO (TRA - BUILDER) #####\n" \
                   "##### ARCHIVE: %s #####\n" \
                   "##### DIR. BUILD EAR: %s #####\n" \
                   "##### DIR. APLICACAO: %s\\%s #####\n" \
                   "##### DIR. alias.properties: %s #####" % \
                   (archive_utilizado, diretorio_build_ear, WORKING_DIRECTORY, NOME_PROJETO, self.__ALIAS_PROPERTIES)
        Log.imprime(mensagem, mensagem)

        comando_dos = 'buildear -o "%s" -p "%s\\%s" -a "%s" -ear "%s" -x' % (
            diretorio_build_ear, WORKING_DIRECTORY, NOME_PROJETO, self.__ALIAS_PROPERTIES, archive_utilizado)
        Log.imprime("EXECUTANDO O COMANDO: " + str(comando_dos))
        LinhaDeComando.executar(comando_dos)
        Log.imprime("ARTEFATO GERADO COM SUCESSO.", "ARTEFATO GERADO COM SUCESSO.")

    def get_versao(self):
        pass

    def get_atributos(self):
        pass

    def executa_scanner_sonar(self):
        pass
