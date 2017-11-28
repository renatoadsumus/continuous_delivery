# coding=utf-8

import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import path
from smtplib import SMTPException
from traceback import format_exc

from python.assistentes.log import Log
from python.settings import BUILDER, PIPELINE_LABEL, PIPELINE_NAME, BUILD_URL, DESTINATARIOS_EMAIL

__author__ = 'ssouza'


class Email:

    def __init__(self):
        self.CAMINHO_DIRETORIO_TEMPLATES = path.dirname(__file__) + "/templates/"
        self.REMETENTE = "devops@infoglobo.com.br"
        self.msg = MIMEMultipart("html")

    @staticmethod
    def get_valores_para_email():
        if BUILDER:
            from python.fabrica_objetos import FabricaObjetos
            builder = FabricaObjetos.obter_builder()
            versao = builder.get_versao()
        else:
            versao = PIPELINE_LABEL.split("-")[-1]
        valores = dict()

        valores["PIPELINE"] = str(PIPELINE_NAME)
        valores["BUILD_URL"] = str(BUILD_URL)
        valores["PIPELINE_LABEL"] = str(PIPELINE_LABEL)
        valores["VERSAO"] = versao

        return valores

    def carregar_template(self, arquivo, dict_valores=None):
        if not dict_valores:
            dict_valores = {}
        fp = open(self.CAMINHO_DIRETORIO_TEMPLATES + arquivo, 'r')
        conteudo = fp.read()

        for chave, valor in dict_valores.items():
            conteudo = conteudo.replace("[%s]" % chave, valor)

        mensagem_template = MIMEText(conteudo, "html")
        self.msg.attach(mensagem_template)
        fp.close()
        return mensagem_template

    def enviar_email(self, titulo, destinatario, mensagem="", out=sys.stdout):

        try:
            servidor = smtplib.SMTP("infomailgw")
            lista_destinatarios = destinatario.split(",")
            self.msg['Subject'] = titulo
            self.msg['From'] = self.REMETENTE
            self.msg['To'] = ", ".join(lista_destinatarios)
            mensagem_email = MIMEText(mensagem)
            self.msg.attach(mensagem_email)

            servidor.sendmail(self.REMETENTE, lista_destinatarios, self.msg.as_string())
            servidor.quit()
            out.write("Email enviado para: %s \n" % lista_destinatarios)
            Log.imprime("SUCESSO -- E-MAIL ENVIADO PARA %s" % lista_destinatarios)
        except SMTPException:
            Log.imprime("ERRO " + format_exc(), classe=Email)
            out.write("ERRO: NAO FOI POSSÍVEL ENVIAR O E-MAIL")

    def enviar_email_sucesso(self, destinatarios=""):
        self.carregar_template("sucesso_deploy.html", self.get_valores_para_email())
        if DESTINATARIOS_EMAIL:
            destinatarios = destinatarios + "," + DESTINATARIOS_EMAIL
        self.enviar_email("SUCESSO NO DEPLOY - " + PIPELINE_NAME + " - " + PIPELINE_LABEL, destinatarios)

    def enviar_email_falha(self, template, destinatarios=""):
        self.carregar_template(template, self.get_valores_para_email())
        if DESTINATARIOS_EMAIL:
            destinatarios = destinatarios + "," + DESTINATARIOS_EMAIL
        self.enviar_email("FALHA NO DEPLOY - " + PIPELINE_NAME + " - " + PIPELINE_LABEL, destinatarios)
