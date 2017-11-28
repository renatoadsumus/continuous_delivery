import json
from traceback import format_exc

from pymongo.collection import Collection

from python.assistentes.log import Log


class Operacoes:
    @staticmethod
    def inserir_json(colecao, string_json):
        if not isinstance(colecao, Collection):
            Log.imprime("VARIAVEL colecao NAO E DO TIPO COLLECTION.\nVALOR OBTIDO: " + str(type(colecao)),
                        "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(1)
        if not string_json:
            Log.imprime("VARIAVEL DA STRING DE INSERCAO VAZIA.", "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(2)
        if string_json == "{}":
            Log.imprime("A STRING DE INSERCAO ESTA VAZIA.", "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(3)
        try:
            documento_json = json.loads(string_json)
            retorno = colecao.insert_one(documento_json)
            if retorno.inserted_id:
                Log.imprime("DOCUMENTO INSERIDO COM SUCESSO.\nDOCUMENTO: " + string_json)
                return True
            else:
                Log.imprime("O DOCUMENTO NAO FOI INSERIDO POR CAUSA DE ALGUM PROBLEMA NAO IDENTIFICADO.",
                            "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            return False
        except ValueError:
            Log.imprime("A STRING DE INSERCAO NAO E UM JSON.\nVALOR OBTIDO: " + str(string_json) + "\n" + format_exc(),
                        "ERRO DE OPERACAO NO MONGODB", classe=Operacoes)
            exit(4)
        except TypeError:
            Log.imprime("A INSERCAO NAO FOI COMPLETADA\n" + format_exc(), "ERRO DE OPERACAO NO MONGODB",
                        classe=Operacoes)
            exit(5)

    @staticmethod
    def alterar_json(colecao, string_busca_json, string_nova_json, operador="set"):
        if not isinstance(colecao, Collection):
            Log.imprime("VARIAVEL colecao NAO E DO TIPO COLLECTION.\nVALOR OBTIDO: " + str(type(colecao)),
                        "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(1)
        if not string_busca_json:
            Log.imprime("VARIAVEL DA STRING DE BUSCA VAZIA.", "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(2)
        if not string_nova_json:
            Log.imprime("VARIAVEL DA STRING DE ALTERACAO VAZIA.", "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(3)
        if string_busca_json == "{}":
            Log.imprime("BUSCA VAZIA.", "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(4)
        if string_nova_json == "{}":
            Log.imprime("JSON DE ALTERACAO VAZIO.", "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(5)
        try:
            documento_busca_json = json.loads(string_busca_json)
            documento_novo_json = json.loads(string_nova_json)
            retorno = colecao.update_one(documento_busca_json, {"$" + operador: documento_novo_json})
            if retorno.modified_count == 1:
                Log.imprime("DOCUMENTO ALTERADO COM SUCESSO.\nALTERACOES FEITAS: " + str(string_nova_json))
                return True
            else:
                Log.imprime("NENHUM DOCUMENTO FOI ALTERADO.\nSTRING DE ALTERACAO: " + str(string_nova_json),
                            classe=Operacoes)
                return False
        except ValueError:
            Log.imprime("STRING DE ALTERACAO NAO ESTA NO FORMATO JSON.\nVALOR OBTIDO: " + str(string_nova_json) +
                        "\n" + format_exc(), "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(6)
        except TypeError:
            Log.imprime("OCORREU UM ERRO DURANTE A ALTERACAO\n" + format_exc(), "ERRO DE OPERACAO NO MONGODB.",
                        classe=Operacoes)
            exit(7)

    @staticmethod
    def excluir_json(colecao, string_busca_json):
        if not isinstance(colecao, Collection):
            Log.imprime("VARIAVEL colecao NAO E DO TIPO COLLECTION.\nVALOR OBTIDO: " + str(type(colecao)),
                        "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(1)
        if not string_busca_json:
            Log.imprime("VARIAVEL DA STRING DE BUSCA VAZIA.", "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(2)
        if string_busca_json == "{}":
            Log.imprime("BUSCA VAZIA.", "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(3)
        try:
            documento_busca_json = json.loads(string_busca_json)
            retorno = colecao.delete_one(documento_busca_json)
            if retorno.deleted_count == 1:
                Log.imprime("DOCUMENTO EXCLUIDO COM SUCESSO")
                return True
            else:
                Log.imprime("NENHUM DOCUMENTO FOI EXCLUIDO", classe=Operacoes)
                return False
        except ValueError:
            Log.imprime("STRING DE BUSCA NAO ESTA NO FORMATO JSON.\nVALOR OBTIDO: " + str(string_busca_json) +
                        "\n" + format_exc(), "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(4)
        except TypeError:
            Log.imprime("OCORREU UM ERRO DURANTE A EXCLUSAO\n" + format_exc(), "ERRO DE OPERACAO NO MONGODB.",
                        classe=Operacoes)
            exit(5)

    @staticmethod
    def buscar_json(colecao, string_busca_json):
        if not isinstance(colecao, Collection):
            Log.imprime("VARIAVEL colecao NAO E DO TIPO COLLECTION.\nVALOR OBTIDO: " + str(type(colecao)),
                        "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(1)
        if not string_busca_json:
            Log.imprime("VARIAVEL DA STRING DE BUSCA VAZIA.", "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(2)
        if string_busca_json == "{}":
            Log.imprime("BUSCA VAZIA.", "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(3)
        try:
            documento_busca_json = json.loads(string_busca_json)
            documentos_encontrados = colecao.find(documento_busca_json)
            return documentos_encontrados
        except ValueError:
            Log.imprime("STRING DE BUSCA NAO ESTA NO FORMATO JSON.\nVALOR OBTIDO: " + str(string_busca_json) +
                        "\n" + format_exc(), "ERRO DE OPERACAO NO MONGODB.", classe=Operacoes)
            exit(4)
        except TypeError:
            Log.imprime("OCORREU UM ERRO DURANTE A BUSCA\n" + format_exc(), "ERRO DE OPERACAO NO MONGODB.",
                        classe=Operacoes)
            exit(5)
