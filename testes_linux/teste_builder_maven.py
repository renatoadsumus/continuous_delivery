# coding=utf-8

import unittest

import mock
from mock import MagicMock

from python.builders.maven import Maven
from python.fabrica_objetos import FabricaObjetos

__author__ = 'ssouza'


@mock.patch("python.tipos_arquivos.arquivo_xml.ArquivoXML")
class TestesMaven(unittest.TestCase):
    DIRETORIO_POM_XML = "fake-dir"

    def teste_get_versao_maven(self, arquivo_xml):
        arquivo_xml.obter_valor_xpath = MagicMock(return_value="1.5.0")
        FabricaObjetos.atribuir_arquivo_xml(arquivo_xml)
        resultado_esperado = '1.5.0'
        maven = Maven(self.DIRETORIO_POM_XML)
        resultado_atual = maven.get_versao()
        self.assertEqual(resultado_esperado, resultado_atual)

    def teste_get_group_id_maven(self, arquivo_xml):
        arquivo_xml.obter_valor_xpath = MagicMock(return_value="br.com.infoglobo")
        FabricaObjetos.atribuir_arquivo_xml(arquivo_xml)
        resultado_esperado = 'br.com.infoglobo'
        maven = Maven(self.DIRETORIO_POM_XML)
        resultado_atual = maven.get_group_id()
        self.assertEqual(resultado_esperado, resultado_atual)

    def teste_get_artifact_id_maven(self, arquivo_xml):
        arquivo_xml.obter_valor_xpath = MagicMock(return_value="infoglobo-anterior-e-proximo")
        FabricaObjetos.atribuir_arquivo_xml(arquivo_xml)
        resultado_esperado = 'infoglobo-anterior-e-proximo'
        maven = Maven(self.DIRETORIO_POM_XML)
        resultado_atual = maven.get_artifact_id()
        self.assertEqual(resultado_esperado, resultado_atual)

    def teste_get_repository_maven(self, arquivo_xml):
        arquivo_xml.obter_valor_xpath = MagicMock(
            return_value="https://inforep01.ogmaster.local:8443/nexus/content/repositories/Teste/")
        FabricaObjetos.atribuir_arquivo_xml(arquivo_xml)
        resultado_esperado = 'Teste'
        maven = Maven(self.DIRETORIO_POM_XML)
        resultado_atual = maven.get_repository()
        self.assertEqual(resultado_esperado, resultado_atual)


if __name__ == '__main__':
    unittest.main()
