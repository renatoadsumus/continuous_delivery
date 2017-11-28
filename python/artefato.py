# coding=utf-8

from abc import ABCMeta, abstractmethod

__author__ = 'ssouza'


class Artefato:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_versao(self):
        pass

    @abstractmethod
    def get_atributos(self):
        pass

    @abstractmethod
    def executa_testes(self):
        pass

    @abstractmethod
    def fechar_artefato(self):
        pass

    @abstractmethod
    def executa_scanner_sonar(self):
        pass
