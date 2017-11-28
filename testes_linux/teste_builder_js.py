import unittest
from os import environ

from python.assistentes.log import Log
from python.builders.js import JS
from python.tipos_arquivos.arquivo import Arquivo, path


class TesteJS(unittest.TestCase):

    def setUp(self):
        environ["CAMINHO_CLOSURE_COMPILER"] = "/opt/closure-compiler/latest/closure-compiler.jar"
        arquivos_js = {"arquivo.js", "arquivo2.js", "arquivo3.js"}
        for js in arquivos_js:
            Log.imprime("CRIANDO ARQUIVO JS DE TESTE " + js, "CRIANDO ARQUIVO JS DE TESTE "
                        + js)
            with open(js, "w")as arq:
                arq.write("function hello(longName){alert('Hello, ' + longName);}hello('New User');")
                arq.close()

    def tearDown(self):
        arquivos_js = {"arquivo.js", "arquivo2.js", "arquivo3.js"}
        for js in arquivos_js:
            Log.imprime("EXCLUINDO O ARQUIVO JS DE TESTE " + js, "EXCLUINDO O ARQUIVO JS DE TESTE "
                        + js)
            arq = Arquivo(js)
            arq.excluir()

    def teste_fechar_artefato(self):
        arquivos_js = {"arquivo.js", "arquivo2.js", "arquivo3.js"}
        builder_js = JS()

        for js in arquivos_js:
            self.assertTrue(path.isfile(js))

        builder_js.fechar_artefato()

        for js in arquivos_js:
            self.assertTrue(path.isfile(js))
