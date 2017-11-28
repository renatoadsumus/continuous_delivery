"""
Modulo que engloba a classe Maven
"""

from python.artefato import Artefato
from python.assistentes.linha_de_comando import LinhaDeComando
from python.assistentes.log import Log

__author__ = 'ssouza'


class Maven(Artefato):
    """
    Classe que representa o builder Maven e suas principais acoes
    """

    def __init__(self, diretorio_pom_xml):
        self.__XPATH_TAG_GROUP_ID = "{http://maven.apache.org/POM/4.0.0}groupId"
        self.__XPATH_TAG_ARTIFACT_ID = "{http://maven.apache.org/POM/4.0.0}artifactId"
        self.__XPATH_TAG_REPOSITORY = "{http://maven.apache.org/POM/4.0.0}distributionManagement"
        self._LISTA_XPATH_TAGS_FILHAS = ["{http://maven.apache.org/POM/4.0.0}repository",
                                         "{http://maven.apache.org/POM/4.0.0}url"]
        self.__XPATH_TAG_VERSION = "{http://maven.apache.org/POM/4.0.0}version"

        from python.fabrica_objetos import FabricaObjetos
        self.diretorio_pom_xml = diretorio_pom_xml
        self.pom_xml = FabricaObjetos.obter_arquivo_xml(diretorio_pom_xml)
        self.versao = None

    def get_versao(self):
        # Metodo responsavel por pegar a versao
        versao = self.pom_xml.obter_valor_xpath(self.__XPATH_TAG_VERSION)
        Log.imprime("VERSAO: " + str(versao))
        return str(versao)

    def get_group_id(self):
        # Metodo responsavel por pegar o id do grupo
        group_id = self.pom_xml.obter_valor_xpath(self.__XPATH_TAG_GROUP_ID)
        Log.imprime("GROUP ID: " + str(group_id))
        return str(group_id)

    def get_artifact_id(self):
        # Metodo responsavel por pegar o id do artefato
        artifact_id = self.pom_xml.obter_valor_xpath(self.__XPATH_TAG_ARTIFACT_ID)
        Log.imprime("ARTIFACT ID: " + str(artifact_id))
        return str(artifact_id)

    def get_repository(self):
        # Metodo responsavel por pegar o repositorio
        repository = self.pom_xml.obter_valor_xpath(self.__XPATH_TAG_REPOSITORY, self._LISTA_XPATH_TAGS_FILHAS)
        split = repository.split("repositories/")
        repository = split[1].split("/")
        Log.imprime("REPOSITORY: " + str(repository))
        return str(repository[0])

    def get_atributos(self):
        # Metodo responsavel por pegar os atributos
        return "jar", self.get_versao(), self.get_artifact_id(), self.get_group_id(), self.get_repository()

    def executa_testes(self):
        # Metodo responsavel por executar os testes do Maven
        Log.imprime("INICIANDO TESTES DO MAVEN", "INICIANDO TESTES DO MAVEN")
        LinhaDeComando.executar("mvn test")
        Log.imprime("TESTES ENCERRADOS COM SUCESSO.", "TESTES ENCERRADOS COM SUCESSO.")

    @staticmethod
    def faz_deploy_nexus():
        # Metodo responsavel por fazer deploy no Nexus
        Log.imprime("INICIANDO DEPLOY NO NEXUS", "INICIANDO DEPLOY NO NEXUS")
        LinhaDeComando.executar("mvn deploy")
        Log.imprime("DEPLOY NO NEXUS EXECUTADO COM SUCESSO.", "DEPLOY NO NEXUS EXECUTADO COM SUCESSO.")

    def fechar_artefato(self):
        # Metodo responsavel por fechar um novo artefato
        comando_build = "mvn clean package"
        Log.imprime("INICIANDO PROCESSO DE FECHAMENTO DO ARTEFATO", "INICIANDO PROCESSO DE FECHAMENTO DO ARTEFATO.")
        LinhaDeComando.executar(comando_build)
        Log.imprime("ARTEFATO GERADO COM SUCESSO.", "ARTEFATO GERADO COM SUCESSO.")

    def executa_scanner_sonar(self):
        comando = "mvn clean org.jacoco:jacoco-maven-plugin:prepare-agent install -Pcoverage-per-test"
        Log.imprime("GERANDO RELATORIO DE COBERTURA", "GERANDO RELATORIO DE COBERTURA")
        LinhaDeComando.executar(comando)

        comando = "mvn sonar:sonar"
        LinhaDeComando.executar(comando)
        Log.imprime("SUCESSO NA EXECUCAO DO SONAR", "SUCESSO NA EXECUCAO DO SONAR")
