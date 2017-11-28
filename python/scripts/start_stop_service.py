# coding=utf-8
from os import getenv
from time import sleep

from python.assistentes.linha_de_comando import LinhaDeComando
from python.assistentes.log import Log

ACAO = getenv("ACAO")
SERVIDOR = getenv("SERVIDOR")
SERVICO = getenv("SERVICO")

comando = "sc \\\\%s start %s" % (SERVIDOR, SERVICO)
if ACAO == "STOP":
    comando = "sc \\\\%s stop %s" % (SERVIDOR, SERVICO)

retorno = LinhaDeComando.executar(comando, retornar_exit_code=True)
if retorno == 0:
    sleep(10)
    retorno = LinhaDeComando.executar(comando, retornar_exit_code=True)

# 1062 -> retorno ao tentar parar um servico parado
# 1056 -> retorno ao tentar iniciar um servico iniciado
if retorno == 1062 or retorno == 1056:
    Log.imprime("Acao %s executada com sucesso" % ACAO, "Acao %s executada com sucesso" % ACAO)
else:
    Log.imprime("Nao foi possivel executar a acao %s" % ACAO, "Nao foi possivel executar a acao %s" % ACAO,
                script="start_stop_service.py", mensagem_de_erro=True)
    exit(1)
