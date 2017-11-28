from datetime import datetime
from xml.dom import minidom

import requests

from python.settings import URL_GO_CD, USUARIO_GO_API, SENHA_GO_API


class Job:
    def __init__(self, id_job):
        self.id = id_job
        self.duracao = ApiGoCd.obter_duracao_execucao_job(self.id)


class Stage:
    def __init__(self, id_stage):
        self.id = id_stage
        self.jobs = []
        self.duracao = ApiGoCd.obter_duracao_execucao_stage(self.id)
        lista_jobs = ApiGoCd.obter_ids_jobs_do_stage(self.id)
        for id_job in list(lista_jobs):
            self.jobs.append(Job(id_job))


class Pipeline:
    def __init__(self, nome):
        self.nome = nome
        self.id = ApiGoCd.obter_n_ids_pipeline(self.nome)
        self.duracao = ApiGoCd.obter_duracao_execucao_pipeline_por_id(self.id)
        self.stages = []
        lista_stages = ApiGoCd.obter_ids_stages_do_pipeline(self.id)
        for id_stage in list(lista_stages):
            self.stages.append(Stage(id_stage))


class ApiGoCd:
    url_api = URL_GO_CD + "api/"
    cabecalho_get = {"Accept": "application/vnd.go.cd.v1+json"}
    cabecalho_post = {"Confirm": "true"}
    auth = (USUARIO_GO_API, SENHA_GO_API)

    @classmethod
    def obter_nome_todos_pipelines(cls):
        url = cls.url_api + "pipelines.xml"
        resposta = requests.get(url, auth=cls.auth)
        if resposta.status_code == 200:
            xml = minidom.parseString(resposta.content.decode())
            pipelines = xml.getElementsByTagName("pipeline")
            nomes = []
            for pipeline in pipelines:
                nomes.append(str(pipeline.getAttribute("href")).
                             replace(cls.url_api + "pipelines/", "").replace("/stages.xml", ""))
            return nomes
        else:
            return None

    @classmethod
    def obter_quantidade_pipelines(cls):
        url = cls.url_api + "pipelines.xml"
        resposta = requests.get(url, auth=cls.auth)
        if resposta.status_code == 200:
            xml = minidom.parseString(resposta.content.decode())
            pipelines = xml.getElementsByTagName("pipeline")
            return len(pipelines)
        else:
            return None

    @classmethod
    def obter_nome_todos_pipeline_groups(cls):
        url = cls.url_api + "config/pipeline_groups"
        resposta = requests.get(url, auth=cls.auth)
        if resposta.status_code == 200:
            groups = resposta.json()
            nomes = []
            for group in groups:
                nomes.append(group["name"])
            return nomes
        else:
            return None

    @classmethod
    def obter_quantidade_pipeline_groups(cls):
        url = cls.url_api + "config/pipeline_groups"
        resposta = requests.get(url, auth=cls.auth)
        if resposta.status_code == 200:
            return len(resposta.json())
        else:
            return None

    @classmethod
    def obter_duracao_execucao_job(cls, id_execucao_job):
        url = cls.url_api + "jobs/%s.xml" % id_execucao_job
        resposta = requests.get(url, auth=cls.auth)
        if resposta.status_code == 200:
            xml = minidom.parseString(resposta.content.decode())
            propriedades = xml.getElementsByTagName("property")
            inicio = None
            fim = None
            for propriedade in propriedades:
                if propriedade.getAttribute("name") == "cruise_timestamp_01_scheduled":
                    inicio = datetime.strptime(propriedade.firstChild.wholeText, "%Y-%m-%dT%H:%M:%S-03:00")
                if propriedade.getAttribute("name") == "cruise_timestamp_06_completed":
                    fim = datetime.strptime(propriedade.firstChild.wholeText, "%Y-%m-%dT%H:%M:%S-03:00")
            duracao = fim - inicio
            return duracao
        else:
            return None

    @classmethod
    def obter_duracao_execucao_stage(cls, id_stage):
        url = cls.url_api + "stages/%s.xml" % id_stage
        resposta = requests.get(url, auth=cls.auth)
        if resposta.status_code == 200:
            xml = minidom.parseString(resposta.content.decode())
            jobs = xml.getElementsByTagName("job")
            # para iniciar a duracao como 00:00
            duracao = datetime.now()
            duracao -= duracao
            for job in jobs:
                id_job = str(job.getAttribute("href").split("/")[-1].replace(".xml", ""))
                duracao += cls.obter_duracao_execucao_job(id_job)
            return duracao
        else:
            return None

    @classmethod
    def obter_ids_jobs_do_stage(cls, id_stage):
        url = cls.url_api + "stages/%s.xml" % id_stage
        resposta = requests.get(url, auth=cls.auth)
        if resposta.status_code == 200:
            xml = minidom.parseString(resposta.content.decode())
            jobs = xml.getElementsByTagName("job")
            lista_ids = []
            for job in jobs:
                id_job = str(job.getAttribute("href").split("/")[-1].replace(".xml", ""))
                lista_ids.append(id_job)
            return lista_ids
        else:
            return None

    @classmethod
    def obter_duracao_execucao_pipeline_por_id(cls, id_pipeline):
        url = cls.url_api + "pipelines/a/%s.xml" % id_pipeline
        resposta = requests.get(url, auth=cls.auth)
        if resposta.status_code == 200:
            xml = minidom.parseString(resposta.content.decode())
            stages = xml.getElementsByTagName("stage")
            # para iniciar a duracao como 00:00
            duracao = datetime.now()
            duracao -= duracao
            for stage in stages:
                id_stage = str(stage.getAttribute("href").split("/")[-1].replace(".xml", ""))
                duracao += cls.obter_duracao_execucao_stage(id_stage)
            return duracao
        else:
            return None

    @classmethod
    def obter_ids_stages_do_pipeline(cls, id_pipeline):
        url = cls.url_api + "pipelines/a/%s.xml" % id_pipeline
        resposta = requests.get(url, auth=cls.auth)
        if resposta.status_code == 200:
            xml = minidom.parseString(resposta.content.decode())
            stages = xml.getElementsByTagName("stage")
            lista_ids = []
            for stage in stages:
                id_stage = str(stage.getAttribute("href").split("/")[-1].replace(".xml", ""))
                lista_ids.append(id_stage)
            return lista_ids
        else:
            return None

    @classmethod
    def obter_n_ids_pipeline(cls, nome_pipeline, n=1):
        url = cls.url_api + "pipelines/" + nome_pipeline + "/history/0"
        resposta = requests.get(url, auth=cls.auth)
        if resposta.status_code == 200:
            historico = resposta.json()
            if len(historico["pipelines"]) > 0:
                if n == 1:
                    return historico["pipelines"][0]["id"]
                elif 1 < n <= 10:
                    ids = []
                    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                        ids.append(historico["pipelines"][i]["id"])
                    return ids
                else:
                    return None
            else:
                return None
        else:
            return None

    @classmethod
    def obter_duracao_ultima_execucao_pipeline(cls, nome_pipeline):
        id_pipeline = cls.obter_n_ids_pipeline(nome_pipeline)
        return cls.obter_duracao_execucao_pipeline_por_id(id_pipeline)

    @classmethod
    def obter_duracao_ultimas_dez_execucoes_pipeline(cls, nome_pipeline):
        ids_pipelines = cls.obter_n_ids_pipeline(nome_pipeline, n=10)
        duracoes = []
        for id_pipeline in ids_pipelines:
            duracoes.append(cls.obter_duracao_execucao_pipeline_por_id(id_pipeline))
        return duracoes

    @classmethod
    def obter_nome_do_pipeline_e_data_da_execucao(cls, id_pipeline):
        url = cls.url_api + "pipelines/a/%s.xml" % id_pipeline
        resposta = requests.get(url, auth=cls.auth)
        if resposta.status_code == 200:
            xml = minidom.parseString(resposta.content.decode())
            nome = xml.getElementsByTagName("pipeline")[0].getAttribute("name")
            data_execucao = xml.getElementsByTagName("scheduleTime")[0].firstChild.wholeText
            return [nome, data_execucao]
        else:
            return [None, None]
