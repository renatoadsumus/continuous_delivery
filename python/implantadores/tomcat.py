"""Modulo que engloba a classe de ImplantadorTomcat"""

from os import path
from subprocess import check_call

from python.assistentes.SSH import SSH
from python.assistentes.log import Log
from python.settings import WORKING_DIRECTORY, DIRETORIO_CHAVES_SERVIDORES, getenv

__author__ = 'vgfarias'


class ImplantadorTomcat(object):
    """Classe que representa o ImplantadorTomcat e suas acoes"""

    def __init__(self):
        self.__SENHA_TOMCAT = getenv("SENHA_TOMCAT")
        self.__CONTEXT_PATH = getenv("ContextPath")
        self.__DOMINIO_TOMCAT = getenv("DominioTomcat")
        self.__SERVIDOR_PORTA_TOMCAT = getenv("ServidorPortaTomcat")
        self.__APLICACAO_PARAR = getenv("AplicacaoParar")
        self.__TEMPO_ESPERAR = getenv("TempoEsperar")
        self.__USUARIO_TOMCAT = getenv("UsuarioTomcat")
        self.__USUARIO_SSH = getenv("UsuarioSSH")
        self.__SENHA_SSH = getenv("SenhaSSH")
        self.__ARQUIVO_CHAVE_SSH = getenv("ArquivoChaveSSH")

        # Chamada ao metodo responsavel por verificar se todas as dependencias foram inicializadas corretamente
        self.__verificar_dependencias()

    def __verificar_dependencias(self):
        # Metodo responsavel por verificar se todas as dependencias foram inicializadas corretamente

        # Verifica se a senha do tomcat foi informada
        if not self.__SENHA_TOMCAT:
            Log.imprime("A SENHA DO TOMCAT NAO FOI INFORMADA", "ERRO NO DEPLOY NO TOMCAT.", classe=ImplantadorTomcat)
            exit(1)

        # Verifica se o context path da aplicacao foi informado
        if not self.__CONTEXT_PATH:
            Log.imprime("O CONTEXT PATH NAO FOI INFORMADO", "ERRO NO DEPLOY NO TOMCAT.", classe=ImplantadorTomcat)
            exit(1)

        # Verifica se o dominio tomcat foi informado
        if not self.__DOMINIO_TOMCAT:
            Log.imprime("O DOMINIO TOMCAT NAO FOI INFORMADO", "ERRO NO DEPLOY NO TOMCAT.", classe=ImplantadorTomcat)
            exit(1)

        # Verifica se o servidor e porta do tomcat foi informado
        if not self.__SERVIDOR_PORTA_TOMCAT:
            Log.imprime("A PORTA DO SERVIDOR TOMCAT NAO FOI INFORMADA", "ERRO NO DEPLOY NO TOMCAT.",
                        classe=ImplantadorTomcat)
            exit(1)

        # Verifica se a aplicacao que deve ser parada no tomcat foi informada
        if not self.__APLICACAO_PARAR:
            Log.imprime("A APLICACAO A SER PARADA NAO FOI INFORMADA", "ERRO NO DEPLOY NO TOMCAT.",
                        classe=ImplantadorTomcat)
            exit(1)

        # Verifica se o tempo de espera para reiniciar o tomcat foi informado
        if not self.__TEMPO_ESPERAR:
            Log.imprime("O TEMPO DE ESPERA NAO FOI INFORMADO", "ERRO NO DEPLOY NO TOMCAT.", classe=ImplantadorTomcat)
            exit(1)

        # Verifica se o usuario de administracao do tomcat foi informado
        if not self.__USUARIO_TOMCAT:
            Log.imprime("USUARIO TOMCAT NAO FOI INFORMADO", "ERRO NO DEPLOY NO TOMCAT.", classe=ImplantadorTomcat)
            exit(1)

        # Verifica se uma forma de autenticacao foi informada
        if not self.__ARQUIVO_CHAVE_SSH and not self.__SENHA_SSH:
            Log.imprime("ARQUIVO CHAVE PARA SSH E A SENHA SSH NAO FORAM INFORMADOS", "ERRO NO DEPLOY NO TOMCAT.",
                        classe=ImplantadorTomcat)
            exit(1)

        # Verifica se o usuario ssh foi informado. Caso nao tenha sido, aponta o usuario correto
        if not self.__USUARIO_SSH:
            self.__USUARIO_SSH = "tfsservice"
            Log.imprime("USUARIO SSH NAO FOI INFORMADO. DEFININDO AUTOMATICAMENTE PARA " + self.__USUARIO_SSH,
                        classe=ImplantadorTomcat)

    def implantar_artefato(self):
        # Metodo responsavel por implantar o artefato

        Log.imprime("RENOMEANDO ARTEFATO COM O CONTEXT PATH QUE SERA IMPLANTADO", "INICIANDO DEPLOY NO TOMCAT")

        # Comando para mover o .war para o local correto
        comando = 'if [ ! -f %s.war ]; then mv %s/*.war %s.war; fi' % (self.__CONTEXT_PATH, WORKING_DIRECTORY,
                                                                       self.__CONTEXT_PATH)

        Log.imprime("EXECUTANDO COMANDO " + comando)
        check_call([comando], shell=True)

        # Faz uma manipulacao de strings para obter o servidor e a porta separadamente
        servidor = self.__SERVIDOR_PORTA_TOMCAT.split(":")[0]
        porta = self.__SERVIDOR_PORTA_TOMCAT.split(":")[1]

        path_arquivo_deploy_tomcat = path.dirname(__file__) + "/../../shell/deploy_tomcat.sh"

        Log.imprime("PREPARANDO PARA ABRIR CONEXAO COM O USUARIO " + str(self.__USUARIO_SSH) + " NO SERVIDOR " +
                    servidor)
        # Preparando a conexao via SSH
        ssh = SSH(servidor, self.__USUARIO_SSH)

        # Verifica se sera utilizada senha para autenticacao
        if self.__SENHA_SSH:
            Log.imprime("UTILIZANDO SENHA PARA AUTENTICACAO")
            ssh.senha(self.__SENHA_SSH)
        elif self.__ARQUIVO_CHAVE_SSH:
            # Caso nao seja autenticacao via senha, e considerado que sera autenticacao via arquivos de chaves
            Log.imprime("UTILIZANDO ARQUIVO DE CHAVES PARA AUTENTICACAO")
            chave = DIRETORIO_CHAVES_SERVIDORES + self.__ARQUIVO_CHAVE_SSH
            ssh.chave_acesso(chave)

        # Abre a conexao SSH
        ssh.abrir_conexao()

        # Envia o arquivo auxiliar de deploy no tomcat para o servidor
        Log.imprime("ENVIANDO ARQUIVO " + path_arquivo_deploy_tomcat)
        ssh.enviar_arquivo(path_arquivo_deploy_tomcat, "/tmp/deploy_tomcat.sh")

        # Envia o arquivo .war para o servidor
        Log.imprime("ENVIANDO ARTEFATO " + self.__CONTEXT_PATH + ".war")
        ssh.enviar_arquivo(self.__CONTEXT_PATH + ".war", "/tmp/" + self.__CONTEXT_PATH + ".war")

        # Monta o comando que altera a permissao do arquivo auxilixar para que possa ser executado no servidor
        comando_permissao = "chmod +x /tmp/deploy_tomcat.sh"
        Log.imprime("EXECUTANDO COMANDO DE ALTERACAO DE PERMISSAO " + comando_permissao)

        # Executa o comando que altera a permissao do arquivo auxiliar
        ssh.executar_comando(comando_permissao)
        comando_deploy = '/tmp/deploy_tomcat.sh "%s" "%s" %s %s %s %s %s' % (
            self.__USUARIO_TOMCAT, self.__SENHA_TOMCAT, self.__DOMINIO_TOMCAT, porta, self.__CONTEXT_PATH,
            self.__APLICACAO_PARAR, self.__TEMPO_ESPERAR)

        # Executa o comando de deploy no servidor
        retorno_comando = ssh.executar_comando(comando_deploy)
        Log.imprime("REMOVENDO ARTEFATO QUE ESTAVA NA PASTA TEMPORARIA")

        # Remove o arquivo .war que ja nao sera mais utilizado
        ssh.executar_comando("rm -f /tmp/" + self.__CONTEXT_PATH + ".war")

        # Fecha a conexao
        ssh.fechar_conexao()

        # Verifica se ouve falha na execucao do comando e caso haja retorna uma mensagem de erro e quebra
        if "FAIL" in str(retorno_comando):
            Log.imprime("ERRO AO EXECUTAR deploy_tomcat.sh - " + retorno_comando, "ERRO NO DEPLOY NO TOMCAT.",
                        classe=ImplantadorTomcat)
            exit(1)

        Log.imprime("DEPLOY ENCERRADO", "DEPLOY ENCERRADO COM SUCESSO")
