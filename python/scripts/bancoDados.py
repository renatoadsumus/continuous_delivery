import pymssql
from os import listdir, stat, getenv, path, remove
from sys import argv
from time import sleep

from python.assistentes.linha_de_comando import LinhaDeComando
from python.assistentes.log import Log
from python.envio_email.envio_email import Email
from python.settings import DESTINATARIOS_EMAIL, WORKING_DIRECTORY


class BancoDados(object):
    def __init__(self):
        self.NOME_BANCO = getenv("NOME_BANCO")
        self.NOME_BANCO_STG = getenv("NOME_BANCO_STG")
        self.USUARIO_BANCO = getenv("USUARIO_BANCO")
        self.SENHA_BANCO = getenv("SENHA_BANCO")
        self.SERVIDOR_PORTA = getenv("SERVIDOR_PORTA")
        self.PASTA_SCRIPT_SQL = getenv("PASTA_SCRIPT_SQL")
        # USUARIO USADO PELAS APLICACOES PARA ACESSAR O BANCO DE DADOS, POR EXEMPLO CADIN, GESTOR JURIDICO, INTRANET
        # self.USUARIO_APLICAO_ACESSO_BANCO = getenv("USUARIO_APLICAO_ACESSO_BANCO")
        if getenv("USUARIO_APLICAO_ACESSO_BANCO"):
            self.USUARIO_APLICAO_ACESSO_BANCO = list(getenv("USUARIO_APLICAO_ACESSO_BANCO").split(","))
        self.AMBIENTE_SVN = getenv("AMBIENTE_SVN")
        self.SERVIDOR_PORTA_STG = getenv("SERVIDOR_PORTA_STG")
        self.CAMINHO_ARQUIVO_BACKUP = "\\\\infojenkins1\\qa-gerenciador-artefatos-deploy\\banco-dados\\"

    @staticmethod
    def obter_versao(servidor, usuario, banco, senha):

        connection = pymssql.connect(host=servidor, user=usuario, password=senha, database=banco)
        cursor = connection.cursor()
        querie = "SELECT top 1 version FROM schema_migrate Order By installed_rank desc"
        cursor.execute(querie)
        row = cursor.fetchone()
        ultima_versao_publicada = row[0]
        connection.close()

        return ultima_versao_publicada

    def obter_versao_svn(self):
        versao_maior = "0.0"

        for file in listdir(WORKING_DIRECTORY + "/" + self.PASTA_SCRIPT_SQL):
            if file.endswith(".sql") and file.startswith("V"):
                versao_atual = "{}.{}".format(file.split("_")[0][1:], file.split("_")[1])

                if int(versao_atual.split(".")[0]) > int(versao_maior.split(".")[0]):
                    versao_maior = versao_atual
                elif int(versao_atual.split(".")[0]) == int(versao_maior.split(".")[0]):
                    if int(versao_atual.split(".")[1]) >= int(versao_maior.split(".")[1]):
                        versao_maior = versao_atual
        return versao_maior

    def __snapshot_foi_criado_com_sucesso(self):

        sleep(5)

        with open("log_comandoCriarSnapshot.txt", "r") as arq:
            if "already exists" in arq.read():
                return False
        try:
            nome_snapshot = self.NOME_BANCO + "_SNAPSHOT"
            pymssql.connect(host=self.SERVIDOR_PORTA, user=self.USUARIO_BANCO, password=self.SENHA_BANCO,
                            database=nome_snapshot)
            Log.imprime("SUCESSO - NA CRIACAO DO SNAPSHOT", "SUCESSO - NA CRIACAO DO SNAPSHOT")
            return True
        except:
            Log.imprime("FALHA - NA CRIACAO DO SNAPSHOT", "FALHA - NA CRIACAO DO SNAPSHOT")
            return False

    def executar_script_sql_no_banco_dados(self):
        self.criar_tabelas_necessarias_para_flyway()

        schema = "schema_migrate"

        if self.AMBIENTE_SVN == "STG_BRANCH":
            schema = "schema_branch"

        numero_scripts_sql = len(listdir(self.PASTA_SCRIPT_SQL))

        if numero_scripts_sql > 1:
            nome_banco_de_dados = "jtds:sqlserver://" + self.SERVIDOR_PORTA + "/" + self.NOME_BANCO
            caminho_sql = "filesystem:" + WORKING_DIRECTORY + "/" + self.PASTA_SCRIPT_SQL
            comando = "-user=" + self.USUARIO_BANCO + " -password=" + self.SENHA_BANCO + " -url=jdbc:" + \
                      nome_banco_de_dados + " -locations=" + caminho_sql + " -table=" + schema
            LinhaDeComando.executar("flyway migrate " + comando)
            sleep(2)
            Log.imprime("COMANDO EXECUATDO FLYWAY..:" + comando)
            LinhaDeComando.executar("flyway validate " + comando)
        else:
            Log.imprime("NAO FOI ENCONTRADO NENHUM SCRIPT SQL PARA SER EXECUTADO",
                        "NAO FOI ENCONTRADO NENHUM SCRIPT SQL PARA SER EXECUTADO")
            return "NENJUM_SQL_NA_PASTA"

    def restaurar_banco_dados_com_ultima_versao_stg(self):

        nome_banco_logico = getenv("NOME_BANCO_LOGICO")
        caminho_mdf_ldf = getenv("CAMINHO_MDF_LDF") + "{0}'"

        if not self.possui_backup():
            self.criar_backup()

        self.colocar_banco_dados_offline()

        comando_restaurar_backup = "restore database " + self.NOME_BANCO_STG + " from disk ='" + \
                                   self.CAMINHO_ARQUIVO_BACKUP + self.NOME_BANCO_STG + \
                                   "-devops.bak' with replace,stats, move '" + nome_banco_logico + "_data' to '" + \
                                   caminho_mdf_ldf.format(self.NOME_BANCO_STG + ".mdf") + ", move '" + \
                                   nome_banco_logico + "_log' to '" + caminho_mdf_ldf.format(self.NOME_BANCO_STG +
                                                                                             "_log.ldf")

        with open("comandoRestaurarBackup.sql", "w") as arq:
            arq.write(comando_restaurar_backup)

        LinhaDeComando.executar("sqlcmd -S " + self.SERVIDOR_PORTA_STG +
                                " -U DEV_INFG_Jenkins -P 95QlyafTZ2s8 -i comandoRestaurarBackup.sql "
                                "-o log_comandoRestaurarBackup.txt")

        falha_processo_restaurar_backup = False

        with open("log_comandoRestaurarBackup.txt", "r") as arq:
            if "processed" in arq.read():
                Log.imprime("SUCESSO - BACKUP RESTAURADO -" + self.NOME_BANCO_STG,
                            "SUCESSO - BACKUP RESTAURADO - " + self.NOME_BANCO_STG)
            else:
                falha_processo_restaurar_backup = True
                Log.imprime("FALHA - NO RESTORE DO BACKUP\n" + arq.read(),
                            "FALHA - NO RESTORE DO BACKUP", classe=BancoDados)

        sleep(5)

        comando_set_online = "alter database " + self.NOME_BANCO_STG + " set online"
        with open("comandoSetOnLine.sql", "w") as arq:
            arq.write(comando_set_online)

        LinhaDeComando.executar("sqlcmd -S " + self.SERVIDOR_PORTA_STG +
                                " -U DEV_INFG_Jenkins -P 95QlyafTZ2s8 -i comandoSetOnLine.sql "
                                "-o log_comandoSetOnLine.txt")

        tamanho_arquivo_log = stat("log_comandoSetOnLine.txt").st_size

        if tamanho_arquivo_log == 0:
            Log.imprime("SUCESSO - VOLTAR O BANCO DE STG ONLINE", "SUCESSO - VOLTAR O BANCO DE STG ONLINE")
        else:
            with open("log_comandoSetOnLine.txt", "r") as arq:
                Log.imprime("FALHA - VOLTAR O BANCO DE STG ONLINE\n" + arq.read(),
                            "FALHA - VOLTAR O BANCO DE STG ONLINE", classe=BancoDados)
            falha_processo_restaurar_backup = True

        if falha_processo_restaurar_backup:
            exit(1)

    def restaurar_banco_dados_stg_com_ultima_versao_prd(self):
        nome_banco_logico = getenv("NOME_BANCO_LOGICO")
        caminho_mdf_ldf = getenv("CAMINHO_MDF_LDF") + self.NOME_BANCO_STG

        self.criar_backup(prd=True)

        self.colocar_banco_dados_offline()

        falha_processo_restaurar_backup = False

        comando_restaurar_backup = "restore database " + self.NOME_BANCO_STG + " from disk ='" + \
                                   self.CAMINHO_ARQUIVO_BACKUP + self.NOME_BANCO + \
                                   "-devops.bak' with replace,stats, move '" + nome_banco_logico + "_data' to '" + \
                                   caminho_mdf_ldf + ".mdf', move '" + nome_banco_logico + "_log' to '" + \
                                   caminho_mdf_ldf + "_log.ldf'"
        with open("comandoRestaurarBackup.sql", "w") as arq:
            arq.write(comando_restaurar_backup)

        LinhaDeComando.executar("sqlcmd -S " + self.SERVIDOR_PORTA_STG +
                                " -U DEV_INFG_Jenkins -P 95QlyafTZ2s8 -i comandoRestaurarBackup.sql "
                                "-o log_comandoRestaurarBackup.txt")

        with open("log_comandoRestaurarBackup.txt", "r") as arq:
            if "processed" in arq.read():
                Log.imprime("SUCESSO - BACKUP RESTAURADO - " + self.NOME_BANCO,
                            "SUCESSO - BACKUP RESTAURADO - " + self.NOME_BANCO)
            else:
                falha_processo_restaurar_backup = True
                Log.imprime("FALHA - NO RESTORE DO BACKUP\n" + arq.read(),
                            "FALHA - NO RESTORE DO BACKUP", classe=BancoDados)
        sleep(5)

        comando_set_online = "alter database " + self.NOME_BANCO_STG + " set online"
        with open("comandoSetOnLine.sql", "w") as arq:
            arq.write(comando_set_online)

        LinhaDeComando.executar("sqlcmd -S " + self.SERVIDOR_PORTA_STG +
                                " -U DEV_INFG_Jenkins -P 95QlyafTZ2s8 -i comandoSetOnLine.sql "
                                "-o log_comandoSetOnLine.txt")

        tamanho_arquivo_log = stat("log_comandoSetOnLine.txt").st_size

        if tamanho_arquivo_log == 0:
            Log.imprime("SUCESSO - VOLTAR O BANCO DE STG ONLINE", "SUCESSO - VOLTAR O BANCO DE STG ONLINE")
        else:
            with open("log_comandoSetOnLine.txt", "r") as arq:
                Log.imprime("FALHA - VOLTAR O BANCO DE STG ONLINE\n" + arq.read(),
                            "FALHA - VOLTAR O BANCO DE STG ONLINE", classe=BancoDados)
            falha_processo_restaurar_backup = True

        comando_renomear_logical_names = "ALTER DATABASE " + self.NOME_BANCO_STG + " MODIFY FILE (NAME=N'" + \
                                         self.NOME_BANCO + "_data', NEWNAME=N'" + self.NOME_BANCO_STG + \
                                         "_data')\nGO\nALTER DATABASE " + self.NOME_BANCO_STG + \
                                         " MODIFY FILE (NAME=N'" + self.NOME_BANCO + "_log', NEWNAME=N'" + \
                                         self.NOME_BANCO_STG + "_log')\nGO\nALTER DATABASE " + self.NOME_BANCO_STG + \
                                         " set recovery simple;\nGO"

        with open("comandoRenomearLogicalNames.sql", "w") as arq:
            arq.write(comando_renomear_logical_names)

        LinhaDeComando.executar("sqlcmd -S " + self.SERVIDOR_PORTA_STG +
                                " -U DEV_INFG_Jenkins -P 95QlyafTZ2s8 -i comandoRenomearLogicalNames.sql "
                                "-o log_comandoRenomearLogicalNames.txt")

        with open("log_comandoRenomearLogicalNames.txt", "r") as arq:
            if "has been set" in arq.read():
                Log.imprime("SUCESSO - LOGICAL NAMES RENOMEAROS - " + self.NOME_BANCO,
                            "SUCESSO - LOGICAL NAMES RENOMEAROS - " + self.NOME_BANCO)
            else:
                falha_processo_restaurar_backup = True
                Log.imprime("FALHA - AO RENOMEAR LOGICAL NAMES\n" + arq.read(),
                            "FALHA - AO RENOMEAR LOGICAL NAMES", classe=BancoDados)

        comando_trocar_usuarios = "USE " + self.NOME_BANCO_STG + "\nGO\n"
        for usuario in self.USUARIO_APLICAO_ACESSO_BANCO:
            comando_trocar_usuarios += "exec sp_dropuser " + usuario + " ;\n"
        comando_trocar_usuarios += "exec sp_grantdbaccess DEV_" + self.USUARIO_APLICAO_ACESSO_BANCO[0] + \
                                   ";\nexec sp_grantdbaccess DEV_INFG_Jenkins;\n" \
                                   "exec sp_addrolemember 'db_owner', 'DEV_" + self.USUARIO_APLICAO_ACESSO_BANCO[0]\
                                   + "';\nexec sp_addrolemember 'db_owner', 'DEV_INFG_Jenkins';\n" \
                                     "exec sp_changedbowner 'sa';\nalter login DEV_" +\
                                   self.USUARIO_APLICAO_ACESSO_BANCO[0] + " enable;\nalter login DEV_" + \
                                   self.USUARIO_APLICAO_ACESSO_BANCO[0] + " with default_database = " + \
                                   self.NOME_BANCO_STG + ";"

        with open("comandoTrocarUsuarioPrdParaStg.sql", "w") as arq:
            arq.write(comando_trocar_usuarios)

        LinhaDeComando.executar("sqlcmd -S " + self.SERVIDOR_PORTA_STG +
                                " -U DEV_INFG_Jenkins -P 95QlyafTZ2s8 -i comandoTrocarUsuarioPrdParaStg.sql "
                                "-o log_comandoTrocarUsuarioPrdParaStg.txt")

        with open("log_comandoTrocarUsuarioPrdParaStg.txt", "r") as arq:
            if "Changed database context to '" + self.NOME_BANCO_STG + "'." in arq.read():
                Log.imprime("SUCESSO - USUARIOS TROCADOS DE PRD PARA STG - " + self.NOME_BANCO,
                            "SUCESSO - USUARIOS TROCADOS DE PRD PARA STG - " + self.NOME_BANCO)
            else:
                falha_processo_restaurar_backup = True
                Log.imprime("FALHA - AO TROCAR OS USUARIOS PRD PARA STG\n" + arq.read(),
                            "FALHA - AO TROCAR OS USUARIOS PRD PARA STG", classe=BancoDados)

        if falha_processo_restaurar_backup:
            exit(1)

        self.criar_backup(prd=False)
        
        remove(self.CAMINHO_ARQUIVO_BACKUP+ self.NOME_BANCO+".bak")

    def colocar_banco_dados_offline(self):
        comando_set_offline = "alter database " + self.NOME_BANCO_STG + " set offline with rollback immediate"

        with open("comandoSetOffLine.sql", "w") as arq:
            arq.write(comando_set_offline)

        LinhaDeComando.executar("sqlcmd -S " + self.SERVIDOR_PORTA_STG +
                                " -U  DEV_INFG_Jenkins -P 95QlyafTZ2s8 -i comandoSetOffLine.sql "
                                "-o log_comandoSetOffLine.txt")
        sleep(2)
        tamanho_arquivo_log = stat("log_comandoSetOffLine.txt").st_size

        with open("log_comandoSetOffLine.txt", "r") as arq:
            if "Estimated rollback completion: 100%." in arq.read():
                Log.imprime("SUCESSO - COLOCAR O BANCO DE STG OFFLINE", "SUCESSO - COLOCAR O BANCO DE STG OFFLINE")
            elif tamanho_arquivo_log == 0:
                Log.imprime("SUCESSO - COLOCAR O BANCO DE STG OFFLINE", "SUCESSO - COLOCAR O BANCO DE STG OFFLINE")
            else:
                Log.imprime("FALHA - COLOCAR O BANCO DE STG OFFLINE\n" + arq.read(),
                            "FALHA - COLOCAR O BANCO DE STG OFFLINE", classe=BancoDados)
                exit(1)

    def criar_backup(self, prd=False):
        if prd:
            conteudo_arquivo = "BACKUP DATABASE " + self.NOME_BANCO + " TO DISK = '" + self.CAMINHO_ARQUIVO_BACKUP + \
                               self.NOME_BANCO + "-devops.bak' with format, compression ;"
            comando = "sqlcmd -S " + self.SERVIDOR_PORTA + " -U " + self.USUARIO_BANCO + \
                      " -P " + self.SENHA_BANCO + " -i comandoCriarBackup.sql -o log_comandoCriarBackup.txt"
        else:
            conteudo_arquivo = "BACKUP DATABASE " + self.NOME_BANCO_STG + " TO DISK = '" + self.CAMINHO_ARQUIVO_BACKUP \
                               + self.NOME_BANCO_STG + "-devops.bak' with format, compression ;"
            comando = "sqlcmd -S " + self.SERVIDOR_PORTA_STG + " -U DEV_INFG_Jenkins -P 95QlyafTZ2s8 -i " \
                                                               "comandoCriarBackup.sql -o log_comandoCriarBackup.txt"

        with open("comandoCriarBackup.sql", "w") as arq:
            arq.write(conteudo_arquivo)
        LinhaDeComando.executar(comando)

        with open("log_comandoCriarBackup.txt", "r") as arq:
            if "successfully" in arq.read():
                Log.imprime("SUCESSO - CRIACAO DO BACKUP", "SUCESSO - CRIACAO DO BACKUP")
            else:
                Log.imprime("FALHA - CRIACAO DO BACKUP.\n" + arq.read(),
                            "FALHA - CRIACAO DO BACKUP", classe=BancoDados)
                exit(1)

    def criar_snapshot(self):

        self.__matar_todas_conexoes_no_banco_dados()

        caminho_snapshot = getenv("CAMINHO_GRAVAR_SNAPSHOT") + self.NOME_BANCO + "_snapshot.ss"

        comando = "CREATE DATABASE " + self.NOME_BANCO + "_SNAPSHOT  ON (  NAME = '" + self.NOME_BANCO + \
                  "_DATA', FILENAME ='" + caminho_snapshot + "') AS SNAPSHOT OF " + \
                  self.NOME_BANCO + " ;"
        with open("comandoCriarSnapshot.sql", "w") as arq:
            arq.write(comando)

        LinhaDeComando.executar("sqlcmd -S " + self.SERVIDOR_PORTA + " -U " + self.USUARIO_BANCO + " -P " +
                                self.SENHA_BANCO + " -i comandoCriarSnapshot.sql -o log_comandoCriarSnapshot.txt")

        if not self.__snapshot_foi_criado_com_sucesso():
            self.habiltar_usuario_aplicacao_acesso_banco_dados()
            Log.imprime("FALHA - JA EXISTE UM SNAPSHOT CRIADO PARA ESSE BANCO\n",
                        "FALHA - JA EXISTE UM SNAPSHOT CRIADO PARA ESSE BANCO\n"
                        "PRIMEIRO DEVE SER EXECUTADO O PASSO DE VALIDACAO DEPLOY", classe=BancoDados)
            exit(1)

    def remover_snapshot(self):

        nome_snapshot = self.NOME_BANCO + "_SNAPSHOT"
        with open("comandoRemoverSnapshot.sql", "w") as arq:
            arq.write("DROP DATABASE " + nome_snapshot + ";")

        LinhaDeComando.executar("sqlcmd -S " + self.SERVIDOR_PORTA + " -U " + self.USUARIO_BANCO + " -P " +
                                self.SENHA_BANCO + " -i comandoRemoverSnapshot.sql -o log_comandoRemoverSnapshot.txt")

        try:
            pymssql.connect(host=self.SERVIDOR_PORTA, user=self.USUARIO_BANCO, password=self.SENHA_BANCO,
                            database=nome_snapshot)
            with open("log_comandoRemoverSnapshot.txt", "r") as arq:
                Log.imprime("FALHA - NA REMOCAO DO SNAPSHOT\n" + arq.read(),
                            "FALHA - NA REMOCAO DO SNAPSHOT", classe=BancoDados)
            exit(1)
        except:
            mensagem_sucesso = "SUCESSO --  REMOVIDO -- " + nome_snapshot
            Log.imprime(mensagem_sucesso, mensagem_sucesso, classe=BancoDados)

            email = Email()
            email.enviar_email(mensagem_sucesso, DESTINATARIOS_EMAIL, mensagem_sucesso)

    def realizar_failback_no_banco_dados(self):

        self.__matar_todas_conexoes_no_banco_dados()

        comando = "RESTORE DATABASE " + self.NOME_BANCO + " FROM DATABASE_SNAPSHOT = '" + self.NOME_BANCO + \
                  "_SNAPSHOT';"

        with open("comandoFailBack.sql", "w") as arq:
            arq.write(comando)

        LinhaDeComando.executar("sqlcmd -S " + self.SERVIDOR_PORTA + " -U " + self.USUARIO_BANCO + " -P " +
                                self.SENHA_BANCO + " -i comandoFailBack.sql -o log_comandoFailBack.txt")

        with open("log_comandoFailBack.txt", "r") as arq:
            Log.imprime("REALIZANDO O FAILBACK\n" + arq.read(), "REALIZANDO O FAILBACK")

        self.habiltar_usuario_aplicacao_acesso_banco_dados()

        """info_banco_dados = InformacoesBancoDados(NOME_BANCO)
        versao_failback = info_banco_dados.obter_revision_deploy_prd_failback()
        ultima_versao_producao = obter_versao("INFOSQL:1433","INFG_Jenkins", NOME_BANCO ,"ANavpzv2CcfEMtcagaIY")

        if versao_failback == ultima_versao_producao:
            print("#################################################")
            print("## DEPLOY REALIZADO COM SUCESSO ##")
            print("## VERSAO PRD FAILBACK...: " + versao_failback + " ##")
            print("## VERSAO PRD ATUAL .....: " + ultima_versao_producao + " ##")
            print("#################################################")
        else:
            print("#################################################")
            print("## FALHA NO DEPLOY ##")
            print("## VERSAO PRD FAILBACK...: " + versao_failback + " ##")
            print("## VERSAO PRD ATUAL .....: " + ultima_versao_producao + " ##")
            print("#################################################")
            exit(1)"""

        self.remover_snapshot()

    def __matar_todas_conexoes_no_banco_dados(self):

        with open(path.dirname(__file__) + "\\..\\..\\sql\\comandoMatarTodasConexoesTemplate.sql", "r") as arq:
            arquivo_alterado = arq.read()

        arquivo_alterado = arquivo_alterado.replace("<LOGIN>", self.USUARIO_APLICAO_ACESSO_BANCO[0])
        arquivo_alterado = arquivo_alterado.replace("<BASE DE DADOS>", self.NOME_BANCO)

        with open("comandoMatarTodasConexoes.sql", "w") as arq:
            arq.write(arquivo_alterado)

        LinhaDeComando.executar("sqlcmd -S " + self.SERVIDOR_PORTA + " -U " + self.USUARIO_BANCO + " -P " +
                                self.SENHA_BANCO + " -i comandoMatarTodasConexoes.sql "
                                                   "-o log_comandoMatarTodasConexoes.txt")

        tamanho_arquivo_log = stat("log_comandoMatarTodasConexoes.txt").st_size

        if tamanho_arquivo_log == 0:
            Log.imprime("SUCESSO - FORAM CANCELADAS TODAS CONEXOES COM O BANCO DE DADOS",
                        "SUCESSO - FORAM CANCELADAS TODAS CONEXOES COM O BANCO DE DADOS")
        else:
            with open("log_comandoMatarTodasConexoes.txt", "r") as arq:
                Log.imprime("FALHA - AO CANCELAR AS CONEXOES DE ACESSO COM O BANCO DE DADOS\n" + arq.read(),
                            "FALHA - AO CANCELAR AS CONEXOES DE ACESSO COM O BANCO DE DADOS", classe=BancoDados)
            exit(1)

    def criar_tabelas_necessarias_para_flyway(self):

        if self.eh_um_banco_de_dados_novo():

            nome_banco_de_dados = "jtds:sqlserver://" + self.SERVIDOR_PORTA + "/" + self.NOME_BANCO
            comando = "-user=" + self.USUARIO_BANCO + " -password=" + self.SENHA_BANCO + " -url=jdbc:" + \
                      nome_banco_de_dados + " -table="
            LinhaDeComando.executar("flyway baseline " + comando + "schema_migrate")
            Log.imprime("TABELA MIGRATE CRIADA COM SUCESSO -" + self.NOME_BANCO,
                        "TABELA MIGRATE CRIADA COM SUCESSO -" + self.NOME_BANCO)

            if self.AMBIENTE_SVN != "PRD_TRUNK":
                LinhaDeComando.executar("flyway baseline " + comando + "schema_branch")
                Log.imprime("TABELA BRANCH CRIADA COM SUCESSO", "TABELA BRANCH CRIADA COM SUCESSO")
            return True

    def eh_um_banco_de_dados_novo(self):

        eh_um_banco_de_dados_novo = False

        connection = pymssql.connect(host=self.SERVIDOR_PORTA, user=self.USUARIO_BANCO, password=self.SENHA_BANCO,
                                     database=self.NOME_BANCO)
        cursor = connection.cursor()

        querie_usada_para_teste = "select * from schema_migrate"

        try:
            cursor.execute(querie_usada_para_teste)
            connection.close()
        except:
            mensagem_log = "O BANCO " + self.NOME_BANCO + " EH NOVO, AINDA SEM A TABELA MIGRATE"
            Log.imprime(mensagem_log, mensagem_log)
            eh_um_banco_de_dados_novo = True

        return eh_um_banco_de_dados_novo

    def possui_backup(self):
        existe_backup = False
        arquivo_backup = self.CAMINHO_ARQUIVO_BACKUP + self.NOME_BANCO_STG + "-devops.bak"
        if path.isfile(arquivo_backup):
            existe_backup = True
        return existe_backup

    def habiltar_usuario_aplicacao_acesso_banco_dados(self):

        with open("comandoHabiltarUsuarioAplicacaoAcessoBancoDados.sql", "w") as arq:
            arq.write("alter login " + self.USUARIO_APLICAO_ACESSO_BANCO[0] + " enable;")

        LinhaDeComando.executar("sqlcmd -S " + self.SERVIDOR_PORTA + " -U " + self.USUARIO_BANCO + " -P " +
                                self.SENHA_BANCO + " -i comandoHabiltarUsuarioAplicacaoAcessoBancoDados.sql "
                                                   "-o log_comandoHabiltarUsuarioAplicacaoAcessoBancoDados.txt")

        tamanho_arquivo_log = stat("log_comandoHabiltarUsuarioAplicacaoAcessoBancoDados.txt").st_size

        if tamanho_arquivo_log == 0:
            Log.imprime("SUCESSO - AO HABILITAR USUARIO DA APLICACAO COM ACESSO COM O BANCO DE DADOS",
                        "SUCESSO - AO HABILITAR USUARIO DA APLICACAO COM ACESSO COM O BANCO DE DADOS")
        else:
            with open("log_comandoHabiltarUsuarioAplicacaoAcessoBancoDados.txt", "r") as arq:
                Log.imprime("FALHA - AO HABILITAR USUARIO DA APLICACAO COM ACESSO COM O BANCO DE DADOS\n" + arq.read(),
                            "FALHA - AO HABILITAR USUARIO DA APLICACAO COM ACESSO COM O BANCO DE DADOS",
                            classe=BancoDados)
            exit(1)


if __name__ == "__main__":
    banco_dados = BancoDados()
    if argv[1] == "criarBackup":
        banco_dados.criar_backup()
    if argv[1] == "criarSnapshot":
        banco_dados.criar_snapshot()
    if argv[1] == "restaurarBaseEspelhoDeProducao":
        banco_dados.restaurar_banco_dados_com_ultima_versao_stg()
    if argv[1] == "restaurarBaseStagingComBkpDeProducao":
        banco_dados.restaurar_banco_dados_stg_com_ultima_versao_prd()
    if argv[1] == "executarScriptSQLNoBancoDados":
        banco_dados.executar_script_sql_no_banco_dados()
        Log.gerar_arquivo_log_logstash()
    if argv[1] == "habiltarUsuarioAplicacaoAcessoBancoDados":
        banco_dados.habiltar_usuario_aplicacao_acesso_banco_dados()
    if argv[1] == "removerSnapshot":
        banco_dados.remover_snapshot()
    if argv[1] == "realizarFailBack":
        banco_dados.realizar_failback_no_banco_dados()
        Log.gerar_arquivo_log_logstash()
