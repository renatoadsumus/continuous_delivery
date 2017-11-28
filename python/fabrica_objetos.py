# coding=utf-8


class FabricaObjetos(object):

    __ArquivoXML = None
    __ArquivoProperties = None
    __Builder = None
    __Maven = None
    # __API_Nexus = None
    __API_GoCd = None
    __Grails = None
    __Gradle = None
    __ArquivoGroovy = None
    __Tibco = None
    __MSBuild = None
    __Docker = None
    __Implantador = None
    __ImplantadorTibco = None
    __ImplantadorTomcat = None
    __ImplantadorZip = None
    __BuilderZip = None
    __ImplantadorSSH = None
    __ImplantadorETL = None
    __ImplantadorDocker = None
    __CSS = None
    __JS = None

    @classmethod
    def obter_arquivo_xml(cls, diretorio_arquivo, xml_namespace=None):
        from python.tipos_arquivos.arquivo_xml import ArquivoXML
        if cls.__ArquivoXML is None:
            cls.__ArquivoXML = ArquivoXML(diretorio_arquivo, xml_namespace)
        return cls.__ArquivoXML

    @classmethod
    def atribuir_arquivo_xml(cls, arquivo_xml):
        cls.__ArquivoXML = arquivo_xml

    @classmethod
    def obter_arquivo_properties(cls, diretorio_arquivo):
        from python.tipos_arquivos.arquivo_properties import ArquivoProperties
        if cls.__ArquivoProperties is None:
            cls.__ArquivoProperties = ArquivoProperties(diretorio_arquivo)
        return cls.__ArquivoProperties

    @classmethod
    def atribuir_arquivo_properties(cls, arquivo_properties):
        cls.__ArquivoProperties = arquivo_properties

    @classmethod
    def obter_arquivo_groovy(cls, diretorio_arquivo):
        from python.tipos_arquivos.arquivo_groovy import ArquivoGroovy
        if cls.__ArquivoGroovy is None:
            cls.__ArquivoGroovy = ArquivoGroovy(diretorio_arquivo)
        return cls.__ArquivoGroovy

    @classmethod
    def atribuir_arquivo_groovy(cls, arquivo_groovy):
        cls.__ArquivoGroovy = arquivo_groovy

    @classmethod
    def obter_builder(cls):
        from python.biblioteca import Builders
        if cls.__Builder is None:
            cls.__Builder = Builders()
        return cls.__Builder

    @classmethod
    def atribuir_builder(cls, builder):
        cls.__Builder = builder

    @classmethod
    def obter_maven(cls, diretorio_pom):
        from python.builders.maven import Maven
        if cls.__Maven is None:
            cls.__Maven = Maven(diretorio_pom)
        return cls.__Maven

    @classmethod
    def atribuir_maven(cls, maven):
        cls.__Maven = maven

    # @classmethod
    # def obter_api_nexus(cls):
    #     from python.apis.api_nexus import ApiNexus
    #     if cls.__API_Nexus is None:
    #         cls.__API_Nexus = ApiNexus()
    #     return cls.__API_Nexus
    #
    # @classmethod
    # def atribuir_api_nexus(cls, api_nexus):
    #     cls.__API_Nexus = api_nexus

    @classmethod
    def obter_api_gocd(cls):
        from python.apis.api_gocd import ApiGoCd
        if cls.__API_GoCd is None:
            cls.__API_GoCd = ApiGoCd()
        return cls.__API_GoCd

    @classmethod
    def atribuir_api_gocd(cls, api_gocd):
        cls.__API_GoCd = api_gocd

    @classmethod
    def obter_grails(cls, diretorio_grails_plugin):
        from python.builders.grails import Grails
        if cls.__Grails is None:
            cls.__Grails = Grails(diretorio_grails_plugin)
        return cls.__Grails

    @classmethod
    def atribuir_grails(cls, grails):
        cls.__Grails = grails

    @classmethod
    def obter_gradle(cls):
        from python.builders.gradle import Gradle
        if cls.__Gradle is None:
            cls.__Gradle = Gradle()
        return cls.__Gradle

    @classmethod
    def atribuir_gradle(cls, gradle):
        cls.__Gradle = gradle

    @classmethod
    def obter_tibco(cls):
        from python.builders.tibco import Tibco
        if cls.__Tibco is None:
            cls.__Tibco = Tibco()
        return cls.__Tibco

    @classmethod
    def atribuir_tibco(cls, tibco):
        cls.__Tibco = tibco

    @classmethod
    def obter_msbuild(cls):
        from python.builders.msbuild import MSBuild
        if cls.__MSBuild is None:
            cls.__MSBuild = MSBuild()
        return cls.__MSBuild

    @classmethod
    def atribuir_msbuild(cls, msbuild):
        cls.__MSBuild = msbuild

    @classmethod
    def obter_builder_zip(cls):
        from python.builders.builder_zip import BuilderZip
        if cls.__BuilderZip is None:
            cls.__BuilderZip = BuilderZip()
        return cls.__BuilderZip

    @classmethod
    def atribuir_builder_zip(cls, builder_zip):
        cls.__BuilderZip = builder_zip

    @classmethod
    def obter_implantador(cls):
        from python.biblioteca import Implantadores
        if cls.__Implantador is None:
            cls.__Implantador = Implantadores()
        return cls.__Implantador

    @classmethod
    def atribuir_implantador(cls, implantador):
        cls.__Implantador = implantador

    @classmethod
    def obter_implantador_tibco(cls):
        from python.implantadores.tibco import ImplantadorTibco
        if cls.__ImplantadorTibco is None:
            cls.__ImplantadorTibco = ImplantadorTibco()
        return cls.__ImplantadorTibco

    @classmethod
    def atribuir_implantador_tibco(cls, implantador_tibco):
        cls.__ImplantadorTibco = implantador_tibco

    @classmethod
    def obter_implantador_tomcat(cls):
        from python.implantadores.tomcat import ImplantadorTomcat
        if cls.__ImplantadorTomcat is None:
            cls.__ImplantadorTomcat = ImplantadorTomcat()
        return cls.__ImplantadorTomcat

    @classmethod
    def atribuir_implantador_tomcat(cls, implantador_tomcat):
        cls.__ImplantadorTomcat = implantador_tomcat

    @classmethod
    def obter_implantador_zip(cls):
        from python.implantadores.zip import ImplantadorZIP
        if cls.__ImplantadorZip is None:
            cls.__ImplantadorZip = ImplantadorZIP()
        return cls.__ImplantadorZip

    @classmethod
    def atribuir_implantador_zip(cls, implantador_zip):
        cls.__ImplantadorZip = implantador_zip

    @classmethod
    def obter_implantador_ssh(cls):
        from python.implantadores.ssh import ImplantadorSSH
        if cls.__ImplantadorSSH is None:
            cls.__ImplantadorSSH = ImplantadorSSH()
        return cls.__ImplantadorSSH

    @classmethod
    def atribuir_implantador_ssh(cls, implantador_ssh):
        cls.__ImplantadorSSH = implantador_ssh

    @classmethod
    def obter_implantador_etl(cls):
        from python.implantadores.etl import ImplantadorETL
        if cls.__ImplantadorETL is None:
            cls.__ImplantadorETL = ImplantadorETL()
        return cls.__ImplantadorETL

    @classmethod
    def atribuir_implantador_etl(cls, implantador_etl):
        cls.__ImplantadorETL = implantador_etl

    @classmethod
    def obter_builder_docker(cls):
        from python.builders.docker import Docker
        if cls.__Docker is None:
            cls.__Docker = Docker()
        return cls.__Docker

    @classmethod
    def atribuir_builder_docker(cls, docker):
        cls.__Docker = docker

    @classmethod
    def obter_implantador_docker(cls):
        from python.implantadores.docker import ImplantadorDocker
        if cls.__ImplantadorDocker is None:
            cls.__ImplantadorDocker = ImplantadorDocker()
        return cls.__ImplantadorDocker

    @classmethod
    def atribuir_implantador_docker(cls, implantador_docker):
        cls.__ImplantadorDocker = implantador_docker

    @classmethod
    def obter_css(cls):
        from python.builders.css import CSS
        if cls.__CSS is None:
            cls.__CSS = CSS()
        return cls.__CSS

    @classmethod
    def atribuir_css(cls, css):
        cls.__CSS = css

    @classmethod
    def obter_js(cls):
        from python.builders.js import JS
        if cls.__JS is None:
            cls.__JS = JS()
        return cls.__JS

    @classmethod
    def atribuir_js(cls, js):
        cls.__JS = js
