# coding=utf-8

import os

from python.tipos_arquivos.arquivo_properties import ArquivoProperties

nome_equipe = os.getenv("NOME_EQUIPE")
nome_projeto = os.getenv("NOME_PROJETO")

arquivo_properties = "gerador_pipelines_go/properties/%s_%s.properties" % (nome_equipe, nome_projeto)
properties = ArquivoProperties(arquivo_properties)
valores = properties.carregar_properties_para_dicionario()

template = "gerador_pipelines_go/templates/%s.xml" % nome_equipe


def carregar_template(arquivo, dict_valores=None):
    if dict_valores is None:
        dict_valores = {}
    with open(arquivo, 'r') as fp:
        conteudo = fp.read()
        for chave, valor in dict_valores.items():
            conteudo = conteudo.replace("[%s]" % chave, valor)
    return conteudo


conteudo_xml = carregar_template(template, valores)
print("########################################################")
print(conteudo_xml)
print("########################################################")
xml_pipeline = "pipeline_%s.xml" % nome_projeto
with open(xml_pipeline, "w") as saida:
    saida.write(conteudo_xml)
print("Conteudo salvo no arquivo: ", xml_pipeline)
