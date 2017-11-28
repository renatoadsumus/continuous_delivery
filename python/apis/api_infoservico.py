# coding=utf-8

from datetime import datetime, timedelta
from os import path
from time import sleep
from traceback import format_exc

import requests

from python.assistentes.log import Log
from python.envio_email.envio_email import Email
from python.settings import getenv, DESTINATARIOS_EMAIL, PIPELINE_NAME, BUILD_URL, TRIGGER_USER, \
    API_INFO_SERVICO, PIPELINE_LABEL


class MudancaAutomatica:

    row_id = "00000"
    assigned_group_id = "00"

    def __init__(self):
        self.CCTI_CLASS = getenv("CCTI_CLASS")
        if not self.CCTI_CLASS:
            Log.imprime("CCTI_CLASS NAO FOI INFORMADO NAS VARIAVEIS DE AMBIENTE",
                        "OCORREU UM ERRO DURANTE A ABERTURA DE MUDANCA.",
                        classe=MudancaAutomatica, mensagem_de_erro=True)
            exit(1)

        self.CCTI_CATEGORY = getenv("CCTI_CATEGORY")
        self.CCTI_TYPE = getenv("CCTI_TYPE")
        self.CCTI_ITEM = getenv("CCTI_ITEM")

        if getenv("TIPO_MUDANCA") == "Normal":
            self.TIPO_MUDANCA = "Normal"
        else:
            self.TIPO_MUDANCA = "Padrão"

        self.ID_FILA_EQUIPE = getenv("ID_FILA_EQUIPE")
        if not self.ID_FILA_EQUIPE:
            Log.imprime("O ID DA FILA DA EQUIPE NAO FOI INFORMADO NAS VARIAVEIS DE AMBIENTE",
                        "OCORREU UM ERRO DURANTE A ABERTURA DE MUDANCA.",
                        classe=MudancaAutomatica, mensagem_de_erro=True)
            exit(1)

        self.destinatarios = "gestaodemudancas@infoglobo.com.br,devops@infoglobo.com.br" + \
                             ("" if DESTINATARIOS_EMAIL is None else "," + DESTINATARIOS_EMAIL)
        self.caminho_templates = path.dirname(__file__) + "/templates/"

    def criar_mudanca_automatica(self):
        headers = {'Content-Type': 'application/soap+xml;charset=iso-8859-1;action="urn:createChangeRequest'}
        numero_mudanca_info_servico = None
        descricao = "Deploy - " + PIPELINE_NAME + " - Link GoCd - " + BUILD_URL

        try:
            with open(self.caminho_templates + 'template_create_change_request.txt', 'r') as file:
                mensagem = file.read()
                mensagem = mensagem.replace('$CCTI_CLASS', self.CCTI_CLASS)
                mensagem = mensagem.replace('$CCTI_CATEGORY', self.CCTI_CATEGORY)
                mensagem = mensagem.replace('$CCTI_TYPE', self.CCTI_TYPE)
                mensagem = mensagem.replace('$CCTI_ITEM', self.CCTI_ITEM)
                mensagem = mensagem.replace('$REQUESTER_NAME', TRIGGER_USER)
                mensagem = mensagem.replace('$TICKET_DESCRIPTION', descricao)
                mensagem = mensagem.replace('$CHANGE_SUBTYPE', self.TIPO_MUDANCA)

            # Realizando um LOOP de retentativas - Identificamos em PRD uma intermitencia da API
            for i in range(5):
                response = requests.post(API_INFO_SERVICO, data=mensagem, headers=headers)
                sleep(2)
                numero_mudanca_info_servico = self.obter_numero_mudanca_criada(str(response.content))

                if numero_mudanca_info_servico:
                    sleep(2)
                    row_id_ = self.obter_row_id_da_mudanca(numero_mudanca_info_servico)
                    sleep(5)
                    self.atualizar_dados_na_mudanca(numero_mudanca_info_servico, row_id_)
                    Log.imprime("NUMERO DE MUDANCA OBTIDO " + numero_mudanca_info_servico)
                    break
            return numero_mudanca_info_servico
        except:
            Log.imprime("FALHA\n" + format_exc(), "FALHA -- NAO FOI CRIADO NUMERO DE MUDANCA",
                        classe=MudancaAutomatica, mensagem_de_erro=True)

    def obter_row_id_da_mudanca(self, numero_mudanca):
        headers = {'Content-Type': 'application/soap/xml;charset=iso-8859-1;action="urn:getChangeRequest'}

        try:
            with open(self.caminho_templates + 'template_get_change_request.txt', 'r') as file:
                body = file.read()
                body = body.replace('$TICKET_IDENTIFIER', numero_mudanca)

            # Realizando um LOOP de retentativas - Identificamos em PRD uma intermitencia da API
            for i in range(5):
                response = requests.post(API_INFO_SERVICO, data=body, headers=headers)

                if str(response.content).__contains__("<ax212:statusCode>000</ax212:statusCode>"):
                    self.row_id = str(response.content).split("ax210:row_id")[1].replace("<", ""). \
                        replace(">", "").replace("/", "")
                    self.assigned_group_id = str(response.content).split("ax210:assigned_group_id>")[1][:2]
                    break
            Log.imprime("SUCESSO -- ROW ID OBTIDO: " + self.row_id)
            return self.row_id
        except:
            Log.imprime("FALHA\n" + format_exc(), "FALHA -- ROW ID NAO OBTIDO", classe=MudancaAutomatica)

    def atualizar_dados_na_mudanca(self, numero_mudanca, row_id_):
        headers = {'Content-Type': 'application/soap/xml;charset=iso-8859-1;action="urn:updateChangeRequest'}

        data_hora_inicio = (datetime.now() + timedelta(hours=1)).strftime("%m/%d/20%y %H:%M:00")
        data_hora_fim = (datetime.now() + timedelta(hours=2)).strftime("%m/%d/20%y %H:%M:00")

        try:
            with open(self.caminho_templates + 'template_update_change_request.txt', 'r') as file:
                mensagem = file.read()
                mensagem = mensagem.replace('$TICKET_IDENTIFIER', numero_mudanca)
                mensagem = mensagem.replace('$ROW_ID', row_id_)
                mensagem = mensagem.replace('$EQUIPE_ID', self.ID_FILA_EQUIPE)
                mensagem = mensagem.replace('$EXECUTOR_MUDANCA', TRIGGER_USER)
                mensagem = mensagem.replace('$START_DATE', data_hora_inicio)
                mensagem = mensagem.replace('$END_DATE', data_hora_fim)
                mensagem = mensagem.replace('$PLAN_IMPLEMENTATION', "JOB GoCd - " + BUILD_URL)

            response = requests.post(API_INFO_SERVICO, data=mensagem, headers=headers)
            Log.imprime("SUCESSO -- DADOS DA MUDANCA ATUALIZADOS")

            if str(response.content).__contains__("<ax212:statusCode>000</ax212:statusCode>"):
                Log.imprime("SUCESSO - CHAMADO ATUALIZADO: " + str(numero_mudanca), "SUCESSO - CHAMADO ATUALIZADO: " +
                            str(numero_mudanca))
            else:
                Log.imprime("OCORREU UM ERRO DURANTE A ATUALIZACAO DO CHAMADO: " + str(numero_mudanca),
                            "FALHA - CHAMADO NAO ATUALIZADO: " + str(numero_mudanca), classe=MudancaAutomatica)
                self.__enviar_email_falha_ao_atualizar_mudanca(numero_mudanca)
        except:
            Log.imprime("FALHA\n" + format_exc(), "FALHA -- ERRO NA ATUALIZACAO DE DADOS", classe=MudancaAutomatica)

    def obter_numero_mudanca_criada(self, nome_arquivo_retorno):
        numero_mudanca = None
        criado_com_sucesso = False

        # Verificando se a mudanca foi criada
        if nome_arquivo_retorno.__contains__("<ax212:statusCode>000</ax212:statusCode>"):
            criado_com_sucesso = True

        if nome_arquivo_retorno.__contains__("![CDATA[200-"):
            numero_mudanca = "200-" + str(nome_arquivo_retorno).split("200-")[1].split("]")[0]

        if numero_mudanca is None or not criado_com_sucesso:
            Log.imprime("FALHA AO CRIAR CHAMADO NO INFOSERVICOS\n" + str(nome_arquivo_retorno),
                        "OCORREU UM ERRO DURANTE A ABERTURA DE MUDANCA", classe=MudancaAutomatica)
            self.__enviar_email_falha_ao_criar_mudanca()
            return numero_mudanca
        else:
            Log.imprime("SUCESSO - CHAMADO CRIADO: " + str(numero_mudanca),
                        "SUCESSO - CHAMADO CRIADO: " + str(numero_mudanca))
            self.__enviar_email_sucesso_criar_mudanca(numero_mudanca)
            return numero_mudanca

    def __enviar_email_sucesso_criar_mudanca(self, numero_mudanca):
        email = Email()
        assunto = "A solicitacao CHG#" + numero_mudanca + " - FOI CRIADA COM SUCESSO."
        with open(email.CAMINHO_DIRETORIO_TEMPLATES + 'email_sucesso_mudanca.txt') as file:
            mensagem = file.read()
            mensagem = mensagem.replace('$CCTI_CLASS', self.CCTI_CLASS)
            mensagem = mensagem.replace('$NUMERO_MUDANCA', numero_mudanca)
            mensagem = mensagem.replace('$NOME_PROJETO', PIPELINE_NAME)
            mensagem = mensagem.replace('$GO_PIPELINE_LABEL', PIPELINE_LABEL)
            mensagem = mensagem.replace('$CCTI_CATEGORY', self.CCTI_CATEGORY)
            mensagem = mensagem.replace('$PIPELINE_GO', BUILD_URL)
        email.enviar_email(assunto, self.destinatarios, mensagem)

    def __enviar_email_falha_ao_criar_mudanca(self):
        assunto = "ERRO na criacao de mudanca automatica - Favor criar manualmente"
        mensagem = "Houve um problema durante a criacao da mudanca para o CCTI: \n" \
                   + self.CCTI_CLASS + " - " + self.CCTI_CATEGORY + \
                   "\nPor favor, crie a solicitacao de mudancas manualmente." \
                   "\nAt., Tecnologia - INFOGLOBO"
        email = Email()
        email.enviar_email(assunto, self.destinatarios, mensagem)

    def __enviar_email_falha_ao_atualizar_mudanca(self, numero_mudanca):
        assunto = "ERRO ao atualizar dados da mudanca - Favor preencher manualmente"
        mensagem = "Houve um problema durante a atualização dos dados da mudanca. \n" \
                   "Link da mudanca: https://csm3.serviceaide.com/#WORKSPACES-" \
                   "SERVICE-DESK-Global-Search/searchWorkspaceKey=" + numero_mudanca + \
                   "\nPor favor, preencha os dados da solicitacao de mudancas manualmente." \
                   "\nAt., Tecnologia - INFOGLOBO"
        email = Email()
        email.enviar_email(assunto, self.destinatarios, mensagem)
