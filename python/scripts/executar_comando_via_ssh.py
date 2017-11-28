from python.assistentes.SSH import SSH
from python.settings import getenv, DIRETORIO_CHAVES_SERVIDORES

SERVIDOR = getenv("SERVIDOR")
CAMINHO = getenv("CAMINHO")
COMANDO = getenv("COMANDO")
PARAMETROS = getenv("PARAMETROS")
USUARIO_SSH = getenv("USUARIO_SSH")
SENHA_SSH = getenv("SENHA_SSH")
ARQUIVO_CHAVE_SSH = getenv("ARQUIVO_CHAVE_SSH")

ssh = SSH(SERVIDOR, USUARIO_SSH)

if SENHA_SSH:
    ssh.senha(SENHA_SSH)
elif ARQUIVO_CHAVE_SSH:
    chave = DIRETORIO_CHAVES_SERVIDORES + ARQUIVO_CHAVE_SSH
    ssh.chave_acesso(chave)

ssh.abrir_conexao()

comando_executar = None

if PARAMETROS:
    comando_executar = "cd %s; ./%s %s" % (CAMINHO, COMANDO, PARAMETROS)
else:
    comando_executar = "cd %s; ./%s" % (CAMINHO, COMANDO)

ssh.executar_comando(comando_executar)

ssh.fechar_conexao()
