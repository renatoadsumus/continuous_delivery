import ftplib
from os import walk, sep, path
from time import sleep
from traceback import format_exc

from python.assistentes.log import Log


class FTP:

    def __init__(self, servidor_ftp, usuario_ftp, senha_ftp, seguranca):
        self.servidor_ftp = servidor_ftp
        self.usuario_ftp = usuario_ftp
        self.senha_ftp = senha_ftp
        self.seguranca = seguranca
        if not seguranca:
            self.ftp = ftplib.FTP(self.servidor_ftp, self.usuario_ftp, self.senha_ftp)
            Log.imprime("INICIANDO CONEXAO SEM SSL.")
        else:
            self.ftp = ftplib.FTP_TLS(self.servidor_ftp, self.usuario_ftp, self.senha_ftp)
            self.ftp.prot_p()
            Log.imprime("INICIANDO CONEXAO COM SSL.")
        self.diretorio_raiz = self.ftp.pwd()

    def enviar_arquivo(self, caminho_arquivo, nome_arquivo):
        with open(caminho_arquivo, 'rb') as arquivo:
            Log.imprime("ENVIANDO ARQUIVO: " + self.ftp.pwd() + nome_arquivo,
                        "ENVIANDO ARQUIVO: " + self.ftp.pwd() + nome_arquivo)
            tentativa = 0
            for tentativa in range(5):
                try:
                    self.storbinary('STOR ' + nome_arquivo, arquivo)
                    break
                except ftplib.error_perm:
                    Log.imprime("ERRO AO ENVIAR O ARQUIVO: " + caminho_arquivo + "\nTENTATIVA: " + str(tentativa+2),
                                "TENTATIVA: " + str(tentativa+2))
                    sleep(5)
            if tentativa == 4:
                self.desconectar()
                Log.imprime("ERRO AO ENVIAR O ARQUIVO APOS 5 TENTATIVAS: " + caminho_arquivo,
                            "ERRO AO ENVIAR O ARQUIVO APOS 5 TENTATIVAS: " + caminho_arquivo)
                exit(1)

    def enviar_diretorio(self, caminho_diretorio, diretorio_ftp):
        self.ftp.cwd(diretorio_ftp)
        Log.imprime("ENVIANDO DIRETORIO " + caminho_diretorio + " PARA " + diretorio_ftp)
        for raiz, diretorios, arquivos in walk(caminho_diretorio, topdown=True):
            relative = raiz[len(caminho_diretorio):].lstrip(sep)
            for diretorio in diretorios:
                try:
                    self.ftp.mkd(path.join(relative, diretorio))
                except ftplib.all_errors:
                    pass
            for arquivo in arquivos:
                self.ftp.cwd(path.join("/", diretorio_ftp, relative))

                self.enviar_arquivo(path.join(caminho_diretorio, relative, arquivo), arquivo)
                self.ftp.cwd(path.join('/', diretorio_ftp))

    def storbinary(self, cmd, fp, blocksize=8192, callback=None, rest=None):
        """
        Devido a um bug com servidores Microsoft de FTPS, foi necessario criar
         este metodo para remover a linha que executa o unwrap() do SSL
        linha 513 do ftplib.py
        """

        self.ftp.voidcmd('TYPE I')
        with self.ftp.transfercmd(cmd, rest) as conn:
            while 1:
                buf = fp.read(blocksize)
                if not buf:
                    break
                conn.sendall(buf)
                if callback:
                    callback(buf)
        return self.ftp.voidresp()

    def baixar_arquivo(self, nome_arquivo_download, caminho_diretorio_download, diretorio_ftp):
        arquivo = open(path.join(caminho_diretorio_download, nome_arquivo_download), "wb")

        Log.imprime("BAIXANDO ARQUIVO " + str(nome_arquivo_download) + " DE " + str(diretorio_ftp),
                    " BAIXANDO ARQUIVO." + str(nome_arquivo_download))
        self.ftp.retrbinary("RETR " + path.join("/", diretorio_ftp, nome_arquivo_download), arquivo.write)
        arquivo.close()

    def limpar_diretorio(self, diretorio_ftp):
        conteudo_diretorio = self.ftp.nlst(diretorio_ftp)
        caminho_diretorio_ftp = self.ftp.pwd()
        for conteudo in conteudo_diretorio:
            print("!!!!! " + conteudo)
            try:
                self.ftp.cwd(path.join(diretorio_ftp, conteudo))
                self.ftp.cwd(caminho_diretorio_ftp)
                self.limpar_diretorio(path.join(diretorio_ftp, conteudo))
            except ftplib.all_errors:
                self.ftp.delete(path.join(diretorio_ftp, conteudo))

        try:
            if diretorio_ftp != "":
                self.ftp.rmd(diretorio_ftp)
        except ftplib.all_errors:
            Log.imprime("ERRO NA REMOCAO DE " + str(diretorio_ftp) + "\n" + format_exc(),
                        " ERRO NA REMOCAO DO DIRETORIO.", classe=FTP)

    def desconectar(self):
        self.ftp.quit()
        Log.imprime("CONEXAO FTP ENCERRADA")
