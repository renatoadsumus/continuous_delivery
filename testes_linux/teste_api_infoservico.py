# coding=utf-8

import unittest
from os import environ, path

from python.apis.api_infoservico import MudancaAutomatica
from python.settings import DESTINATARIOS_EMAIL


class TestesApiInfoServico(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        environ["CCTI_CLASS"] = "SUPORTE A HARDWARE"
        environ["CCTI_CATEGORY"] = "Switchs / Roteadores"
        environ["CCTI_TYPE"] = "Mudança"
        environ["CCTI_ITEM"] = "Hardware"
        environ["ID_FILA_EQUIPE"] = "50"
        # os.environ["TIPO_MUDANCA"] = "Normal"

    def test_criar_mudanca(self):
        mudanca = MudancaAutomatica()
        mudanca.destinatarios = DESTINATARIOS_EMAIL
        mudanca.caminho_templates = path.dirname(__file__) + "/templates/"
        resultado_mudanca_atual = mudanca.criar_mudanca_automatica()
        self.assertTrue(resultado_mudanca_atual.__contains__("200-"))

    def test_ler_resposta_de_sucesso_no_retorno(self):
        mensagem_retorno = "b'--MIMEBoundary_62f72e96e9c1b72112d7fbfe267877d966225f9af96aa5bb\r\nContent-Type: appli" \
                           "cation/xop+xml; charset=UTF-8; type=\"application/soap+xml\"\r\nContent-Transfer-Encodin" \
                           "g: binary\r\nContent-ID: <0.12f72e96e9c1b72112d7fbfe267877d966225f9af96aa5bb@apache.org>" \
                           "\r\n\r\n<?xml version=\'1.0\' encoding=\'UTF-8\'?><soapenv:Envelope xmlns:soapenv=\"http" \
                           "://www.w3.org/2003/05/soap-envelope\"><soapenv:Body><ns:createChangeRequestResponse xmln" \
                           "s:ns=\"http://wrappers.webservice.appservices.core.inteqnet.com\"><ns:return xmlns:ax212" \
                           "=\"http://beans.webservice.components.inteqnet.com/xsd\" xmlns:ax210=\"http://beans.webs" \
                           "ervice.appservices.core.inteqnet.com/xsd\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-" \
                           "instance\" xsi:type=\"ax212:DefaultServiceResponse\"><ax212:errors></ax212:errors><ax212" \
                           ":notes>An unsupported JSON? response output format was requested by the web service clie" \
                           "nt. The output response is being returned in the default format of XML configured for th" \
                           "e web service: ChangeRequest.createChangeRequest</ax212:notes><ax212:resourceName></ax21" \
                           "2:resourceName><ax212:responseBean xsi:type=\"ax212:Bean\"/><ax212:responseFormat>XML</a" \
                           "x212:responseFormat><ax212:responseStatus>OK</ax212:responseStatus><ax212:responseText>&" \
                           "lt;?xml version=\"1.0\" encoding=\"UTF-8\"?>&#xd;\n&lt;records>&lt;record>&lt;item_id>&l" \
                           "t;![CDATA[31679]]&gt;&lt;/item_id>&lt;ticket_identifier>&lt;![CDATA[200-2239]]&gt;&lt;/t" \
                           "icket_identifier>&lt;/record>&lt;/records>&#xd;\n</ax212:responseText><ax212:statusCode>" \
                           "000</ax212:statusCode><ax212:statusMessage>Success: The request was successfully fulfill" \
                           "ed by the server; the service returned results of the operation.</ax212:statusMessage><a" \
                           "x212:warnings></ax212:warnings></ns:return></ns:createChangeRequestResponse></soapenv:Bo" \
                           "dy></soapenv:Envelope>\r\n--MIMEBoundary_62f72e96e9c1b72112d7fbfe267877d966225f9af96aa5b" \
                           "b--\r\n'"
        mudanca = MudancaAutomatica()
        mudanca.destinatarios = DESTINATARIOS_EMAIL
        resultado_atual = mudanca.obter_numero_mudanca_criada(mensagem_retorno)
        self.assertTrue(resultado_atual.__contains__("200-"))

    def test_ler_resposta_de_falha_no_retorno(self):
        mensagem_retorno = "b'--MIMEBoundary_94dd4e96e9c1b7211afc1575267877d911905f9af96aa5bb\r\nContent-Type: appli" \
                           "cation/xop+xml; charset=UTF-8; type=\"application/soap+xml\"\r\nContent-Transfer-Encodin" \
                           "g: binary\r\nContent-ID: <0.84dd4e96e9c1b7211afc1575267877d911905f9af96aa5bb@apache.org>" \
                           "\r\n\r\n<?xml version=\'1.0\' encoding=\'UTF-8\'?><soapenv:Envelope xmlns:soapenv=\"http" \
                           "://www.w3.org/2003/05/soap-envelope\"><soapenv:Body><ns:createChangeRequestResponse xmln" \
                           "s:ns=\"http://wrappers.webservice.appservices.core.inteqnet.com\"><ns:return xmlns:ax212" \
                           "=\"http://beans.webservice.components.inteqnet.com/xsd\" xmlns:ax210=\"http://beans.webs" \
                           "ervice.appservices.core.inteqnet.com/xsd\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-" \
                           "instance\" xsi:type=\"ax212:DefaultServiceResponse\"><ax212:errors></ax212:errors><ax212" \
                           ":notes>An unsupported JSON? response output format was requested by the web service clie" \
                           "nt. The output response is being returned in the default format of XML configured for th" \
                           "e web service: ChangeRequest.createChangeRequest</ax212:notes><ax212:resourceName></ax21" \
                           "2:resourceName><ax212:responseBean xsi:type=\"ax212:Bean\"/><ax212:responseFormat>XML</a" \
                           "x212:responseFormat> <ax212:responseStatus>SERVICE_PARAMETER_VALIDATION_FAILURE</ax212:r" \
                           "esponseStatus><ax212:responseText>&lt;?xml version=\"1.0\" encoding=\"UTF-8\"?>&#xd;\n&l" \
                           "t;records>&lt;record>&lt;item_id>&lt;![CDATA[31677]]&gt;&lt;/item_id>&lt;ticket_identifi" \
                           "er>&lt;![CDATA[]]&gt;&lt;/ticket_identifier>&lt;/record>&lt;/records>&#xd;\n</ax212:resp" \
                           "onseText><ax212:statusCode>301</ax212:statusCode><ax212:statusMessage>Execution Error: A" \
                           "n unexpected error occurred during data-validation of the request parameters passed duri" \
                           "ng invocation of the web Service:ChangeRequest.createChangeRequest</ax212:statusMessage>" \
                           "<ax212:warnings></ax212:warnings></ns:return></ns:createChangeRequestResponse></soapenv:" \
                           "Body></soapenv:Envelope>\r\n--MIMEBoundary_94dd4e96e9c1b7211afc1575267877d911905f9af96aa" \
                           "5bb--\r\n'"
        mudanca = MudancaAutomatica()
        mudanca.destinatarios = DESTINATARIOS_EMAIL
        resultado_atual = mudanca.obter_numero_mudanca_criada(mensagem_retorno)
        resultado_esperado = None
        self.assertEquals(resultado_esperado, resultado_atual)

    def test_obter_mudanca_existente(self):
        mudanca = MudancaAutomatica()
        mudanca.destinatarios = DESTINATARIOS_EMAIL
        mudanca.caminho_templates = path.dirname(__file__) + "/templates/"
        resultado_atual = mudanca.obter_row_id_da_mudanca("200-2293")
        resultado_esperado = "31751"
        self.assertEquals(resultado_esperado, resultado_atual)
        resultado_esperado_group_id = "50"
        resultado_atual_group_id = mudanca.assigned_group_id
        self.assertEquals(resultado_esperado_group_id, resultado_atual_group_id)

    def test_obter_mudanca_nao_existente(self):
        mudanca = MudancaAutomatica()
        mudanca.destinatarios = DESTINATARIOS_EMAIL
        mudanca.caminho_templates = path.dirname(__file__) + "/templates/"
        resultado_atual = mudanca.obter_row_id_da_mudanca("200-3293")
        resultado_esperado = "00000"
        self.assertEquals(resultado_esperado, resultado_atual)

if __name__ == '__main__':
    unittest.main()
