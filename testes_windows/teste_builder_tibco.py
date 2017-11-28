# import unittest
# from os import environ, path
#
# from python.assistentes.log import Log
# from python.builders.tibco import Tibco
# from python.settings import WORKING_DIRECTORY, getenv
# from python.tipos_arquivos.arquivo import Arquivo
#
#
# class TesteTibco(unittest.TestCase):
#     def setUp(self):
#         environ["NOME_PROJETO"] = "Funcionario"
#
#     def tearDown(self):
#         Log.imprime("APAGANDO ARQUIVOS GERADOS PELO TESTE DO BUILDER TIBCO", "APAGANDO ARQUIVOS GERADOS PELO TESTE "
#                                                                              "DO BUILDER TIBCO")
#         arquivo_ear = Arquivo(path.join(WORKING_DIRECTORY, getenv("NOME_PROJETO") + ".ear"))
#         arquivo_ear.excluir()
#         arquivo_log = Arquivo(path.join(WORKING_DIRECTORY, "log-validacao.log"))
#         arquivo_log.excluir()
#
#     def teste_fechar_pacote(self):
#         tibco = Tibco()
#
#         self.assertFalse(path.isfile(path.join(WORKING_DIRECTORY, getenv("NOME_PROJETO") + ".ear")))
#
#         tibco.fechar_artefato()
#
#         self.assertTrue(path.isfile(path.join(WORKING_DIRECTORY, getenv("NOME_PROJETO") + ".ear")))
#
#     def teste_executa_teste(self):
#         tibco = Tibco()
#
#         self.assertFalse(path.isfile(path.join(WORKING_DIRECTORY, "log-validacao.log")))
#
#         tibco.executa_testes()
#
#         self.assertTrue(path.isfile(path.join(WORKING_DIRECTORY, "log-validacao.log")))
#
# if __name__ == '__main__':
#     unittest.main()
