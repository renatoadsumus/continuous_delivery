import unittest

from python.assistentes.linha_de_comando import LinhaDeComando


class TestesLinhaDeComando(unittest.TestCase):

    def teste_executar_comando_sem_exit_code_com_sucesso(self):
        comando = "echo Teste passou"
        valor_esperado = 0
        valor_obtido = LinhaDeComando.executar(comando)
        self.assertEqual(valor_obtido, valor_esperado)

    def teste_executar_comando_sem_exit_code_com_erro(self):
        comando = "ech"
        with self.assertRaises(SystemExit) as ex:
            LinhaDeComando.executar(comando)
        self.assertNotEqual(ex.exception.code, 0)

    def teste_executar_comando_com_exit_code_com_sucesso(self):
        comando = "echo Teste passou"
        valor_esperado = 0
        valor_obtido = LinhaDeComando.executar(comando, retornar_exit_code=True)
        self.assertEqual(valor_obtido, valor_esperado)

    def teste_executar_comando_com_exit_code_com_erro(self):
        comando = "ech"
        valor_obtido = LinhaDeComando.executar(comando, retornar_exit_code=True)
        self.assertNotEqual(valor_obtido, 0)


if __name__ == '__main__':
    unittest.main()
