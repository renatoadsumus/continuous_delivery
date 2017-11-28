# coding=utf-8
from os import environ, getenv, getcwd

URL_NEXUS = "http://inforep01.ogmaster.local:8080/nexus/service/local/artifact/maven/content?g="
URL_GO_CD = "http://infogocd.ogmaster.local:8080/go/"
USUARIO_GO_API = "goapiuser"
SENHA_GO_API = "#W4ZaGak"
DIRETORIO_CHAVES_SERVIDORES = "/home/tfsservice/.ssh/"
SONNAR_SCANNER = "/opt/sonar-scanner/latest/bin/sonar-scanner"
SCANNER_MSBUILD_HOME = "E:\\sonar-scanner-msbuild"

if environ["PY_AMBIENTE_EXECUCAO"] == "PRD":
    DESTINATARIOS_EMAIL = getenv("DESTINATARIOS_EMAIL")
    BUILDER = getenv("BUILDER")
    ARQUIVO_PARA_BUILD = getenv("ARQUIVO_PARA_BUILD")
    NOME_PROJETO = getenv("NOME_PROJETO")
    NOME_PROJETO_SONAR = getenv("NOME_PROJETO_SONAR")
    DEPENDENCIAS_PROJETO = getenv("DEPENDENCIAS_PROJETO")
    IMPLANTADOR = getenv("IMPLANTADOR")
    GRAILS_HOME = getenv("GRAILS_HOME")
    ESTRUTURA_PASTA_TIBCO = getenv("ESTRUTURA_PASTA_TIBCO")
    SERVIDOR_DEPLOY = getenv("SERVIDOR_DEPLOY")
    NOME_EQUIPE = getenv("NOME_EQUIPE")
    MUDANCA = getenv("MUDANCA")
    USUARIO_SSH = getenv("USUARIO_SSH")
    API_INFO_SERVICO = "https://csm3.serviceaide.com/servicedesk/webservices/ChangeRequest?wsdl"
    MSBUILD_HOME = getenv("MSBUILD_HOME")

    if getenv("JENKINS_URL"):
        PIPELINE_NAME = getenv("JOB_NAME")
        PIPELINE_COUNTER = getenv("BUILD_NUMBER")
        PIPELINE_LABEL = "Execucao-{}".format(PIPELINE_COUNTER)
        TRIGGER_USER = getenv("BUILD_USER")  # Precisa ativar a opcao "Set jenkins user build variables" no Job
        BUILD_URL = getenv("BUILD_URL")
        WORKING_DIRECTORY = getenv("WORKSPACE")

    elif getenv("GO_SERVER_URL"):
        PIPELINE_NAME = getenv("GO_PIPELINE_NAME")
        PIPELINE_COUNTER = getenv("GO_PIPELINE_COUNTER")
        STAGE_NAME = getenv("GO_STAGE_NAME")
        STAGE_COUNTER = getenv("GO_STAGE_COUNTER")
        PIPELINE_LABEL = getenv("GO_PIPELINE_LABEL")
        TRIGGER_USER = getenv("GO_TRIGGER_USER")
        BUILD_URL = "{}pipelines/{}/{}/{}/{}/".format(
            URL_GO_CD, PIPELINE_NAME, PIPELINE_COUNTER, STAGE_NAME, STAGE_COUNTER)
        WORKING_DIRECTORY = getenv("WORKING_DIRECTORY")
    else:
        print("##### ERRO - VARIAVEIS JENKINS_URL E GO_SERVER_URL NAO ENCONTRADAS #####")
        exit(1)
else:
    WORKING_DIRECTORY = getcwd()
    ARQUIVO_PARA_BUILD = "pom.xml"
    PIPELINE_NAME = "Teste_QA"
    PIPELINE_COUNTER = "111"
    STAGE_NAME = "deploy_Nexus"
    STAGE_COUNTER = "1"
    PIPELINE_LABEL = "111-96644"
    TRIGGER_USER = "rfonseca"
    BUILD_URL = "{}pipelines/{}/{}/{}/{}/".format(
        URL_GO_CD, PIPELINE_NAME, PIPELINE_COUNTER, STAGE_NAME, STAGE_COUNTER)
    DESTINATARIOS_EMAIL = "victor.farias@infoglobo.com.br, " \
                          "gabriela.silva@infoglobo.com.br, renato.fonseca@infoglobo.com.br"
    BUILDER = "MAVEN"
    GRAILS_PLUGIN_GROOVY = "ExemploGrailsPlugin.groovy"
    GRAILS_HOME = "fake-path"
    IMPLANTADOR = "TOMCAT"
    NOME_PROJETO = "teste_unitario"
    NOME_PROJETO_SONAR = "nome_teste_sonar"
    DEPENDENCIAS_PROJETO = "teste1,teste2"
    ESTRUTURA_PASTA_TIBCO = "diretorio_tibco"
    SERVIDOR_DEPLOY = "servidor_teste"
    NOME_EQUIPE = "equipe_QA"
    USUARIO_SSH = "tfsservice"
    API_INFO_SERVICO = "https://csmstaging.serviceaide.com/servicedesk/webservices/ChangeRequest?wsdl"
    MSBUILD_HOME = "C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319"
