import unittest

from pymongo.errors import OperationFailure

from python.mongo.conexao import Conexao


class TestesMongoConexao(unittest.TestCase):
    USUARIO_TESTE = "teste_usuario"
    SENHA_TESTE = "0GpAsVbh"
    BANCO_TESTE = "teste_mongo"
    COLLECTION_TESTE = "teste_unitario"

    def teste_acessar_colecao_existente(self):
        conexao = Conexao(self.USUARIO_TESTE, self.SENHA_TESTE, self.BANCO_TESTE, self.COLLECTION_TESTE)
        valor_obtido = conexao.acessar_colecao(self.COLLECTION_TESTE)
        conexao.fechar_conexao()
        self.assertTrue(valor_obtido)

    def teste_acessar_colecao_nao_existente(self):
        conexao = Conexao(self.USUARIO_TESTE, self.SENHA_TESTE, self.BANCO_TESTE, self.COLLECTION_TESTE)
        with self.assertRaises(SystemExit) as ex:
            conexao.acessar_colecao("Nao Existe")
        conexao.fechar_conexao()
        self.assertEqual(ex.exception.code, 3)

    def teste_acessar_colecao_com_nome_vazio(self):
        conexao = Conexao(self.USUARIO_TESTE, self.SENHA_TESTE, self.BANCO_TESTE, "")
        with self.assertRaises(SystemExit) as ex:
            conexao.acessar_colecao("")
        conexao.fechar_conexao()
        self.assertEqual(ex.exception.code, 1)

    def teste_acessar_colecao_sem_acessar_banco(self):
        conexao = Conexao(self.USUARIO_TESTE, self.SENHA_TESTE)
        with self.assertRaises(SystemExit) as ex:
            conexao.acessar_colecao(self.COLLECTION_TESTE)
        conexao.fechar_conexao()
        self.assertEqual(ex.exception.code, 2)

    def teste_acessar_banco_existente(self):
        conexao = Conexao(self.USUARIO_TESTE, self.SENHA_TESTE, self.BANCO_TESTE, self.COLLECTION_TESTE)
        valor_obtido = conexao.acessar_banco(self.BANCO_TESTE)
        conexao.fechar_conexao()
        self.assertTrue(valor_obtido)

    def teste_acessar_banco_nao_existente(self):
        conexao = Conexao(self.USUARIO_TESTE, self.SENHA_TESTE, self.BANCO_TESTE, self.COLLECTION_TESTE)
        with self.assertRaises(SystemExit) as ex:
            conexao.acessar_banco("NaoExiste")
        conexao.fechar_conexao()
        self.assertEqual(ex.exception.code, 3)

    def teste_acessar_banco_com_nome_vazio(self):
        conexao = Conexao(self.USUARIO_TESTE, self.SENHA_TESTE, "", self.COLLECTION_TESTE)
        with self.assertRaises(SystemExit) as ex:
            conexao.acessar_banco("")
        conexao.fechar_conexao()
        self.assertEqual(ex.exception.code, 1)

    def teste_abrir_conexao_usuario_e_senha_validos(self):
        conexao = Conexao(self.USUARIO_TESTE, self.SENHA_TESTE, self.BANCO_TESTE, self.COLLECTION_TESTE)
        self.assertTrue(conexao)
        conexao.fechar_conexao()

    def teste_abrir_conexao_usuario_ou_senha_vazios(self):
        with self.assertRaises(SystemExit) as ex:
            Conexao("", "SenhaFalsa", self.BANCO_TESTE, self.COLLECTION_TESTE)
        self.assertEqual(ex.exception.code, 1)
        with self.assertRaises(SystemExit) as ex:
            Conexao("usuarioErrado", "", self.BANCO_TESTE, self.COLLECTION_TESTE)
        self.assertEqual(ex.exception.code, 1)
        with self.assertRaises(SystemExit) as ex:
            Conexao("", "", self.BANCO_TESTE, self.COLLECTION_TESTE)
        self.assertEqual(ex.exception.code, 1)

    def teste_abrir_conexao_usuario_e_senha_invalidos(self):
        with self.assertRaises(OperationFailure) as ex:
            Conexao("usuarioErrado", "SenhaFalsa", self.BANCO_TESTE, self.COLLECTION_TESTE)
        self.assertNotEqual(ex.exception.code, 0)

if __name__ == '__main__':
    unittest.main()
