"""
Script que executa o sonar para monitoramento do projeto
"""

from traceback import format_exc

from python.assistentes.log import Log
from python.fabrica_objetos import FabricaObjetos

__author__ = 'ssouza'

builder = FabricaObjetos.obter_builder()

try:
    builder.executa_scanner_sonar()
    Log.imprime("SUCESSO NA EXECUCAO DO SONAR", "SUCESSO NA EXECUCAO DO SONAR")
except:
    Log.imprime("FALHA\n" + format_exc(), "FALHA NA EXECUCAO DO SONAR",
                script="executar_sonar.py", mensagem_de_erro=True)
    exit(1)
