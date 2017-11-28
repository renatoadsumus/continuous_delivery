# coding=utf-8

from python.apis.api_infoservico import MudancaAutomatica
from python.assistentes.log import Log
from python.mongo.informacoes_artefatos_gocd import InformacoesArtefatos
from python.settings import NOME_PROJETO, NOME_EQUIPE, PIPELINE_LABEL


class CriarMudancaAutomatica(object):
    def __init__(self, nome_equipe, nome_projeto):
        if not nome_projeto:
            Log.imprime("NOME DO PROJETO NAO INFORMADO.", "ERRO DURANTE ATUALIZACAO DE INFORMACOES EM PRD.",
                        script="criar_mudanca_automatica.py", mensagem_de_erro=True)
            exit(1)

        if not nome_equipe:
            Log.imprime("NOME DA EQUIPE NAO INFORMADO.", "ERRO DURANTE ATUALIZACAO DE INFORMACOES EM PRD.",
                        script="criar_mudanca_automatica.py", mensagem_de_erro=True)
            exit(1)

        self.nome_equipe = nome_equipe
        self.nome_projeto = nome_projeto

    def criar_mudanca_automatica(self):
        informacoes = InformacoesArtefatos(self.nome_equipe, self.nome_projeto)
        revision_deploy_prd = PIPELINE_LABEL.split("-")[-1]

        if (revision_deploy_prd != informacoes.obter_revision_deploy_prd()) \
                and (informacoes.obter_status_deploy_prd() == "F"):
            mudanca_automatica = MudancaAutomatica()
            numero_mudanca = mudanca_automatica.criar_mudanca_automatica()
            if numero_mudanca:
                informacoes.alterar(numero_mudanca=numero_mudanca, status_deploy_prd="I")
        else:
            numero_mudanca = informacoes.obter_numero_mudanca()
            Log.imprime("MUDANCA PARA ESSE DEPLOY JA FOI CRIADA ANTERIORMENTE" "\nNUMERO MUDANCA: " + numero_mudanca +
                        "\nSTATUS DEPLOY: " + informacoes.obter_status_deploy_prd() +
                        "\nREVISION GO: " + revision_deploy_prd +
                        "\nREVISION MONGO PRD: " + str(informacoes.obter_revision_deploy_prd()),
                        "MUDANCA PARA ESSE DEPLOY JA FOI CRIADA ANTERIORMENTE" "\nNUMERO MUDANCA: " + numero_mudanca,
                        classe=CriarMudancaAutomatica, script="criar_mudanca_automatica.py")

        Log.imprime("INFORMACOES ALTERADAS NO MONGO COM SUCESSO."
                    "\nREVISION_DEPLOY_PRD: " + revision_deploy_prd,
                    classe=CriarMudancaAutomatica, script="criar_mudanca_automatica.py")
        return numero_mudanca

if __name__ == "__main__":
    criar_mudanca = CriarMudancaAutomatica(NOME_EQUIPE, NOME_PROJETO)
    criar_mudanca.criar_mudanca_automatica()
