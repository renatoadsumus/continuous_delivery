# coding=utf-8

import unittest

from freezegun import freeze_time

from python.assistentes.manipulador_data_hora import ManipuladorDataHora

__author__ = 'ssouza'


@freeze_time("2016-01-01")
class TestesManipuladorDataHora(unittest.TestCase):

    def teste_get_data_hora_atual(self):
        resultado_esperado = '"2016-01-01 00:00:00"'
        resultado_atual = ManipuladorDataHora.obter_data_hora_atual()
        self.assertEqual(resultado_esperado, resultado_atual)

    def teste_obter_horario_incrementada(self):
        resultado_esperado = "10:10"
        hora_incrementada = ManipuladorDataHora.obter_hora_incrementada(minutos=10, horas=10)
        self.assertEqual(resultado_esperado, hora_incrementada)

    def teste_obter_hora(self):
        resultado_esperado = "00:00"
        hora = ManipuladorDataHora.obter_hora_atual()
        self.assertEqual(resultado_esperado, hora)

    def teste_obter_data(self):
        resultado_esperado = "01/01/2016"
        data = ManipuladorDataHora.obter_data_atual()
        self.assertEqual(resultado_esperado, data)

    def teste_validacao_data(self):
        data = ManipuladorDataHora.obter_data_hora_atual()
        validador = ManipuladorDataHora.validar_formato_data(data, '"\d{4}-\d{2}-\d{2} \d{2}\:\d{2}\:\d{2}"')
        self.assertTrue(validador, msg="Formato de data invalido")

if __name__ == '__main__':
    unittest.main()
