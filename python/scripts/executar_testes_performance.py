from subprocess import check_call
from sys import argv
from traceback import format_exc

from python.assistentes.SSH import SSH
from python.assistentes.log import Log
from python.settings import DIRETORIO_CHAVES_SERVIDORES

arquivoChaveSSH = None
servidor = "infojmeter"
jmeterTeste = None
arquivoCsv = None
arquivoLimites = None
senhaJmeter = None

for parametro in argv:
    if "-arquivoChaveSSH" in parametro:
        arquivoChaveSSH = parametro.replace("-arquivoChaveSSH=", "")
    if "-jmeterTeste" in parametro:
        jmeterTeste = parametro.replace("-jmeterTeste=", "")
    if "-arquivoCsv" in parametro:
        arquivoCsv = parametro.replace("-arquivoCsv=", "")
    if "-arquivoLimites" in parametro:
        arquivoLimites = parametro.replace("-arquivoLimites=", "")
    if "-senhaJmeter" in parametro:
        senhaJmeter = parametro.replace("-senhaJmeter=", "")

JAR_VALIDADOR_TESTE_PERFORMANCE = "/opt/validador-teste-performance-1.1.jar"
chave = DIRETORIO_CHAVES_SERVIDORES + arquivoChaveSSH

try:
    Log.imprime("CONECTANDO AO SERVIDOR DE TESTES\nServidor: %s" % servidor)
    # Usando usuario jmeter temporariamente
    # ssh = SSH(servidor, "tfsservice")
    # ssh.chave_acesso(chave)
    ssh = SSH(servidor, "jmeter")
    ssh.senha(senhaJmeter)
    ssh.abrir_conexao()
    ssh.executar_comando("/home/jmeter/autojmeter " + jmeterTeste)
    ssh.obter_arquivo("/home/jmeter/reports/" + arquivoCsv, ".")
    ssh.fechar_conexao()

    Log.imprime("EXECUTANDO A VALIDACAO", "EXECUTANDO A VALIDACAO")

    arquivoLimites = "scripts/assistentes_performance/" + arquivoLimites
    comando = 'java -cp %s leitor.jmeter.validacao.deploy.Processar %s %s | tee output.txt' % \
              (JAR_VALIDADOR_TESTE_PERFORMANCE, arquivoCsv, arquivoLimites)
    check_call([comando], shell=True)
    Log.imprime("SUCESSO -- VALIDACAO EXECUTADA", "SUCESSO -- VALIDACAO EXECUTADA")
except:
    Log.imprime("Erro ao executar Testes de Performance do JMeter\n" + format_exc(),
                "Erro ao executar Testes de Performance do JMeter",
                script="executar_testes_performace.py", mensagem_de_erro=True)
    exit(1)
