# coding=utf-8

import smtplib
import unittest
from io import StringIO

from mock import Mock

from python.envio_email.envio_email import Email

__author__ = 'ssouza'


class TestesEnvioEmail(unittest.TestCase):
    def setUp(self):
        smtplib.SMTP = Mock('smtplib.SMTP')
        smtplib.SMTP.mock_returns = Mock('smtp_connection')
        self.email = Email()
        self.out = StringIO()

    def tearDown(self):
        self.email = None
        self.out = None

    def teste_enviar_email_com_sucesso(self):
        resultado_esperado = "Email enviado para: ['samanta.souza@infoglobo.com.br']"
        self.email.enviar_email("Email Teste", "samanta.souza@infoglobo.com.br",
                                "E-mail de teste unitário", out=self.out)
        resultado_recebido = self.out.getvalue().strip()
        assert resultado_recebido == resultado_esperado


if __name__ == '__main__':
    unittest.main()
