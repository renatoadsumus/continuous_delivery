# coding=utf-8

from os import getenv
from subprocess import check_call
from traceback import format_exc

from python.assistentes.log import Log

try:
    comando = "/opt/sonar-scanner/latest/bin/sonar-scanner"
    if str(getenv("SISTEMA_OPERACIONAL")).lower() == "windows":
        comando = "E:\\sonar-scanner-windows\\latest\\bin\\sonar-scanner.bat"
    check_call([comando], shell=True)
    Log.imprime("SUCESSO NA EXECUCAO DO SONAR", "SUCESSO NA EXECUCAO DO SONAR")
except:
    Log.imprime("FALHA\n" + format_exc(), "FALHA NA EXECUCAO DO SONAR",
                script="executar_sonar.py", mensagem_de_erro=True)
    exit(1)
