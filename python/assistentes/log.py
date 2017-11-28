"""
Modulo que engloba a classe Log
"""

import logging
from datetime import datetime
from os import path, getenv

from python.assistentes.manipulador_data_hora import ManipuladorDataHora
from python.settings import WORKING_DIRECTORY


class Log(object):
    """
    Classe que representa o Log e suas acoes
    """
    logging.basicConfig(filename=path.join(WORKING_DIRECTORY, "LOG.txt"), level=logging.DEBUG)

    @staticmethod
    def imprime(mensagem_log, mensagem_impressa=None, classe=None, script=None, mensagem_de_erro=False):
        if mensagem_impressa:
            mensagem_impressa = str(mensagem_impressa)
            if mensagem_de_erro:
                mensagem_impressa += " #####\n##### ENTRE EM CONTATO COM A EQUIPE DE DEVOPS: #####\n##### EMAIL: " \
                                     "devops@infoglobo.com.br #####\n##### RAMAL: 9844 OU 9706"
            print("")
            print("##### " + mensagem_impressa + " #####")
            print("")

        logging.debug("")
        logging.debug(" " + ManipuladorDataHora.obter_data_hora_atual() + " " + str(mensagem_log))
        if classe:
            nome_classe = classe.__name__
            caminho_classe = classe.__module__
            logging.debug(" " + ManipuladorDataHora.obter_data_hora_atual() + " CLASSE: " + nome_classe)
            logging.debug(" " + ManipuladorDataHora.obter_data_hora_atual() + " CAMINHO DA CLASSE: " + caminho_classe)
        if script:
            logging.debug(" " + ManipuladorDataHora.obter_data_hora_atual() + " SCRIPT: " + script)
        logging.debug("")

    @staticmethod
    def gerar_arquivo_log_logstash():
        index_log = getenv("INDEXACAO_LOG_EXECUCAO")
        if index_log:
            arquivo_log_logstash = WORKING_DIRECTORY + "/../devops-metricas.log"
            data = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00")
            string_log = "{} {}\n".format(data, index_log)
            Log.imprime("Variavel de log informada: " + index_log)
            Log.imprime("Salvando entrada no log para o Logstash: " + arquivo_log_logstash)
            with open(arquivo_log_logstash, "a+") as arq_log:
                arq_log.write(string_log)
