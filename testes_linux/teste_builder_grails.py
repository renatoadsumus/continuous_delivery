# coding=utf-8

import unittest

import mock
from mock import MagicMock

from python.builders.grails import Grails
from python.fabrica_objetos import FabricaObjetos

__author__ = 'ssouza'


@mock.patch("python.tipos_arquivos.arquivo_groovy.ArquivoGroovy")
class TestesGrails(unittest.TestCase):
    DIRETORIO_ARQUIVO_GROOVY = "fake-dir"

    def teste_get_versao_grails(self, arquivo_groovy):
        arquivo_groovy.obter_valor_chave = MagicMock(return_value="1.11")
        FabricaObjetos.atribuir_arquivo_groovy(arquivo_groovy)
        resultado_esperado = '1.11'
        grails = Grails(self.DIRETORIO_ARQUIVO_GROOVY)
        resultado_atual = grails.get_versao()
        self.assertEqual(resultado_esperado, resultado_atual)

    def teste_get_artifact_id_grails(self, arquivo_groovy):
        arquivo_groovy.obter_valor_chave = MagicMock(return_value="controle-acesso")
        FabricaObjetos.atribuir_arquivo_groovy(arquivo_groovy)
        resultado_esperado = 'controle-acesso'
        grails = Grails(self.DIRETORIO_ARQUIVO_GROOVY)
        resultado_atual = grails.get_artifact_id()
        self.assertEqual(resultado_esperado, resultado_atual)

    def teste_get_group_id_grails(self, arquivo_groovy):
        arquivo_groovy.obter_valor_chave = MagicMock(return_value="br.com.infoglobo.classificados")
        FabricaObjetos.atribuir_arquivo_groovy(arquivo_groovy)
        resultado_esperado = 'br.com.infoglobo.classificados'
        grails = Grails(self.DIRETORIO_ARQUIVO_GROOVY)
        resultado_atual = grails.get_group_id()
        self.assertEqual(resultado_esperado, resultado_atual)

    def teste_get_repository_grails(self, arquivo_groovy):
        arquivo_groovy.obter_valor_chave = MagicMock(
            return_value="http://inforep01.ogmaster.local:8080/nexus/content/repositories/releases")
        FabricaObjetos.atribuir_arquivo_groovy(arquivo_groovy)
        resultado_esperado = 'releases'
        grails = Grails(self.DIRETORIO_ARQUIVO_GROOVY)
        resultado_atual = grails.get_repository()
        self.assertEqual(resultado_esperado, resultado_atual)


if __name__ == '__main__':
    unittest.main()
