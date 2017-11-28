import unittest
from os import stat, remove, environ
from shutil import copyfile

from python.scripts.bancoDados import BancoDados
from python.settings import WORKING_DIRECTORY


class TestesBancoDados(unittest.TestCase):
    @classmethod
    def setUp(cls):
        environ["NOME_BANCO"] = "DEV_INFG_CelulaQualidade_DSV"
        environ["USUARIO_BANCO"] = "DEV_INFG_Jenkins"
        environ["SENHA_BANCO"] = "95QlyafTZ2s8"
        environ["SERVIDOR_PORTA"] = "INFOSQLDSV"
        environ["PASTA_SCRIPT_SQL"] = "scripts\stg"
        environ["USUARIO_APLICAO_ACESSO_BANCO"] = "backup_Tempo_real"
        environ["AMBIENTE_SVN"] = "STG_TRUNK"
        environ["CAMINHO_MDF_LDF"] = "D:\\Program Files\\Microsoft SQL Server\\MSSQL10.MSSQLSERVER\\MSSQL\\DATA\\"
        environ["CAMINHO_GRAVAR_SNAPSHOT"] = "E:\\Snapshots\\"
        environ["SERVIDOR_PORTA_STG"] = "INFOSQLDSV"

        environ["NOME_BANCO_STG"] = "DEV_INFG_CelulaQualidade_HOM"
        environ["NOME_BANCO_LOGICO"] = "DEV_INFG_CelulaQualidade_HOM"

        banco_dados_prd = BancoDados()
        banco_dados_prd.restaurar_banco_dados_com_ultima_versao_stg()

        environ["NOME_BANCO_STG"] = "DEV_INFG_CelulaQualidade_DSV"
        environ["NOME_BANCO_LOGICO"] = "DEV_INFG_CelulaQualidade_DSV"

        banco_dados_stg = BancoDados()
        banco_dados_stg.restaurar_banco_dados_com_ultima_versao_stg()

    def test_restaurar_backup_de_uma_base_existente(self):

        banco_dados_stg = BancoDados()

        # Quando tento criar o backup do banco E tento restaurar
        banco_dados_stg.criar_backup()
        banco_dados_stg.restaurar_banco_dados_com_ultima_versao_stg()

        # Entao verifico que o arquivo de backup foi criado
        resultado_esperado = 'successfully' in open('log_comandoCriarBackup.txt').read()
        self.assertTrue(resultado_esperado)

        # Entao banco de dados e colocado em Offline
        tamanho_arquivo_log = stat("log_comandoSetOffLine.txt").st_size
        self.assertTrue(tamanho_arquivo_log == 0)

        # Entao o backup é restaurado com sucesso
        resultado_atual = False
        if 'processed' in open('log_comandoRestaurarBackup.txt').read():
            resultado_atual = True

        self.assertTrue(resultado_atual)

        # Então banco de dados e colocado em Online
        tamanho_arquivo_log = stat("log_comandoSetOnLine.txt").st_size
        self.assertTrue(tamanho_arquivo_log == 0)

    def test_restaurar_backup_de_prd_em_uma_base_stg(self):
        environ["USUARIO_BANCO"] = "INFG_Jenkins"
        environ["SENHA_BANCO"] = "95QlyafTZ2s8"
        environ["NOME_BANCO"] = "INFG_CelulaQualidade_DSV"
        environ["NOME_BANCO_LOGICO"] = "INFG_CelulaQualidade_DSV"
        environ["USUARIO_APLICAO_ACESSO_BANCO"] = "INFG_CelulaQualidade_DSV"
        banco_dados_stg = BancoDados()

        # Quando tento criar o backup do banco E tento restaurar
        banco_dados_stg.restaurar_banco_dados_stg_com_ultima_versao_prd()

        # Entao verifico que o arquivo de backup foi criado
        resultado_esperado = 'successfully' in open('log_comandoCriarBackup.txt').read()
        self.assertTrue(resultado_esperado)

        # Entao banco de dados e colocado em Offline
        tamanho_arquivo_log = stat("log_comandoSetOffLine.txt").st_size
        self.assertTrue(tamanho_arquivo_log == 0)

        # Entao o backup é restaurado com sucesso
        resultado_atual = False
        if 'processed' in open('log_comandoRestaurarBackup.txt').read():
            resultado_atual = True

        self.assertTrue(resultado_atual)

        # Então banco de dados e colocado em Online
        tamanho_arquivo_log = stat("log_comandoSetOnLine.txt").st_size
        self.assertTrue(tamanho_arquivo_log == 0)

        environ["NOME_BANCO_STG"] = "DEV_INFG_CelulaQualidade_DSV"
        environ["NOME_BANCO_LOGICO"] = "DEV_INFG_CelulaQualidade_DSV"
        banco_dados_stg = BancoDados()

        # Removendo arquivo de bkp gerado pelo restaurar_banco_dados_stg_com_ultima_versao_prd() e
        # substituindo pelo backup com os dados anteriores ao processo para nao afetar os demais testes.
        arquivo_backup_atual = banco_dados_stg.CAMINHO_ARQUIVO_BACKUP + "DEV_INFG_CelulaQualidade_DSV-devops.bak"
        arquivo_backup_baseline = banco_dados_stg.CAMINHO_ARQUIVO_BACKUP + "DEV_INFG_CelulaQualidade_DSV-baseline.bak"
        remove(arquivo_backup_atual)
        copyfile(arquivo_backup_baseline, arquivo_backup_atual)

        banco_dados_stg.restaurar_banco_dados_com_ultima_versao_stg()

    def test_nao_em_criar_backup_para_banco_dados_inexistente(self):

        # Dado que nao exista a base de dados DEV_INFG_CelulaQualidade_ERRO
        environ["NOME_BANCO_STG"] = "DEV_INFG_CelulaQualidade_ERRO"

        # Quando tento criar o backup do banco
        banco_dados = BancoDados()

        with self.assertRaises(SystemExit) as error:
            banco_dados.criar_backup()

        # Entao recebo Exception 1
        self.assertEqual(1, error.exception.code, " Houve um ERRO EXIT diferente de 1 ")

    def test_executar_com_sucesso__novos_script_sql_no_banco_dados_producao(self):

        print("Quando executo os scripts SQL em STG")
        environ["NOME_BANCO"] = "DEV_INFG_CelulaQualidade_DSV"
        banco_dados_stg = BancoDados()
        banco_dados_stg.executar_script_sql_no_banco_dados()

        print("Então verifico que as versoes de STG Trunk e da pasta testes\scripts\stg sao iguais")
        versao_implantada_esperada = "1.2"
        versao_implantada_atual_stg = banco_dados_stg.obter_versao("INFOSQLDSV", "DEV_INFG_Jenkins",
                                                                   "DEV_INFG_CelulaQualidade_DSV", "95QlyafTZ2s8")

        self.assertEquals(versao_implantada_esperada, versao_implantada_atual_stg)

        print("Dado que nao tenha executado os scripts SQLs na base de PRD")
        environ["AMBIENTE_SVN"] = "PRD_TRUNK"
        environ["NOME_BANCO_STG"] = "DEV_INFG_CelulaQualidade_DSV"
        environ["NOME_BANCO"] = "DEV_INFG_CelulaQualidade_HOM"

        print("Quando executo os scripts SQL em PRD")
        banco_dados_prd = BancoDados()
        banco_dados_prd.executar_script_sql_no_banco_dados()

        # Entao verifico que as versoes de STG e PRD sao iguais
        versao_implantada_esperada = "1.2"
        versao_implantada_atual_prd = banco_dados_prd.obter_versao("INFOSQLDSV", "DEV_INFG_Jenkins",
                                                                   "DEV_INFG_CelulaQualidade_HOM", "95QlyafTZ2s8")

        self.assertEquals(versao_implantada_esperada, versao_implantada_atual_prd)

    def test_executar_com_sucesso_novos_script_sql_no_banco_dados_staging_com_snapshot(self):
        # Dado que eu tenha baixado os scripts sql no
        print("Quando executo os scripts SQL em STG")
        banco_dados = BancoDados()
        banco_dados.executar_script_sql_no_banco_dados()

        print("Então verifico que a versao so svn eh igual do banco de STG Trunk")
        versao_esperada = "1.2"
        versao_atual = banco_dados.obter_versao_svn()

        self.assertEquals(versao_esperada, versao_atual)

    def test_executar_com_sucesso_novos_script_sql_no_banco_dados_staging_sem_snapshot(self):
        del environ["USUARIO_APLICAO_ACESSO_BANCO"]
        # Dado que eu tenha baixado os scripts sql no
        print("Quando executo os scripts SQL em STG")
        banco_dados = BancoDados()
        banco_dados.executar_script_sql_no_banco_dados()

        print("Então verifico que a versao so svn eh igual do banco de STG Trunk")
        versao_esperada = "1.2"
        versao_atual = banco_dados.obter_versao_svn()

        self.assertEquals(versao_esperada, versao_atual)

    def test_criar_com_sucesso_e_remover_snapshot_de_um_banco_existente(self):

        # Dado que nao possua um snapshot com o nome DEV_INFG_MOTOR_SNAPSHOT
        environ["NOME_BANCO"] = "DEV_INFG_CelulaQualidade_HOM"
        banco_dados = BancoDados()

        # Quando tento criar o snapshot
        banco_dados.criar_snapshot()

        # Entao o mesmo foi criado com sucesso
        tamanho_arquivo_log = stat("log_comandoCriarSnapshot.txt").st_size
        self.assertTrue(tamanho_arquivo_log == 0)

        # Quando tento remover o snapshot
        banco_dados.remover_snapshot()

        # Entao o mesmo foi removido com sucesso
        tamanho_arquivo_log = stat("log_comandoRemoverSnapshot.txt").st_size
        self.assertTrue(tamanho_arquivo_log == 0)

    def test_nao_criar_dois_snapshot_com_mesmo_nome(self):

        # Dado que possua um snapshot com o nome DEV_INFG_MOTOR_SNAPSHOT
        environ["NOME_BANCO"] = "DEV_INFG_CelulaQualidade_HOM"
        banco_dados = BancoDados()
        banco_dados.criar_snapshot()

        # Quando tento criar um novo snapshot com mesmo nome DEV_INFG_MOTOR_SNAPSHOT
        with self.assertRaises(SystemExit) as error:
            banco_dados.criar_snapshot()

        # Entao recebo Exception 1
        banco_dados.remover_snapshot()
        self.assertEqual(1, error.exception.code, " Houve um ERRP EXIT diferente de 1")

    def test_realizar_failback_de_um_snapshot_criado_com_sucesso_ja_com_a_tabela_migrate_existente(self):

        print("Dado que eu tenha no Banco as tabelas migrate e branch")
        print("Quando executo os scripts SQL em STG")
        environ["NOME_BANCO"] = "DEV_INFG_CelulaQualidade_HOM"
        banco_dados = BancoDados()
        banco_dados.criar_snapshot()
        banco_dados.executar_script_sql_no_banco_dados()

        print("E tento realizar Failback")
        banco_dados.realizar_failback_no_banco_dados()

        print("Entao verifico que o failback foi realizado com sucesso")
        versao_implantada_esperada = "1"
        versao_implantada_atual_prd = banco_dados.obter_versao("INFOSQLDSV", "DEV_INFG_Jenkins",
                                                               "DEV_INFG_CelulaQualidade_HOM", "95QlyafTZ2s8")
        self.assertEquals(versao_implantada_esperada, versao_implantada_atual_prd)

    def test_obter_versao_svn_com_um_numero_na_segunda_parte(self):

        arq = open(WORKING_DIRECTORY + "\\scripts\\stg\\V1_2__ScriptTesteUnitario.sql", "w")
        arq.close()
        arq = open(WORKING_DIRECTORY + "\\scripts\\stg\\V1_9__ScriptTesteUnitario.sql", "w")
        arq.close()

        banco_dados = BancoDados()
        resultado_atual = banco_dados.obter_versao_svn()
        resultado_esperado = '1.9'
        self.assertEqual(resultado_esperado, resultado_atual)

        remove(WORKING_DIRECTORY + "\\scripts\\stg\\V1_2__ScriptTesteUnitario.sql")
        remove(WORKING_DIRECTORY + "\\scripts\\stg\\V1_9__ScriptTesteUnitario.sql")

    def test_criar_tabela_schema_migrate(self):

        environ["NOME_BANCO"] = "DEV_INFG_CelulaQualidade_DSV"

        # Dado que na base ainda não tenha a tabela schema_migrate criado
        # Quando executo o flayway para criar a tabela schema_migrate
        banco_dados = BancoDados()
        resultado_atual = banco_dados.criar_tabelas_necessarias_para_flyway()
        # Então verifico que a tabela foi criada com sucesso
        self.assertTrue(resultado_atual)

    def test_obter_versao_svn_com_dois_numeros_na_segunda_parte(self):
        arq = open(WORKING_DIRECTORY + "\\scripts\\stg\\V1_2__ScriptTesteUnitario.sql", "w")
        arq.close()
        arq = open(WORKING_DIRECTORY + "\\scripts\\stg\\V1_9__ScriptTesteUnitario.sql", "w")
        arq.close()
        arq = open(WORKING_DIRECTORY + "\\scripts\\stg\\V1_10__ScriptTesteUnitario.sql", "w")
        arq.close()

        banco_dados = BancoDados()
        resultado_atual = banco_dados.obter_versao_svn()

        resultado_esperado = '1.10'
        self.assertEqual(resultado_esperado, resultado_atual)

        remove(WORKING_DIRECTORY + "\\scripts\\stg\\V1_2__ScriptTesteUnitario.sql")
        remove(WORKING_DIRECTORY + "\\scripts\\stg\\V1_9__ScriptTesteUnitario.sql")
        remove(WORKING_DIRECTORY + "\\scripts\\stg\\V1_10__ScriptTesteUnitario.sql")

    def test_nao_executar_comando_sql_com_a_pasta_de_sql_vazia(self):
        environ["PASTA_SCRIPT_SQL"] = "scripts\stg_sem_sql"

        banco_dados = BancoDados()
        resultado_atual = banco_dados.executar_script_sql_no_banco_dados()
        resultado_esperado = "NENJUM_SQL_NA_PASTA"
        self.assertEquals(resultado_esperado, resultado_atual)


if __name__ == '__main__':
    unittest.main()
