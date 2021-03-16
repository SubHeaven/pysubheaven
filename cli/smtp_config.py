# -*- coding: utf-8 -*-
import codecs
import os
import smtplib
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))

from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

import res.config_loader
import smtptool
import input_base

from subheaven.arg_parser import *

def list_mailboxes():
    smtptool.list_mailboxes()

def do_config(smtp):
    new_smtp = res.config_loader.default_config()["smtp"]
    new_smtp['url'] = input_base.input_text("Por favor, informe o endereço do servidor de smtp: \n", smtp['url'])
    new_smtp['port'] = input_base.input_number("Por favor, informe a porta do servidor de smtp: \n", smtp['port'])
    new_smtp['acc'] = input_base.input_text("Por favor, informe a conta de login no servidor: \n", smtp['acc'])
    new_smtp['pass'] = input_base.input_text("Por favor, informe a senha de login no servidor: \n", smtp['pass'])
    new_smtp['email'] = input_base.input_text("Por favor, informe o email configurado para envio: \n", smtp['email'])
    new_smtp['imap'] = input_base.input_text("Por favor, informe o servidor de IMAP (Opcional): \n", smtp['imap'])
    new_smtp['imap_port'] = input_base.input_number("Por favor, informe a porta do servidor de IMAP (Opcional): \n", smtp['imap_port'])
    new_smtp['email_pass'] = input_base.input_text("Por favor, informe a senha do email (Opcional): \n", smtp['email_pass'])
    new_smtp['imap_folder'] = input_base.input_text("Por favor, informe o nome da pasta de emails enviados (Opcional): \n", smtp['imap_folder'])
    return new_smtp

def show_config(config):
    for k in config:
        print(f"    {k} = {config[k]}")

def test_email(smtp):
    if smtp["url"] == "" or smtp["acc"] == "" or smtp["pass"] == "":
        print("Configuração de email não está completo. Configure-o com o comando smtp_config")
        return
    else:
        email = input_base.input_text("Informe o email de envio de teste: ", default="subheaven.paulo@gmail.com", obrigatorio=True)
        smtptool.send_email("Olá Mundo!", "Teste de email do smtptool", email)

@arg_parser(".".join(os.path.basename(__file__).split(".")[0:-1]), 'Configura uma conta para envio de emails via smtp')
@boolean_param('view', 'Mostrar configuração.')
@boolean_param('test', 'Testar envio.')
@boolean_param('mailboxes', 'Listar caixas de email do servidor de IMAP. Usado para verificar o nome da pasta \n               de emails enviados para que sejam gravadas as devidas cópias.')
def process():
    config = res.config_loader.config()
    if params['view']:
        print("Configuração atual:")
        show_config(config['smtp'])
    elif params['mailboxes']:
        list_mailboxes()
    elif params['test']:
        test_email(config['smtp'])
    else:
        config['smtp'] = do_config(config['smtp'])
        res.config_loader.save_config(config)
        print("")
        print("Configuração salva com sucesso!")
        show_config(config['smtp'])

if __name__ == "__main__":
    process()
