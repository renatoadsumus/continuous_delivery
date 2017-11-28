"""
Script que atua no fechamento do pacote com auxilio da FabricaObjetos
"""

from traceback import format_exc

from python.assistentes.log import Log
from python.envio_email.envio_email import Email
from python.fabrica_objetos import FabricaObjetos

__author__ = 'ssouza'

builder = FabricaObjetos.obter_builder()
email = Email()

try:
    builder.fechar_artefato()
    Log.imprime("PACOTE GERADO COM SUCESSO", "PACOTE GERADO COM SUCESSO")
    Log.gerar_arquivo_log_logstash()
except:
    Log.imprime("ERRO NO EMPACOTAMENTO DO ARTEFATO\n" + format_exc(),
                "ERRO NO EMPACOTAMENTO DO ARTEFATO.", script="fechar_artefato.py")
    exit(1)
