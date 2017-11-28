import unittest
from os import environ, path

from python.scripts.manipulador_load_balance_tibco_https import ManipuladorLoadBalanceTibcoHTTPS


class TestesManipuladorLoadBalanceTibcoHTTPS(unittest.TestCase):
    def setUp(self):
        self.PORTA_SERVICO = "7113"
        self.PASTA_CONF_APACHE = path.abspath(path.dirname(__file__))
        self.SERVIDORES_APACHE = "pasta_teste"
        self.SERVIDORES_LOAD_BALANCE = "lbtibco_gp,balance"
        self.NOVO_BACKEND = "infotbc2"

        environ["PORTA_SERVICO"] = self.PORTA_SERVICO
        environ["PASTA_CONF_APACHE"] = self.PASTA_CONF_APACHE
        environ["SERVIDORES_APACHE"] = self.SERVIDORES_APACHE
        environ["SERVIDORES_LOAD_BALANCE"] = self.SERVIDORES_LOAD_BALANCE

        self.lbhttps = ManipuladorLoadBalanceTibcoHTTPS()

    def __informacoes_do_arquivo_para_antes_do_teste(self, arquivo_caminho):
        with open(arquivo_caminho, "r") as arq:
            content = arq.read()
            arquivo_qtd_linhas = content.count("\n")
            arquivo_count_lb1 = content.count("{}:{}".format(self.SERVIDORES_LOAD_BALANCE.split(",")[0],
                                                             self.PORTA_SERVICO))
            arquivo_count_lb2 = content.count("{}:{}".format(self.SERVIDORES_LOAD_BALANCE.split(",")[1],
                                                             self.PORTA_SERVICO))
        return arquivo_qtd_linhas, arquivo_count_lb1, arquivo_count_lb2

    def __informacoes_do_arquivo_para_depois_do_teste(self, arquivo_caminho, novo_servidor):
        with open(arquivo_caminho, "r") as arq:
            content = arq.read()
            arquivo_qtd_linhas = content.count("\n")
            arquivo_count_lb = content.count("{}:{}".format(novo_servidor, self.PORTA_SERVICO))
        return arquivo_qtd_linhas, arquivo_count_lb

    def teste_editar_conf_apache(self):
        
        arquivo1_caminho = path.join(self.PASTA_CONF_APACHE, self.SERVIDORES_APACHE, "api.conf")
        arquivo2_caminho = path.join(self.PASTA_CONF_APACHE, self.SERVIDORES_APACHE, "apissl.conf")

        arquivo1_qtd_linhas, arquivo1_count_lb1, arquivo1_count_lb2 = \
            self.__informacoes_do_arquivo_para_antes_do_teste(arquivo1_caminho)

        arquivo2_qtd_linhas, arquivo2_count_lb1, arquivo2_count_lb2 = \
            self.__informacoes_do_arquivo_para_antes_do_teste(arquivo2_caminho)

        self.lbhttps.editar_conf_apache(self.NOVO_BACKEND)

        arquivo1_qtd_linhas_obtido, arquivo1_count_novo_lb_obtido = \
            self.__informacoes_do_arquivo_para_depois_do_teste(arquivo1_caminho, self.NOVO_BACKEND)

        arquivo2_qtd_linhas_obtido, arquivo2_count_novo_lb_obtido = \
            self.__informacoes_do_arquivo_para_depois_do_teste(arquivo2_caminho, self.NOVO_BACKEND)

        self.assertEqual(arquivo1_qtd_linhas, arquivo1_qtd_linhas_obtido)
        self.assertEqual(arquivo2_qtd_linhas, arquivo2_qtd_linhas_obtido)
        self.assertEqual(arquivo1_count_lb1 + arquivo1_count_lb2, arquivo1_count_novo_lb_obtido)
        self.assertEqual(arquivo2_count_lb1 + arquivo2_count_lb2, arquivo2_count_novo_lb_obtido)

if __name__ == '__main__':
    unittest.main()
