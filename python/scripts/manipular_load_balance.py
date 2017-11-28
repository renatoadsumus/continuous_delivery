from sys import argv
from time import sleep

import requests

from python.assistentes.SSH import SSH
from python.assistentes.log import Log
from python.settings import getenv, DIRETORIO_CHAVES_SERVIDORES

etapa = None

for parametro in argv:
    if "-etapa" in parametro:
        etapa = str(parametro.replace("-etapa=", ""))

CONTEXT_PATH = getenv("ContextPath")
SERVIDOR_PORTA_TOMCAT = getenv("ServidorPortaTomcat")
CAMINHO_HEALTHCHECK = getenv("CaminhoArquivoHealthCheck")
USUARIO_SSH = getenv("UsuarioSSH")
SENHA_SSH = getenv("SenhaSSH")
ARQUIVO_CHAVE_SSH = getenv("ArquivoChaveSSH")
URL_VERIFICACAO = getenv("CaminhoUrlVerificacao")

if not CONTEXT_PATH:
    Log.imprime("CONTEXT_PATH nao informado", "ERRO NO LOAD BALANCE",
                script="manipular_load_balance.py", mensagem_de_erro=True)
    exit(1)

if not CAMINHO_HEALTHCHECK:
    Log.imprime("CAMINHO_HEALTHCHECK nao informado", "ERRO NO LOAD BALANCE",
                script="manipular_load_balance.py", mensagem_de_erro=True)
    exit(1)

if not SERVIDOR_PORTA_TOMCAT:
    Log.imprime("SERVIDOR_PORTA_TOMCAT nao informado", "ERRO NO LOAD BALANCE",
                script="manipular_load_balance.py", mensagem_de_erro=True)
    exit(1)

if not ARQUIVO_CHAVE_SSH and not SENHA_SSH:
    Log.imprime("Arquivo chave para SSH ou a senha para SSH nao foi informado", "ERRO NO LOAD BALANCE",
                script="manipular_load_balance.py", mensagem_de_erro=True)
    exit(1)

if not USUARIO_SSH:
    USUARIO_SSH = "tfsservice"

servidor = SERVIDOR_PORTA_TOMCAT.split(":")[0]

if not etapa:
    Log.imprime("Parametro etapa nao informado", "ERRO NO LOAD BALANCE",
                script="manipular_load_balance.py", mensagem_de_erro=True)
    exit(1)

url_check = "http://" + SERVIDOR_PORTA_TOMCAT + "/" + URL_VERIFICACAO
resposta = requests.get(url_check)
Log.imprime("url_check: " + url_check)
Log.imprime("resposta.text: " + resposta.text)
if resposta.status_code != 200:
    mensagem = "ERRO ao verificar healthcheck pela url na etapa" + etapa
    mensagem += "Status code: " + resposta.status_code
    Log.imprime(mensagem, mensagem, script="manipular_load_balance.py", mensagem_de_erro=True)
    exit(1)

if etapa.lower() == "pre_deploy":
    comando_ssh = "rm " + CAMINHO_HEALTHCHECK + " || echo 'Arquivo " + CAMINHO_HEALTHCHECK + " nao encontrado'"
else:
    comando_ssh = "echo HEALTHCHECK > " + CAMINHO_HEALTHCHECK + " || echo 'Nao foi possivel criar o arquivo" \
                  + CAMINHO_HEALTHCHECK + "'"

ssh = SSH(servidor, USUARIO_SSH)
if SENHA_SSH:
    ssh.senha(SENHA_SSH)
elif ARQUIVO_CHAVE_SSH:
    chave = DIRETORIO_CHAVES_SERVIDORES + ARQUIVO_CHAVE_SSH
    ssh.chave_acesso(chave)

ssh.abrir_conexao()
ssh.executar_comando(comando_ssh)
ssh.fechar_conexao()

Log.imprime("Esperando por 2 minutos", "Esperando por 2 minutos")
sleep(120)
