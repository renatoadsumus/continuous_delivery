import unittest
from os import environ, path, remove

from freezegun import freeze_time

from python.assistentes.log import Log, WORKING_DIRECTORY


@freeze_time("01-01-2016")
class TestesLinhaDeComando(unittest.TestCase):
    @classmethod
    def setUp(cls):
        environ["INDEXACAO_LOG_EXECUCAO"] = "[Cadin]:BANCO_DADOS-Deploy_Producao"
        cls.arquivo_log_logstash = WORKING_DIRECTORY + "/../devops-metricas.log"

    def teste_gerar_arquivo_log_logstash(self):
        valor_esperado = "2016-01-01T00:00:00-03:00 [Cadin]:BANCO_DADOS-Deploy_Producao"
        Log.gerar_arquivo_log_logstash()
        self.assertTrue(path.isfile(self.arquivo_log_logstash))
        with open(self.arquivo_log_logstash, "r") as arq_log:
            valor_obtido = arq_log.read().splitlines()[-1]
        self.assertEqual(valor_obtido, valor_esperado)

    def teste_nao_gerar_arquivo_log_logstash(self):
        if path.isfile(self.arquivo_log_logstash):
            remove(self.arquivo_log_logstash)
        del environ["INDEXACAO_LOG_EXECUCAO"]
        Log.gerar_arquivo_log_logstash()
        self.assertFalse(path.isfile(self.arquivo_log_logstash))


if __name__ == '__main__':
    unittest.main()
