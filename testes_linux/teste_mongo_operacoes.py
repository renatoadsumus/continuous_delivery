import unittest

from python.mongo.conexao import Conexao
from python.mongo.operacoes import Operacoes as Op


class TestesMongoOperacoes(unittest.TestCase):
    conexao = None

    @classmethod
    def setUpClass(cls):
        usuario_teste = "teste_usuario"
        senha_teste = "0GpAsVbh"
        banco_teste = "teste_mongo"
        collection_teste = "teste_unitario"
        cls.conexao = Conexao(usuario_teste, senha_teste, banco_teste, collection_teste)
        cls.colecao = cls.conexao.obter_colecao()

    @classmethod
    def tearDownClass(cls):
        cls.conexao.fechar_conexao()

    def teste_buscar_documento_existente(self):
        string_json = '{"projeto": "teste_busca"}'
        valor_obtido = Op.buscar_json(self.colecao, string_json)[0]
        valor_esperado = "teste_busca"
        self.assertEqual(valor_obtido.get("projeto"), valor_esperado)

    def teste_buscar_com_string_vazia(self):
        string_json = ''
        with self.assertRaises(SystemExit) as ex:
            Op.buscar_json(self.colecao, string_json)
        self.assertEqual(ex.exception.code, 2)

    def teste_buscar_com_json_vazio(self):
        string_json = '{}'
        with self.assertRaises(SystemExit) as ex:
            Op.buscar_json(self.colecao, string_json).count()
        self.assertEqual(ex.exception.code, 3)

    def teste_buscar_documento_sem_fornecer_a_colecao(self):
        string_json = '{"projeto": "teste_busca"}'
        with self.assertRaises(SystemExit) as ex:
            Op.buscar_json(None, string_json)
        self.assertEqual(ex.exception.code, 1)

    def teste_buscar_documento_inexistente(self):
        string_json = '{"projeto": "projetoFalso"}'
        valor_obtido = Op.buscar_json(self.colecao, string_json).count()
        self.assertEqual(valor_obtido, 0)

    def teste_inserir_documento_valido(self):
        string_json = '{"projeto": "teste_inserir"}'
        retorno = Op.inserir_json(self.colecao, string_json)
        self.assertTrue(retorno)
        valor_obtido = Op.buscar_json(self.colecao, string_json).count()
        self.assertEqual(valor_obtido, 1)
        Op.excluir_json(self.colecao, string_json)

    def teste_inserir_string_vazia(self):
        string_json = ''
        with self.assertRaises(SystemExit) as ex:
            Op.inserir_json(self.colecao, string_json)
        self.assertEqual(ex.exception.code, 2)

    def teste_inserir_json_vazio(self):
        string_json = '{}'
        with self.assertRaises(SystemExit) as ex:
            Op.inserir_json(self.colecao, string_json)
        self.assertEqual(ex.exception.code, 3)

    def teste_inserir_documento_sem_fornecer_a_colecao(self):
        string_json = '{"projeto": "teste_inserir"}'
        with self.assertRaises(SystemExit) as ex:
            Op.buscar_json(None, string_json)
        self.assertEqual(ex.exception.code, 1)

    def teste_inserir_documento_duplicado(self):
        string_json = '{"projeto": "teste_inserir"}'
        Op.inserir_json(self.colecao, string_json)
        Op.inserir_json(self.colecao, string_json)
        valor_obtido = Op.buscar_json(self.colecao, string_json).count()
        self.assertEqual(valor_obtido, 2)
        retorno = Op.excluir_json(self.colecao, string_json)
        self.assertTrue(retorno)
        retorno2 = Op.excluir_json(self.colecao, string_json)
        self.assertTrue(retorno2)

    def teste_excluir_documento_valido(self):
        string_json = '{"projeto": "teste_excluir"}'
        Op.inserir_json(self.colecao, string_json)
        valor_obtido = Op.buscar_json(self.colecao, string_json).count()
        self.assertEqual(valor_obtido, 1)
        Op.excluir_json(self.colecao, string_json)
        valor_obtido = Op.buscar_json(self.colecao, string_json).count()
        self.assertEqual(valor_obtido, 0)

    def teste_excluir_documento_inexistente(self):
        string_json = '{"projeto": "projetoFalso"}'
        retorno = Op.excluir_json(self.colecao, string_json)
        self.assertFalse(retorno)

    def teste_excluir_string_vazia(self):
        string_json = ''
        with self.assertRaises(SystemExit) as ex:
            Op.excluir_json(self.colecao, string_json)
        self.assertEqual(ex.exception.code, 2)

    def teste_excluir_json_vazio(self):
        string_json = '{}'
        with self.assertRaises(SystemExit) as ex:
            Op.inserir_json(self.colecao, string_json)
        self.assertEqual(ex.exception.code, 3)

    def teste_excluir_documento_sem_fornecer_a_colecao(self):
        string_json = '{"projeto": "teste_excluir"}'
        with self.assertRaises(SystemExit) as ex:
            Op.buscar_json(None, string_json)
        self.assertEqual(ex.exception.code, 1)

    def teste_alterar_documento_valido(self):
        string_json_inserir = '{"projeto": "teste_altera"}'
        Op.inserir_json(self.colecao, string_json_inserir)
        string_json_alterar = '{"projeto": "teste_alterado"}'
        retorno = Op.alterar_json(self.colecao, string_json_inserir, string_json_alterar)
        self.assertTrue(retorno)
        Op.excluir_json(self.colecao, string_json_alterar)

    def teste_alterar_string_busca_vazia(self):
        string_json = ''
        string_nova = '{"projeto" : "teste_alterado}'
        with self.assertRaises(SystemExit) as ex:
            Op.alterar_json(self.colecao, string_json, string_nova)
        self.assertEqual(ex.exception.code, 2)

    def teste_alterar_string_nova_vazia(self):
        string_json_inserir = '{"projeto": "teste_altera"}'
        Op.inserir_json(self.colecao, string_json_inserir)
        string_nova_json = ''
        with self.assertRaises(SystemExit) as ex:
            Op.alterar_json(self.colecao, string_json_inserir, string_nova_json)
        self.assertEqual(ex.exception.code, 3)
        Op.excluir_json(self.colecao, string_json_inserir)

    def teste_alterar_json_busca_vazia(self):
        string_json = '{}'
        string_nova = '{"projeto" : "teste_alterado}'
        with self.assertRaises(SystemExit) as ex:
            Op.alterar_json(self.colecao, string_json, string_nova)
        self.assertEqual(ex.exception.code, 4)

    def teste_alterar_json_nova_vazia(self):
        string_json_inserir = '{"projeto": "teste_altera"}'
        Op.inserir_json(self.colecao, string_json_inserir)
        string_nova_json = '{}'
        with self.assertRaises(SystemExit) as ex:
            Op.alterar_json(self.colecao, string_json_inserir, string_nova_json)
        self.assertEqual(ex.exception.code, 5)
        Op.excluir_json(self.colecao, string_json_inserir)

    def teste_alterar_documento_inexistente(self):
        string_json = '{"projeto": "teste_altera"}'
        string_nova_json = '{"projeto": "teste_alterado"}'
        retorno = Op.alterar_json(self.colecao, string_json, string_nova_json)
        self.assertFalse(retorno)

    def teste_alterar_documento_sem_fornecer_a_colecao(self):
        string_json = '{"projeto": "teste_alterar"}'
        with self.assertRaises(SystemExit) as ex:
            Op.alterar_json(None, string_json, "")
        self.assertEqual(ex.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
