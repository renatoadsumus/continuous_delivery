import shutil
import unittest
from os import environ, makedirs, path, getenv
from python.assistentes.linha_de_comando import LinhaDeComando

from python.assistentes.ftp import FTP
from python.implantadores.zip import ImplantadorZIP


class TestesImplantadorZIP(unittest.TestCase):

    def setUp(self):
        environ["SSL"] = "False"
        environ["LIMPAR_DESTINO"] = "True"
        environ["NOME_PROJETO"] = "compilado_sem_webconfig"
        environ["DIRETORIO_FTP"] = ""
        makedirs(".\\descompactado")
        makedirs(".\\sincronizado")

    def tearDown(self):
        shutil.rmtree(".\\descompactado")
        shutil.rmtree(".\\sincronizado")

    def test_implantar_artefato_com_arquivo_ambiente_com_nome_invalido(self):
        # Dado que nao exista o arquivo Web.config_STG no ZIP mas existem outros arquivos de configuracao
        environ["AMBIENTE"] = "STG"
        environ["NOME_ARQUIVO_CONFIGURACAO_AMBIENTE"] = "Web.config"

        # Quando tento instalar o pacote
        implantador_zip = ImplantadorZIP()

        with self.assertRaises(SystemExit) as error:
            implantador_zip.implantar_artefato()

        # Entao recebo uma mensagem de Erro
        self.assertEqual(1, error.exception.code, " Houve um ERRP EXIT diferente de 1")

    def test_implantar_artefato_com_arquivo_ambiente_com_compartilhamento_limpando_todo_diretorio_destino(self):
        # Dado que nao exista a pasta descompactado e a pasta_deploy esteja vazia
        environ["AMBIENTE"] = "QLT"
        environ["NOME_ARQUIVO_CONFIGURACAO_AMBIENTE"] = "Web.config"
        environ["CAMINHO_COMPARTILHAMENTO"] = "\\\\INFOJENKINS1\\teste_unitario_caminho_compartilhamento"
        environ["CAMINHO_APAGAR_COMPARTILHAMENTO"] = "apagarConteudo.bat"
        environ["PASTAS_NAO_APAGAR"] = ""

        # Quando tento instalar o pacote
        implantador_zip = ImplantadorZIP()
        implantador_zip.implantar_artefato()

        # Entao o arquivo de configuracao Web.config_QLT e renomeado para Web.config
        # E vejo o Web.config na pasta_deploy
        self.assertEqual(True, path.isfile(getenv("CAMINHO_COMPARTILHAMENTO") + "\\Web.config"))

        implantador_zip.limpar_pasta_compartilhada()

        self.assertEqual(False, path.isfile(getenv("CAMINHO_COMPARTILHAMENTO") + "\\Web.config"))

    def test_implantar_artefato_com_arquivo_ambiente_com_compartilhamento_nao_limpando_diretorio_destino(self):
        # Dado que nao exista a pasta descompactado e a pasta_deploy esteja vazia
        environ["AMBIENTE"] = "QLT"
        environ["NOME_ARQUIVO_CONFIGURACAO_AMBIENTE"] = "Web.config"
        environ["CAMINHO_COMPARTILHAMENTO"] = "\\\\INFOJENKINS1\\teste_unitario_caminho_compartilhamento"
        environ["CAMINHO_APAGAR_COMPARTILHAMENTO"] = "apagarConteudo.bat"
        environ["PASTAS_NAO_APAGAR"] = ""

        # Quando tento instalar o pacote
        implantador_zip = ImplantadorZIP()
        implantador_zip.implantar_artefato()

        # Entao o arquivo de configuracao Web.config_QLT e renomeado para Web.config
        # E vejo o Web.config na pasta_deploy
        self.assertEqual(True, path.isfile(getenv("CAMINHO_COMPARTILHAMENTO") + "\\Web.config"))

        implantador_zip.limpar_pasta_compartilhada()

        self.assertEqual(False, path.isfile(getenv("CAMINHO_COMPARTILHAMENTO") + "\\Web.config"))

    def test_limpar_todo_diretorio_destino(self):
        environ["CAMINHO_COMPARTILHAMENTO"] = "\\\\INFOJENKINS1\\teste_unitario_caminho_compartilhamento"
        environ["CAMINHO_APAGAR_COMPARTILHAMENTO"] = "apagarConteudo.bat"
        environ["PASTAS_NAO_APAGAR"] = ""

        makedirs(path.join(environ["CAMINHO_COMPARTILHAMENTO"], "pasta_teste_apagar"))

        self.assertEqual(True, path.isdir(path.join(environ["CAMINHO_COMPARTILHAMENTO"], "pasta_teste_apagar")))

        implantador_zip = ImplantadorZIP()
        implantador_zip.limpar_pasta_compartilhada()

        self.assertEqual(False, path.isdir(path.join(environ["CAMINHO_COMPARTILHAMENTO"], "pasta_teste_apagar")))

    def test_limpar_diretorio_destino_exceto_pastas_determinadas(self):
        environ["CAMINHO_COMPARTILHAMENTO"] = "\\\\INFOJENKINS1\\teste_unitario_caminho_compartilhamento"
        environ["CAMINHO_APAGAR_COMPARTILHAMENTO"] = "apagarConteudo.bat"
        environ["PASTAS_NAO_APAGAR"] = "pasta_teste_nao_apagar"

        makedirs(path.join(environ["CAMINHO_COMPARTILHAMENTO"], "pasta_teste_nao_apagar"))
        makedirs(path.join(environ["CAMINHO_COMPARTILHAMENTO"], "pasta_teste_apagar"))

        self.assertEqual(True, path.isdir(path.join(environ["CAMINHO_COMPARTILHAMENTO"], "pasta_teste_nao_apagar")))
        self.assertEqual(True, path.isdir(path.join(environ["CAMINHO_COMPARTILHAMENTO"], "pasta_teste_apagar")))

        implantador_zip = ImplantadorZIP()
        implantador_zip.limpar_pasta_compartilhada()

        self.assertEqual(True, path.isdir(path.join(environ["CAMINHO_COMPARTILHAMENTO"], "pasta_teste_nao_apagar")))
        self.assertEqual(False, path.isdir(path.join(environ["CAMINHO_COMPARTILHAMENTO"], "pasta_teste_apagar")))

        environ["PASTAS_NAO_APAGAR"] = ""

        implantador_zip = ImplantadorZIP()
        implantador_zip.limpar_pasta_compartilhada()

        self.assertEqual(False, path.isdir(path.join(environ["CAMINHO_COMPARTILHAMENTO"], "pasta_teste_nao_apagar")))

    # def test_implantar_artefato_sem_arquivo_ambiente_via_FTP(self):
    #     environ["AMBIENTE"] = "QLT"
    #     environ["SERVIDOR_FTP"] = "172.17.36.96"
    #     environ["USUARIO_FTP"] = "testeftp"
    #     environ["SENHA_FTP"] = "TesteQA1234"
    #     environ["DIRETORIO_FTP"] = ""
    #
    #     implantador_zip = ImplantadorZIP()
    #     implantador_zip.implantar_artefato()
    #
    #     ftp = FTP(getenv("SERVIDOR_FTP"), getenv("USUARIO_FTP"), getenv("SENHA_FTP"), seguranca=False)
    #
    #     LinhaDeComando.executar("sleep 5")
    #
    #     ftp.baixar_arquivo("build.xml", ".\\sincronizado", getenv("DIRETORIO_FTP"))
    #
    #     self.assertEqual(True, path.isfile(".\\sincronizado\\build.xml"))
    #
    #     ftp.limpar_diretorio(getenv("DIRETORIO_FTP"))
    #
    #     ftp.desconectar()


if __name__ == '__main__':
    unittest.main()
