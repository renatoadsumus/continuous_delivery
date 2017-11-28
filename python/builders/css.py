# from os import getenv

from python.artefato import Artefato
from python.assistentes.linha_de_comando import LinhaDeComando
from python.assistentes.log import Log
from python.tipos_arquivos.arquivo import Arquivo


class CSS(Artefato):

    def __init__(self):
        pass
        # self.__ARQUIVO_CSS = getenv("ARQUIVO_CSS").split(".")[0]

    def fechar_artefato(self):
        arquivos_css = LinhaDeComando.executar_com_output('find . -name "*.css"').split(".css\n")
        arquivos_css.pop()

        for css in arquivos_css:
            comando_css = "csso %s.css --output %s_min.css" % (css, css)
            Log.imprime("INICIANDO O PROCESSO DE MINIFICACAO DO ARQUIVO " + css + ".css",
                        "INICIANDO O PROCESSO DE MINIFICACAO DO ARQUIVO " + css + ".css.")

            Log.imprime("EXECUTANDO O COMANDO: " + comando_css)
            LinhaDeComando.executar(comando_css)
            Log.imprime("COMANDO EXECUTADO COM SUCESSO.", "ARQUIVO " + css + ".css MINIFICADO COM SUCESSO.")

            arquivo_antigo = Arquivo(css + ".css")
            Log.imprime("EXCLUINDO O ARQUIVO ORIGINAL", "EXCLUINDO O ARQUIVO ORIGINAL.")
            arquivo_antigo.excluir()

            arquivo_novo = Arquivo(css + "_min.css")
            Log.imprime("RENOMEANDO O ARQUIVO MINIFICADO", "RENOMEADO O ARQUIVO MINIFICADO")
            arquivo_novo.renomear(css + ".css")

    def get_versao(self):
        pass

    def get_atributos(self):
        pass

    def executa_testes(self):
        pass

    def executa_scanner_sonar(self):
        pass
