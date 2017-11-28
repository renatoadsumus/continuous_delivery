# coding=utf-8

from traceback import format_exc

import paramiko
from scp import SCPClient

from python.assistentes.log import Log


class SSH:
    def __init__(self, servidor, usuario):
        self.usuario = usuario
        self.servidor = servidor
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.scp = None
        self.senha_servidor = None
        self.arquivo_chave = None

    def senha(self, senha_servidor):
        self.senha_servidor = senha_servidor

    def chave_acesso(self, arquivo_chave):
        self.arquivo_chave = arquivo_chave

    def abrir_conexao(self):
        try:
            if self.senha_servidor is not None:
                self.ssh.connect(self.servidor, username=self.usuario, password=self.senha_servidor)
            else:
                self.ssh.load_system_host_keys(self.arquivo_chave)
                self.ssh.connect(self.servidor, username=self.usuario)
        except:
            Log.imprime("FALHA\n" + format_exc(), "FALHA -- ERRO NA CONEXAO SSH", classe=SSH)
            exit(1)
        try:
            self.scp = SCPClient(self.ssh.get_transport())
        except:
            Log.imprime("ERRO NA CONEXAO SSH\n" + format_exc(), "ERRO NA CONEXAO SCP", classe=SSH)
            exit(1)
        Log.imprime("CONEXAO ABERTA COM SUCESSO.\nUSUARIO " + self.usuario + "\nSERVIDOR " + self.servidor,
                    "CONEXAO SSH ABERTA COM SUCESSO")

    def executar_comando(self, comando, timeout=None, bufsize=-1):

        if comando:
            Log.imprime("COMANDO A SER EXECUTADO VIA SSH: " + comando, "EXECUTANDO COMANDO VIA SSH")
            chan = self.ssh.get_transport().open_session(timeout=timeout)
            chan.get_pty()
            chan.settimeout(timeout)
            chan.exec_command(comando)

            saida = ""
            output_instantaneo = True
            while not chan.exit_status_ready():
                if chan.recv_ready():
                    output_instantaneo = False
                    retorno = chan.recv(1024)
                    saida += retorno.decode("utf-8")
                    print(retorno.decode("utf-8"), end="")
            # stdin = chan.makefile('wb', bufsize)

            if output_instantaneo:
                stdout = chan.makefile('r', bufsize)
                for linha in stdout:
                    saida += str(linha)
                if saida:
                    print(saida, end="")

            stderr = chan.makefile_stderr('r', bufsize)
            saida_erro = ""
            for linha in stderr:
                saida_erro += str(linha)
            if saida_erro:
                print("ERRO:", saida_erro)

            retorno = chan.recv_exit_status()
            if retorno != 0:
                print("ExitCode:", retorno)
                self.fechar_conexao()
                exit(retorno)
            return saida

    def fechar_conexao(self):
        self.ssh.close()
        self.scp.close()
        Log.imprime("CONEXAO SSH ENCERRADA", "CONEXAO SSH ENCERRADA")

    def obter_arquivo(self, path_origem_arquivo, path_destino_arquivo=''):
        Log.imprime("OBTENDO ARQUIVO " + path_origem_arquivo + " QUE SERA SALVO EM " + path_destino_arquivo,
                    "OBTENDO ARQUIVO " + path_origem_arquivo)
        try:
            self.scp.get(path_origem_arquivo, path_destino_arquivo, False, True)
            Log.imprime("ARQUIVO " + path_origem_arquivo + " SALVO EM " + path_destino_arquivo)
        except:
            Log.imprime("OCORREU UM ERRO AO TENTAR OBTER O ARQUIVO " + path_origem_arquivo + format_exc(),
                        "OCORREU UM ERRO AO TENTAR OBTER O ARQUIVO " + path_origem_arquivo, classe=SSH)
            exit(1)

    def enviar_arquivo(self, path_origem_arquivo, path_destino_arquivo):
        Log.imprime("ENVIANDO ARQUIVO " + path_origem_arquivo + " PARA " + path_destino_arquivo,
                    "ENVIANDO ARQUIVO " + path_origem_arquivo)
        try:
            self.scp.put(path_origem_arquivo, path_destino_arquivo)
            Log.imprime("ARQUIVO " + path_origem_arquivo + " ENVIADO PARA " + path_destino_arquivo)
        except:
            Log.imprime("OCORREU UM ERRO NO ENVIO PARA " + path_destino_arquivo + format_exc(),
                        "OCORREU UM ERRO NO ENVIO PARA " + path_destino_arquivo, classe=SSH)
            exit(1)

if __name__ == "__main__":
    import os

    servidor = os.getenv("SERVIDOR")
    usuario = os.getenv("USUARIO")
    senha = os.getenv("SENHA")
    comando_ssh = os.getenv("COMANDO")

    ssh = SSH(servidor, usuario)
    ssh.senha(senha)

    ssh.abrir_conexao()
    ssh.executar_comando(comando_ssh)
    ssh.fechar_conexao()


# python -u SSH.py "docker build -t adminv7/solr:${GO_TO_REVISION_AMBIENTE_ADMINV7} ."
# python -u SSH.py