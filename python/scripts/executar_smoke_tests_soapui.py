from os import getenv

from python.assistentes.linha_de_comando import LinhaDeComando
from python.assistentes.log import Log

XML_PROJETO = getenv("XML_PROJETO")
ENDPOINT_TESTES = getenv("ENDPOINT_TESTES")
TEST_SUIT = getenv("TEST_SUIT")
WORKING_DIRECTORY = getenv("WORKING_DIRECTORY")
DIRETORIO_SOAPUI = getenv("DIR_SOAPUI")

mensagem = "XML DE TESTES: %s" % XML_PROJETO + \
           "\nTEST SUIT: %s" % TEST_SUIT + \
           "\nENDPOINT TESTES: %s" % ENDPOINT_TESTES
Log.imprime(mensagem, mensagem)

diretorio_xml_testes = XML_PROJETO.split("/")[0]

mensagem = "REALIZANDO UPDATE PARA A ULTIMA VERSAO DO XML DE TESTES DO SVN..." \
           "\nDIRETORIO XML TESTES: %s" % diretorio_xml_testes
Log.imprime(mensagem, mensagem)

comando_update = "cd %s && svn up && cd .." % diretorio_xml_testes
LinhaDeComando.executar(comando_update)

flag_endpoint = ""
if ENDPOINT_TESTES:
    flag_endpoint = "-e %s" % ENDPOINT_TESTES

comando = "/bin/bash %s/testrunner.sh %s -s \"%s\" -j -f %s -r %s" % (DIRETORIO_SOAPUI, XML_PROJETO, TEST_SUIT,
                                                                      WORKING_DIRECTORY, flag_endpoint)

if LinhaDeComando.executar(comando, retornar_exit_code=True) is not 0:
    mensagem = "ERRO NA EXECUCAO DO TESTE" \
               "\nTestSuit = %s" % TEST_SUIT + \
               "\nENDPOINT = %s" % ENDPOINT_TESTES
    Log.imprime(mensagem, mensagem +
                "\nREEXECUTE O TESTE E CASO O ERRO OCORRA NOVAMENTE ENTRE EM CONTATO COM A EQUIPE DE DEVOPS",
                script="executar_smoke_tests_soapui.py", mensagem_de_erro=True)
    exit(1)
