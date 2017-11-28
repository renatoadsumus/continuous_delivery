# """Modulo que engloba a classe ApiNexus"""
#
# import requests
#
# from python.assistentes.log import Log
# from python.settings import URL_NEXUS
#
# __author__ = 'ssouza'
#
#
# class ApiNexus(object):
#     """Classe que representa a API do Nexus e suas principais acoes"""
#     def __init__(self):
#         #Inicializa o objeto da ApiNexus
#         from python.fabrica_objetos import FabricaObjetos
#         self.builder = FabricaObjetos.obter_builder()
#
#     def get_resposta_http_builder(self):
#         #Faz uma requisicao e retorna uma resposta a esta requisicao
#         tipo_artefato, versao, artifact_id, group_id, repository = self.builder.get_atributos()
#         url = URL_NEXUS + group_id + '&a=' + artifact_id + '&v=' + versao + '&r=' + repository + '&e=' + tipo_artefato
#         #Montagem da URL da requisicao
#
#         Log.imprime(url, url)
#         codigo_de_retorno = requests.get(url).status_code
#         #Faz a requisicao e retorna a resposta
#         return codigo_de_retorno
