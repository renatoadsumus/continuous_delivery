# coding=utf-8

from traceback import format_exc

from python.assistentes.log import Log
from python.assistentes.manipulador_data_hora import ManipuladorDataHora
from python.envio_email.envio_email import Email
from python.fabrica_objetos import FabricaObjetos
from python.mongo.informacoes_artefatos_gocd import InformacoesArtefatos
from python.settings import PIPELINE_NAME, NOME_EQUIPE, NOME_PROJETO, environ
from python.tipos_arquivos.arquivo_properties import ArquivoProperties

__author__ = 'apinto'

try:

    if PIPELINE_NAME.__contains__("producao"):
        informacoes = InformacoesArtefatos(NOME_EQUIPE, NOME_PROJETO)
        numero_mudanca = str(informacoes.obter_numero_mudanca())
        environ["NUMERO_MUDANCA"] = numero_mudanca
        Log.imprime("INICIANDO O PROCESSO DE DEPLOY", "INICIANDO DEPLOY.\nMUDANCA: " + numero_mudanca)

    implantador = FabricaObjetos.obter_implantador()
    implantador.implantar_artefato()

    data_hora_execucao = ManipuladorDataHora.obter_data_hora_atual()
    data_hora_deploy = ArquivoProperties("data-hora-deploy.properties")
    data_hora_deploy.alterar_valor_chave("Data_Hora_Inicio_Analise", data_hora_execucao)
    Log.imprime("HORA DO DEPLOY: " + data_hora_execucao)

    if PIPELINE_NAME.__contains__("producao"):
        email = Email()
        destinatarios = "gestaodemudancas@infoglobo.com.br,sistemasdeproducao@infoglobo.com.br,," \
                        "devops@infoglobo.com.br,infra_ti@infoglobo.com.br"
        email.enviar_email_sucesso(destinatarios)
    Log.imprime("DEPLOY EXECUTADO COM SUCESSO", "DEPLOY EXECUTADO COM SUCESSO")
    Log.gerar_arquivo_log_logstash()
except:
    Log.imprime("ERRO NA EXECUCAO DO DEPLOY\n" + format_exc(), "ERRO NA EXECUCAO DO DEPLOY.",
                script="implantar_artefato.py", mensagem_de_erro=True)
    exit(1)
