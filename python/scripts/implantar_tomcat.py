# coding=utf-8

from subprocess import check_call
from sys import argv
from traceback import format_exc

from python.assistentes.SSH import SSH
from python.assistentes.log import Log
from python.assistentes.manipulador_data_hora import ManipuladorDataHora
from python.settings import WORKING_DIRECTORY, DIRETORIO_CHAVES_SERVIDORES, environ
from python.tipos_arquivos.arquivo_properties import ArquivoProperties

contextPath = None
dominio = None
servidorPorta = None
aplicacaoParar = None
tempoEsperar = None
usuarioTomcat = None
arquivoChaveSSH = None

SENHA_TOMCAT = environ["SENHA_TOMCAT"]

for parametro in argv:
    if "-tomcatContextPath" in parametro:
        contextPath = parametro.replace("-tomcatContextPath=", "")
    if "-dominio" in parametro:
        dominio = parametro.replace("-dominio=", "")
    if "-servidorPorta" in parametro:
        servidorPorta = parametro.replace("-servidorPorta=", "")
    if "-aplicacaoParar" in parametro:
        aplicacaoParar = parametro.replace("-aplicacaoParar=", "")
    if "-tempoEsperar" in parametro:
        tempoEsperar = parametro.replace("-tempoEsperar=", "")
    if "-usuarioTomcat" in parametro:
        usuarioTomcat = parametro.replace("-usuarioTomcat=", "")
    if "-arquivoChaveSSH" in parametro:
        arquivoChaveSSH = parametro.replace("-arquivoChaveSSH=", "")

mensagem = "CRIANDO ARTEFATO COM O CONTEXT PATH QUE SERA IMPLANTADO"
mensagem += "Context Path: %s" % contextPath
Log.imprime(mensagem, mensagem)

comando = 'if [ ! -f %s.war ]; then mv %s/*.war %s.war; fi' % (contextPath, WORKING_DIRECTORY, contextPath)
try:
    check_call([comando], shell=True)
    Log.imprime("SUCESSO -- COMANDO EXECUTADO", "SUCESSO -- COMANDO EXECUTADO")
except:
    Log.imprime("FALHA\n" + format_exc(), "FALHA -- COMANDO NAO EXECUTADO",
                script="implantar_tomcat.py", mensagem_de_erro=True)

servidor = servidorPorta.split(":")[0]
porta = servidorPorta.split(":")[1]

mensagem = "CONECTANDO AO SERVIDOR DA APLICACAO"
mensagem += "Servidor: %s" % servidor
Log.imprime(mensagem, mensagem)

chave = DIRETORIO_CHAVES_SERVIDORES + arquivoChaveSSH
pathArquivoDeployTomcat = WORKING_DIRECTORY + "/scripts/shell/deploy_tomcat.sh"

ssh = SSH(servidor, "tfsservice")
ssh.chave_acesso(chave)
ssh.abrir_conexao()
ssh.enviar_arquivo(pathArquivoDeployTomcat, "/tmp/deploy_tomcat.sh")
ssh.enviar_arquivo(contextPath + ".war", "/tmp/" + contextPath + ".war")
ssh.executar_comando("chmod +x /tmp/deploy_tomcat.sh")
comando_deploy = '/tmp/deploy_tomcat.sh "%s" "%s" %s %s %s %s %s' % (usuarioTomcat, SENHA_TOMCAT, dominio, porta,
                                                                     contextPath, aplicacaoParar, tempoEsperar)
retorno_comando = ssh.executar_comando(comando_deploy)
ssh.executar_comando("rm -f /tmp/" + contextPath + ".war")
ssh.fechar_conexao()
data_hora_execucao = ManipuladorDataHora.obter_data_hora_atual()
data_hora_deploy = ArquivoProperties("data-hora-deploy.properties")
data_hora_deploy.alterar_valor_chave("Data_Hora_Inicio_Analise", data_hora_execucao)
