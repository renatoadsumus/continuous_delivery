# # coding=utf-8
#
# import unittest
#
# import mock
# from mock import MagicMock
#
# from python.fabrica_objetos import FabricaObjetos
# from python.scripts.verificacoes_pre_deploy import Verificacoes
#
# __author__ = 'ssouza'
#
#
# class TestesVerificacoes(unittest.TestCase):
#     @mock.patch("python.biblioteca.Builders")
#     def teste_not_versionamento_semantico(self, builder):
#         builder.get_versao = MagicMock(return_value="1")
#         FabricaObjetos.atribuir_builder(builder)
#         verificacoes = Verificacoes()
#         resultado_atual = verificacoes.is_versionamento_semantico()
#         self.assertFalse(resultado_atual)
#
#     @mock.patch("python.biblioteca.Builders")
#     def teste_is_versionamento_semantico(self, builder):
#         builder.get_versao = MagicMock(return_value="1.3.0")
#         FabricaObjetos.atribuir_builder(builder)
#         verificacoes = Verificacoes()
#         resultado_atual = verificacoes.is_versionamento_semantico()
#         self.assertTrue(resultado_atual)
#
#     @mock.patch("python.apis.api_nexus.ApiNexus")
#     def teste_versao_existe_nexus(self, api_nexus):
#         api_nexus.get_resposta_http_builder = MagicMock(return_value=200)
#         FabricaObjetos.atribuir_api_nexus(api_nexus)
#         verificacoes = Verificacoes()
#         resultado_atual = verificacoes.versao_ja_existe_no_nexus()
#         self.assertTrue(resultado_atual)
#
#     @mock.patch("python.apis.api_nexus.ApiNexus")
#     def teste_versao_nao_existe_nexus(self, api_nexus):
#         api_nexus.get_resposta_http_builder = MagicMock(return_value=404)
#         FabricaObjetos.atribuir_api_nexus(api_nexus)
#         verificacoes = Verificacoes()
#         resultado_atual = verificacoes.versao_ja_existe_no_nexus()
#         self.assertFalse(resultado_atual)
#
#
# if __name__ == '__main__':
#     unittest.main()
