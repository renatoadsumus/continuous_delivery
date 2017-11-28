# coding=utf-8

from python.assistentes.log import Log
from python.settings import BUILDER, ARQUIVO_PARA_BUILD, IMPLANTADOR

__author__ = 'ssouza'


class Builders:

    if BUILDER is not None:
        Log.imprime("Builder informado: " + BUILDER)
        if BUILDER == "MAVEN":
            maven = None

            def __init__(self):
                from python.fabrica_objetos import FabricaObjetos
                self.maven = FabricaObjetos.obter_maven(ARQUIVO_PARA_BUILD)

            def get_versao(self):
                return self.maven.get_versao()

            def get_atributos(self):
                return "jar", self.get_versao(), self.maven.get_artifact_id(), self.maven.get_group_id(), \
                       self.maven.get_repository()

            def executa_testes(self):
                self.maven.executa_testes()

            def faz_deploy_nexus(self):
                self.maven.faz_deploy_nexus()

            def fechar_artefato(self):
                self.maven.fechar_artefato()

            def executa_scanner_sonar(self):
                self.maven.executa_scanner_sonar()

        elif BUILDER == "GRAILS":
            grails = None

            def __init__(self):
                from python.fabrica_objetos import FabricaObjetos
                self.grails = FabricaObjetos.obter_grails(ARQUIVO_PARA_BUILD)

            def get_versao(self):
                return self.grails.get_versao()

            def get_atributos(self):
                return "zip", self.get_versao(), self.grails.get_artifact_id(), self.grails.get_group_id(), \
                       self.grails.get_repository()

            def executa_testes(self):
                self.grails.executa_testes()

            def faz_deploy_nexus(self):
                self.executa_testes()
                self.grails.faz_deploy_nexus()

            def fechar_artefato(self):
                self.grails.fechar_artefato()

            def executa_scanner_sonar(self):
                self.grails.executa_scanner_sonar()

        elif BUILDER == "GRADLE":
            gradle = None

            def __init__(self):
                from python.fabrica_objetos import FabricaObjetos
                self.gradle = FabricaObjetos.obter_gradle()

            def executa_testes(self):
                self.gradle.executa_testes()

            def fechar_artefato(self):
                self.gradle.fechar_artefato()

            def executa_scanner_sonar(self):
                self.gradle.executa_scanner_sonar()

        elif BUILDER == "TIBCO":
            tibco = None

            def __init__(self):
                from python.fabrica_objetos import FabricaObjetos
                self.tibco = FabricaObjetos.obter_tibco()

            def executa_testes(self):
                self.tibco.executa_testes()

            def fechar_artefato(self):
                self.tibco.fechar_artefato()

            def executa_scanner_sonar(self):
                self.tibco.executa_scanner_sonar()

        elif BUILDER == "MSBUILD":
            msbuild = None

            def __init__(self):
                from python.fabrica_objetos import FabricaObjetos
                self.msbuild = FabricaObjetos.obter_msbuild()

            def executa_testes(self):
                self.msbuild.executa_testes()

            def fechar_artefato(self):
                self.msbuild.fechar_artefato()

            def executa_scanner_sonar(self):
                self.msbuild.executa_scanner_sonar()

        elif BUILDER == "ZIP":
            builder_zip = None

            def __init__(self):
                from python.fabrica_objetos import FabricaObjetos
                self.builder_zip = FabricaObjetos.obter_builder_zip()

            def fechar_artefato(self):
                self.builder_zip.fechar_artefato()

            def executa_scanner_sonar(self):
                self.builder_zip.executa_scanner_sonar()

        elif BUILDER == "DOCKER":
            builder_docker = None

            def __init__(self):
                from python.fabrica_objetos import FabricaObjetos
                self.builder_docker = FabricaObjetos.obter_builder_docker()

            def fechar_artefato(self):
                self.builder_docker.fechar_artefato()

            def executa_scanner_sonar(self):
                self.builder_docker.executa_scanner_sonar()

        elif BUILDER == "CSS":
            css = None

            def __init__(self):
                from python.fabrica_objetos import FabricaObjetos
                self.css = FabricaObjetos.obter_css()

            def fechar_artefato(self):
                self.css.fechar_artefato()

            def executa_scanner_sonar(self):
                self.css.executa_scanner_sonar()

        elif BUILDER == "JS":
            js = None

            def __init__(self):
                from python.fabrica_objetos import FabricaObjetos
                self.js = FabricaObjetos.obter_js()

            def fechar_artefato(self):
                self.js.fechar_artefato()

            def executa_scanner_sonar(self):
                self.js.executa_scanner_sonar()

        else:
            Log.imprime("Builder informado nao existe")

    else:
        Log.imprime("Builder nao informado")


class Implantadores:

    if IMPLANTADOR is not None:
        Log.imprime("Implantador informado: " + IMPLANTADOR)
        if IMPLANTADOR == "TIBCO":
            tibco = None

            def __init__(self):
                from python.fabrica_objetos import FabricaObjetos
                self.tibco = FabricaObjetos.obter_implantador_tibco()

            def implantar_artefato(self):
                self.tibco.implantar_artefato()

        elif IMPLANTADOR == "TOMCAT":
            tomcat = None

            def __init__(self):
                from python.fabrica_objetos import FabricaObjetos
                self.tomcat = FabricaObjetos.obter_implantador_tomcat()

            def implantar_artefato(self):
                self.tomcat.implantar_artefato()

        elif IMPLANTADOR == "ZIP":
            implantador_zip = None

            def __init__(self):
                from python.fabrica_objetos import FabricaObjetos
                self.implantador_zip = FabricaObjetos.obter_implantador_zip()

            def implantar_artefato(self):
                self.implantador_zip.implantar_artefato()

        elif IMPLANTADOR == "SSH":
            implantador_ssh = None

            def __init__(self):
                from python.fabrica_objetos import FabricaObjetos
                self.implantador_ssh = FabricaObjetos.obter_implantador_ssh()

            def implantar_artefato(self):
                self.implantador_ssh.implantar_artefato()

        elif IMPLANTADOR == "ETL":
            implantador_etl = None

            def __init__(self):
                from python.fabrica_objetos import FabricaObjetos
                self.implantador_etl = FabricaObjetos.obter_implantador_etl()

            def implantar_artefato(self):
                self.implantador_etl.implantar_artefato()

        elif IMPLANTADOR == "DOCKER":
            implantador_docker = None

            def __init__(self):
                from python.fabrica_objetos import FabricaObjetos
                self.implantador_docker = FabricaObjetos.obter_implantador_docker()

            def implantar_artefato(self):
                self.implantador_docker.implantar_artefato()

        else:
            Log.imprime("Implantador informado nao existe")
    else:
        Log.imprime("Implantador nao informado")
