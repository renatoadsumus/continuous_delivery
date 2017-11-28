from os import path

from python.assistentes.SSH import SSH
from python.assistentes.log import Log
from python.settings import NOME_PROJETO, getenv, DIRETORIO_CHAVES_SERVIDORES, WORKING_DIRECTORY


class ImplantadorSSH:

    def __init__(self):
        self.arquivo_envio = NOME_PROJETO + '.' + getenv("EXTENSAO").lower()
        self.servidor_ssh = getenv("SERVIDOR_SSH")
        self.senha_ssh = getenv("SENHA_SSH")
        self.usuario_ssh = getenv("USUARIO_SSH")
        self.arquivo_chave_ssh = getenv("ArquivoChaveSSH")
        self.diretorio_ssh = getenv("DIRETORIO_SSH")

        if not NOME_PROJETO:
            Log.imprime("NOME DO PROJETO NAO INFORMADO", "ERRO NA IMPLANTACAO VIA SSH.", classe=ImplantadorSSH)
            exit(1)

        if not getenv("EXTENSAO"):
            Log.imprime("EXTENSAO DO ARQUIVO DE ENVIO NAO INFORMADA", "ERRO NA IMPLANTACAO VIA SSH.",
                        classe=ImplantadorSSH)
            exit(1)

        if not self.servidor_ssh:
            Log.imprime("SERVIDOR NAO INFORMADO", "ERRO NA IMPLANTACAO VIA SSH.", classe=ImplantadorSSH)
            exit(1)

        if not self.senha_ssh and not self.arquivo_chave_ssh:
            Log.imprime("NENHUMA FORMA DE AUTENTICACAO INFORMADA", "ERRO NA IMPLANTACAO VIA SSH.",
                        classe=ImplantadorSSH)
            exit(1)

        if not self.usuario_ssh:
            Log.imprime("USUARIO NAO INFORMADO", "ERRO NA IMPLANTACAO VIA SSH.", classe=ImplantadorSSH)
            exit(1)

        if not self.diretorio_ssh:
            Log.imprime("DIRETORIO PARA ENVIO NAO INFORMADO", "ERRO NA IMPLANTACAO VIA SSH.", 
                        classe=ImplantadorSSH)
            exit(1)

    def implantar_artefato(self):
        Log.imprime("IMPLANTANDO " + self.arquivo_envio + " NO DIRETORIO " + self.diretorio_ssh +
                    " NO SERVIDOR " + self.servidor_ssh, "INICIANDO DEPLOY VIA SSH")

        Log.imprime("PREPARANDO PARA ABRIR CONEXAO COM O USUARIO " + self.usuario_ssh + " NO SERVIDOR " +
                    self.servidor_ssh)
        ssh = SSH(self.servidor_ssh, self.usuario_ssh)

        if self.senha_ssh:
            Log.imprime("UTILIZANDO SENHA PARA AUTENTICACAO")
            ssh.senha(self.senha_ssh)
        elif self.arquivo_chave_ssh:
            Log.imprime("UTILIZANDO ARQUIVO DE CHAVES PARA AUTENTICACAO")
            chave = DIRETORIO_CHAVES_SERVIDORES + self.arquivo_chave_ssh
            ssh.chave_acesso(chave)

        Log.imprime("ABRINDO CONEXAO")
        ssh.abrir_conexao()

        Log.imprime("ENVIANDO ARQUIVO " + path.join(WORKING_DIRECTORY, self.arquivo_envio) + " PARA " +
                    self.diretorio_ssh)
        ssh.enviar_arquivo(path.join(WORKING_DIRECTORY, self.arquivo_envio), self.diretorio_ssh)

        Log.imprime("DEPLOY ENCERRADO", "DEPLOY ENCERRADO COM SUCESSO")

