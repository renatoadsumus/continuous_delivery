from python.assistentes.ftp import FTP
from python.assistentes.log import Log
from os import getenv

host_ftp = getenv("SERVIDOR_FTP")
usuario_ftp = getenv("USUARIO_FTP")
senha_ftp = getenv("SENHA_FTP")
ssl = getenv("SSL")
diretorio_ftp = getenv("DIRETORIO_FTP")
diretorio_enviar = getenv("DIRETORIO_ENVIAR")

Log.imprime("INICIANDO PROCESSO DE DEPLOY DOS ARQUIVOS PARA O SERVIDOR " + host_ftp,
            "INICIANDO PROCESSO DE DEPLOY DOS ARQUIVOS")

use_ssl = False
if ssl.lower() == "true":
    use_ssl = True

Log.imprime("ESTABELECENDO CONEXAO COM O SERVIDOR")

ftp = FTP(host_ftp, usuario_ftp, senha_ftp, use_ssl)

Log.imprime("LIMPANDO O DIRETORIO DE DESTINO NO SERVIDOR", "LIMPANDO O DIRETORIO DE DESTINO NO SERVIDOR")

ftp.limpar_diretorio(diretorio_ftp)

Log.imprime("ENVIANDO ARQUIVOS PARA O SERVIDOR", "ENVIANDO ARQUIVOS PARA O SERVIDOR")

ftp.enviar_diretorio(diretorio_enviar, diretorio_ftp)

ftp.desconectar()

Log.imprime("DEPLOY ENCERRADO COM SUCESSO", "DEPLOY ENCERRADO COM SUCESSO")

