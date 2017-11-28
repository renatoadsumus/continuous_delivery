# coding=utf-8

from datetime import datetime, timedelta
from re import compile

__author__ = 'ssouza'


class ManipuladorDataHora:

    @staticmethod
    def obter_data_hora_atual():
        return datetime.now().strftime('"%Y-%m-%d %H:%M:%S"')

    @staticmethod
    def obter_hora_incrementada(horas=0, minutos=0):
        hora_atual = datetime.now()
        hora_incrementada = hora_atual + timedelta(hours=horas, minutes=minutos)
        return hora_incrementada.strftime("%H:%M")

    @staticmethod
    def obter_hora_atual():
        return datetime.now().strftime("%H:%M")

    @staticmethod
    def obter_data_atual():
        return datetime.now().strftime("%d/%m/%Y")

    @staticmethod
    def validar_formato_data(data, formato):
        padrao = compile(formato)
        if padrao.match(data) is not None:
            return True
        return False

if __name__ == "__main__":
    ManipuladorDataHora.obter_data_hora_atual()
