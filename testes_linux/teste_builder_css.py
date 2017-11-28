import unittest

from python.assistentes.log import Log
from python.builders.css import CSS
from python.tipos_arquivos.arquivo import Arquivo, path


class TesteCSS(unittest.TestCase):

    def setUp(self):
        arquivos_css = {"arquivo.css", "arquivo2.css", "arquivo3.css"}
        for css in arquivos_css:
            Log.imprime("CRIANDO ARQUIVO CSS DE TESTE " + css, "CRIANDO ARQUIVO CSS DE TESTE "
                        + css)
            with open(css, "w")as arq:
                arq.write("body{background-color: red;}")
                arq.close()

    def tearDown(self):
        arquivos_css = {"arquivo.css", "arquivo2.css", "arquivo3.css"}
        for css in arquivos_css:
            Log.imprime("EXCLUINDO O ARQUIVO CSS DE TESTE " + css, "EXCLUINDO O ARQUIVO CSS DE TESTE "
                        + css)
            arq = Arquivo(css)
            arq.excluir()

    def teste_fechar_artefato(self):
        arquivos_css = {"arquivo.css", "arquivo2.css", "arquivo3.css"}
        builder_css = CSS()

        for css in arquivos_css:
            self.assertTrue(path.isfile(css))

        builder_css.fechar_artefato()

        for css in arquivos_css:
            self.assertTrue(path.isfile(css))

