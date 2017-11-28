import os.path
from traceback import format_exc

from python.apis.api_sonar import Sonar
from python.assistentes.log import Log
from python.envio_email.envio_email import Email
from python.mongo.informacoes_artefatos_gocd import InformacoesArtefatos
from python.settings import getenv, NOME_PROJETO, NOME_EQUIPE, DESTINATARIOS_EMAIL, PIPELINE_NAME, WORKING_DIRECTORY
from python.tipos_arquivos.arquivo_xml import ArquivoXML

try:
    string_assunto = "INFORMACOES SOBRE QUALIDADE DO PRODUTO " + NOME_PROJETO
    string_mensagem = ""
    metodo_armazenamento = getenv("METODO_ARMAZENAMENTO_INFO_TESTES")

    if metodo_armazenamento == "SONAR":

        sonar = Sonar(getenv("NOME_PROJETO_SONAR"))

        informacoes = InformacoesArtefatos(NOME_EQUIPE, NOME_PROJETO)

        cobertura_testes_unitarios_anterior = float(informacoes.obter_cobertura_testes_unitarios())
        if cobertura_testes_unitarios_anterior == "":
            cobertura_testes_unitarios_anterior = 0

        quantidade_issues_total_aplicacao_anterior = int(informacoes.obter_quantidade_issues_total_aplicacao())
        if quantidade_issues_total_aplicacao_anterior == "":
            quantidade_issues_total_aplicacao_anterior = 0

        quantidade_testes_unitarios_anterior = int(informacoes.obter_quantidade_testes_unitarios())
        if quantidade_testes_unitarios_anterior == "":
            quantidade_testes_unitarios_anterior = 0

        cobertura_testes_unitarios_atual = float(sonar.obter_percentual_cobertura())
        quantidade_issues_total_aplicacao_atual = int(sonar.obter_quantidade_issues())
        quantidade_testes_unitarios_atual = int(sonar.obter_quantidade_testes())

        if cobertura_testes_unitarios_anterior > cobertura_testes_unitarios_atual:
            string_mensagem += "A cobertura de testes unitarios no projeto diminuiu: de " + \
                               str(cobertura_testes_unitarios_anterior) + \
                               " para " + str(cobertura_testes_unitarios_atual) + ". "

        if quantidade_testes_unitarios_anterior > quantidade_testes_unitarios_atual:
            string_mensagem += "A quantidade de testes unitarios no projeto diminuiu: de " + \
                               str(quantidade_testes_unitarios_anterior) + " para " + \
                               str(quantidade_testes_unitarios_atual) + ". "

        if quantidade_issues_total_aplicacao_anterior < quantidade_issues_total_aplicacao_atual:
            string_mensagem += "A quantidade de issues total do projeto aumentou: de " + \
                               str(quantidade_issues_total_aplicacao_anterior) + " para " + \
                               str(quantidade_issues_total_aplicacao_atual) + ". "

        informacoes.alterar(cobertura_testes_unitarios=str(cobertura_testes_unitarios_atual),
                            quantidade_issues_total=str(quantidade_issues_total_aplicacao_atual),
                            quantidade_testes_unitarios=str(quantidade_testes_unitarios_atual))

        if string_mensagem:
            email = Email()

            email.enviar_email(string_assunto, DESTINATARIOS_EMAIL, string_mensagem)

    # elif metodo_armazenamento == "RELATORIO_MAVEN":
    #
    #     if PIPELINE_NAME.split("_")[-1] == "integracao":
    #
    #         try:
    #             relatorio_smoke_tests = ArquivoXML("relatorio-smoke-tests.xml")
    #
    #         except:
    #             Log.imprime("FALHA\n" + format_exc(), "NAO FOI POSSIVEL ACESSAR O RELATORIO DE SMOKE TESTS",
    #                         script="monitorar_atualizar_quantidade_testes.py", mensagem_de_erro=True)
    #             exit(1)
    #
    #         relatorio_smoke_tests = ArquivoXML("relatorio-smoke-tests.xml")
    #
    #         quantidade_smoke_tests_atual = int(relatorio_smoke_tests.quantidade_elementos("testcase"))
    #
    #         informacoes = InformacoesArtefatos(NOME_EQUIPE, NOME_PROJETO)
    #
    #         quantidade_smoke_tests_anterior = int(informacoes.obter_quantidade_smoke_tests())
    #
    #         if quantidade_smoke_tests_anterior > quantidade_smoke_tests_atual:
    #             string_mensagem += "A quantidade de smoke tests Maven do projeto diminuiu: de " + \
    #                                str(quantidade_smoke_tests_anterior) + " para " + \
    #                                str(quantidade_smoke_tests_atual) + ". "
    #
    #         informacoes.alterar(quantidade_smoke_tests=str(quantidade_smoke_tests_atual))
    #
    #         if string_mensagem:
    #             email = Email()
    #
    #             email.enviar_email(string_assunto, DESTINATARIOS_EMAIL, string_mensagem)
    #
    #     elif PIPELINE_NAME.split("_")[-1] == "staging":
    #
    #         try:
    #             relatorio_testes_regressivos = ArquivoXML("relatorio-testes-regressivos.xml")
    #
    #             quantidade_testes_regressivos_atual = int(relatorio_testes_regressivos.quantidade_elementos("testcase"))
    #
    #             informacoes = InformacoesArtefatos(NOME_EQUIPE, NOME_PROJETO)
    #
    #             quantidade_testes_regressivos_anterior = int(informacoes.obter_quantidade_testes_regressivos())
    #
    #             if quantidade_testes_regressivos_anterior > quantidade_testes_regressivos_atual:
    #                 string_mensagem += "A quantidade de testes regressivos Maven do projeto diminuiu: de " + \
    #                                    str(quantidade_testes_regressivos_anterior) + " para " + \
    #                                    str(quantidade_testes_regressivos_atual) + ". "
    #
    #             informacoes.alterar(quantidade_testes_regressivos=str(quantidade_testes_regressivos_atual))
    #
    #             if string_mensagem:
    #                 email = Email()
    #
    #                 email.enviar_email(string_assunto, DESTINATARIOS_EMAIL, string_mensagem)
    #         except:
    #             Log.imprime("FALHA\n" + format_exc(), "NAO FOI POSSIVEL ACESSAR O RELATORIO DE TESTES REGRESSIVOS",
    #                         script="monitorar_atualizar_quantidade_testes.py", mensagem_de_erro=True)
    #             exit(1)
    #
    elif metodo_armazenamento == "RELATORIO_SOAPUI/MAVEN":

        if PIPELINE_NAME.split("_")[-1] == "integracao":

            if getenv("QUANTIDADE_RELATORIOS"):
                quantidade_smoke_tests_atual = 0
                i = 1
                while i <= int(getenv("QUANTIDADE_RELATORIOS")):
                    try:
                        relatorio_smoke_tests = ArquivoXML(os.path.join(WORKING_DIRECTORY,"relatorio-smoke-tests-" + str(i) + ".xml"))

                    except:
                        Log.imprime("FALHA\n" + format_exc(), "NAO FOI POSSIVEL ACESSAR O RELATORIO DE SMOKE TESTS",
                                script="monitorar_atualizar_quantidade_testes.py", mensagem_de_erro=True)
                        exit(1)

                    quantidade_smoke_tests_atual += int(relatorio_smoke_tests.obter_valor_atributo(".", "tests"))

                    i += 1

                else:
                    try:
                        relatorio_smoke_tests = ArquivoXML(os.path.join(WORKING_DIRECTORY,"relatorio-smoke-tests.xml"))

                    except:
                        Log.imprime("FALHA\n" + format_exc(), "NAO FOI POSSIVEL ACESSAR O RELATORIO DE SMOKE TESTS",
                                script="monitorar_atualizar_quantidade_testes.py", mensagem_de_erro=True)
                        exit(1)

                    quantidade_smoke_tests_atual = int(relatorio_smoke_tests.obter_valor_atributo(".", "tests"))

                informacoes = InformacoesArtefatos(NOME_EQUIPE, NOME_PROJETO)

                quantidade_smoke_tests_anterior = int(informacoes.obter_quantidade_smoke_tests())

                if quantidade_smoke_tests_anterior > quantidade_smoke_tests_atual:
                    string_mensagem += "A quantidade de smoke tests do projeto diminuiu: de " + \
                                       str(quantidade_smoke_tests_anterior) + " para " + \
                                       str(quantidade_smoke_tests_atual) + ". "

                informacoes.alterar(quantidade_smoke_tests=str(quantidade_smoke_tests_atual))

                if string_mensagem:
                    email = Email()

                    email.enviar_email(string_assunto, DESTINATARIOS_EMAIL, string_mensagem)

        elif PIPELINE_NAME.split("_")[-1] == "staging":

            if getenv("QUANTIDADE_RELATORIOS"):
                quantidade_testes_regressivos_atual = 0
                i = 1
                while i <= getenv("QUANTIDADE_RELATORIOS"):
                    try:
                        relatorio_testes_regressivos = ArquivoXML(os.path.join(WORKING_DIRECTORY,"relatorio-testes-regressivos-" + str(i) + ".xml"))

                    except:
                        Log.imprime("FALHA\n" + format_exc(), "NAO FOI POSSIVEL ACESSAR O RELATORIO DE TESTES REGRESSIVOS",
                                    script="monitorar_atualizar_quantidade_testes.py", mensagem_de_erro=True)
                        exit(1)

                    quantidade_testes_regressivos_atual += int(relatorio_testes_regressivos.obter_valor_atributo(".", "tests"))

                    i += 1

            else:
                try:
                    relatorio_testes_regressivos = ArquivoXML(os.path.join(WORKING_DIRECTORY,"relatorio-testes-regressivos.xml"))

                except:
                    Log.imprime("FALHA\n" + format_exc(), "NAO FOI POSSIVEL ACESSAR O RELATORIO DE TESTES REGRESSIVOS",
                                script="monitorar_atualizar_quantidade_testes.py", mensagem_de_erro=True)
                    exit(1)

                quantidade_testes_regressivos_atual = int(relatorio_testes_regressivos.obter_valor_atributo(".", "tests"))

            informacoes = InformacoesArtefatos(NOME_EQUIPE, NOME_PROJETO)

            quantidade_testes_regressivos_anterior = int(informacoes.obter_quantidade_testes_regressivos())

            if quantidade_testes_regressivos_anterior > quantidade_testes_regressivos_atual:
                string_mensagem += "A quantidade de testes regressivos do projeto diminuiu: de " + \
                                    str(quantidade_testes_regressivos_anterior) + " para " + \
                                    str(quantidade_testes_regressivos_atual) + ". "

            informacoes.alterar(quantidade_testes_regressivos=quantidade_testes_regressivos_atual)

            if string_mensagem:
                email = Email()

                email.enviar_email(string_assunto, DESTINATARIOS_EMAIL, string_mensagem)
except:
    Log.imprime("Houve um erro durante a execucao, pulando monitoramento")

