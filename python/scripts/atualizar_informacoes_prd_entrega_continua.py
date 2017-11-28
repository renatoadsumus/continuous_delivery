from python.assistentes.log import Log
from python.assistentes.manipulador_data_hora import ManipuladorDataHora
from python.mongo.informacoes_artefatos_gocd import InformacoesArtefatos
from python.settings import NOME_PROJETO, NOME_EQUIPE, PIPELINE_LABEL

cobertura_testes_unitarios = None
dependencias = None
quantidade_issues_total_aplicacao = None

if not NOME_PROJETO:
    Log.imprime("NOME DO PROJETO NAO INFORMADO.", "ERRO DURANTE ATUALIZACAO DE INFORMACOES EM PRD.",
                script="atualizar_informacoes_prd_entrega_continua.py", mensagem_de_erro=True)
    exit(1)

if not NOME_EQUIPE:
    Log.imprime("NOME DA EQUIPE NAO INFORMADO.", "ERRO DURANTE ATUALIZACAO DE INFORMACOES EM PRD.",
                script="atualizar_informacoes_prd_entrega_continua.py", mensagem_de_erro=True)
    exit(1)

revision_deploy_prd = PIPELINE_LABEL.split("-")[-1]

data_hora_deploy_prd = ManipuladorDataHora.obter_data_atual().replace("\'", "")

Log.imprime("INICIANDO ALTERACAO DAS INFORMACOES DE PRD.\nNOME DO PROJETO: " + NOME_PROJETO + "\nNOME DA EQUIPE: " +
            NOME_EQUIPE + "\nREVISION EM PRD: " + revision_deploy_prd + "\nDATA: " + data_hora_deploy_prd)

informacoes = InformacoesArtefatos(NOME_EQUIPE, NOME_PROJETO)

informacoes.alterar(revision_deploy_prd=revision_deploy_prd, data_deploy_prd=data_hora_deploy_prd,
                    status_deploy_prd="F")

Log.imprime("INFORMACOES ALTERADAS NO MONGO COM SUCESSO."
            "\nREVISION_DEPLOY_PRD: " + revision_deploy_prd +
            "\nDATA_DEPLOY_PRD: " + data_hora_deploy_prd,
            "PROCESSO DE DEPLOY FINALIZADO"
            "\nREVISION ATUAL EM PRD: " + revision_deploy_prd +
            "\nDATA DE DEPLOY: " + data_hora_deploy_prd +
            "\nSTATUS DE DEPLOY PRD: F")
