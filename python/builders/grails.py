# coding=utf-8

import sys

from python.artefato import Artefato
from python.assistentes.linha_de_comando import LinhaDeComando
from python.assistentes.log import Log
from python.settings import GRAILS_HOME, SONNAR_SCANNER

__author__ = 'ssouza'


class Grails(Artefato):

    def __init__(self, diretorio_grails_plugin):
        self.__GROUP_ID = "defgroupId"
        self.__ARTIFACT_ID = "defname"
        self.__REPOSITORY = "defrepository"
        self.__VERSION = "defversion"
        from python.fabrica_objetos import FabricaObjetos
        self.diretorio_grails_plugin = FabricaObjetos.obter_arquivo_groovy(diretorio_grails_plugin)
        self.versao = None
        self.GRAILS_HOME = GRAILS_HOME

    def get_versao(self):
        versao = self.diretorio_grails_plugin.obter_valor_chave(self.__VERSION)
        Log.imprime("VERSAO: " + str(versao))
        return str(versao)

    def get_artifact_id(self):
        artifact_id = self.diretorio_grails_plugin.obter_valor_chave(self.__ARTIFACT_ID)
        Log.imprime("ARTIFACT ID: " + str(artifact_id))
        return str(artifact_id)

    def get_group_id(self):
        group_id = self.diretorio_grails_plugin.obter_valor_chave(self.__GROUP_ID)
        Log.imprime("GROUP ID: " + str(group_id))
        return str(group_id)

    def get_repository(self):
        repository = self.diretorio_grails_plugin.obter_valor_chave(self.__REPOSITORY)
        split = repository.split("repositories/")
        repository = split[1].split("/")
        Log.imprime("REPOSITORY: " + str(repository[0]))
        return str(repository[0])

    def get_atributos(self):
        return "zip", self.get_versao(), self.get_artifact_id(), self.get_group_id(), self.get_repository()

    def executa_testes(self, out=sys.stdout):
        comando = "%s/bin/grails -Dgrails.work.dir=target test-app -coverage --non-interactive --plain-output " \
                  "--stacktrace" % self.GRAILS_HOME
        Log.imprime("INICIANDO TESTES DO GRAILS", "INICIANDO TESTES DO GRAILS")
        LinhaDeComando.executar(comando)
        Log.imprime("TESTES ENCERRADOS COM SUCESSO.", "TESTES ENCERRADOS COM SUCESSO")

        comando = "%s/bin/grails compile --non-interactive --plain-output" % self.GRAILS_HOME
        Log.imprime("COMPILANDO CLASSES PARA O SONAR", "COMPILANDO CLASSES PARA O SONAR")
        LinhaDeComando.executar(comando)

    def faz_deploy_nexus(self):
        comando = "%s/bin/grails maven-deploy" % self.GRAILS_HOME
        Log.imprime("INICIANDO DEPLOY NO NEXUS", "INICIANDO DEPLOY NO NEXUS")
        LinhaDeComando.executar(comando)
        Log.imprime("DEPLOY NO NEXUS EXECUTADO COM SUCESSO", "DEPLOY NO NEXUS EXECUTADO COM SUCESSO.")

    def fechar_artefato(self, out=sys.stdout):
        comando_clean = "%s/bin/grails clean" % self.GRAILS_HOME
        Log.imprime("INICIANDO PROCESSO DE CLEAN", "INICIANDO PROCESSO DE FECHAMENTO DO ARTEFATO.")
        LinhaDeComando.executar(comando_clean)
        Log.imprime("PROCESSO DE CLEAN ENCERRADO COM SUCESSO")

        comando_deploy = "%s/bin/grails war --verbose" % self.GRAILS_HOME
        Log.imprime("INICIANDO PROCESSO DE FECHAMENTO DO WAR")
        LinhaDeComando.executar(comando_deploy)
        Log.imprime("ARTEFATO GERADO COM SUCESSO", "ARTEFATO GERADO COM SUCESSO.")

    def executa_scanner_sonar(self):
        LinhaDeComando.executar(SONNAR_SCANNER)
        Log.imprime("SUCESSO NA EXECUCAO DO SONAR", "SUCESSO NA EXECUCAO DO SONAR")
