from python.apis.api_sonar import Sonar
from python.assistentes.log import Log
from python.settings import NOME_PROJETO_SONAR

sonar = Sonar(NOME_PROJETO_SONAR)

if sonar.verifica_se_existe_analise_em_progresso_ou_pendente():
    if sonar.obter_status_quality_gates():
        Log.imprime("O QUALITY GATE LIBEROU A CONTINUIDADE DO PROCESSO DE GERACAO DE PACOTE", "O QUALITY GATE LIBEROU A CONTINUIDADE DO PROCESSO DE GERACAO DE PACOTE")
    else:
        Log.imprime("O QUALITY GATE NAO LIBEROU A CONTINUIDADE DO PROCESSO DE GERACAO DE PACOTE", "O QUALITY GATE NAO LIBEROU A CONTINUIDADE DO PROCESSO DE GERACAO DE PACOTE")
        exit(1)
else:
    Log.imprime("A ANALISE DO SONAR AINDA NAO FOI CONCLUIDA. GERACAO DE PACOTE NAO FOI LIBERADA", "A ANALISE DO SONAR AINDA NAO FOI CONCLUIDA. GERACAO DE PACOTE NAO FOI LIBERADA")
    exit(1)