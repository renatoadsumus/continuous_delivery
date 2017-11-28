from os import getenv

from python.artefato import Artefato
from python.assistentes.linha_de_comando import LinhaDeComando
from python.assistentes.log import Log
from python.tipos_arquivos.arquivo import Arquivo


class JS(Artefato):

    def __init__(self):
        # CAMINHO LINUX (COMENTAR PARA TESTE LOCAL)
        self.__CAMINHO_CLOSURE_COMPILER = getenv("CAMINHO_CLOSURE_COMPILER")
        # CAMINHO WINDOWS (DESCOMENTAR PARA TESTE LOCAL)
        # self.__CAMINHO_CLOSURE_COMPILER = "C:\\closure_compiler_v20170423\\closure-compiler.jar"

    def fechar_artefato(self):
        arquivos_js = LinhaDeComando.executar_com_output('find . -name "*.js"').split(".js\n")
        arquivos_js.pop()

        for js in arquivos_js:
            comando_js = "java -jar %s --js %s.js --js_output_file %s_min.js" % (self.__CAMINHO_CLOSURE_COMPILER,
                                                                       js, js)
            Log.imprime("INICIANDO O PROCESSO DE MINIFICACAO DO ARQUIVO " + js + ".js",
                        "INICIANDO O PROCESSO DE MINIFICACAO DO ARQUIVO " + js + ".js.")

            Log.imprime("EXECUTANDO O COMANDO: " + comando_js)
            LinhaDeComando.executar(comando_js)
            Log.imprime("COMANDO EXECUTADO COM SUCESSO.", "ARQUIVO " + js + ".js MINIFICADO COM SUCESSO.")

            arquivo_antigo = Arquivo(js + ".js")
            Log.imprime("EXCLUINDO O ARQUIVO ORIGINAL", "EXCLUINDO O ARQUIVO ORIGINAL.")
            arquivo_antigo.excluir()

            arquivo_novo = Arquivo(js + "_min.js")
            Log.imprime("RENOMEANDO O ARQUIVO MINIFICADO", "RENOMEADO O ARQUIVO MINIFICADO")
            arquivo_novo.renomear(js + ".js")

    def get_versao(self):
        pass

    def get_atributos(self):
        pass

    def executa_testes(self):
        pass

    def executa_scanner_sonar(self):
        pass
