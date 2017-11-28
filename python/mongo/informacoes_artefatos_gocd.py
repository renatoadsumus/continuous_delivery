
from python.assistentes.log import Log
from python.mongo.conexao import Conexao
from python.mongo.operacoes import Operacoes
from python.settings import USUARIO_GO_API, SENHA_GO_API


class InformacoesArtefatos(object):

    def __init__(self, equipe, nome_projeto):
        if not nome_projeto:
            Log.imprime("NOME DO PROJETO NAO FOI INFORMADO.", "OCORREU UM ERRO AO OBTER UMA INFORMACAO NECESSARIA.",
                        classe=InformacoesArtefatos)
            exit(1)

        if not equipe:
            Log.imprime("NOME DA EQUIPE NAO FOI INFORMADO.", "OCORREU UM ERRO AO OBTER UMA INFORMACAO NECESSARIA.",
                        classe=InformacoesArtefatos)
            exit(1)

        self.equipe = equipe
        self.nome_projeto = nome_projeto
        self.__conexao = Conexao(USUARIO_GO_API, SENHA_GO_API, "qa_informacoes_entrega_continua", self.equipe)
        self.colecao = self.__conexao.obter_colecao()
        self.projeto = self.__busca_projeto()
        self.__conexao.fechar_conexao()

    def __busca_projeto(self):
        string_busca = '{"projeto":"' + self.nome_projeto + '"}'
        documentos_encontrados = Operacoes.buscar_json(self.colecao, string_busca)

        if documentos_encontrados.count() == 0:
            Log.imprime("A BUSCA NAO RETORNOU NENHUM DOCUMENTO REFERENTE AO PROJETO.\nNOME DE PROJETO INFORMADO: " +
                        self.nome_projeto + "INSERINDO PROJETO NO MONGO", classe=InformacoesArtefatos)

            Operacoes.inserir_json(self.colecao, string_busca)

        self.__conexao.fechar_conexao()
        return documentos_encontrados[0]

    def alterar(self, revision_deploy_stg=None, revision_deploy_prd=None, data_deploy_stg=None, data_deploy_prd=None,
                cobertura_testes_unitarios=None, dependencias=list(), load_balance_backend=None,
                quantidade_issues_total=None, numero_mudanca=None,
                quantidade_testes_unitarios=None, quantidade_smoke_tests=None, quantidade_testes_regressivos=None,
                status_deploy_prd=None):
        string_busca = '{"projeto":"' + self.nome_projeto + '"}'
        # Montagem da string de alteracao
        string_alteracao = '{'
        if revision_deploy_stg:
            string_alteracao += '"revision_deploy_stg":"' + revision_deploy_stg + '",'
        if revision_deploy_prd:
            string_alteracao += '"revision_deploy_prd":"' + revision_deploy_prd + '",'
        if data_deploy_stg:
            string_alteracao += '"data_deploy_stg":"' + data_deploy_stg + '",'
        if data_deploy_prd:
            string_alteracao += '"data_deploy_prd":"' + data_deploy_prd + '",'
        if status_deploy_prd:
            string_alteracao += '"status_deploy_prd":"' + status_deploy_prd + '",'
        if cobertura_testes_unitarios:
            string_alteracao += '"cobertura_testes_unitarios":"' + str(cobertura_testes_unitarios) + '",'
        if dependencias:

            string_alteracao += '"quantidade_issues_findbugs":['
            for dependencia in dependencias:
                dados_dependencia = dependencia.split(":")
                dependencia_nome = dados_dependencia[0]
                quantidade_issues_dependencia = dados_dependencia[1]
                string_alteracao += '{"dependencia":"' + dependencia_nome + '",'
                string_alteracao += '"quantidade_issues":"' + str(quantidade_issues_dependencia) + '"},'
            string_alteracao += '],'

        if quantidade_issues_total:
            string_alteracao += '"quantidade_issues_total_aplicacao":"' + str(quantidade_issues_total) + '",'
        if numero_mudanca:
            string_alteracao += '"numero_mudanca":"' + numero_mudanca + '",'
        if quantidade_testes_unitarios:
            string_alteracao += '"quantidade_testes_unitarios":"' + str(quantidade_testes_unitarios) + '",'
        if load_balance_backend:
            string_alteracao += '"load_balance_backend":"' + load_balance_backend + '",'
        if quantidade_smoke_tests:
            string_alteracao += '"quantidade_smoke_tests":"' + str(quantidade_smoke_tests) + '",'
        if quantidade_testes_regressivos:
            string_alteracao += '"quantidade_testes_regressivos":"' + str(quantidade_testes_regressivos) + '",'
        string_alteracao += '}'
        string_alteracao = string_alteracao.replace(',}', '}').replace(',]', ']')

        if string_alteracao == '{}':
            Log.imprime("NENHUMA ALTERACAO FOI FEITA.", classe=InformacoesArtefatos)
        else:
            self.__conexao = Conexao(USUARIO_GO_API, SENHA_GO_API, "qa_informacoes_entrega_continua", self.equipe)
            Operacoes.alterar_json(self.colecao, string_busca, string_alteracao)
            self.__conexao.fechar_conexao()

    def obter_revision_deploy_stg(self):
        return self.projeto.get("revision_deploy_stg")

    def obter_revision_deploy_prd(self):
        if self.projeto.get("revision_deploy_prd"):
            return self.projeto.get("revision_deploy_prd")
        else:
            return 0

    def obter_data_deploy_stg(self):
        return self.projeto.get("data_deploy_stg")

    def obter_data_deploy_prd(self):
        return self.projeto.get("data_deploy_prd")

    def obter_cobertura_testes_unitarios(self):
        return self.projeto.get("cobertura_testes_unitarios")

    def obter_numero_mudanca(self):
        return self.projeto.get("numero_mudanca")

    def obter_load_balance_backend(self):
        return self.projeto.get("load_balance_backend")

    def obter_status_deploy_prd(self):
        if self.projeto.get("status_deploy_prd") == "I":
            return "I"
        else:
            return "F"

    def obter_quantidade_issues_findbugs(self):
        lista_dependencias = []
        lista_dependencias_dict = self.__busca_projeto().get("quantidade_issues_findbugs")
        for dependencia_dict in lista_dependencias_dict:
            nome_dependencia = dependencia_dict.get("dependencia")
            quantidade_issues_dependencia = dependencia_dict.get("quantidade_issues")
            lista_dependencias.append(nome_dependencia + ':' + quantidade_issues_dependencia)
        return lista_dependencias

    def obter_quantidade_issues_total_aplicacao(self):
        return self.projeto.get("quantidade_issues_total_aplicacao")

    def obter_quantidade_testes_unitarios(self):
        return self.projeto.get("quantidade_testes_unitarios")

    def obter_quantidade_smoke_tests(self):
        return self.projeto.get("quantidade_smoke_tests")

    def obter_quantidade_testes_regressivos(self):
        return self.projeto.get("quantidade_testes_regressivos")

