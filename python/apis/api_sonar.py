import json
import requests
from traceback import format_exc
from time import sleep

from python.assistentes.log import Log


class Sonar(object):

    def __init__(self, nome_projeto_sonar):
        self.URL_SONAR_ISSUES = "http://infosonar:9000/api/issues/search?resolved=false&componentKeys="
        self.URL_SONAR_COBERTURA = "http://infosonar:9000/api/measures/component?metricKeys=coverage&componentKey="
        self.URL_SONAR_TESTES = "http://infosonar:9000/api/measures/component?metricKeys=tests&componentKey="
        self.URL_SONAR_QUALITY_GATE_STATUS = "http://infosonar:9000/api/qualitygates/project_status?projectKey="
        self.URL_SONAR_INFORMACOES_PROJETO = "http://infosonar:9000/api/components/show?component="
        self.URL_SONAR_ATIVIDADE_STATUS = "http://infosonar:9000/api/ce/component?componentKey="
        self.quantidade_issues = None
        self.percentual_cobertura = None
        self.quantidade_testes = None
        self.quality_gate_status = None
        self.nome_projeto_sonar = nome_projeto_sonar

    def obter_quantidade_issues(self):
        if self.quantidade_issues is None:
            url_consulta = self.URL_SONAR_ISSUES + self.nome_projeto_sonar
            response = requests.get(url_consulta)
            data = json.loads(response.text)
            try:
                total_issues = int(data['total'])
                if total_issues >= 0:
                    return total_issues
                else:
                    return 0
            except:
                Log.imprime("NAO FOI POSSIVEL OBTER A QUANTIDADE DE ISSUES."
                            "\nURL DE CONSULTA: " + url_consulta +
                            "\nERRRO: " + format_exc(),
                            "NAO FOI POSSIVEL OBTER A QUANTIDADE DE ISSUES", classe=Sonar)
                return 0
        else:
            Log.imprime("QUANTIDADE DE ISSUES OBTIDA: " + str(self.quantidade_issues))
            return self.quantidade_issues

    def obter_percentual_cobertura(self):
        if self.percentual_cobertura is None:
            url_consulta = self.URL_SONAR_COBERTURA + self.nome_projeto_sonar
            response = requests.get(url_consulta)
            data = json.loads(response.text)
            try:
                total_cobertura = float(data['component']['measures'][0]['value'])
                if total_cobertura >= 0.0:
                    return total_cobertura
                else:
                    return 0
            except:
                Log.imprime("NAO FOI POSSIVEL OBTER O PERCENTUAL DE COBERTURA."
                            "\nURL DE CONSULTA: " + url_consulta +
                            "\nERRRO: " + format_exc(),
                            "NAO FOI POSSIVEL OBTER O PERCENTUAL DE COBERTURA", classe=Sonar)
                return 0
        else:
            Log.imprime("PERCENTUAL DE COBERTURA OBTIDO: " + str(self.percentual_cobertura))
            return self.percentual_cobertura

    def obter_quantidade_testes(self):
        if self.quantidade_testes is None:
            url_consulta = self.URL_SONAR_TESTES + self.nome_projeto_sonar
            response = requests.get(url_consulta)
            data = json.loads(response.text)
            try:
                total_testes = int(data['component']['measures'][0]['value'])
                if total_testes >= 0:
                    return total_testes
                else:
                    return 0
            except:
                Log.imprime("NAO FOI POSSIVEL OBTER A QUANTIDADE DE TESTES."
                            "\nURL DE CONSULTA: " + url_consulta +
                            "\nERRRO: " + format_exc(),
                            "NAO FOI POSSIVEL OBTER A QUANTIDADE DE TESTES.", classe=Sonar)
                return 0
        else:
            Log.imprime("QUANTIDADE DE TESTES OBTIDA: " + str(self.quantidade_testes))
            return self.quantidade_testes

    def obter_status_quality_gates(self):
        url_consulta = self.URL_SONAR_QUALITY_GATE_STATUS + self.nome_projeto_sonar
        response = requests.get(url_consulta)

        data = json.loads(response.text)
        try:
            status_quality_gate = data['projectStatus']['status']
            if status_quality_gate == "ERROR":
                Log.imprime("O STATUS DO QUALITY GATE E DE ERROR", "O STATUS DO QUALITY GATE E DE ERROR")
                return False
            else:
                Log.imprime("O STATUS DO QUALITY GATE NAO E DE ERROR", "O STATUS DO QUALITY GATE NAO E DE ERROR")
                return True
        except:
            Log.imprime("NAO FOI POSSIVEL OBTER O STATUS DO QUALITY GATE.\nURL DE CONSULTA: " + url_consulta +
                        "\nERRO: " + format_exc(), "NAO FOI POSSIVEL OBTER O STATUS DO QUALITY GATE.", classe=Sonar)
            return False


    def verifica_se_existe_analise_em_progresso_ou_pendente(self):
        url_consulta = self.URL_SONAR_ATIVIDADE_STATUS + self.nome_projeto_sonar
        response = requests.get(url_consulta)

        data = json.loads(response.text)
        try:
            status_analise = data['current']['status']
            Log.imprime("VALOR DO STATUS DA ANALISE: " + status_analise)

            contador = 0

            while ((status_analise == "IN_PROGRESS") or (status_analise == "PENDING")) and contador < 5:
                Log.imprime("VALOR DO STATUS DA ANALISE: " + status_analise + ". VALOR DO CONTADOR: " + str(contador))
                contador = contador + 1
                sleep(90)
                response = requests.get(url_consulta)
                data = json.loads(response.text)
                status_analise = data['current']['status']
        except:
            Log.imprime("NAO FOI POSSIVEL VERIFICAR O STATUS DA ANALISE.")
            return False

        if (status_analise == "IN_PROGRESS") or (status_analise == "PENDING"):
            Log.imprime("O STATUS DA ANALISE CONTINUA COMO NAO TERMINADA APESAR DO TEMPO DE ESPERA")
            return False
        else:
            Log.imprime("O STATUS DA ANALISE INDICA QUE FOI ENCERRADA")
            return True
