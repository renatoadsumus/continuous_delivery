import unittest
from os import environ, path, getcwd

from mock import patch

from python.implantadores.etl import ImplantadorETL


class TestesImplantadorETL(unittest.TestCase):

    def setUp(self):
        environ["CHAVE_SEGURANCA_PACOTE"] = "4e9e4d4b14db5a38fab793864d2dffc4"
        environ["SENHA_BANCO_DE_DADOS"] = "95QlyafTZ2s8"  # senha servidor dsv
        environ["NOME_PROJETO"] = "teste_unitario"
        environ["NOME_PROJETO"] = "teste_unitario"
        environ["CAMINHO_PACKAGES"] = "\\Integracao\\CRM\\ExpurgoDiario"

    @patch("python.settings.PIPELINE_NAME")
    def teste_copiar_arquivos_dtsconfig(self, mock_pipeline_name):
        mock_pipeline_name.return_value = "pipeline-staging"
        etl = ImplantadorETL()
        etl.caminho_dtsconfig = getcwd()
        etl.copiar_arquivos_dtsconfig()
        self.assertTrue(path.exists("pckExpurgoDiarioSalesForceAtividade.dtsConfig"))

    @patch("python.assistentes.linha_de_comando.LinhaDeComando.executar_com_output")
    @patch("python.settings.PIPELINE_NAME")
    def test_copiar_arquivos_dtsx(self, mock_pipeline_name, mock_executar_com_output):
        mock_executar_com_output.return_value = "The operation completed successfully."
        mock_pipeline_name.return_value = "pipeline-staging"
        etl = ImplantadorETL()
        etl.copiar_arquivos_dtsx()
        comando_esperado = "dtutil /FILE teste_unitario\\pckExpurgoDiarioSalesForceAtividade.dtsx " \
                           "/COPY SQL;\\Integracao\\CRM\\ExpurgoDiario\\pckExpurgoDiarioSalesForceAtividade " \
                           "/QUIET /DestS azrssisdsv /DECRYPT 4e9e4d4b14db5a38fab793864d2dffc4 " \
                           "/DestU DEV_INFG_Jenkins /DestP 95QlyafTZ2s8"
        mock_executar_com_output.assert_called_with(comando_esperado)


if __name__ == '__main__':
    unittest.main()
