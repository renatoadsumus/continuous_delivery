# coding=utf-8

import unittest

from python.tipos_arquivos.arquivo_properties import *


class TestesArquivoProperties(unittest.TestCase):
    NOME_ARQUIVO = "arquivo.properties"

    def setUp(self):
        self.properties = ArquivoProperties(self.NOME_ARQUIVO)

    def tearDown(self):
        self.properties = None

    def teste_escrever_properties_do_dicionario(self):
        dicionario = {'Name': 'Zara', 'Age': 7}
        self.properties.dicionario_para_properties(dicionario)
        self.assertTrue(self.arquivo_contem("Age=7"))
        self.assertTrue(self.arquivo_contem("Name=Zara"))

    def teste_alterar_valor_chave_existente(self):
        dicionario = {'Name': 'Zara', 'Age': 7}
        self.properties.dicionario_para_properties(dicionario)
        self.properties.alterar_valor_chave("Age", 10)
        self.assertTrue(self.arquivo_contem("Age=10"))
        self.assertFalse(self.arquivo_contem("Age=7"))

    def teste_alterar_valor_chave_nao_existente(self):
        dicionario = {'Name': 'Zara', 'Age': 7}
        self.properties.dicionario_para_properties(dicionario)
        self.properties.alterar_valor_chave("Class", "Second")
        self.assertTrue(self.arquivo_contem("Class=Second"))

    def teste_obter_valor_chave_existente(self):
        valor_esperado = "Zara"
        valor_recebido = self.properties.obter_valor_chave("Name")
        self.assertEquals(valor_esperado, valor_recebido)

    def teste_existe_chave(self):
        chave = "Age"
        valor_recebido = self.properties.existe_chave(chave)
        self.assertTrue(valor_recebido)

    def teste_nao_existe_chave(self):
        chave = "Age"
        valor = "7"
        valor_recebido = self.properties.adicionar_chave(chave, valor)
        self.assertFalse(valor_recebido)

    def arquivo_contem(self, valor):
        arquivo_properties = open(self.NOME_ARQUIVO, "r")
        linha = arquivo_properties.readline()
        while linha:
            if str(linha).__contains__(valor):
                arquivo_properties.close()
                return True
            linha = arquivo_properties.readline()
        arquivo_properties.close()
        return False


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
