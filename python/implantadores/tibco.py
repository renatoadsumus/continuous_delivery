"""Modulo que engloba a classe ImplantadorTibco"""

from python.assistentes.SSH import SSH
from python.assistentes.log import Log, path
from python.settings import NOME_PROJETO, SERVIDOR_DEPLOY, WORKING_DIRECTORY, PIPELINE_NAME, PIPELINE_LABEL, \
    ESTRUTURA_PASTA_TIBCO, DIRETORIO_CHAVES_SERVIDORES, getenv, environ

__author__ = 'apinto'


class ImplantadorTibco(object):
    """Classe que representa o ImplantadorTibco e suas principais acoes"""

    def __init__(self):
        self.__ARQUIVO_XML = NOME_PROJETO + "_" + SERVIDOR_DEPLOY + ".xml"
        self.__CAMINHO_ARQUIVO_XML = path.join(WORKING_DIRECTORY, "xml_configuracao", self.__ARQUIVO_XML)
        self.__ARTEFATO = NOME_PROJETO + ".ear"
        self.__CAMINHO_ARTEFATO = path.join(WORKING_DIRECTORY, self.__ARTEFATO)
        self.__ARQUIVO_CHAVE_SSH = "teste.ppk"
        self.__SENHA_SSH = getenv("SENHA_SSH")
        self.__USUARIO_SSH = environ.get("UsuarioSSH")
        self.__REVISION_XML = getenv("GO_REVISION_XML_CONFIGURACAO")
        # variavel originada no implantar_artefato
        self.__MUDANCA = getenv("NUMERO_MUDANCA")
        self.__verificar_dependencias()
        self.__servidor_master = getenv("SERVIDOR_MASTER")

    def __verificar_dependencias(self):

        if not path.isfile(self.__CAMINHO_ARQUIVO_XML):
            Log.imprime("XML DE CONFIGURACAO NAO ENCONTRADO", "XML DE CONFIGURACAO NAO ENCONTRADO.",
                        classe=ImplantadorTibco)
            exit(1)

        if not path.isfile(self.__CAMINHO_ARTEFATO):
            Log.imprime("ARTEFATO NAO ENCONTRADO", "ARTEFATO NAO ENCONTRADO.", classe=ImplantadorTibco)
            exit(1)

        if not self.__ARQUIVO_CHAVE_SSH and not self.__SENHA_SSH:
            Log.imprime("CHAVE OU SENHA PARA A CONEXAO SSH NAO FOI INFORMADO",
                        "CHAVE OU SENHA PARA A CONEXAO SSH NAO FOI INFORMADO.", classe=ImplantadorTibco)
            exit(1)

        if not self.__USUARIO_SSH:
            self.__USUARIO_SSH = "tfsservice"
            Log.imprime("USUARIO SSH NAO FOI INFORMADO. DEFININDO AUTOMATICAMENTE PARA " + self.__USUARIO_SSH)

    def implantar_artefato(self):

        if PIPELINE_NAME.__contains__("adapter") and PIPELINE_NAME.split("_")[-1] == "integracao":
            Log.imprime("INICIANDO DEPLOY DO ADAPTER NO AMBIENTE DE INTEGRACAO",
                        "INICIANDO DEPLOY DO ADAPTER NO AMBIENTE DE INTEGRACAO.")
            comando_touch = "touch /var/log/tibco/DEV_INFG_TIBCO/" + NOME_PROJETO + "/" + NOME_PROJETO + "SAP.log"

            comentario_deploy = "EAR: %s - XML: Revision-%s" % (PIPELINE_LABEL, self.__REVISION_XML)

            comando_deploy = "cd /opt/tibco/deploy/scripts; ./Deploy.sh ../artefatos/%s ../artefatos/%s %s \"%s\"" % (
                self.__ARQUIVO_XML, self.__ARTEFATO, ESTRUTURA_PASTA_TIBCO, comentario_deploy)

            comando_validate = "cd /opt/tibco/deploy/scripts; ./ValidaDeployAdapterSAP.sh " + NOME_PROJETO

            Log.imprime("PREPARANDO PARA ABRIR CONEXAO COM O USUARIO " + self.__USUARIO_SSH + " NO SERVIDOR " +
                        self.__servidor_master)
            ssh = SSH(self.__servidor_master, self.__USUARIO_SSH)

            if self.__SENHA_SSH:
                Log.imprime("UTILIZANDO SENHA PARA AUTENTICACAO", classe=ImplantadorTibco)
                ssh.senha(self.__SENHA_SSH)

            elif self.__ARQUIVO_CHAVE_SSH:
                Log.imprime("UTILIZANDO ARQUIVO DE CHAVES PARA AUTENTICACAO", classe=ImplantadorTibco)
                chave = DIRETORIO_CHAVES_SERVIDORES + self.__ARQUIVO_CHAVE_SSH
                ssh.chave_acesso(chave)
            Log.imprime("ABRINDO CONEXAO", classe=ImplantadorTibco)
            ssh.abrir_conexao()

            Log.imprime("ENVIANDO ARQUIVO " + self.__CAMINHO_ARQUIVO_XML + " PARA /opt/tibco/deploy/artefatos")
            ssh.enviar_arquivo(self.__CAMINHO_ARQUIVO_XML, "/opt/tibco/deploy/artefatos")

            Log.imprime("ENVIANDO ARTEFATO " + self.__CAMINHO_ARTEFATO + " PARA /opt/tibco/deploy/artefatos")

            ssh.enviar_arquivo(self.__CAMINHO_ARTEFATO, "/opt/tibco/deploy/artefatos")

            ssh.executar_comando(comando_touch)

            saida = ssh.executar_comando(comando_deploy)

            ssh.executar_comando(comando_validate)

            ssh.fechar_conexao()

        elif PIPELINE_NAME.__contains__("adapter") and PIPELINE_NAME.split("_")[-1] == "staging":

            Log.imprime("INICIANDO DEPLOY DO ADAPTER NO AMBIENTE DE STAGING",
                        "INICIANDO DEPLOY DO ADAPTER NO AMBIENTE DE STAGING.")

            if SERVIDOR_DEPLOY.__contains__("2"):
                comando_touch = "touch /var/log/tibco/DEV_INFG_TIBCO_QLT/" + NOME_PROJETO + "-qlt2/" + \
                                NOME_PROJETO + "-qlt2SAP.log"
                comando_validate = "cd /opt/tibco/deploy/scripts; ./ValidaDeployAdapterSAP.sh " + NOME_PROJETO + "-qlt2"
            else:

                comando_touch = "touch /var/log/tibco/DEV_INFG_TIBCO_QLT/" + NOME_PROJETO + "/" + \
                                NOME_PROJETO + "SAP.log"
                comando_validate = "cd /opt/tibco/deploy/scripts; ./ValidaDeployAdapterSAP.sh " + NOME_PROJETO

            comentario_deploy = "EAR: %s - XML: Revision-%s" % (PIPELINE_LABEL, self.__REVISION_XML)

            comando_deploy = "cd /opt/tibco/deploy/scripts; ./Deploy.sh ../arquivos/%s ../arquivos/%s %s \"%s\"" % (
                self.__ARQUIVO_XML, self.__ARTEFATO, ESTRUTURA_PASTA_TIBCO, comentario_deploy)

            Log.imprime("PREPARANDO PARA ABRIR CONEXAO COM O USUARIO " + self.__USUARIO_SSH + " NO SERVIDOR " +
                        SERVIDOR_DEPLOY)
            ssh = SSH(SERVIDOR_DEPLOY, self.__USUARIO_SSH)
            if self.__SENHA_SSH:
                Log.imprime("UTILIZANDO SENHA PARA AUTENTICACAO")
                ssh.senha(self.__SENHA_SSH)
            elif self.__ARQUIVO_CHAVE_SSH:
                Log.imprime("UTILIZANDO ARQUIVO DE CHAVES PARA AUTENTICACAO")
                chave = DIRETORIO_CHAVES_SERVIDORES + self.__ARQUIVO_CHAVE_SSH
                ssh.chave_acesso(chave)

            ssh.abrir_conexao()
            ssh.executar_comando(comando_touch)
            ssh.fechar_conexao()

            Log.imprime("PREPARANDO PARA ABRIR CONEXAO COM O USUARIO " + self.__USUARIO_SSH + " NO SERVIDOR " +
                        self.__servidor_master)
            ssh = SSH(self.__servidor_master, self.__USUARIO_SSH)
            if self.__SENHA_SSH:
                Log.imprime("UTILIZANDO SENHA PARA AUTENTICACAO")
                ssh.senha(self.__SENHA_SSH)
            elif self.__ARQUIVO_CHAVE_SSH:
                Log.imprime("UTILIZANDO ARQUIVO DE CHAVES PARA AUTENTICACAO")
                chave = DIRETORIO_CHAVES_SERVIDORES + self.__ARQUIVO_CHAVE_SSH
                ssh.chave_acesso(chave)

            ssh.abrir_conexao()

            Log.imprime("ENVIANDO ARQUIVO " + self.__CAMINHO_ARQUIVO_XML + " PARA /opt/tibco/deploy/arquivos")
            ssh.enviar_arquivo(self.__CAMINHO_ARQUIVO_XML, "/opt/tibco/deploy/arquivos")

            Log.imprime("ENVIANDO ARTEFATO " + self.__CAMINHO_ARTEFATO + " PARA /opt/tibco/deploy/arquivos")
            ssh.enviar_arquivo(self.__CAMINHO_ARTEFATO, "/opt/tibco/deploy/arquivos")

            saida = ssh.executar_comando(comando_deploy)

            ssh.fechar_conexao()

            Log.imprime("PREPARANDO PARA ABRIR CONEXAO COM O USUARIO " + self.__USUARIO_SSH + " NO SERVIDOR " +
                        SERVIDOR_DEPLOY)
            ssh = SSH(SERVIDOR_DEPLOY, self.__USUARIO_SSH)
            if self.__SENHA_SSH:
                Log.imprime("UTILIZANDO SENHA PARA AUTENTICACAO")
                ssh.senha(self.__SENHA_SSH)

            elif self.__ARQUIVO_CHAVE_SSH:
                Log.imprime("UTILIZANDO ARQUIVO DE CHAVES PARA AUTENTICACAO")
                chave = DIRETORIO_CHAVES_SERVIDORES + self.__ARQUIVO_CHAVE_SSH
                ssh.chave_acesso(chave)

            ssh.abrir_conexao()

            ssh.executar_comando(comando_validate)

            ssh.fechar_conexao()

        elif PIPELINE_NAME.__contains__("adapter") and PIPELINE_NAME.split("_")[-1] == "producao":

            Log.imprime("INICIANDO DEPLOY DO ADAPTER NO AMBIENTE DE PRODUCAO",
                        "INICIANDO DEPLOY DO ADAPTER NO AMBIENTE DE PRODUCAO.")

            if SERVIDOR_DEPLOY.__contains__("1"):
                comando_touch = "touch /var/log/tibco/TIBCO/" + NOME_PROJETO + "_tbc1/" + NOME_PROJETO + "_tbc1SAP.log"
                comando_validate = "cd /opt/tibco/deploy/scripts; ./ValidaDeployAdapterSAP.sh " + NOME_PROJETO + "_tbc1"
            else:
                comando_touch = "touch /var/log/tibco/TIBCO/" + NOME_PROJETO + "_tbc2/" + NOME_PROJETO + "_tbc2SAP.log"
                comando_validate = "cd /opt/tibco/deploy/scripts; ./ValidaDeployAdapterSAP.sh " + NOME_PROJETO + "_tbc2"

            comentario_deploy = "EAR: %s - XML: Revision-%s - Mudança: %s" % (PIPELINE_LABEL,
                                                                              self.__REVISION_XML, self.__MUDANCA)

            comando_deploy = "cd /opt/tibco/deploy/scripts; ./Deploy.sh ../arquivos/%s ../arquivos/%s %s_%s \"%s\"" % (
                self.__ARQUIVO_XML, self.__ARTEFATO, ESTRUTURA_PASTA_TIBCO, SERVIDOR_DEPLOY, comentario_deploy)

            Log.imprime("PREPARANDO PARA ABRIR CONEXAO COM O USUARIO " + self.__USUARIO_SSH + " NO SERVIDOR " +
                        SERVIDOR_DEPLOY)
            ssh = SSH(SERVIDOR_DEPLOY, self.__USUARIO_SSH)
            if self.__SENHA_SSH:
                Log.imprime("UTILIZANDO SENHA PARA AUTENTICACAO")
                ssh.senha(self.__SENHA_SSH)
            elif self.__ARQUIVO_CHAVE_SSH:
                Log.imprime("UTILIZANDO ARQUIVO DE CHAVES PARA AUTENTICACAO")
                chave = DIRETORIO_CHAVES_SERVIDORES + self.__ARQUIVO_CHAVE_SSH
                ssh.chave_acesso(chave)

            ssh.abrir_conexao()

            ssh.executar_comando(comando_touch)

            ssh.fechar_conexao()

            Log.imprime("PREPARANDO PARA ABRIR CONEXAO COM O USUARIO " + self.__USUARIO_SSH + " NO SERVIDOR " +
                        self.__servidor_master)
            ssh = SSH(self.__servidor_master, self.__USUARIO_SSH)
            if self.__SENHA_SSH:
                Log.imprime("UTILIZANDO SENHA PARA AUTENTICACAO")
                ssh.senha(self.__SENHA_SSH)

            elif self.__ARQUIVO_CHAVE_SSH:
                Log.imprime("UTILIZANDO ARQUIVO DE CHAVES PARA AUTENTICACAO")
                chave = DIRETORIO_CHAVES_SERVIDORES + self.__ARQUIVO_CHAVE_SSH
                ssh.chave_acesso(chave)

            ssh.abrir_conexao()

            Log.imprime("ENVIANDO ARQUIVO " + self.__CAMINHO_ARQUIVO_XML + " PARA /opt/tibco/deploy/arquivos")

            ssh.enviar_arquivo(self.__CAMINHO_ARQUIVO_XML, "/opt/tibco/deploy/arquivos")

            Log.imprime("ENVIANDO ARTEFATO " + self.__CAMINHO_ARTEFATO + " PARA /opt/tibco/deploy/arquivos")

            ssh.enviar_arquivo(self.__CAMINHO_ARTEFATO, "/opt/tibco/deploy/arquivos")

            saida = ssh.executar_comando(comando_deploy)

            ssh.fechar_conexao()

            Log.imprime("PREPARANDO PARA ABRIR CONEXAO COM O USUARIO " + self.__USUARIO_SSH + " NO SERVIDOR " +
                        SERVIDOR_DEPLOY)
            ssh = SSH(SERVIDOR_DEPLOY, self.__USUARIO_SSH)
            if self.__SENHA_SSH:
                Log.imprime("UTILIZANDO SENHA PARA AUTENTICACAO")
                ssh.senha(self.__SENHA_SSH)
            elif self.__ARQUIVO_CHAVE_SSH:
                Log.imprime("UTILIZANDO ARQUIVO DE CHAVES PARA AUTENTICACAO")
                chave = DIRETORIO_CHAVES_SERVIDORES + self.__ARQUIVO_CHAVE_SSH
                ssh.chave_acesso(chave)

            ssh.abrir_conexao()

            ssh.executar_comando(comando_validate)

            ssh.fechar_conexao()

        elif PIPELINE_NAME.split("_")[-1] == "producao":

            Log.imprime("INICIANDO DEPLOY DO SERVICO NO AMBIENTE DE PRODUCAO",
                        "INICIANDO DEPLOY DO SERVICO NO AMBIENTE DE PRODUCAO.")

            comentario_deploy = "EAR: %s - XML: Revision-%s - Mudança: %s" % (PIPELINE_LABEL, self.__REVISION_XML,
                                                                              self.__MUDANCA)

            comando_deploy = "cd /opt/tibco/deploy/scripts; ./Deploy.sh ../arquivos/%s ../arquivos/%s %s_%s \"%s\"" % (
                self.__ARQUIVO_XML, self.__ARTEFATO, ESTRUTURA_PASTA_TIBCO, SERVIDOR_DEPLOY, comentario_deploy)

            Log.imprime("PREPARANDO PARA ABRIR CONEXAO COM O USUARIO " + self.__USUARIO_SSH + " NO SERVIDOR infotbc1")

            ssh = SSH(self.__servidor_master, self.__USUARIO_SSH)

            if self.__SENHA_SSH:
                Log.imprime("UTILIZANDO SENHA PARA AUTENTICACAO")
                ssh.senha(self.__SENHA_SSH)
            elif self.__ARQUIVO_CHAVE_SSH:
                Log.imprime("UTILIZANDO ARQUIVO DE CHAVES PARA AUTENTICACAO")
                chave = DIRETORIO_CHAVES_SERVIDORES + self.__ARQUIVO_CHAVE_SSH
                ssh.chave_acesso(chave)

            ssh.abrir_conexao()

            Log.imprime("ENVIANDO ARQUIVO " + self.__CAMINHO_ARQUIVO_XML + " PARA /opt/tibco/deploy/artefatos")
            ssh.enviar_arquivo(self.__CAMINHO_ARQUIVO_XML, "/opt/tibco/deploy/arquivos")

            Log.imprime("ENVIANDO ARTEFATO " + self.__CAMINHO_ARTEFATO + " PARA /opt/tibco/deploy/artefatos")
            ssh.enviar_arquivo(self.__CAMINHO_ARTEFATO, "/opt/tibco/deploy/arquivos")

            saida = ssh.executar_comando(comando_deploy)

            ssh.fechar_conexao()

        elif PIPELINE_NAME.split("_")[-1] == "integracao" or PIPELINE_NAME.split("_")[-1] == "staging":

            Log.imprime("INICIANDO DEPLOY DO SERVICO", "INICIANDO DEPLOY DO SERVICO")

            comentario_deploy = "EAR: %s - XML: Revision-%s" % (PIPELINE_LABEL, self.__REVISION_XML)

            comando_deploy = "cd /opt/tibco/deploy/scripts; ./Deploy.sh ../artefatos/%s ../artefatos/%s %s \"%s\""\
                             % (self.__ARQUIVO_XML, self.__ARTEFATO, ESTRUTURA_PASTA_TIBCO, comentario_deploy)

            Log.imprime("PREPARANDO PARA ABRIR CONEXAO COM O USUARIO " + self.__USUARIO_SSH + " NO SERVIDOR " +
                        self.__servidor_master)

            ssh = SSH(self.__servidor_master, self.__USUARIO_SSH)

            if self.__SENHA_SSH:
                Log.imprime("UTILIZANDO SENHA PARA AUTENTICACAO")
                ssh.senha(self.__SENHA_SSH)
            elif self.__ARQUIVO_CHAVE_SSH:
                Log.imprime("UTILIZANDO ARQUIVO DE CHAVES PARA AUTENTICACAO")
                chave = DIRETORIO_CHAVES_SERVIDORES + self.__ARQUIVO_CHAVE_SSH
                ssh.chave_acesso(chave)

            ssh.abrir_conexao()

            Log.imprime("ENVIANDO ARQUIVO " + self.__CAMINHO_ARQUIVO_XML + " PARA /opt/tibco/deploy/artefatos")

            ssh.enviar_arquivo(self.__CAMINHO_ARQUIVO_XML, "/opt/tibco/deploy/artefatos")

            Log.imprime("ENVIANDO ARTEFATO " + self.__CAMINHO_ARTEFATO + " PARA /opt/tibco/deploy/artefatos")

            ssh.enviar_arquivo(self.__CAMINHO_ARTEFATO, "/opt/tibco/deploy/artefatos")

            saida = ssh.executar_comando(comando_deploy)

            ssh.fechar_conexao()

        else:
            Log.imprime("CHAVE DE AMBIENTE DE DEPLOY DESCONHECIDO: " + PIPELINE_NAME.split("_")[-1],
                        "CHAVE DE AMBIENTE DE DEPLOY DESCONHECIDO.", classe=ImplantadorTibco)
            saida = ""
            exit(1)

        if "Finished successfully" not in str(saida):
            Log.imprime("ERRO NO DEPLOY DO TIBCO\n" + saida, "ERRO NO DEPLOY DO TIBCO.", classe=ImplantadorTibco)
            exit(1)

        Log.imprime("DEPLOY ENCERRADO", "DEPLOY ENCERRADO COM SUCESSO")
