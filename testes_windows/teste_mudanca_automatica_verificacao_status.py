# coding=utf-8

import unittest

from mock import patch

from python.mongo.conexao import Conexao
from python.mongo.operacoes import Operacoes
from python.scripts.criar_mudanca_automatica import CriarMudancaAutomatica, InformacoesArtefatos
from python.settings import USUARIO_GO_API, SENHA_GO_API, environ


class TesteCriarMudanca(unittest.TestCase):
    NOME_EQUIPE = "equipe_QA"
    NOME_PROJETO = "teste_unitario"

    @classmethod
    def setUpClass(cls):
        environ["CCTI_CLASS"] = "SUPORTE A HARDWARE"
        environ["CCTI_CATEGORY"] = "Switchs / Roteadores"
        environ["CCTI_TYPE"] = "Mudança"
        environ["CCTI_ITEM"] = "Hardware"
        environ["ID_FILA_EQUIPE"] = "50"

        cls.info_artefato = InformacoesArtefatos(cls.NOME_EQUIPE, cls.NOME_PROJETO)
        cls.mudanca_automatica = CriarMudancaAutomatica(cls.NOME_EQUIPE, cls.NOME_PROJETO)
        cls.mongo = Operacoes()
        conexao = Conexao(USUARIO_GO_API, SENHA_GO_API, "qa_informacoes_entrega_continua", cls.NOME_EQUIPE)
        cls.colecao = conexao.obter_colecao()

    @classmethod
    def tearDownClass(cls):
        print("")

    def teste_a_nao_abrir_uma_nova_mudanca_para_um_pipeline_ja_iniciado(self):
        string_busca = '{ "projeto": "' + "teste_unitario" + '"}'
        string_nova = '{"revision_deploy_prd":"' + "99" + '", "status_deploy_prd":"' + "I" + '"}'
        operacoes = Operacoes()
        operacoes.alterar_json(self.colecao, string_busca, string_nova)

        valor_esperado = self.info_artefato.obter_numero_mudanca()
        valor_obtido = self.mudanca_automatica.criar_mudanca_automatica()

        self.assertEqual(valor_esperado, valor_obtido)

    def teste_b_nao_abrir_mudanca_quando_revision_do_gocd_for_igual_a_revision_do_mongo(self):
        string_busca = '{ "projeto": "' + "teste_unitario" + '"}'
        string_nova = '{"revision_deploy_prd":"' + "96644" + '", "status_deploy_prd":"' + "F" + '"}'
        operacoes = Operacoes()
        operacoes.alterar_json(self.colecao, string_busca, string_nova)

        valor_esperado = self.info_artefato.obter_numero_mudanca()
        valor_obtido = self.mudanca_automatica.criar_mudanca_automatica()

        self.assertEqual(valor_esperado, valor_obtido)

    @patch("python.scripts.criar_mudanca_automatica.MudancaAutomatica.criar_mudanca_automatica",
           return_value="200-0000")
    def teste_c_abrir_mudanca_quando_revision_do_GoCd_for_diferente_que_no_Mongo(self, mock):
        # https://www.toptal.com/python/an-introduction-to-mocking-in-python
        string_busca = '{ "projeto": "' + "teste_unitario" + '"}'
        string_nova = '{"revision_deploy_prd":"' + "99" + '", "status_deploy_prd":"' + "F" + '"}'
        operacoes = Operacoes()
        operacoes.alterar_json(self.colecao, string_busca, string_nova)

        # valor_esperado = self.info_artefato.obter_numero_mudanca()
        valor_obtido = self.mudanca_automatica.criar_mudanca_automatica()
        mock.assert_called()

        self.assertIsNotNone(valor_obtido)
        # self.assertNotEqual(valor_esperado, valor_obtido)

if __name__ == '__main__':
    unittest.main()
