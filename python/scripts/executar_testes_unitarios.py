"""
Script que executa os testes unitarios de acordo com a tecnologia necessaria
"""

from traceback import format_exc

from python.assistentes.log import Log
from python.fabrica_objetos import FabricaObjetos

__author__ = 'ssouza'

builder = FabricaObjetos.obter_builder()

try:
    builder.executa_testes()
    Log.imprime("Sucesso na execucao dos testes unitarios")
except:
    Log.imprime("Erro na execucao dos testes unitarios\n" + format_exc(),
                "Erro na execucao dos testes unitarios", script="executar_testes_unitarios.py", mensagem_de_erro=True)
    exit(1)
