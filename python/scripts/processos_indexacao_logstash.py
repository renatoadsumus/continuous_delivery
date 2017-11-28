from datetime import datetime
from os import getenv, path


def gerar_arquivo_log_logstash(index_log, tipo_log):
    jenkins_home = getenv("JENKINS_HOME")
    if jenkins_home:
        arquivo_log_logstash = path.join(jenkins_home, "jobs", "{}-metricas.log".format(tipo_log))
    else:
        go_home_pipeline = getenv("WORKING_DIRECTORY")
        arquivo_log_logstash = path.join(go_home_pipeline, "../{}-metricas.log".format(tipo_log))
    data = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00")
    string_log = "{} {}\n".format(data, index_log)
    print("Variavel de log informada: " + string_log)
    print("Salvando entrada no log para o Logstash: " + arquivo_log_logstash)
    with open(arquivo_log_logstash, "a+") as arq_log:
        arq_log.write(string_log)

INDEXACAO_LOG_EXECUCAO = getenv("INDEXACAO_LOG_EXECUCAO")
TIPO_LOG = getenv("TIPO_LOG")


if not INDEXACAO_LOG_EXECUCAO or not TIPO_LOG:
    print("####### Uma ou mais variaveis nao foram informadas #######")
    print("INDEXACAO_LOG_EXECUCAO = {}\nTIPO_LOG = {}".format(INDEXACAO_LOG_EXECUCAO, TIPO_LOG))
    exit(0)

if TIPO_LOG not in ["processos", "devops"]:
    print("Tipo de log incorreto: {}".format(TIPO_LOG))
    exit(0)

gerar_arquivo_log_logstash(INDEXACAO_LOG_EXECUCAO, TIPO_LOG)
