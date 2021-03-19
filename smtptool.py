# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
import res.config_loader

import imaplib
import smtplib
import time

from email import encoders
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def list_mailboxes():
    config = res.config_loader.config()['smtp']
    imap = imaplib.IMAP4_SSL(config['imap'], config['imap_port'])
    try:
        rv, data = imap.login(config['email'], config['email_pass'])
    except imaplib.IMAP4.error:
        print ("LOGIN FAILED!!! ")
        sys.exit(1)

    rv, mailboxes = imap.list()
    if rv == 'OK':
        print("Mailboxes:")
        for box in mailboxes:
            print(box)

def send_email(nome, html, subject, email, anexos=[]):
    config = res.config_loader.config()['smtp']
    if nome in config:
        smtp = config[nome]

        user = smtp['acc']
        password = smtp['pass']
        sender = smtp['email']
        recipients = email

        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipients
        msg.attach(MIMEText(html, "html", _charset='utf-8'))

        for anexo in anexos:
            if os.path.isfile(anexo):
                with codecs.open(anexo, "r", "latin1") as file:                        
                    part = MIMEBase('application', "octet-stream")
                    part.set_payload((file).read())
                    encoders.encode_base64(part)
                    filename = os.path.basename(anexo).replace(" ", "_")
                    part.add_header('Content-Disposition', "attachment; filename=%s" % filename)
                    part.add_header('Content-ID', f"<{str(i)}>")
                    part.add_header('X-Attachment-Id', f"{str(i)}")
                    msg.attach(part)

        s = smtplib.SMTP(smtp['url'], smtp['port'])
        # s.set_debuglevel(1)
        s.login(user, password)
        s.sendmail(sender, recipients, msg.as_string())
        s.quit()

        if smtp['imap'] != "" and smtp['email_pass'] != "":
            imap = imaplib.IMAP4_SSL(smtp['imap'], int(smtp['imap_port']))
            try:
                rv, data = imap.login(smtp['email'], smtp['email_pass'])
            except imaplib.IMAP4.error:
                print ("LOGIN FAILED!!! ")
                sys.exit(1)

            print(imap.append(smtp['imap_folder'], None, imaplib.Time2Internaldate(time.time()), msg.as_string().encode('utf8')))
            imap.logout()

            # imap = imaplib.IMAP4_SSL("imap.somacontabilidades.com.br", 993)
            # try:
            #     rv, data = imap.login("notificacaoiacon@somacontabilidades.com.br", "soma@202010")
            # except imaplib.IMAP4.error:
            #     print ("LOGIN FAILED!!! ")
            #     sys.exit(1)

            # print(imap.append('"Mensagens enviadas"', None, imaplib.Time2Internaldate(time.time()), msg.as_string().encode('utf8')))
            # imap.logout()
    else:
        print(f"Não existe configuração de SMTP com esse nome \"{nome}\"")
    