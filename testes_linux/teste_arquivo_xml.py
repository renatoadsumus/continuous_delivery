# coding=utf-8

import unittest
from python.settings import *
from python.tipos_arquivos.arquivo_xml import ArquivoXML
from os import path
__author__ = 'ssouza'


class TestesManipulacaoArquivoXML(unittest.TestCase):

    __XPATH_TAG_VERSION = "{http://maven.apache.org/POM/4.0.0}version"
    __XPATH_TAG_GROUP_ID = "{http://maven.apache.org/POM/4.0.0}groupId"
    __XPATH_TAG_ARTIFACT_ID = "{http://maven.apache.org/POM/4.0.0}artifactId"
    __XPATH_TAG_REPOSITORY = "{http://maven.apache.org/POM/4.0.0}distributionManagement"
    _LISTA_XPATH_TAGS_FILHAS_REPOSITORY = ["{http://maven.apache.org/POM/4.0.0}repository",
                                           "{http://maven.apache.org/POM/4.0.0}url"]
    __XPATH_TAG_BUILD = "{http://maven.apache.org/POM/4.0.0}build"
    _LISTA_XPATH_TAGS_FILHAS_BUILD = ["{http://maven.apache.org/POM/4.0.0}pluginManagement",
                                      "{http://maven.apache.org/POM/4.0.0}plugins",
                                      "{http://maven.apache.org/POM/4.0.0}plugin",
                                      "{http://maven.apache.org/POM/4.0.0}version"]
    __XML_NAMESPACE = "http://maven.apache.org/POM/4.0.0"

    def setUp(self):
        self.arquivo_xml = ArquivoXML(path.dirname(__file__) + "/" + ARQUIVO_PARA_BUILD)
        self.arquivo_xml.alterar_valor_xpath(self.__XPATH_TAG_VERSION, "1.3.0")

    def tearDown(self):
        self.arquivo_xml = None

    def teste_obter_versao_pom_xml(self):
        versao_esperada = "1.3.0"
        versao_recebida = self.arquivo_xml.obter_valor_xpath(self.__XPATH_TAG_VERSION)
        self.assertEqual(versao_esperada, versao_recebida)

    def teste_obter_versao_pom_xml_passando_namespace(self):
        versao_esperada = "1.3.0"
        arquivo_xml = ArquivoXML(path.dirname(__file__) + "/" + ARQUIVO_PARA_BUILD, self.__XML_NAMESPACE)
        versao_recebida = arquivo_xml.obter_valor_xpath(self.__XPATH_TAG_VERSION)
        self.assertEqual(versao_esperada, versao_recebida)

    def teste_alterar_versao_pom_xml(self):
        versao_esperada = "1.3.0.1234"
        self.arquivo_xml.alterar_valor_xpath(self.__XPATH_TAG_VERSION, versao_esperada)
        versao_recebida = self.arquivo_xml.obter_valor_xpath(self.__XPATH_TAG_VERSION)
        self.assertEqual(versao_esperada, versao_recebida)

    def teste_obter_version_plugin_pom_xml(self):
        versao_esperada = "2.1"
        versao_recebida = self.arquivo_xml.obter_valor_xpath(self.__XPATH_TAG_BUILD,
                                                             self._LISTA_XPATH_TAGS_FILHAS_BUILD)
        self.assertEqual(versao_esperada, versao_recebida)


if __name__ == '__main__':
    unittest.main()
