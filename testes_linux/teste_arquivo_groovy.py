# coding=utf-8

import unittest

from python.tipos_arquivos.arquivo_groovy import *
from os import path


class TestesArquivoProperties(unittest.TestCase):
    NOME_ARQUIVO = path.dirname(__file__) + "/ExemploGrailsPlugin.groovy"

    def setUp(self):
        self.properties = ArquivoGroovy(self.NOME_ARQUIVO)

    def tearDown(self):
        self.properties = None

    def teste_obter_valor_chave_existente_version(self):
        valor_esperado = "1.10.1"
        valor_recebido = self.properties.obter_valor_chave("defversion")
        self.assertEquals(valor_esperado, valor_recebido)

    def teste_obter_valor_chave_existente_repository(self):
        valor_esperado = "http://inforep01.ogmaster.local:8080/nexus/content/repositories/"
        valor_recebido = self.properties.obter_valor_chave("defrepository")
        self.assertEquals(valor_esperado, valor_recebido)

    def teste_obter_valor_chave_existente_group_id(self):
        valor_esperado = "br.com.infoglobo.classificados"
        valor_recebido = self.properties.obter_valor_chave("defgroupId")
        self.assertEquals(valor_esperado, valor_recebido)


if __name__ == '__main__':
    unittest.main()
