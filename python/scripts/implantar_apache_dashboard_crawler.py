from os import getenv

from python.assistentes.SSH import SSH

aplicacao = "dashboard_crawler"
artefato_zip = "web-crawler-app.zip"
artefato_jar = "web-crawler-app.jar"
destino = "/opt/dashboard/crawlerGCOM"
caminho_completo_zip = destino + "/" + artefato_zip
caminho_completo__jar = destino + "/" + artefato_jar


servidor = getenv("SERVIDOR")
usuario = getenv("USUARIO")
senha = getenv("SENHA")

ssh = SSH(servidor, usuario)
ssh.senha(senha)
ssh.abrir_conexao()

ssh.executar_comando("/etc/init.d/" + aplicacao + " stop")

ssh.executar_comando("rm -v " + caminho_completo_zip)
ssh.executar_comando("rm -v " + caminho_completo__jar)
ssh.executar_comando("rm -vfr " + destino + "/lib")
ssh.enviar_arquivo(artefato_zip, caminho_completo_zip)
# ssh.executar_comando("unzip -v " + caminho_completo)
ssh.executar_comando("cd " + destino + " && unzip " + caminho_completo_zip)

ssh.executar_comando("/etc/init.d/" + aplicacao + " start")

ssh.fechar_conexao()
