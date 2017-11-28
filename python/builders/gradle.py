"""Modulo que engloba a classe do builder Gradle"""

from python.artefato import Artefato
from python.assistentes.linha_de_comando import LinhaDeComando
from python.assistentes.log import Log


class Gradle(Artefato):
    """Classe que representa o builder da tecnologia Gradle e suas acoes"""

    def get_versao(self):
        # Metodo nao implementado para obter versao
        pass

    def get_atributos(self):
        # Metodo nao implementado para obter valor de atributos
        pass

    def executa_testes(self):
        # Metodo que roda os testes do Gradle
        Log.imprime("INICIANDO TESTES DO GRADLE", "INICIANDO TESTES DO GRADLE")
        LinhaDeComando.executar("gradle testClasses")
        Log.imprime("TESTES ENCERRADOS COM SUCESSO", "TESTES ENCERRADOS COM SUCESSO")

    def fechar_artefato(self):
        # Metodo que fecha um novo artefato construido com o Gradle
        Log.imprime("INICIANDO PROCESSO DE FECHAMENTO DO ARTEFATO", "INICIANDO PROCESSO DE FECHAMENTO DO ARTEFATO")
        LinhaDeComando.executar("gradle build")
        Log.imprime("ARTEFATO GERADO COM SUCESSO", "ARTEFATO GERADO COM SUCESSO")

    def executa_scanner_sonar(self):
        pass
