from python.settings import getenv, DIRETORIO_CHAVES_SERVIDORES
from python.assistentes.SSH import SSH
from sys import argv

etapa = None

for parametro in argv:
    if "-etapa" in parametro:
        etapa = str(parametro).replace("-etapa=", "")

SERVIDOR_LOADBALANCE = getenv("SERVIDOR_LOADBALANCE")
USUARIO_LOADBALANCE = "tfsservice"
SENHA_LOADBALANCE = getenv("SENHA_LOADBALANCE")
ARQUIVO_CHAVE_SSH = "teste.ppk"
BACKEND = getenv("BACKEND")
SERVIDOR_BACKEND = getenv("SERVIDOR_BACKEND")


ssh = SSH(SERVIDOR_LOADBALANCE, USUARIO_LOADBALANCE)
if SENHA_LOADBALANCE:
    ssh.senha(SENHA_LOADBALANCE)
elif ARQUIVO_CHAVE_SSH:
    chave = DIRETORIO_CHAVES_SERVIDORES + ARQUIVO_CHAVE_SSH
    ssh.chave_acesso(chave)

ssh.abrir_conexao()

for BKE in BACKEND.split(","):
    if etapa.lower() == "pre_deploy":
        comando_ssh = "echo disable server " + BKE + "/" + SERVIDOR_BACKEND \
                      + " | sudo nc -U /var/lib/haproxy/stats"
    else:
        comando_ssh = "echo enable server " + BKE + "/" + SERVIDOR_BACKEND \
                      + " | sudo nc -U /var/lib/haproxy/stats"
    ssh.executar_comando(comando_ssh)

ssh.fechar_conexao()
