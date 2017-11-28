# # coding=utf-8
#
# from python.assistentes.log import Log
# from python.envio_email.envio_email import Email
#
# __author__ = 'ssouza'
#
#
# class Verificacoes(object):
#     def __init__(self):
#         from python.fabrica_objetos import FabricaObjetos
#         self.builder = FabricaObjetos.obter_builder()
#         # self.api_nexus = FabricaObjetos.obter_api_nexus()
#
#     def is_versionamento_semantico(self):
#         versao = self.builder.get_versao()
#         split = versao.split('.')
#         return len(split) == 3
#
#     def versao_ja_existe_no_nexus(self):
#         resposta = self.api_nexus.get_resposta_http_builder()
#         return resposta != 404
#
#
# if __name__ == "__main__":
#     email = Email()
#     verificacoes = Verificacoes()
#
#     if verificacoes.versao_ja_existe_no_nexus():
#         email.enviar_email_falha("validador_biblioteca_existente.html")
#         mensagem = "Verifique a versao da biblioteca.\nEssa versao ja existe!!!"
#         Log.imprime(mensagem, mensagem, script="verificacoes_pre_deploy.py", mensagem_de_erro=True)
#         exit(1)
#     elif not verificacoes.is_versionamento_semantico():
#         email.enviar_email_falha("validador_versionamento_semantico.html")
#         mensagem = "Verifique a versao da biblioteca.\nEla nao possui os 3 nameros " \
#                    "referentes ao versionamento semantico!!\nEx: 1.0.1"
#         Log.imprime(mensagem, mensagem, script="verificacoes_pre_deploy.py", mensagem_de_erro=True)
#         exit(1)
