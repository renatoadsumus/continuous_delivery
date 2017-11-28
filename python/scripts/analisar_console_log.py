""""Faz a leitura do log e define se o pipeline pode continuar ou se sera interrompido"""

from python.assistentes.log import Log
from python.settings import WORKING_DIRECTORY

fileOutputTxt = "%s/output.txt" % WORKING_DIRECTORY
#Monta o path do arquivo de log e depois o abre para leitura

with open(fileOutputTxt, 'r') as f:
    for line in f:
        #Passa por todas as linhas no arquivo
        if "SIM" in line:
            Log.imprime("Resultado desse estagio impede a continuacao do pipeline",
                        "Resultado desse estagio impede a continuacao do pipeline")
            exit(1)
#Procura por um "SIM" dentro do arquivo de log, que indica que existe um erro e o pipeline deve ser interrompido

