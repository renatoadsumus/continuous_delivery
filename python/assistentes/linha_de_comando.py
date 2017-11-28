# -*- coding: utf-8 -*-
import subprocess

from python.assistentes.log import Log


class LinhaDeComando:

    @staticmethod
    def executar(command, retornar_exit_code=None):
        retorno = subprocess.call(command, shell=True, stderr=subprocess.STDOUT)
        Log.imprime("EXECUTANDO COMANDO: " + command)
        if not retornar_exit_code:
            if not (retorno == 0):
                Log.imprime("ERRO NA EXECUCAO DO COMANDO.\nRETORNO: " + str(retorno),
                            "ERRO NA EXECUCAO DO COMANDO", classe=LinhaDeComando)
                exit(retorno)
        return retorno

    @staticmethod
    def executar_com_output(comando):
        retorno = subprocess.Popen(comando, stdout=subprocess.PIPE, shell=True, stderr=subprocess.STDOUT)
        Log.imprime("EXECUTANDO COMANDO: " + comando)
        output_tupla = retorno.communicate()
        output_string = output_tupla[0].decode()
        Log.imprime("RETORNO DO COMANDO: " + output_string)
        return output_string

    @staticmethod
    def lancar_erro(mensagem=None):
        if mensagem is not None:
            Log.imprime("MENSAGEM DE ERRO:\n" + mensagem)
        exit(1)
