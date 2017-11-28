import unittest

from python.apis.api_gocd import ApiGoCd


class TestesAPIGoCd(unittest.TestCase):
    def setUp(self):
        self.api = ApiGoCd

    def teste_obter_nome_todos_pipelines(self):
        valor_obtido = self.api.obter_nome_todos_pipelines()
        valor_esperado = "scripts_continuous_delivery"
        self.assertNotEqual(valor_obtido, None)
        self.assertTrue(valor_esperado in valor_obtido)

    def teste_obter_quantidade_pipelines(self):
        valor_obtido = self.api.obter_quantidade_pipelines()
        valor_esperado = 0
        self.assertNotEqual(valor_obtido, None)
        self.assertTrue(valor_obtido > valor_esperado)

    def teste_obter_nome_todos_pipeline_groups(self):
        valor_obtido = self.api.obter_nome_todos_pipeline_groups()
        valor_esperado = "DevOps"
        self.assertNotEqual(valor_obtido, None)
        self.assertTrue(valor_esperado in valor_obtido)

    def teste_obter_quantidade_pipeline_groups(self):
        valor_obtido = self.api.obter_quantidade_pipeline_groups()
        valor_esperado = 0
        self.assertNotEqual(valor_obtido, None)
        self.assertTrue(valor_obtido > valor_esperado)

    def teste_obter_duracao_execucao_job(self):
        valor_obtido = self.api.obter_duracao_execucao_job(11915)
        valor_esperado = "0:00:27"
        self.assertNotEqual(valor_obtido, None)
        self.assertEqual(valor_esperado, str(valor_obtido))

    def teste_obter_duracao_execucao_stage(self):
        valor_obtido = self.api.obter_duracao_execucao_stage(11680)
        valor_esperado = "0:00:27"
        self.assertNotEqual(valor_obtido, None)
        self.assertEqual(valor_esperado, str(valor_obtido))

    def teste_obter_ids_jobs_do_stage(self):
        valor_obtido = self.api.obter_ids_jobs_do_stage(11680)
        valor_esperado = ["11915"]
        self.assertNotEqual(valor_obtido, None)
        self.assertEqual(valor_esperado, valor_obtido)

    def teste_obter_ids_stages_do_pipeline(self):
        valor_obtido = self.api.obter_ids_stages_do_pipeline(6131)
        valor_esperado = ["11680", "11682", "11686", "11688"]
        self.assertNotEqual(valor_obtido, None)
        self.assertEqual(valor_esperado, valor_obtido)

    def teste_obter_id_ultima_execucao_pipeline(self):
        valor_obtido = self.api.obter_n_ids_pipeline("teste_api_gocd")
        tipo_esperado = int
        self.assertNotEqual(valor_obtido, None)
        self.assertEqual(tipo_esperado, type(valor_obtido))

    def teste_obter_ids_ultimas_dez_execucoes_pipeline(self):
        valor_obtido = self.api.obter_n_ids_pipeline("teste_api_gocd", n=10)
        tipo_esperado = list
        tamanho_esperado = 10
        self.assertNotEqual(valor_obtido, None)
        self.assertEqual(tipo_esperado, type(valor_obtido))
        self.assertEqual(tamanho_esperado, len(valor_obtido))

    def teste_obter_duracao_execucao_pipeline_por_id(self):
        valor_obtido = self.api.obter_duracao_execucao_pipeline_por_id(6131)
        valor_esperado = "0:11:35"
        self.assertNotEqual(valor_obtido, None)
        self.assertEqual(valor_esperado, str(valor_obtido))

    def teste_obter_duracao_ultima_execucao_pipeline(self):
        from datetime import timedelta
        valor_obtido = self.api.obter_duracao_ultima_execucao_pipeline("teste_api_gocd")
        tipo_esperado = timedelta
        self.assertNotEqual(valor_obtido, None)
        self.assertEqual(tipo_esperado, type(valor_obtido))

    def teste_obter_duracao_ultimas_dez_execucoes_pipeline(self):
        from datetime import timedelta
        valor_obtido = self.api.obter_duracao_ultimas_dez_execucoes_pipeline("teste_api_gocd")
        tipo_esperado = list
        tamanho_esperado = 10
        tipo_valores_esperado = timedelta
        self.assertNotEqual(valor_obtido, None)
        self.assertEqual(tipo_esperado, type(valor_obtido))
        self.assertEqual(tamanho_esperado, len(valor_obtido))
        self.assertEqual(tipo_valores_esperado, type(valor_obtido[0]))

    def teste_obter_nome_do_pipeline_e_data_da_execucao(self):
        valor_obtido = self.api.obter_nome_do_pipeline_e_data_da_execucao(6131)
        nome_esperado = "scripts_continuous_delivery"
        data_esperada = "2017-03-08T10:13:04-03:00"
        self.assertNotEqual(valor_obtido, [None, None])
        self.assertEqual(nome_esperado, valor_obtido[0])
        self.assertEqual(data_esperada, valor_obtido[1])


if __name__ == '__main__':
    unittest.main()
