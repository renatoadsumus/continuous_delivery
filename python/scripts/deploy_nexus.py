# coding=utf-8

from traceback import format_exc

from python.assistentes.log import Log
from python.envio_email.envio_email import Email
from python.fabrica_objetos import FabricaObjetos

__author__ = 'ssouza'

builder = FabricaObjetos.obter_builder()
email = Email()

try:
    builder.faz_deploy_nexus()
    Log.imprime("Deploy efetuado com sucesso no Nexus", "Deploy efetuado com sucesso no Nexus")
    Log.gerar_arquivo_log_logstash()
    email.enviar_email_sucesso()
except:
    Log.imprime("Erro no deploy do nexus"
                "\n" + format_exc(),
                "Erro no deploy do nexus",
                script="deploy_nexus.py", mensagem_de_erro=True)
    email.enviar_email_falha("falha_deploy.html")
    exit(1)
