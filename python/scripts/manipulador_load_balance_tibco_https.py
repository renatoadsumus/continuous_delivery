from os import listdir

from python.assistentes.SSH import SSH
from python.settings import getenv, DIRETORIO_CHAVES_SERVIDORES


class ManipuladorLoadBalanceTibcoHTTPS(object):
    def __init__(self):
        self.USUARIO_SSH = "tfsservice"
        self.ARQUIVO_CHAVE_SSH = "id_rsa"
        self.CAMINHO_CONF_APACHE = "/etc/httpd/scripts/arquivos/"
        self.script_reload_apache = "/etc/httpd/scripts/DeployApache.sh"

        self.PORTA_SERVICO = getenv("PORTA_SERVICO")
        self.PASTA_CONF_APACHE = getenv("PASTA_CONF_APACHE")

        # lista dos servidores apache, separado por virgula
        self.SERVIDORES_APACHE = getenv("SERVIDORES_APACHE")

        # lista dos servidores de load balance, separado por virgula
        self.SERVIDORES_LOAD_BALANCE = getenv("SERVIDORES_LOAD_BALANCE")

    def editar_conf_apache(self, novo_backend):
        for servidor in self.SERVIDORES_APACHE.split(","):
            pasta_servidor = self.PASTA_CONF_APACHE + "/" + servidor
            for arquivo_conf in listdir(pasta_servidor):
                if arquivo_conf.endswith(".conf"):
                    with open(pasta_servidor + "/" + arquivo_conf, "r") as conf:
                        new_conf = conf.read()
                    for load_balance in self.SERVIDORES_LOAD_BALANCE.split(","):
                        new_conf = new_conf.replace("{}:{}".format(load_balance, self.PORTA_SERVICO),
                                                    "{}:{}".format(novo_backend, self.PORTA_SERVICO))
                    with open(pasta_servidor + "/" + arquivo_conf, "w") as conf:
                        conf.write(new_conf)

    def atualizar_conf_apache(self):
        novo_servidor_backend = getenv("NOVO_SERVIDOR_BACKEND")
        if novo_servidor_backend:
            self.editar_conf_apache(novo_servidor_backend)

        chave = DIRETORIO_CHAVES_SERVIDORES + self.ARQUIVO_CHAVE_SSH

        for servidor in self.SERVIDORES_APACHE.split(","):
            pasta_servidor = self.PASTA_CONF_APACHE + "/" + servidor
            ssh = SSH(servidor, self.USUARIO_SSH)
            ssh.chave_acesso(chave)
            ssh.abrir_conexao()

            for arquivo_conf in listdir(pasta_servidor):
                if arquivo_conf.endswith(".conf"):
                    ssh.enviar_arquivo(pasta_servidor + "/" + arquivo_conf, self.CAMINHO_CONF_APACHE)
                    comando_reload_apache = "{} {}".format(self.script_reload_apache, arquivo_conf)
                    ssh.executar_comando(comando_reload_apache)
            ssh.fechar_conexao()

if __name__ == '__main__':
    lbhttps = ManipuladorLoadBalanceTibcoHTTPS()
    lbhttps.atualizar_conf_apache()
