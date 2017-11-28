# coding=utf-8

import xml.etree.ElementTree as XmlTree
from xml.etree import ElementTree

__author__ = 'ssouza'


class ArquivoXML(object):
    def __init__(self, diretorio_arquivo, xml_namespace=None):
        self.diretorio_arquivo = diretorio_arquivo
        self.xml = XmlTree.parse(diretorio_arquivo)
        self.xml_root = self.xml.getroot()
        if xml_namespace is not None:
            ElementTree.register_namespace("", xml_namespace)

    def obter_valor_xpath(self, xpath, lista_filhos=None):
        if lista_filhos is None:
            return self.xml_root.find(xpath).text
        else:
            pai = self.xml_root.find(xpath)
            lista_filhos[0] = pai.find(lista_filhos[0])
            x = 1
            tamanho_lista = len(lista_filhos)
            elemento = ""
            while x <= (tamanho_lista - 1):
                lista_filhos[x] = lista_filhos[x - 1].find(lista_filhos[x])
                elemento = lista_filhos[x]
                x += 1
            return elemento.text

    def alterar_valor_xpath(self, xpath, versao):
        self.xml_root.find(xpath).text = versao
        self.xml.write(self.diretorio_arquivo)

    def quantidade_elementos(self, xpath):
        return len(self.xml_root.findall(xpath))

    def obter_valor_atributo(self, xpath_elemento, atributo):
        return self.xml_root.findall(xpath_elemento)[0].get(atributo)

    def obter_elemento_via_nome(self, nome_elemento):
        return self.xml_root.findtext(nome_elemento)

