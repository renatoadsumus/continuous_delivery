from python.artefato import Artefato
from python.assistentes.linha_de_comando import LinhaDeComando
from python.assistentes.log import Log
from python.settings import PIPELINE_LABEL, MSBUILD_HOME, SCANNER_MSBUILD_HOME
from python.tipos_arquivos.arquivo_properties import ArquivoProperties
# from python.tipos_arquivos.arquivo_xml import ArquivoXML


class MSBuild(Artefato):

    def __init__(self):
        # self.__XPATH_TAG_VERSION = ".//{http://schemas.microsoft.com/developer/msbuild/2003}Version"
        # self.__XML_NAMESPACE = "http://schemas.microsoft.com/developer/msbuild/2003"
        self.__versao = PIPELINE_LABEL.split("-")[-1]
        # self.__build_xml = ArquivoXML(ARQUIVO_PARA_BUILD, self.__XML_NAMESPACE)
        self.__caminho_msbuild = MSBUILD_HOME + "\\MSBuild.exe"
        self.__scanner = SCANNER_MSBUILD_HOME + "\\SonarQube.Scanner.MSBuild.exe"

    def fechar_artefato(self):
        comando = self.__caminho_msbuild + " build.xml"
        Log.imprime("INICIANDO PROCESSO DE FECHAMENTO DO ARTEFATO", "INICIANDO PROCESSO DE FECHAMENTO DO ARTEFATO.")
        LinhaDeComando.executar(comando)
        Log.imprime("ARTEFATO GERADO COM SUCESSO.", "ARTEFATO GERADO COM SUCESSO.")

    def get_versao(self):
        return self.__versao

    def get_atributos(self):
        pass

    def executa_testes(self):
        pass

    def executa_scanner_sonar(self):
        arq_prop = ArquivoProperties("sonar-msbuild.properties")
        project_key = arq_prop.obter_valor_chave("project_key")
        project_name = arq_prop.obter_valor_chave("project_name")
        project_version = arq_prop.obter_valor_chave("project_version")
        project_branch = arq_prop.obter_valor_chave("project_branch")
        if project_branch:
            comando = "%s begin /k:\"%s\" /n:\"%s\" /v:\"%s\" /d:sonar.branch=%s" % (
            self.__scanner, project_key, project_name, project_version, project_branch)
        else:
            comando = "%s begin /k:\"%s\" /n:\"%s\" /v:\"%s\"" % (self.__scanner, project_key, project_name, project_version)
        Log.imprime("PREPARANDO SCANNER MSBUILD DO SONAR", "PREPARANDO SCANNER MSBUILD DO SONAR")
        LinhaDeComando.executar(comando)

        comando = "\"%s\" build.xml" % self.__caminho_msbuild
        Log.imprime("REALIZANDO REBUILD DA APLICACAO PARA O SONAR", "REALIZANDO REBUILD DA APLICACAO PARA O SONAR")
        LinhaDeComando.executar(comando)

        comando = "%s end" % self.__scanner
        Log.imprime("FINALIZANDO SCANNER MSBUILD DO SONAR", "FINALIZANDO SCANNER MSBUILD DO SONAR")
        LinhaDeComando.executar(comando)
