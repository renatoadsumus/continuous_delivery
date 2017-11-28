from python.assistentes.log import Log
from python.assistentes.manipulador_data_hora import ManipuladorDataHora
from python.mongo.informacoes_artefatos_gocd import InformacoesArtefatos
from python.settings import NOME_PROJETO, NOME_EQUIPE, PIPELINE_LABEL

if NOME_PROJETO is None:
    Log.imprime("NOME DO PROJETO NAO INFORMADO.", "ERRO DURANTE ATUALIZACAO DE INFORMACOES EM STG.",
                script="atualizar_informacoes_stg_entrega_continua.py", mensagem_de_erro=True)
    exit(1)

if NOME_EQUIPE is None:
    Log.imprime("NOME DA EQUIPE NAO INFORMADO.", "ERRO DURANTE ATUALIZACAO DE INFORMACOES EM STG.",
                script="atualizar_informacoes_stg_entrega_continua.py", mensagem_de_erro=True)
    exit(1)

data_deploy_stg = ManipuladorDataHora.obter_data_hora_atual().replace("\"", "")

revision_deploy_stg = PIPELINE_LABEL.split("-")[-1]

Log.imprime("INICIANDO ALTERACAO DAS INFORMACOES DE PRD."
            "\nNOME DO PROJETO: " + NOME_PROJETO +
            "\nNOME DA EQUIPE: " + NOME_EQUIPE +
            "\nREVISION EM PRD: " + revision_deploy_stg +
            "\nDATA: " + data_deploy_stg)

informacoes = InformacoesArtefatos(NOME_EQUIPE, NOME_PROJETO)

informacoes.alterar(revision_deploy_stg=revision_deploy_stg, data_deploy_stg=data_deploy_stg)

Log.imprime("INFORMACOES ALTERADAS NO MONGO COM SUCESSO."
            "\nREVISION_DEPLOY_STG: " + revision_deploy_stg +
            "\nDATA_DEPLOY_STG: " + data_deploy_stg,
            "PROCESSO DE DEPLOY FINALIZADO"
            "\nREVISION ATUAL EM STG: " + revision_deploy_stg +
            "\nDATA DE DEPLOY: " + data_deploy_stg)
