# # coding=utf-8
# import unittest
#
# import mock
# from mock import MagicMock
#
# from python.apis.api_nexus import ApiNexus
# from python.fabrica_objetos import FabricaObjetos
#
# __author__ = 'ssouza'
#
#
# @mock.patch("python.biblioteca.Builders")
# class TestesAPINexus(unittest.TestCase):
#     def teste_nao_existe_builder(self, builder):
#         builder.get_atributos = MagicMock(
#             return_value=["jar", "1.3.0", "nao-existe", "br.com.infoglobo", "Plataforma"])
#         FabricaObjetos.atribuir_builder(builder)
#         resultado_esperado = 404
#         api = ApiNexus()
#         resultado_atual = api.get_resposta_http_builder()
#         self.assertEquals(resultado_esperado, resultado_atual)
#
#     def teste_existe_builder(self, builder):
#         builder.get_atributos = MagicMock(
#             return_value=["jar", "1.2.1", "infoglobo-anterior-e-proximo", "br.com.infoglobo", "Plataforma"])
#         FabricaObjetos.atribuir_builder(builder)
#         resultado_esperado = 200
#         api = ApiNexus()
#         resultado_atual = api.get_resposta_http_builder()
#         self.assertEquals(resultado_esperado, resultado_atual)
#
#     def teste_nao_existe_builder_grails(self, builder):
#         builder.get_atributos = MagicMock(
#             return_value=["zip", "1.11", "mail-service", "br.com.infoglobo.classificados", "releases"])
#         FabricaObjetos.atribuir_builder(builder)
#         resultado_esperado = 404
#         api = ApiNexus()
#         resultado_atual = api.get_resposta_http_builder()
#         self.assertEquals(resultado_esperado, resultado_atual)
#
#     def teste_existe_builder_grails(self, builder):
#         builder.get_atributos = MagicMock(
#             return_value=["zip", "1.1.1", "mail-service", "br.com.infoglobo.classificados", "releases"])
#         FabricaObjetos.atribuir_builder(builder)
#         resultado_esperado = 200
#         api = ApiNexus()
#         resultado_atual = api.get_resposta_http_builder()
#         self.assertEquals(resultado_esperado, resultado_atual)
#
#
# if __name__ == '__main__':
#     unittest.main()
