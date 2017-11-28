from python.assistentes.SSH import SSH
from python.assistentes.log import Log
from python.settings import getenv, DIRETORIO_CHAVES_SERVIDORES

__USUARIO_SSH = getenv("UsuarioSSH")
__SENHA_SSH = getenv("SenhaSSH")
__ARQUIVO_CHAVE_SSH = getenv("ArquivoChaveSSH")
__SERVIDOR_SSH = getenv("ServidorSSH")

if not __ARQUIVO_CHAVE_SSH and not __SENHA_SSH:
    Log.imprime("Arquivo chave para SSH ou a senha para SSH nao foi informado",
                "ERRO NA VALIDACAO DO NAGIOS", script="nagios_validar_configuracao.py", mensagem_de_erro=True)
    exit(1)

if not __USUARIO_SSH:
    __USUARIO_SSH = "tfsservice"

ssh = SSH(__SERVIDOR_SSH, __USUARIO_SSH)
if __SENHA_SSH:
    ssh.senha(__SENHA_SSH)
elif __ARQUIVO_CHAVE_SSH:
    chave = DIRETORIO_CHAVES_SERVIDORES + __ARQUIVO_CHAVE_SSH
    ssh.chave_acesso(chave)
ssh.abrir_conexao()

ssh.executar_comando("sleep 30")
ssh.executar_comando("/usr/local/nagios/libexec/webinject.pl -c conf/classif567_cfg.xml")
ssh.executar_comando("/usr/local/nagios/libexec/webinject.pl -c conf/classif568_cfg.xml")
ssh.fechar_conexao()
