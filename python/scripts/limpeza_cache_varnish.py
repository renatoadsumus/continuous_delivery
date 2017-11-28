from python.assistentes.SSH import SSH
from python.assistentes.log import Log
from python.settings import USUARIO_SSH, DIRETORIO_CHAVES_SERVIDORES, getenv

servidor_deploy = getenv("SERVIDOR_SSH")
senha_ssh = getenv("SENHA_SSH")
caminho_sh_limpeza_cache = getenv("CAMINHO_SH_LIMPEZA_CACHE")
host_header = getenv("HOST_HEADER")
url_path = getenv("URL_PATH")
arquivo_chave_ssh = getenv("ARQUIVO_CHAVE_SSH")
comando_variaveis_ambiente = "source /etc/profile && source .bashrc && source .bash_profile && "

comando = comando_variaveis_ambiente + caminho_sh_limpeza_cache + " " + host_header + " " + url_path

Log.imprime("INICIANDO LIMPEZA DE CACHE", "INICIANDO LIMPEZA DE CACHE")

ssh = SSH(servidor_deploy, USUARIO_SSH)

if senha_ssh:
    Log.imprime("UTILIZANDO SENHA PARA AUTENTICACAO")
    ssh.senha(senha_ssh)
elif arquivo_chave_ssh:
    Log.imprime("UTILIZANDO ARQUIVO DE CHAVES PARA AUTENTICACAO")
    chave = DIRETORIO_CHAVES_SERVIDORES + arquivo_chave_ssh
    ssh.chave_acesso(chave)

ssh.abrir_conexao()

Log.imprime("EXECUTANDO O COMANDO " + comando, "EXECUTANDO O COMANDO " + comando)

saida_comando_limpeza = ssh.executar_comando(comando)

Log.imprime("SAIDA DO COMANDO: " + saida_comando_limpeza)

ssh.fechar_conexao()

Log.imprime("LIMPEZA FINALIZADA", "LIMPEZA FINALIZADA")

