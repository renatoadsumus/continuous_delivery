import unittest

from python.mongo.conexao import Conexao
from python.mongo.informacoes_artefatos_gocd import InformacoesArtefatos
from python.mongo.operacoes import Operacoes
from python.settings import USUARIO_GO_API, SENHA_GO_API


class TestesMongoInformacoesArtefatos(unittest.TestCase):
    NOME_EQUIPE = "equipe_QA"
    NOME_PROJETO = "teste_unitario"

    @classmethod
    def setUpClass(cls):
        cls.info_artefato = InformacoesArtefatos(cls.NOME_EQUIPE, cls.NOME_PROJETO)
        cls.mongo = Operacoes()
        conexao = Conexao(USUARIO_GO_API, SENHA_GO_API, "qa_informacoes_entrega_continua", cls.NOME_EQUIPE)
        cls.colecao = conexao.obter_colecao()

    @classmethod
    def tearDownClass(cls):
        print("")

    def atualizar_informacoes(self):
        self.info_artefato = InformacoesArtefatos(self.NOME_EQUIPE, self.NOME_PROJETO)

    def teste_obter_revision_deploy_stg(self):

        string_busca = '{ "projeto": "' + "teste_unitario" + '"}'
        string_nova = '{"status_deploy_prd":"' + "I" + '"}'

        self.mongo.alterar_json(self.colecao, string_busca, string_nova)
        self.atualizar_informacoes()

        valor_obtido = self.info_artefato.obter_revision_deploy_stg()
        valor_esperado = '1'
        self.assertEqual(valor_obtido, valor_esperado)

    def teste_obter_revision_deploy_prd(self):
        string_busca = '{ "projeto": "' + "teste_unitario" + '"}'
        string_nova = '{"revision_deploy_prd":"' + "99" + '", "status_deploy_prd":"' + "F" + '"}'

        self.mongo.alterar_json(self.colecao, string_busca, string_nova)
        self.atualizar_informacoes()

        valor_obtido = self.info_artefato.obter_revision_deploy_prd()
        valor_esperado = '99'
        self.assertEqual(valor_obtido, valor_esperado)

    def teste_obter_data_deploy_stg(self):
        valor_obtido = self.info_artefato.obter_data_deploy_stg()
        valor_esperado = '01/02/2001'
        self.assertEqual(valor_obtido, valor_esperado)

    def teste_obter_data_deploy_prd(self):
        valor_obtido = self.info_artefato.obter_data_deploy_prd()
        valor_esperado = '02/02/2001'
        self.assertEqual(valor_obtido, valor_esperado)

    def teste_obter_cobertura_testes_unitarios(self):
        valor_obtido = self.info_artefato.obter_cobertura_testes_unitarios()
        valor_esperado = '10'
        self.assertEqual(valor_obtido, valor_esperado)

    def teste_obter_quantidade_issues_total_aplicacao(self):
        valor_obtido = self.info_artefato.obter_quantidade_issues_total_aplicacao()
        valor_esperado = '5'
        self.assertEqual(valor_obtido, valor_esperado)

    def teste_obter_quantidade_issues_findbugs(self):
        valor_obtido = self.info_artefato.obter_quantidade_issues_findbugs()
        valor_esperado = ["dependencia1:2", "dependencia2:3"]
        self.assertEqual(valor_obtido, valor_esperado)

    def teste_obter_status_deploy_prd_com_valor_campo_diferente_de_I(self):
        string_busca = '{ "projeto": "' + "teste_unitario" + '"}'
        string_nova = '{"status_deploy_prd":"' + "F" + '"}'

        self.mongo.alterar_json(self.colecao, string_busca, string_nova)
        self.atualizar_informacoes()

        valor_obtido = self.info_artefato.obter_status_deploy_prd()
        valor_esperado = "F"
        self.assertEqual(valor_obtido, valor_esperado)

    def teste_se_nao_existe_a_chave_obter_status_deploy_prd(self):
        string_busca = '{"projeto":"projetoFalso"}'
        string_nova = '{"status_deploy_prd":""}'

        InformacoesArtefatos(self.NOME_EQUIPE, "projetoFalso")

        self.mongo.alterar_json(self.colecao, string_busca, string_nova, operador="unset")
        self.atualizar_informacoes()
        valor_obtido = self.info_artefato.obter_status_deploy_prd()
        valor_esperado = "F"
        self.assertEqual(valor_obtido, valor_esperado)

        documentos_encontrados = self.mongo.excluir_json(self.colecao, string_busca)
        valor_obtido = documentos_encontrados
        valor_esperado = True
        self.assertEqual(valor_obtido, valor_esperado)

    def teste_obter_status_deploy_prd_com_valor_campo_igual_I(self):
        string_busca = '{ "projeto": "' + "teste_unitario" + '"}'
        string_nova = '{"status_deploy_prd":"' + "I" + '"}'

        self.mongo.alterar_json(self.colecao, string_busca, string_nova)
        self.atualizar_informacoes()

        valor_obtido = self.info_artefato.obter_status_deploy_prd()
        valor_esperado = "I"
        self.assertEqual(valor_obtido, valor_esperado)

        string_nova = '{"status_deploy_prd":"' + "F" + '"}'
        self.mongo.alterar_json(self.colecao, string_busca, string_nova)

    def teste_verificar_inserir_excluir_projeto(self):
        string_busca = '{"projeto":"' + "projetoFalso" + '"}'

        documentos_encontrados = self.mongo.buscar_json(self.colecao, string_busca)
        valor_obtido = documentos_encontrados.count()
        valor_esperado = 0
        self.assertEqual(valor_obtido, valor_esperado)

        InformacoesArtefatos(self.NOME_EQUIPE, "projetoFalso")
        documentos_encontrados = self.mongo.buscar_json(self.colecao, string_busca)
        valor_obtido = documentos_encontrados.count()
        valor_esperado = 1
        self.assertEqual(valor_obtido, valor_esperado)

        documentos_encontrados = self.mongo.excluir_json(self.colecao, string_busca)
        valor_obtido = documentos_encontrados
        valor_esperado = True
        self.assertEqual(valor_obtido, valor_esperado)

    def teste_alterar_revision_deploy_stg(self):
        self.info_artefato.alterar(revision_deploy_stg='3')
        self.atualizar_informacoes()
        valor_obtido = self.info_artefato.obter_revision_deploy_stg()
        valor_esperado = '3'
        self.assertEqual(valor_obtido, valor_esperado)
        self.info_artefato.alterar(revision_deploy_stg='1')

    def teste_alterar_revision_deploy_prd(self):
        self.info_artefato.alterar(revision_deploy_prd='4')
        self.atualizar_informacoes()
        valor_obtido = self.info_artefato.obter_revision_deploy_prd()
        valor_esperado = '4'
        self.assertEqual(valor_obtido, valor_esperado)
        self.info_artefato.alterar(revision_deploy_prd='2')

    def teste_alterar_data_deploy_stg(self):
        self.info_artefato.alterar(data_deploy_stg='21/12/2012')
        self.atualizar_informacoes()
        valor_obtido = self.info_artefato.obter_data_deploy_stg()
        valor_esperado = '21/12/2012'
        self.assertEqual(valor_obtido, valor_esperado)
        self.info_artefato.alterar(data_deploy_stg='01/02/2001')

    def teste_alterar_data_deploy_prd(self):
        self.info_artefato.alterar(data_deploy_prd='21/12/2012')
        self.atualizar_informacoes()
        valor_obtido = self.info_artefato.obter_data_deploy_prd()
        valor_esperado = '21/12/2012'
        self.assertEqual(valor_obtido, valor_esperado)
        self.info_artefato.alterar(data_deploy_prd='02/02/2001')

    def teste_alterar_cobertura_testes_unitarios(self):
        self.info_artefato.alterar(cobertura_testes_unitarios='100')
        self.atualizar_informacoes()
        valor_obtido = self.info_artefato.obter_cobertura_testes_unitarios()
        valor_esperado = '100'
        self.assertEqual(valor_obtido, valor_esperado)
        self.info_artefato.alterar(cobertura_testes_unitarios='10')

    def teste_alterar_quantidade_issues_total_aplicacao(self):
        self.info_artefato.alterar(quantidade_issues_total='50')
        self.atualizar_informacoes()
        valor_obtido = self.info_artefato.obter_quantidade_issues_total_aplicacao()
        valor_esperado = '50'
        self.assertEqual(valor_obtido, valor_esperado)
        self.info_artefato.alterar(quantidade_issues_total='5')

    def teste_alterar_quantidade_issues_findbugs(self):
        self.info_artefato.alterar(dependencias=["dependencia1:20", "dependencia2:30"])
        self.atualizar_informacoes()
        valor_obtido = self.info_artefato.obter_quantidade_issues_findbugs()
        valor_esperado = ["dependencia1:20", "dependencia2:30"]
        self.assertEqual(valor_obtido, valor_esperado)
        self.info_artefato.alterar(dependencias=["dependencia1:2", "dependencia2:3"])

    def teste_alterar_quantidade_issues_findbugs_vazio(self):
        self.info_artefato.alterar(dependencias=[])
        self.atualizar_informacoes()
        valor_obtido = self.info_artefato.obter_quantidade_issues_findbugs()
        valor_esperado = ["dependencia1:2", "dependencia2:3"]
        self.assertEqual(valor_obtido, valor_esperado)

    def teste_alterar_dois_valores_ao_mesmo_tempo(self):
        self.info_artefato.alterar(revision_deploy_stg='3', revision_deploy_prd='4')
        self.atualizar_informacoes()
        valor_obtido_stg = self.info_artefato.obter_revision_deploy_stg()
        valor_obtido_prd = self.info_artefato.obter_revision_deploy_prd()
        valor_esperado_stg = '3'
        valor_esperado_prd = '4'
        self.assertEqual(valor_obtido_stg, valor_esperado_stg)
        self.assertEqual(valor_obtido_prd, valor_esperado_prd)
        self.info_artefato.alterar(revision_deploy_stg='1')
        self.info_artefato.alterar(revision_deploy_prd='2')

if __name__ == '__main__':
    unittest.main()
