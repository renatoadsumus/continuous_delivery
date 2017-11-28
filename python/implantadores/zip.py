"""Modulo que engloba a classe de ImplantadorZIP"""

from os import path, walk, makedirs
from shutil import copy

from python.assistentes.SSH import SSH
from python.assistentes.ftp import FTP
from python.assistentes.linha_de_comando import LinhaDeComando
from python.assistentes.log import Log
from python.assistentes.zip import ZIP
from python.settings import WORKING_DIRECTORY, NOME_PROJETO, DIRETORIO_CHAVES_SERVIDORES, getenv
from python.tipos_arquivos.arquivo import Arquivo


class ImplantadorZIP(object):
    """Classe que representa o ImplantadorZIP e todas as suas acoes"""

    def __init__(self):
        self.host_ftp = getenv("SERVIDOR_FTP")
        self.usuario_ftp = getenv("USUARIO_FTP")
        self.senha_ftp = getenv("SENHA_FTP")
        self.nome_arquivo_configuracao_ambiente = getenv("NOME_ARQUIVO_CONFIGURACAO_AMBIENTE")
        self.ambiente = getenv("AMBIENTE")
        self.caminho_compartilhamento = getenv("CAMINHO_COMPARTILHAMENTO")
        self.ssl = getenv("SSL")
        self.diretorio_ftp = getenv("DIRETORIO_FTP")
        self.diretorio_descompactacao = "descompactado"
        self.pastas_nao_apagar = getenv("PASTAS_NAO_APAGAR")
        self.servidor_ssh = getenv("SERVIDOR_SSH")
        self.senha_ssh = getenv("SENHA_SSH")
        self.usuario_ssh = getenv("USUARIO_SSH")
        self.arquivo_chave_ssh = getenv("ARQUIVO_CHAVE_SSH")
        self.diretorio_ssh = getenv("DIRETORIO_SSH")

    def implantar_artefato(self):
        # Metodo para implantacao do artefato no ambiente
        zp = ZIP()

        zp.descompactar(path.join(WORKING_DIRECTORY, NOME_PROJETO + ".zip"), self.diretorio_descompactacao)
        # Descompacta o zip no local desejado

        Log.imprime("CAMINHO DE COMPARTILHAMENTO DA IMPLANTACAO: " + str(self.caminho_compartilhamento))
        Log.imprime("NOME DO ARQUIVO DE CONFIGURACAO DO AMBIENTE: " + str(self.nome_arquivo_configuracao_ambiente))

        Log.imprime("HOST FTP: " + str(self.host_ftp))
        Log.imprime("SERVIDOR SSH: " + str(self.servidor_ssh))

        # Checa se existe um arquivo de configuracao para o ambiente em questao com o metodo responsavel
        if self.nome_arquivo_configuracao_ambiente:
            self.__verificar_existencia_arquivo_ambiente()

        # Reconhece o meio pelo qual o zip deve ser implantado e chama o metodo responsavel
        if self.caminho_compartilhamento is not None:
            self.__implantar_caminho_compartilhamento()
        elif self.host_ftp is not None:
            self.__implantar_via_ftp()
        elif self.servidor_ssh is not None:
            self.__implantar_via_ssh()
        else:
            Log.imprime("MEIO DE IMPLANTACAO NAO FOI INFORMADO.", "ERRO DURANTE A IMPLANTACAO DO ZIP.",
                        classe=ImplantadorZIP)
            exit(1)

    def __verificar_existencia_arquivo_ambiente(self):
        # Implanta um arquivo de configuracao no servidor copiando por FTP.
        # O arquivo deve estar no formato <nome_arquivo_configuracao_ambiente>_QLT e sera renomeado para
        # <nome_arquivo_configuracao_ambiente> no servidor
        caminho_arquivo_local_ambiente = path.join(WORKING_DIRECTORY, "descompactado",
                                                   self.nome_arquivo_configuracao_ambiente + "_" +
                                                   self.ambiente.upper())

        arquivo_ambiente = Arquivo(caminho_arquivo_local_ambiente)
        Log.imprime("CAMINHO DO ARQUIVO LOCAL DE AMBIENTE: " + caminho_arquivo_local_ambiente)

        # Verifica a existencia do arquivo de configuracao e retorna uma mensagem e erro caso necessario
        if not arquivo_ambiente.existe():
            Log.imprime("O ARQUIVO DE CONFIGURACAO DE AMBIENTE NAO FOI ENCONTRADO",
                        "ERRO DURANTE A IMPLANTACAO DO ZIP.", classe=ImplantadorZIP)
            exit(1)
        caminho_arquivo_local_default = path.join(WORKING_DIRECTORY, "descompactado",
                                                  self.nome_arquivo_configuracao_ambiente)

        # Localiza e remove o arquivo default e renomeia o arquivo de configuracao correto para o ambiente de
        #  implantacao
        arquivo_default = Arquivo(caminho_arquivo_local_default)
        nome_arquivo = arquivo_default.nome()
        arquivo_default.excluir()
        arquivo_ambiente.renomear(nome_arquivo)
        Log.imprime("IMPLANTANDO ARQUIVO DE CONFIGURACAO.")

    def __implantar_caminho_compartilhamento(self):
        # Metodo responsavel pela implantacao do zip via caminho de compartilhamento

        # Verifica se existem pastas a serem apagadas no caminho de compartilhamento e chama o metodo responsavel
        # caso necessario
        if self.pastas_nao_apagar is not None:
            Log.imprime("LIMPANDO CAMINHO DE COMPARTILHAMENTO")
            self.limpar_pasta_compartilhada()

        Log.imprime("COPIANDO ARQUIVO PARA O SERVIDOR VIA CAMINHO DE COMPARTILHAMENTO " +
                    self.caminho_compartilhamento, "INICIANDO DEPLOY DO ZIP")

        # shutil.copytree(diretorio_descompactacao, caminho_compartilhamento)

        for raiz, diretorios, arquivos in walk(self.diretorio_descompactacao):
            for arquivo in arquivos:
                caminho_absoluto_arquivo = path.join(raiz, arquivo)
                caminho_relativo_arquivo = caminho_absoluto_arquivo.replace(self.diretorio_descompactacao, "")
                caminho_arquivo_compartilhamento = self.caminho_compartilhamento + caminho_relativo_arquivo
                caminho_diretorio_compartilhamento = path.dirname(caminho_arquivo_compartilhamento)
                if not path.isdir(caminho_diretorio_compartilhamento):
                    makedirs(caminho_diretorio_compartilhamento)

                Log.imprime("COPIANDO ARQUIVO " + caminho_absoluto_arquivo + " PARA " +
                            caminho_arquivo_compartilhamento, "COPIANDO ARQUIVO " + caminho_relativo_arquivo)

                copy(caminho_absoluto_arquivo, caminho_arquivo_compartilhamento)

        Log.imprime("DEPLOY ENCERRADO", "DEPLOY ENCERRADO COM SUCESSO")

    def __implantar_via_ftp(self):
        # Metodo responsavel pela implantacao do zip via conexao FTP

        Log.imprime("COPIANDO ARQUIVO PARA O SERVIDOR " + self.host_ftp, "INICIANDO DEPLOY DO ZIP")

        # Verifica se sera necessaria conexao SSL
        Log.imprime("SSL: " + self.ssl.upper())
        use_ssl = False
        if self.ssl.lower() == "true":
            use_ssl = True

        Log.imprime("ESTABELECENDO CONEXAO COM O SERVIDOR")

        # Abre a conexao via FTP com o servidor com o assistente FTP e envia o diretorio descompactado para o servidor
        ftp = FTP(self.host_ftp, self.usuario_ftp, self.senha_ftp, use_ssl)

        ftp.enviar_diretorio(self.diretorio_descompactacao, self.diretorio_ftp)

        ftp.desconectar()
        # Encerra a conexao via FTP

        Log.imprime("DEPLOY ENCERRADO COM SUCESSO", "DEPLOY ENCERRADO COM SUCESSO")

    def limpar_pasta_compartilhada(self):
        # Metodo responsavel por limpar o caminho de compartilhamento

        Log.imprime("INICIANDO LIMPEZA DO CAMINHO DE COMPARTILHAMENTO " + self.caminho_compartilhamento)

        # Copia um arquivo .bat para o caminho de compartilhamento
        LinhaDeComando.executar("copy " + path.dirname(__file__) + "\\..\\..\\batch\\apagarConteudo.bat" + " " +
                                self.caminho_compartilhamento)

        # Usa o comando net use para executar o .bat no caminho de compartilhamento
        LinhaDeComando.executar("net use i: " + self.caminho_compartilhamento)

        LinhaDeComando.executar("i: && call apagarConteudo.bat " + self.pastas_nao_apagar + " && c:")

        LinhaDeComando.executar("net use i: /delete /yes")

        # Apaga o proprio arquivo .bat para nao deixar resquicios do processo de limpeza no servidor
        LinhaDeComando.executar("del " + path.join(self.caminho_compartilhamento, "apagarConteudo.bat"))

        Log.imprime("LIMPEZA DO CAMINHO DE COMPARTILHAMENTO REALIZADA COM SUCESSO")

    def __implantar_via_ssh(self):
        # Metodo responsavel pela implantacao do zip via conexao SSH

        arquivo_zip = NOME_PROJETO + ".zip"
        Log.imprime("IMPLANTANDO " + arquivo_zip + " NO SERVIDOR " + self.servidor_ssh + " NO DIRETORIO " +
                    self.diretorio_ssh + " VIA SSH", "INICIANDO DEPLOY DO ZIP")

        Log.imprime("PREPARANDO PARA ABRIR CONEXAO COM O USUARIO " + self.usuario_ssh + " NO SERVIDOR " +
                    self.servidor_ssh)

        # Prepara para abrir conexao SSH com o servidor
        ssh = SSH(self.servidor_ssh, self.usuario_ssh)

        # Verifica se a autenticacao sera feita via senha ou via arquivo de chaves
        if self.senha_ssh:
            Log.imprime("UTILIZANDO SENHA PARA AUTENTICACAO")
            ssh.senha(self.senha_ssh)
        elif self.arquivo_chave_ssh:
            Log.imprime("UTILIZANDO ARQUIVO DE CHAVES PARA AUTENTICACAO")
            chave = DIRETORIO_CHAVES_SERVIDORES + self.arquivo_chave_ssh
            ssh.chave_acesso(chave)

        # Abre a conexao
        ssh.abrir_conexao()

        # Envia o arquivo zip para o servidor no diretorio desejado
        ssh.enviar_arquivo(path.join(WORKING_DIRECTORY, arquivo_zip), self.diretorio_ssh)

        # Executa o comando para descompactar o arquivo no servidor
        Log.imprime("INICIANDO PROCESSO DE DESCOMPACTACAO DO ZIP NO DESTINO")
        comando_unzip = "unzip -l " + self.diretorio_ssh + "/" + arquivo_zip + " -d " + self.diretorio_ssh
        ssh.executar_comando(comando_unzip)
        comando_unzip = "unzip -o " + self.diretorio_ssh + "/" + arquivo_zip + " -d " + self.diretorio_ssh
        ssh.executar_comando(comando_unzip)
        Log.imprime("PROCESSO DE DESCOMPACTACAO ENCERRADO COM SUCESSO")

        ssh.executar_comando("rm " + self.diretorio_ssh + "/" + arquivo_zip)

        # Fecha a conexao
        ssh.fechar_conexao()

        Log.imprime("DEPLOY ENCERRADO COM SUCESSO", "DEPLOY ENCERRADO COM SUCESSO")
