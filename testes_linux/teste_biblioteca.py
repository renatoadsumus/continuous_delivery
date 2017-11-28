# coding=utf-8

import unittest

import mock
from mock import MagicMock

from python.biblioteca import Builders
from python.fabrica_objetos import FabricaObjetos

__author__ = 'ssouza'


@mock.patch("python.builders.maven.Maven")
class TestesBiblioteca(unittest.TestCase):
    def teste_get_versao_builder_maven(self, maven):
        maven.get_versao = MagicMock(return_value="1.5.0")
        FabricaObjetos.atribuir_maven(maven)
        resultado_esperado = '1.5.0'
        builder = Builders()
        resultado_atual = builder.get_versao()
        self.assertEqual(resultado_esperado, resultado_atual)


if __name__ == '__main__':
    unittest.main()
